"""P0 review fixes: learned E8, nullmean control, Holm correction."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from adapt.runner import run_intervention
from adapt.telemetry import holm_bonferroni


def test_learned_intervention_nonempty():
    ckpt = Path(__file__).parent.parent / "checkpoints" / "learned_rec_s0.npz"
    if not ckpt.exists():
        return  # no checkpoint in this env; analytical path covers CI
    cfg = {"protocol": "intervention", "family": "linear",
           "strategies": ["learned_state"],
           "strategy_kwargs": {"learned_state": {"checkpoint": str(ckpt)}},
           "task_seeds": list(range(10)), "n_demos": 4,
           "noise": 0.0, "split": "test", "tol": 0.5,
           "perturbations": ["zero", "swap", "nullmean"]}
    res = run_intervention(cfg)
    assert "learned_state" in res["summary"], res["summary"].keys()
    assert "nullmean" in res["summary"]["learned_state"]
    row = res["summary"]["learned_state"]["nullmean"]
    assert "mcnemar_p_holm" in row and "holm_reject" in row


def test_analytical_nullmean_and_holm():
    cfg = {"protocol": "intervention", "family": "linear",
           "strategies": ["state"],
           "strategy_kwargs": {"state": {}},
           "task_seeds": list(range(10)), "n_demos": 4,
           "noise": 0.0, "split": "test", "tol": 0.5,
           "perturbations": ["zero", "shuffle", "noise", "swap", "nullmean"]}
    res = run_intervention(cfg)
    s = res["summary"]["state"]
    assert set(s.keys()) == {"zero", "shuffle", "noise", "swap", "nullmean"}
    # restore ~= base for the zero control on an easy linear task
    assert abs(s["zero"]["acc_restored"] - s["zero"]["acc_base"]) < 1e-9
    assert all("mcnemar_p_holm" in s[p] for p in s)


def test_holm_monotone():
    r = holm_bonferroni([0.01, 0.04, 0.03])
    assert r["p_adjusted"][0] <= r["p_adjusted"][2] <= r["p_adjusted"][1]
    e = holm_bonferroni([])
    assert e == {"reject": [], "p_adjusted": []}
