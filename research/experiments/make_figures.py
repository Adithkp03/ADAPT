"""Generate Phase 2 figures from results.json files. System python."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).parent
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)


def load(*parts):
    return json.loads((ROOT.joinpath(*parts) / "results.json").read_text())


def fig_acquisition():
    r = load("001_task_acquisition_linear")
    names = list(r["summary"].keys())
    acc = [r["summary"][n]["accuracy"] for n in names]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(names, acc, color=["#999", "#4C78A8", "#E45756", "#54A24B", "#B279A2"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("accuracy (N=200, linear, 4 demos)")
    ax.set_title("Exp A — task acquisition by adaptation substrate")
    for i, v in enumerate(acc):
        ax.text(i, v + 0.02, f"{v:.2f}", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "fig1_acquisition.png", dpi=120)
    print("fig1")


def fig_demo_scaling():
    r = load("002_demo_scaling_linear")
    xs, series = [], {}
    for label, res in r["sweeps"]:
        k = int(label.split("=")[1])
        xs.append(k)
        for n, m in res["summary"].items():
            series.setdefault(n, []).append(m["accuracy"])
    fig, ax = plt.subplots(figsize=(7, 4))
    for n, ys in series.items():
        ax.plot(xs, ys, marker="o", label=n)
    ax.set_xlabel("demonstrations N_D")
    ax.set_ylabel("accuracy")
    ax.set_title("Exp B — demonstration scaling (linear)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig2_demo_scaling.png", dpi=120)
    print("fig2")


def fig_compute():
    r = load("003_compute_scaling_linear")
    xs, series = [], {}
    for label, res in r["sweeps"]:
        k = int(label.split("=")[1])
        xs.append(k)
        for n, m in res["summary"].items():
            series.setdefault(n, []).append(m["accuracy"])
    fig, ax = plt.subplots(figsize=(7, 4))
    for n, ys in series.items():
        ax.plot(xs, ys, marker="o", label=n)
    ax.set_xlabel("adaptation steps K")
    ax.set_ylabel("accuracy")
    ax.set_title("Exp C — adaptation compute scaling (linear)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig3_compute.png", dpi=120)
    print("fig3")


def fig_capacity():
    r = load("004_state_capacity_linear")
    xs, ys = [], []
    for label, res in r["sweeps"]:
        v = label.split("=")[1]
        xs.append(v)
        ys.append(res["summary"]["state"]["accuracy"])
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(xs, ys, color="#54A24B")
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("state-dim proxy d_s (None=full)")
    ax.set_ylabel("state accuracy")
    ax.set_title("Exp D — capacity proxy cliff (linear)")
    fig.tight_layout()
    fig.savefig(FIG / "fig4_capacity.png", dpi=120)
    print("fig4")


def fig_interference():
    for fam in ["linear", "symbolic"]:
        r = load(f"005_interference_{fam}")
        names = list(r["summary"].keys())
        a0 = [r["summary"][n]["acc_A_initial"] for n in names]
        rt = [r["summary"][n]["retention_A"] for n in names]
        x = range(len(names))
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar([i - 0.2 for i in x], a0, 0.4, label="initial A")
        ax.bar([i + 0.2 for i in x], rt, 0.4, label="retention A after B")
        ax.set_xticks(list(x))
        ax.set_xticklabels(names, fontsize=8)
        ax.set_ylim(0, 1.05)
        ax.set_title(f"Exp E — interference A->B->A ({fam})")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(FIG / f"fig5_interference_{fam}.png", dpi=120)
    print("fig5")


def fig_intervention():
    r = load("008_intervention_linear")
    for strat in ["state"]:
        d = r["summary"][strat]
        perts = list(d.keys())
        base = [d[p]["acc_base"] for p in perts]
        pert = [d[p]["acc_perturbed"] for p in perts]
        x = range(len(perts))
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar([i - 0.2 for i in x], base, 0.4, label="adapted")
        ax.bar([i + 0.2 for i in x], pert, 0.4, label="state destroyed")
        ax.set_xticks(list(x))
        ax.set_xticklabels(perts)
        ax.set_ylim(0, 1.05)
        ax.set_title("E8 — causal state intervention (linear, state strategy)")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(FIG / "fig6_intervention.png", dpi=120)
    print("fig6")


def fig_frontier():
    """Adaptation gain (over frozen, linear 001) vs retention (005 linear)."""
    a = load("001_task_acquisition_linear")
    e = load("005_interference_linear")
    frozen = a["summary"]["frozen"]["accuracy"]
    fig, ax = plt.subplots(figsize=(6, 4))
    for n in ["context", "param_tta", "state", "ttt_state"]:
        gain = a["summary"][n]["accuracy"] - frozen
        ret = e["summary"][n]["retention_A"]
        ax.scatter(gain, ret, s=80, label=n)
        ax.annotate(n, (gain, ret), fontsize=8, xytext=(4, 4),
                    textcoords="offset points")
    ax.set_xlabel("adaptation gain over frozen (Exp A)")
    ax.set_ylabel("retention of A after B (Exp E)")
    ax.set_title("Frontier — gain vs retention (linear)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "fig7_frontier.png", dpi=120)
    print("fig7")


if __name__ == "__main__":
    fig_acquisition()
    fig_demo_scaling()
    fig_compute()
    fig_capacity()
    fig_interference()
    fig_intervention()
    fig_frontier()
    print("all figures done")
