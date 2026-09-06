"""Phase 2C mechanistic validation: probing, transfer, extrapolation.

- probe: linear probe s' -> (a,b) on learned + analytical states.
- transfer: adapt once on D_A, predict K fresh queries (state reuse).
- extrapolate: queries inside vs outside demo x-range.
Writes research/experiments/009_mechanistic/results.json.
Run with system python after checkpoints exist.
Usage: system-python experiments/mechanistic.py <checkpoint_dir>
"""
import json
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from adapt.tasks import generate_task
from adapt.strategies import make_strategy
from adapt.telemetry import regression_correct

CKPT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("checkpoints")
OUT = Path(__file__).parent.parent / "research" / "experiments" / "009_mechanistic"
OUT.mkdir(parents=True, exist_ok=True)


def collect_states(strategy_name, kw, seeds):
    S, R = [], []
    for s in seeds:
        t = generate_task("linear", s, n_demos=4, split="test")
        st = make_strategy(strategy_name, family="linear", **kw)
        st.reset()
        st.adapt(t.demonstrations)
        S.append(np.asarray(st.get_state(), float).ravel())
        R.append([t.hidden_rule["a"], t.hidden_rule["b"]])
    return np.array(S), np.array(R)


def probe(strategy_name, kw, seeds=(range(0, 60), range(60, 120))):
    """Linear probe fit on first half, MSE on second; chance = mean predictor."""
    Str, Rtr = collect_states(strategy_name, kw, list(seeds[0]))
    Ste, Rte = collect_states(strategy_name, kw, list(seeds[1]))
    X = np.concatenate([Str, np.ones((len(Str), 1))], axis=1)
    W, _, _, _ = np.linalg.lstsq(X, Rtr, rcond=None)
    Xe = np.concatenate([Ste, np.ones((len(Ste), 1))], axis=1)
    pred = Xe @ W
    mse = float(np.mean((pred - Rte) ** 2))
    chance = float(np.mean((Rtr.mean(axis=0) - Rte) ** 2))
    return {"probe_mse": mse, "chance_mse": chance,
            "ratio": mse / chance if chance > 0 else None}


def transfer(strategy_name, kw, n_tasks=50, n_queries=5):
    rng = np.random.RandomState(7)
    hits = []
    for s in range(n_tasks):
        t = generate_task("linear", 5000 + s, n_demos=4, split="test")
        st = make_strategy(strategy_name, family="linear", **kw)
        st.reset()
        st.adapt(t.demonstrations)
        a, b = t.hidden_rule["a"], t.hidden_rule["b"]
        for _ in range(n_queries):
            xq = float(rng.uniform(-5, 5))
            hits.append(regression_correct(st.predict(xq), a * xq + b))
    return {"transfer_acc": sum(hits) / len(hits), "n": len(hits)}


def extrapolate(strategy_name, kw, n_tasks=100):
    rng = np.random.RandomState(11)
    inn, out = [], []
    for s in range(n_tasks):
        t = generate_task("linear", 9000 + s, n_demos=4, split="test")
        st = make_strategy(strategy_name, family="linear", **kw)
        st.reset()
        st.adapt(t.demonstrations)
        a, b = t.hidden_rule["a"], t.hidden_rule["b"]
        xq_in = float(rng.uniform(-5, 5))
        xq_out = float(rng.choice([-1, 1]) * rng.uniform(6, 9))
        inn.append(regression_correct(st.predict(xq_in), a * xq_in + b))
        out.append(regression_correct(st.predict(xq_out), a * xq_out + b))
    return {"interp_acc": sum(inn) / len(inn), "extrap_acc": sum(out) / len(out)}


def main():
    res = {}
    cands = {"analytical_state": ("state", {}),
             "learned_state": ("learned_state",
                               {"checkpoint": str(CKPT / "learned_rec_s0.npz")})}
    for label, (name, kw) in cands.items():
        try:
            pr = probe(name, kw)
        except Exception as e:
            pr = {"error": str(e)}
        tr = transfer(name, kw)
        ex = extrapolate(name, kw)
        res[label] = {"probe": pr, "transfer": tr, "extrapolation": ex}
        print(label, json.dumps(res[label], default=str)[:300])
    (OUT / "results.json").write_text(json.dumps(res, indent=2, default=str))
    print(f"wrote {OUT / 'results.json'}")


if __name__ == "__main__":
    main()
