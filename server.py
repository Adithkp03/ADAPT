"""Phase 3 experiment API + static frontend server (stdlib only).

Serves web/ and exposes the REAL Phase 2 engine over HTTP — no fake
results: every learner-facing number comes from src/adapt via the same
paired/reset/provenance semantics as the research runner.

Endpoints:
  GET  /api/health
  GET  /api/meta            strategies/families/evidence taxonomy
  POST /api/episode         one task, one strategy -> pred vs truth + telemetry
  POST /api/compare         one task, N strategies (paired, same episodes)
  POST /api/interference    single-seed A->B->A retention
  POST /api/intervene       single-seed E8 perturb/restore per perturbation
  POST /api/sweep           accuracy vs n_demos|noise|state_dim|steps
  GET  /api/precomputed?exp=<id>   vetted research results (PRECOMPUTED badge)
  GET  /api/figure?name=<f>        research figures (PRECOMPUTED)

Run: system-python server.py [--port 8001]
"""
import hashlib
import json
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from adapt import runner as R
from adapt import tasks as T
from adapt import strategies as S
from adapt import telemetry as TL
from adapt.evidence import evidence_for

RESULTS = ROOT / "research" / "experiments"
FIGURES = RESULTS / "figures"
EXP_IDS = ["001_task_acquisition_linear", "001_task_acquisition_symbolic",
           "002_demo_scaling_linear", "003_compute_scaling_linear",
           "004_state_capacity_linear", "005_interference_linear",
           "006_noise_linear", "008_intervention_linear",
           "009_learned_linear_s0", "009_learned_intervention",
           "009_mechanistic"]


def _fmt(family, v):
    if family in ("linear", "quadratic"):
        return f"{float(v):.3f}"
    if family in ("symbolic", "compositional"):
        return " ".join(str(int(x)) for x in v)
    return [[int(c) for c in row] for row in v]


def _rule_text(family, rule):
    if family == "linear":
        return f"y = {rule['a']:.3f} x + {rule['b']:.3f} (hidden)"
    if family == "quadratic":
        return (f"y = {rule['a']:.3f} x^2 + {rule['b']:.3f} x + "
                f"{rule['c']:.3f} (hidden)")
    if family == "symbolic":
        return f"y = ({rule['mult']}x + {rule['offset']}) mod 8 (hidden)"
    if family == "compositional":
        ops = " o ".join(o["op"] + (f"({o.get('offset', o.get('to', ''))})"
                                    if "offset" in o or "to" in o else "")
                         for o in rule["ops"])
        return f"chain: {ops} (hidden)"
    return f"grid rule: {rule['rule']} (hidden)"


def _prov(task, extra=None):
    cfg = {"family": task.family, "seed": task.seed,
           "n_demos": len(task.demonstrations), "split": task.split}
    if extra:
        cfg.update(extra)
    return {
        "seed": task.seed, "split": task.split,
        "task_generator_version": T.GENERATOR_VERSION,
        "model_version": S.MODEL_VERSION,
        "git_commit": R._git_commit(),
        "config_hash": R._config_hash(cfg),
        "result_schema_version": R.RESULT_SCHEMA_VERSION,
    }


def _episode_payload(task, strategy_name, skw):
    r = R.run_episode(task, strategy_name, skw)
    tel = r["telemetry"]
    fam = task.family
    return {
        "experiment_id": "ep_" + R._config_hash(
            {"fam": fam, "strat": strategy_name, "seed": task.seed,
             "kw": {k: str(v) for k, v in skw.items()}})[:10],
        "task": {
            "family": fam,
            "family_display": S.FAMILY_DISPLAY.get(fam, fam),
            "demonstrations": [
                {"x": _fmt(fam, x), "y": _fmt(fam, y)}
                for x, y in task.demonstrations],
            "query": _fmt(fam, task.query),
            "rule_hidden": _rule_text(fam, task.hidden_rule),
        },
        "strategy": strategy_name,
        "strategy_display": S.STRATEGY_DISPLAY.get(strategy_name,
                                                  strategy_name),
        "prediction": _fmt(fam, r["pred"]),
        "ground_truth": _fmt(fam, task.ground_truth),
        "correct": bool(r["correct"]),
        "telemetry": {
            "persistent_delta": tel["persistent_delta"],
            "state_delta": tel["state_delta"],
            "steps": tel["steps"],
            "t_adapt_ms": tel["t_adapt_ms"],
            "t_predict_ms": tel["t_predict_ms"],
            "latency_ms": tel["latency_ms"],
            "param_count": tel["param_count"],
            "state_dim": tel["state_dim"],
            "state_bytes": tel["state_bytes"],
            "loss_before": tel["loss_before"],
            "loss_after": tel["loss_after"],
            "grad_norm": tel["grad_norm"],
        },
        "provenance": _prov(task, {"strategy": strategy_name}),
        "execution_type": "live",
        "evidence_type": evidence_for([strategy_name]),
        "badges": ["LIVE", "SYNTHETIC"],
    }


