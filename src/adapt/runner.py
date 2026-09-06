"""Paired experiment runner with provenance (D2.1).

Same task episodes for every strategy (paired design). Episodic reset
enforced: reset() before every episode. Provenance recorded per run:
experiment_id, git_commit, config_hash, seeds, model/task versions.
"""
import copy
import hashlib
import json
import platform
import subprocess
import time
import numpy as np

from .tasks import generate_task, GENERATOR_VERSION
from .strategies import MODEL_VERSION, make_strategy
from .telemetry import is_correct, accuracy_ci, paired_diff_ci



def _git_commit():
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL, timeout=10)
        return out.decode().strip()
    except Exception:
        return "unknown"


def _config_hash(cfg):
    return hashlib.sha256(
        json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:12]


def run_episode(task, strategy_name, s_kwargs):
    kw = dict(s_kwargs)
    tol = kw.pop("tol", 0.5)
    strat = make_strategy(strategy_name, family=task.family, **kw)
    strat.reset()
    t = time.perf_counter()
    strat.adapt(task.demonstrations)
    if strategy_name == "context":
        pred = strat.predict(task.query, family=task.family)
    else:
        pred = strat.predict(task.query)
    lat = (time.perf_counter() - t) * 1000
    tel = strat.telemetry()
    tel["latency_ms"] = tel.get("latency_ms", 0.0) + 0.0  # adapt time inside
    ok = is_correct(task.family, pred, task.ground_truth,
                    tol=tol)
    return {"correct": bool(ok), "telemetry": tel, "latency_ms": float(lat),
            "strategy": strat, "pred": pred}


def run(config):
    """config keys: family, strategies[list], strategy_kwargs{...},
    seeds[list], n_demos, noise, split, tol, extra(free-form)."""
    t_start = time.perf_counter()
    seeds = list(config["seeds"])
    strats = list(config["strategies"])
    skw = dict(config.get("strategy_kwargs", {}))
    tasks = [generate_task(config["family"], s,
                           n_demos=config.get("n_demos", 4),
                           noise=config.get("noise", 0.0),
                           split=config.get("split", "eval"))
             for s in seeds]
    per_strategy = {name: [] for name in strats}
    teles = {name: [] for name in strats}
    for task in tasks:
        for name in strats:
            kw = dict(skw.get(name, {}))
            kw.setdefault("tol", config.get("tol", 0.5))
            fam_kw = {k: v for k, v in kw.items() if k != "tol"}
            r = run_episode(task, name, {"tol": kw["tol"], **fam_kw})
            per_strategy[name].append(r["correct"])
            teles[name].append(r["telemetry"])
    summary = {}
    for name in strats:
        acc, ci = accuracy_ci(per_strategy[name])
        tel = teles[name]
        summary[name] = {
            "accuracy": acc,
            "ci95": list(ci),
            "n": len(seeds),
            "mean_persistent_delta": float(np.mean([t["persistent_delta"] for t in tel])),
            "mean_state_delta": float(np.mean([t["state_delta"] for t in tel])),
            "mean_latency_ms": float(np.mean([t["latency_ms"] for t in tel])),
        }
    # paired diffs vs frozen (if present) else vs first strategy
    base = "frozen" if "frozen" in strats else strats[0]
    diffs = {}
    for name in strats:
        if name == base:
            continue
        d, ci = paired_diff_ci(per_strategy[name], per_strategy[base])
        diffs[f"{name}_minus_{base}"] = {"diff": d, "ci95": list(ci)}
    prov = {
        "git_commit": _git_commit(),
        "config_hash": _config_hash({k: v for k, v in config.items()}),
        "model_version": MODEL_VERSION,
        "task_generator_version": GENERATOR_VERSION,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "seeds": seeds,
        "wall_s": float(time.perf_counter() - t_start),
    }
    return {"config": config, "summary": summary, "diffs": diffs,
            "provenance": prov,
            "evidence_type": "TOY_EXPERIMENT"}


