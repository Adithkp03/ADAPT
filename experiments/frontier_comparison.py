"""D4.7 frontier comparison study: adaptation gain vs retention per mechanism.

Compares OUR measurements (linear family, test split) across controlled +
learned substrates. Published BDH/BDH-CQ rows appear in the markdown ONLY,
never in the same numbers table — mechanism-level comparison (§23).

Outputs:
  research/bdh/frontier_comparison.csv
  research/experiments/figures/fig8_frontier_tradeoff.png
Run: system-python experiments/frontier_comparison.py
"""
import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
import numpy as np

from adapt import runner as R
from adapt import strategies as S
from adapt import tasks as T
from adapt import telemetry as TL

FAMILY = "linear"
N_ACC = 50
N_RET = 20
MECHS = {
    "frozen": {},
    "context": {},
    "param_tta": {"steps": 8, "lr": 0.05},
    "state": {},
    "ttt_state": {"steps": 8, "lr": 0.05},
    "learned_state": {"checkpoint": "checkpoints/learned_rec_s0.npz"},
    "learned_tta": {"checkpoint": "checkpoints/learned_ptt_s0.npz",
                    "steps": 5},
    "learned_ttt": {"checkpoint": "checkpoints/learned_ttt_s0.npz"},
}


def accuracy(name, kw, n):
    hits, lat, dth, dst = [], [], [], []
    for i in range(n):
        t = T.generate_task(FAMILY, i, n_demos=4, noise=0.0, split="test")
        skw = dict(kw)
        skw.setdefault("tol", 0.5)
        r = R.run_episode(t, name, skw)
        hits.append(r["correct"])
        tel = r["telemetry"]
        lat.append(tel["latency_ms"])
        dth.append(tel["persistent_delta"])
        dst.append(tel["state_delta"])
    acc, ci = TL.accuracy_ci(hits)
    return acc, ci, float(np.mean(lat)), float(np.mean(dth)), float(
        np.mean(dst))


def retention(name, kw, n):
    """A->B->A retention of A (fraction of pairs where A stays correct)."""
    keep = []
    for i in range(n):
        s = 1000 + i
        tA = T.generate_task(FAMILY, s, n_demos=4, noise=0.0, split="test")
        tB = None
        for a in range(10):
            c = T.generate_task(FAMILY, 100000 + s * 10 + a, n_demos=4,
                                noise=0.0, split="test")
            if c.hidden_rule != tA.hidden_rule:
                tB = c
                break
        st = S.make_strategy(name, family=FAMILY,
                             **{k: v for k, v in kw.items()
                                if k != "tol"})
        st.reset()
        st.adapt(tA.demonstrations)
        if name == "context":
            p0 = st.predict(tA.query, family=FAMILY)
            st.adapt(tB.demonstrations)
            p1 = st.predict(tA.query, family=FAMILY)
        else:
            p0 = st.predict(tA.query)
            st.adapt(tB.demonstrations)
            p1 = st.predict(tA.query)
        ok0 = TL.is_correct(FAMILY, p0, tA.ground_truth, 0.5)
        ok1 = TL.is_correct(FAMILY, p1, tA.ground_truth, 0.5)
        keep.append((ok0, ok1))
    a0 = sum(1 for k, _ in keep if k) / n
    ret = sum(1 for k, k2 in keep if k and k2) / max(1, sum(
        1 for k, _ in keep if k))
    return a0, ret


def main():
    rows = []
    for name, kw in MECHS.items():
        acc, ci, lat, dth, dst = accuracy(name, kw, N_ACC)
        a0, ret = retention(name, kw, N_RET)
        rows.append({"mechanism": name, "display": S.STRATEGY_DISPLAY[name],
                     "accuracy": round(acc, 3),
                     "ci95_lo": round(ci[0], 3), "ci95_hi": round(ci[1], 3),
                     "latency_ms": round(lat, 3),
                     "mean_persistent_delta": round(dth, 4),
                     "mean_state_delta": round(dst, 3),
                     "acc_A_initial": round(a0, 3),
                     "retention_A": round(ret, 3),
                     "n_acc": N_ACC, "n_ret": N_RET})
        print(f"{name}: acc={acc:.3f} ret={ret:.3f} lat={lat:.2f}ms "
              f"dTh={dth:.4f} dS={dst:.2f}", flush=True)
    frozen_acc = rows[0]["accuracy"]
    for r in rows:
        r["adaptation_gain"] = round(r["accuracy"] - frozen_acc, 3)
    out = ROOT / "research" / "bdh" / "frontier_comparison.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out}")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        for r in rows:
            ax[0].scatter(r["adaptation_gain"], r["retention_A"])
            ax[0].annotate(r["mechanism"], (r["adaptation_gain"],
                                            r["retention_A"]), fontsize=8)
        ax[0].set_xlabel("adaptation gain (acc − frozen acc, linear)")
        ax[0].set_ylabel("retention of A after B (A→B→A)")
        ax[0].set_title("Gain vs retention — OUR measurements only")
        ax[0].grid(True, alpha=0.3)
        for r in rows:
            ax[1].scatter(r["latency_ms"], r["accuracy"])
            ax[1].annotate(r["mechanism"], (r["latency_ms"], r["accuracy"]),
                           fontsize=8)
        ax[1].set_xlabel("mean latency per episode (ms)")
        ax[1].set_ylabel("accuracy (linear, 50 eps)")
        ax[1].set_title("Cost vs accuracy — OUR measurements only")
        ax[1].grid(True, alpha=0.3)
        fig.tight_layout()
        figpath = (ROOT / "research" / "experiments" / "figures" /
                   "fig8_frontier_tradeoff.png")
        fig.savefig(figpath, dpi=100)
        print(f"wrote {figpath}")
    except ImportError:
        print("matplotlib unavailable — CSV only")


if __name__ == "__main__":
    main()