def _flat_kw(body, name):
    """Accept flat {lr:..} or nested {<strategy>: {..}} kwargs."""
    raw = dict(body.get("strategy_kwargs", {}))
    sub = raw.get(name)
    return dict(sub) if isinstance(sub, dict) else raw


def _body(handler):
    n = int(handler.headers.get("Content-Length", 0))
    return json.loads(handler.rfile.read(n) or b"{}")


class Handler(BaseHTTPRequestHandler):
    server_version = "AdaptLab/1"

    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        b = json.dumps(obj, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == "/api/health":
            return self._json({"ok": True,
                               "schema": R.RESULT_SCHEMA_VERSION})
        if u.path == "/api/meta":
            return self._json({
                "strategies": [
                    {"key": k, "display": v} for k, v in
                    S.STRATEGY_DISPLAY.items()],
                "families": [
                    {"key": k, "display": v} for k, v in
                    S.FAMILY_DISPLAY.items()],
                "evidence_types": ["CONTROLLED_TOY",
                                   "LEARNED_MODEL_EXPERIMENT",
                                   "PUBLISHED_RESULT", "ILLUSTRATION"],
                "result_schema_version": R.RESULT_SCHEMA_VERSION,
            })
        if u.path == "/api/precomputed":
            exp = q.get("exp", [""])[0]
            if exp not in EXP_IDS:
                return self._json({"error": "unknown exp"}, 404)
            res = json.loads((RESULTS / exp / "results.json").read_text())
            res["execution_type"] = "precomputed"
            res["badges"] = ["PRECOMPUTED", "SYNTHETIC"]
            return self._json(res)
        if u.path == "/api/figure":
            name = q.get("name", [""])[0].replace("/", "")
            p = FIGURES / name
            if not name.endswith(".png") or not p.exists():
                return self._json({"error": "unknown figure"}, 404)
            b = p.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            return self.wfile.write(b)
        # static
        rel = u.path.lstrip("/") or "index.html"
        p = (ROOT / "web" / rel).resolve()
        if not str(p).startswith(str(ROOT / "web")) or not p.is_file():
            return self._json({"error": "not found"}, 404)
        ctype = {"html": "text/html", "js": "text/javascript",
                 "css": "text/css", "json": "application/json",
                 "png": "image/png"}.get(p.suffix.lstrip("."), "text/plain")
        b = p.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype + (
            "; charset=utf-8" if ctype.startswith("text") else ""))
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):  # noqa: C901
        try:
            body = _body(self)
        except Exception:
            return self._json({"error": "bad json"}, 400)
        try:
            if self.path == "/api/episode":
                fam = body.get("family", "linear")
                task = T.generate_task(
                    fam, int(body.get("seed", 7)),
                    n_demos=int(body.get("n_demos", 4)),
                    noise=float(body.get("noise", 0.0)),
                    split=body.get("split", "test"))
                skw = _flat_kw(body, body.get("strategy", "state"))
                skw.setdefault("tol", 0.5)
                return self._json(_episode_payload(
                    task, body.get("strategy", "state"), skw))
            if self.path == "/api/compare":
                fam = body.get("family", "linear")
                task = T.generate_task(
                    fam, int(body.get("seed", 7)),
                    n_demos=int(body.get("n_demos", 4)),
                    noise=float(body.get("noise", 0.0)),
                    split=body.get("split", "test"))
                gkw = body.get("strategy_kwargs", {})
                rows = {}
                for name in body.get("strategies",
                                     ["context", "param_tta", "state"]):
                    skw = dict(gkw.get(name, {}))
                    skw.setdefault("tol", 0.5)
                    r = R.run_episode(task, name, skw)
                    rows[name] = {
                        "display": S.STRATEGY_DISPLAY.get(name, name),
                        "prediction": _fmt(fam, r["pred"]),
                        "correct": bool(r["correct"]),
                        "persistent_delta": r["telemetry"][
                            "persistent_delta"],
                        "state_delta": r["telemetry"]["state_delta"],
                        "latency_ms": r["telemetry"]["latency_ms"],
                    }
                return self._json({
                    "task": {
                        "family": fam,
                        "family_display": S.FAMILY_DISPLAY.get(fam, fam),
                        "demonstrations": [
                            {"x": _fmt(fam, x), "y": _fmt(fam, y)}
                            for x, y in task.demonstrations],
                        "query": _fmt(fam, task.query),
                        "ground_truth": _fmt(fam, task.ground_truth),
                        "rule_hidden": _rule_text(fam, task.hidden_rule),
                    },
                    "rows": rows,
                    "provenance": _prov(task),
                    "execution_type": "live",
                    "evidence_type": evidence_for(list(rows)),
                    "badges": ["LIVE", "SYNTHETIC"],
                })
            if self.path == "/api/interference":
                fam = body.get("family", "linear")
                name = body.get("strategy", "state")
                skw = {k: v for k, v in
                       _flat_kw(body, name).items()
                       if k != "tol"}
                tol = float(body.get("tol", 0.5))
                s = int(body.get("seed", 7))
                n, noise = int(body.get("n_demos", 4)), float(
                    body.get("noise", 0.0))
                tA = T.generate_task(fam, s, n_demos=n, noise=noise,
                                     split="test")
                tB = None
                for a in range(10):
                    c = T.generate_task(fam, 100000 + s * 10 + a,
                                        n_demos=n, noise=noise, split="test")
                    if c.hidden_rule != tA.hidden_rule:
                        tB = c
                        break
                strat = S.make_strategy(name, family=fam, **skw)
                strat.reset()
                strat.adapt(tA.demonstrations)
                pA0 = (strat.predict(tA.query, family=fam) if name ==
                       "context" else strat.predict(tA.query))
                strat.adapt(tB.demonstrations)
                pB = (strat.predict(tB.query, family=fam) if name ==
                      "context" else strat.predict(tB.query))
                pAr = (strat.predict(tA.query, family=fam) if name ==
                       "context" else strat.predict(tA.query))
                ok = lambda p, t: bool(TL.is_correct(fam, p, t, tol))  # noqa
                return self._json({
                    "A": {"query": _fmt(fam, tA.query),
                          "ground_truth": _fmt(fam, tA.ground_truth),
                          "pred_before": _fmt(fam, pA0),
                          "pred_after": _fmt(fam, pAr),
                          "correct_before": ok(pA0, tA.ground_truth),
                          "correct_after": ok(pAr, tA.ground_truth)},
                    "B": {"query": _fmt(fam, tB.query),
                          "ground_truth": _fmt(fam, tB.ground_truth),
                          "pred": _fmt(fam, pB),
                          "correct": ok(pB, tB.ground_truth)},
                    "strategy_display": S.STRATEGY_DISPLAY.get(name, name),
                    "mode": "continual (no reset A->B, explicit)",
                    "execution_type": "live",
                    "evidence_type": evidence_for([name]),
                    "badges": ["LIVE", "SYNTHETIC"],
                })
            if self.path == "/api/intervene":
                import numpy as np
                fam = body.get("family", "linear")
                name = body.get("strategy", "state")
                skw = {k: v for k, v in
                       _flat_kw(body, name).items()
                       if k != "tol"}
                tol = float(body.get("tol", 0.5))
                s = int(body.get("seed", 7))
                n, noise = int(body.get("n_demos", 4)), float(
                    body.get("noise", 0.0))
                tA = T.generate_task(fam, s, n_demos=n, noise=noise,
                                     split="test")
                tB = T.generate_task(fam, 200000 + s, n_demos=n,
                                     noise=noise, split="test")
                rng = np.random.RandomState(s)
                rows = {}
                for p in body.get("perturbations",
                                  ["zero", "swap", "nullmean"]):
                    st = S.make_strategy(name, family=fam, **skw)
                    st.reset()
                    st.adapt(tA.demonstrations)
                    sA = np.asarray(st.get_state(), float).copy()
                    base = bool(TL.is_correct(
                        fam, st.predict(tA.query), tA.ground_truth, tol))
                    other = S.make_strategy(name, family=fam, **skw)
                    other.reset()
                    other.adapt(tB.demonstrations)
                    sB = np.asarray(other.get_state(), float).copy()
                    if p == "zero":
                        st.set_state(np.zeros_like(sA))
                    elif p == "shuffle":
                        st.set_state(rng.permutation(sA))
                    elif p == "noise":
                        st.set_state(sA + rng.normal(
                            0, max(1e-9, np.abs(sA).mean()),
                            size=sA.shape))
                    elif p == "swap":
                        st.set_state(sB)
                    elif p == "nullmean":
                        acc = np.zeros_like(sA)
                        for j in range(8):
                            tJ = T.generate_task(
                                fam, 300000 + s * 16 + j, n_demos=n,
                                noise=noise, split="test")
                            tmp = S.make_strategy(name, family=fam, **skw)
                            tmp.reset()
                            tmp.adapt(tJ.demonstrations)
                            acc += np.asarray(tmp.get_state(), float)
                        st.set_state(acc / 8.0)
                    else:
                        return self._json({"error": "bad perturbation"},
                                          400)
                    pert = bool(TL.is_correct(
                        fam, st.predict(tA.query), tA.ground_truth, tol))
                    st.set_state(sA)
                    rest = bool(TL.is_correct(
                        fam, st.predict(tA.query), tA.ground_truth, tol))
                    rows[p] = {"base": base, "perturbed": pert,
                               "restored": rest}
                return self._json({
                    "task": {"query": _fmt(fam, tA.query),
                             "ground_truth": _fmt(fam, tA.ground_truth)},
                    "rows": rows,
                    "strategy_display": S.STRATEGY_DISPLAY.get(name, name),
                    "note": "Causal weight rests on swap (matched "
                            "counterfactual) + nullmean (on-manifold "
                            "null). Shuffle-failure alone is not "
                            "claimed as information removal.",
                    "execution_type": "live",
                    "evidence_type": evidence_for([name]),
                    "badges": ["LIVE", "SYNTHETIC"],
                })
            if self.path == "/api/sweep":
                import numpy as np
                fam = body.get("family", "linear")
                name = body.get("strategy", "state")
                base_kw = _flat_kw(body, name)
                var = body.get("var", "n_demos")
                values = list(body.get("values", [1, 2, 4, 6, 8]))[:8]
                eps = min(int(body.get("episodes", 25)), 50)
                seed0 = int(body.get("seed_base", 0))
                pts = []
                for v in values:
                    kw, nd, noise = dict(base_kw), 4, 0.0
                    if var == "n_demos":
                        nd = int(v)
                    elif var == "noise":
                        noise = float(v)
                    elif var == "state_dim":
                        kw["state_dim"] = None if v in (
                            "full", None) else int(v)
                    elif var == "steps":
                        kw["steps"] = int(v)
                    else:
                        return self._json({"error": "bad var"}, 400)
                    hits = []
                    for i in range(eps):
                        t = T.generate_task(fam, seed0 + i, n_demos=nd,
                                            noise=noise, split="test")
                        skw = dict(kw)
                        skw.setdefault("tol", 0.5)
                        r = R.run_episode(t, name, skw)
                        hits.append(r["correct"])
                    acc, ci = TL.accuracy_ci(hits)
                    pts.append({"value": v, "accuracy": acc,
                                "ci95": list(ci), "n": eps})
                return self._json({
                    "var": var, "points": pts,
                    "strategy_display": S.STRATEGY_DISPLAY.get(name, name),
                    "execution_type": "live",
                    "evidence_type": evidence_for([name]),
                    "badges": ["LIVE", "SYNTHETIC"],
                })
            return self._json({"error": "unknown endpoint"}, 404)
        except Exception as e:
            return self._json({"error": f"{type(e).__name__}: {e}"}, 500)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8001)
    args = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"AdaptLab on http://127.0.0.1:{args.port}  (Ctrl-C to stop)",
          flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