def run_interference(config):
    """A -> B -> A retention. Continual mode: NO reset between A and B
    (explicit, logged). Measures initial A accuracy, B accuracy, and
    retention of A after B."""
    import time
    t_start = time.perf_counter()
    seeds = list(config["seeds"])
    strats = list(config["strategies"])
    skw = dict(config.get("strategy_kwargs", {}))
    fam = config["family"]
    out = {}
    for name in strats:
        init_hits, b_hits, ret_hits = [], [], []
        lat = []
        for s in seeds:
            tA = generate_task(fam, s, n_demos=config.get("n_demos", 4),
                               noise=config.get("noise", 0.0),
                               split=config.get("split", "eval"))
            # force A/B rules to differ (discrete families) so retention
            # measures interference, not same-rule coincidence
            tB = None
            for attempt in range(10):
                cand = generate_task(fam, 100000 + s * 10 + attempt,
                                     n_demos=config.get("n_demos", 4),
                                     noise=config.get("noise", 0.0),
                                     split=config.get("split", "eval"))
                if cand.hidden_rule != tA.hidden_rule:
                    tB = cand
                    break
            if tB is None:
                tB = cand
            kw = dict(skw.get(name, {}))
            tol = kw.pop("tol", config.get("tol", 0.5))
            strat = make_strategy(name, family=fam, **kw)
            strat.reset()
            t = time.perf_counter()
            strat.adapt(tA.demonstrations)
            pA0 = strat.predict(tA.query) if name != "context" else strat.predict(tA.query, family=fam)
            strat.adapt(tB.demonstrations)  # continual: no reset (logged)
            pB = strat.predict(tB.query) if name != "context" else strat.predict(tB.query, family=fam)
            pAr = strat.predict(tA.query) if name != "context" else strat.predict(tA.query, family=fam)
            lat.append((time.perf_counter() - t) * 1000)
            init_hits.append(is_correct(fam, pA0, tA.ground_truth, tol))
            b_hits.append(is_correct(fam, pB, tB.ground_truth, tol))
            ret_hits.append(is_correct(fam, pAr, tA.ground_truth, tol))
        ai, cii = accuracy_ci(init_hits)
        ab, cib = accuracy_ci(b_hits)
        ar, cir = accuracy_ci(ret_hits)
        out[name] = {"acc_A_initial": ai, "ci_A": list(cii),
                     "acc_B": ab, "ci_B": list(cib),
                     "retention_A": ar, "ci_R": list(cir),
                     "retention_drop": float(ai - ar),
                     "n": len(seeds),
                     "mean_latency_ms": float(__import__("numpy").mean(lat)),
                     "mode": "continual (no reset A->B, explicit)"}
    prov = {"git_commit": _git_commit(),
            "config_hash": _config_hash({k: v for k, v in config.items()}),
            "model_version": MODEL_VERSION,
            "task_generator_version": GENERATOR_VERSION,
            "platform": __import__("platform").platform(),
            "seeds": seeds, "wall_s": float(time.perf_counter() - t_start)}
    return {"config": config, "summary": out, "diffs": {},
            "provenance": prov, "evidence_type": "TOY_EXPERIMENT"}


def run_intervention(config):
    """E8 causal test: adapt A -> measure -> perturb state ->
    measure -> restore -> measure. Perturbations: zero, shuffle,
    noise, swap-with-B. Reports drop and recovery."""
    import time
    import numpy as np
    t_start = time.perf_counter()
    seeds = list(config["seeds"])
    strats = [n for n in config["strategies"] if n in ("state", "ttt_state")]
    skw = dict(config.get("strategy_kwargs", {}))
    fam = config["family"]
    perts = config.get("perturbations", ["zero", "shuffle", "noise", "swap"])
    out = {}
    for name in strats:
        rows = {p: {"base": [], "pert": [], "restored": []} for p in perts}
        for s in seeds:
            tA = generate_task(fam, s, n_demos=config.get("n_demos", 4),
                               noise=config.get("noise", 0.0),
                               split=config.get("split", "eval"))
            tB = generate_task(fam, 200000 + s, n_demos=config.get("n_demos", 4),
                               noise=config.get("noise", 0.0),
                               split=config.get("split", "eval"))
            kw = dict(skw.get(name, {}))
            tol = kw.pop("tol", config.get("tol", 0.5))
            rng = np.random.RandomState(s)
            for p in perts:
                strat = make_strategy(name, family=fam, **kw)
                strat.reset()
                strat.adapt(tA.demonstrations)
                sA = strat.get_state().copy()
                base_ok = is_correct(fam, strat.predict(tA.query), tA.ground_truth, tol)
                # second strategy instance for swap state
                other = make_strategy(name, family=fam, **kw)
                other.reset()
                other.adapt(tB.demonstrations)
                sB = other.get_state().copy()
                if p == "zero":
                    strat.set_state(np.zeros_like(sA))
                elif p == "shuffle":
                    strat.set_state(rng.permutation(sA))
                elif p == "noise":
                    strat.set_state(sA + rng.normal(0, max(1e-9, np.abs(sA).mean()), size=sA.shape))
                elif p == "swap":
                    strat.set_state(sB)
                pert_ok = is_correct(fam, strat.predict(tA.query), tA.ground_truth, tol)
                strat.set_state(sA)
                rest_ok = is_correct(fam, strat.predict(tA.query), tA.ground_truth, tol)
                rows[p]["base"].append(base_ok)
                rows[p]["pert"].append(pert_ok)
                rows[p]["restored"].append(rest_ok)
        summ = {}
        for p, r in rows.items():
            ab, _ = accuracy_ci(r["base"])
            ap, _ = accuracy_ci(r["pert"])
            ar, _ = accuracy_ci(r["restored"])
            d, ci = paired_diff_ci(r["base"], r["pert"])
            summ[p] = {"acc_base": ab, "acc_perturbed": ap,
                       "acc_restored": ar, "drop": float(ab - ap),
                       "paired_drop": d, "paired_drop_ci95": list(ci)}
        out[name] = summ
    prov = {"git_commit": _git_commit(),
            "config_hash": _config_hash({k: v for k, v in config.items()}),
            "model_version": MODEL_VERSION,
            "task_generator_version": GENERATOR_VERSION,
            "platform": __import__("platform").platform(),
            "seeds": seeds, "wall_s": float(time.perf_counter() - t_start)}
    return {"config": config, "summary": out, "diffs": {},
            "provenance": prov, "evidence_type": "TOY_EXPERIMENT"}


def run_with_protocol(config):
    p = config.get("protocol", "standard")
    if p == "interference":
        return run_interference(config)
    if p == "intervention":
        return run_intervention(config)
    return run(config)


def sweep(base_config, key, values, name_fn=None):
    """Vary base_config[key] over values; return list of (label, result)."""
    import copy
    out = []
    for v in values:
        cfg = copy.deepcopy(base_config)
        cfg[key] = v
        label = name_fn(v) if name_fn else f"{key}={v}"
        out.append((label, run_with_protocol(cfg)))
    return out
