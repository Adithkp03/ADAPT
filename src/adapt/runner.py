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
from .telemetry import (is_correct, accuracy_ci, paired_diff_ci,
                        mcnemar_exact, cohen_h)
from .evidence import evidence_for

# Machine-readable result schema version (review Patch 6). Bump on any
# breaking change to the run()/run_interference()/run_intervention()
# result dict layout; Phase 3 readers MUST check this field.
RESULT_SCHEMA_VERSION = 1



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
    t0 = time.perf_counter()
    strat.adapt(task.demonstrations)
    t_adapt = (time.perf_counter() - t0) * 1000
    t1 = time.perf_counter()
    if strategy_name == "context":
        pred = strat.predict(task.query, family=task.family)
    else:
        pred = strat.predict(task.query)
    t_predict = (time.perf_counter() - t1) * 1000
    tel = strat.telemetry()
    tel["t_adapt_ms"] = tel.get("t_adapt_ms", 0.0) or t_adapt
    tel["t_predict_ms"] = tel.get("t_predict_ms", 0.0) or t_predict
    tel["latency_ms"] = tel["t_adapt_ms"] + tel["t_predict_ms"]
    lat = tel["latency_ms"]
    ok = is_correct(task.family, pred, task.ground_truth,
                    tol=tol)
    return {"correct": bool(ok), "telemetry": tel, "latency_ms": float(lat),
            "strategy": strat, "pred": pred}


def run(config):
    """config keys: family, strategies[list], strategy_kwargs{...},
    task_seeds[list] (seeds= legacy alias), n_demos, noise, split, tol."""
    t_start = time.perf_counter()
    seeds = list(config.get("task_seeds", config.get("seeds")))
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
    # paired diffs vs frozen (if present) else vs first strategy.
    # task_seeds are task identity; model_seed (provenance) is separate.
    base = "frozen" if "frozen" in strats else strats[0]
    diffs = {}
    for name in strats:
        if name == base:
            continue
        d, ci = paired_diff_ci(per_strategy[name], per_strategy[base])
        pa, _ = accuracy_ci(per_strategy[name])
        pb, _ = accuracy_ci(per_strategy[base])
        diffs[f"{name}_minus_{base}"] = {
            "diff": d, "ci95": list(ci),
            "mcnemar_p": mcnemar_exact(per_strategy[name], per_strategy[base]),
            "cohen_h": cohen_h(pa, pb)}
    # back-compat: configs may use seeds=... (= task_seeds)
    task_seeds = list(config.get("task_seeds", seeds))
    prov = {
        "git_commit": _git_commit(),
        "config_hash": _config_hash({k: v for k, v in config.items()}),
        "model_version": MODEL_VERSION,
        "task_generator_version": GENERATOR_VERSION,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "task_seeds": task_seeds,
        "model_seed": config.get("model_seed", 0),
        "seeds": seeds,
        "wall_s": float(time.perf_counter() - t_start),
    }
    return {"config": config, "summary": summary, "diffs": diffs,
            "provenance": prov,
            "evidence_type": evidence_for(strats),
            "result_schema_version": RESULT_SCHEMA_VERSION}


def run_interference(config):
    """A -> B -> A retention. Continual mode: NO reset between A and B
    (explicit, logged). Measures initial A accuracy, B accuracy, and
    retention of A after B."""
    import time
    t_start = time.perf_counter()
    seeds = list(config.get("task_seeds", config.get("seeds")))
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
            "provenance": prov, "evidence_type": "TOY_EXPERIMENT",
            "result_schema_version": RESULT_SCHEMA_VERSION}


def run_intervention(config):
    """E8 causal test: adapt A -> measure -> perturb state ->
    measure -> restore -> measure. Perturbations: zero, shuffle,
    noise, swap-with-B (matched control), nullmean (population-null:
    mean state over K unrelated tasks — on-manifold task-information
    removal).

    Interpretation rule: 'shuffle causes failure' alone does NOT prove
    task-information removal — for learned coordinates it may only
    prove decoder coordinate-correspondence violation (malformed
    input). Causal weight rests on swap (matched counterfactual) +
    nullmean (s_A minus task-specific component, on-manifold) with
    restore ~= base. Supports analytical (state/ttt_state) and learned
    (learned_state/learned_ttt) substrates; strategies without
    get_state/set_state are skipped and logged."""
    import time
    import numpy as np
    t_start = time.perf_counter()
    seeds = list(config.get("task_seeds", config.get("seeds")))
    wanted = list(config["strategies"])
    stateful = ("state", "ttt_state", "learned_state", "learned_ttt")
    strats = [n for n in wanted if n in stateful]
    skipped = [n for n in wanted if n not in stateful]
    skw = dict(config.get("strategy_kwargs", {}))
    fam = config["family"]
    perts = config.get("perturbations", ["zero", "shuffle", "noise", "swap", "nullmean"])
    out = {}
    if skipped:
        out["_skipped_no_state_hooks"] = skipped
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
                sA = np.asarray(strat.get_state(), float).copy()
                base_ok = is_correct(fam, strat.predict(tA.query), tA.ground_truth, tol)
                # second strategy instance for swap state
                other = make_strategy(name, family=fam, **kw)
                other.reset()
                other.adapt(tB.demonstrations)
                sB = np.asarray(other.get_state(), float).copy()
                if p == "zero":
                    strat.set_state(np.zeros_like(sA))
                elif p == "shuffle":
                    strat.set_state(rng.permutation(sA))
                elif p == "noise":
                    strat.set_state(sA + rng.normal(0, max(1e-9, np.abs(sA).mean()), size=sA.shape))
                elif p == "swap":
                    strat.set_state(sB)
                elif p == "nullmean":
                    # on-manifold population null: mean state over 8
                    # unrelated tasks; removes task-specific component
                    # while staying in the learned state's typical set
                    acc = np.zeros_like(sA)
                    for j in range(8):
                        tJ = generate_task(fam, 300000 + s * 16 + j,
                                           n_demos=config.get("n_demos", 4),
                                           noise=config.get("noise", 0.0),
                                           split=config.get("split", "eval"))
                        tmp = make_strategy(name, family=fam, **kw)
                        tmp.reset()
                        tmp.adapt(tJ.demonstrations)
                        acc = acc + np.asarray(tmp.get_state(), float)
                    strat.set_state(acc / 8.0)
                else:
                    raise ValueError(f"unknown perturbation {p}")
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
                       "paired_drop": d, "paired_drop_ci95": list(ci),
                       "mcnemar_p": mcnemar_exact(r["base"], r["pert"])}
        # Holm correction across perturbations (multiple comparisons)
        ps = [summ[p]["mcnemar_p"] for p in perts]
        from .telemetry import holm_bonferroni
        holm = holm_bonferroni(ps)
        for p, pa, rej in zip(perts, holm["p_adjusted"], holm["reject"]):
            summ[p]["mcnemar_p_holm"] = pa
            summ[p]["holm_reject"] = bool(rej)
        out[name] = summ
    prov = {"git_commit": _git_commit(),
            "config_hash": _config_hash({k: v for k, v in config.items()}),
            "model_version": MODEL_VERSION,
            "task_generator_version": GENERATOR_VERSION,
            "platform": __import__("platform").platform(),
            "seeds": seeds, "wall_s": float(time.perf_counter() - t_start)}
    return {"config": config, "summary": out, "diffs": {},
            "provenance": prov, "evidence_type": "TOY_EXPERIMENT",
            "result_schema_version": RESULT_SCHEMA_VERSION}


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
