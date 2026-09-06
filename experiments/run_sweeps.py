"""Sweep driver: demo scaling (002), compute (003), capacity (004),
noise (006), complexity (007). Writes one JSON per sweep under
research/experiments/<id>/results.json. Run with system python."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from adapt.runner import run_with_protocol, sweep

OUT = Path(__file__).parent.parent / "research" / "experiments"
BASE_KW = {"param_tta": {"steps": 8, "lr": 0.05},
           "state": {"state_dim": None, "seed": 0},
           "ttt_state": {"steps": 8, "lr": 0.05}}


def base(family, strategies, seeds=100, n_demos=4, noise=0.0):
    return {"protocol": "standard", "family": family,
            "strategies": strategies, "strategy_kwargs": dict(BASE_KW),
            "seeds": list(range(seeds)), "n_demos": n_demos,
            "noise": noise, "split": "eval", "tol": 0.5}


def save(exp_id, payload):
    d = OUT / exp_id
    d.mkdir(parents=True, exist_ok=True)
    p = d / "results.json"
    p.write_text(json.dumps(payload, indent=2, default=str))
    print(f"[{exp_id}] wrote {p}")
    for label, r in payload["sweeps"]:
        parts = " | ".join(
            f"{n}={m['accuracy']:.2f}" for n, m in r["summary"].items())
        print(f"  {label}: {parts}")


def exp_002():
    """Demo scaling N_D=1..8, linear + symbolic."""
    for fam, strats in [("linear", ["frozen", "context", "param_tta", "state", "ttt_state"]),
                        ("symbolic", ["frozen", "context", "param_tta", "state"])]:
        b = base(fam, strats)
        if fam == "symbolic":
            b["strategy_kwargs"] = {"param_tta": {"steps": 8, "lr": 0.5},
                                    "state": {"state_dim": None, "seed": 0}}
        sw = sweep(b, "n_demos", [1, 2, 3, 4, 6, 8])
        save(f"002_demo_scaling_{fam}", {"sweeps": sw})


def exp_003():
    """Compute scaling: param_TTA steps 0..16 and ttt_state steps."""
    import copy
    b = base("linear", ["param_tta", "ttt_state", "state"])
    out = []
    for k in [0, 1, 2, 4, 8, 16]:
        cfg = copy.deepcopy(b)
        cfg["strategy_kwargs"]["param_tta"]["steps"] = k
        cfg["strategy_kwargs"]["ttt_state"]["steps"] = k
        out.append((f"K={k}", run_with_protocol(cfg)))
    save("003_compute_scaling_linear", {"sweeps": out})


def exp_004():
    """Capacity proxy: state_dim None(full),4,2,1 on linear (stat dim 5).

    d_s is an OPERATIONAL PROXY: prediction reads stats through a
    project-and-reconstruct bottleneck, lossy when d_s < 5.
    """
    out = []
    for d in [None, 4, 2, 1]:
        cfg = base("linear", ["state", "context"])
        cfg["strategy_kwargs"] = {"state": {"state_dim": d, "seed": 0}}
        out.append((f"d_s={d}", run_with_protocol(cfg)))
    save("004_state_capacity_linear", {"sweeps": out})


def exp_006():
    """Noise robustness epsilon 0..0.2, linear + symbolic."""
    for fam in ["linear", "symbolic"]:
        strats = ["context", "param_tta", "state"]
        b = base(fam, strats)
        if fam == "symbolic":
            b["strategy_kwargs"] = {"param_tta": {"steps": 8, "lr": 0.5},
                                    "state": {"state_dim": None, "seed": 0}}
        sw = sweep(b, "noise", [0.0, 0.05, 0.1, 0.2, 0.35])
        save(f"006_noise_{fam}", {"sweeps": sw})


def exp_007():
    """Complexity sweep across families (fixed strategies)."""
    import copy
    out = []
    for fam in ["linear", "quadratic", "symbolic", "compositional"]:
        strats = ["context", "param_tta", "state"]
        cfg = base(fam, strats)
        if fam in ("symbolic", "compositional"):
            cfg["strategy_kwargs"] = {"param_tta": {"steps": 8, "lr": 0.5},
                                      "state": {"state_dim": None, "seed": 0}}
        if fam == "quadratic":
            cfg["strategy_kwargs"] = {"param_tta": {"steps": 16, "lr": 0.05},
                                      "state": {"state_dim": None, "seed": 0},
                                      "ttt_state": {"steps": 16, "lr": 0.05}}
            cfg["strategies"] = ["context", "param_tta", "state", "ttt_state"]
        out.append((fam, run_with_protocol(cfg)))
    save("007_complexity", {"sweeps": out})


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = {"002": exp_002, "003": exp_003, "004": exp_004,
            "006": exp_006, "007": exp_007}
    if which == "all":
        for f in jobs.values():
            f()
    else:
        jobs[which]()
