import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from adapt.runner import run


def _cfg():
    return {"protocol": "standard", "family": "linear",
            "strategies": ["frozen", "context", "param_tta", "state"],
            "strategy_kwargs": {"param_tta": {"steps": 4, "lr": 0.05},
                                "state": {"state_dim": None, "seed": 0}},
            "seeds": list(range(20)), "n_demos": 4, "noise": 0.0,
            "split": "eval", "tol": 0.5}


def test_runner_reproducible():
    r1 = run(_cfg())
    r2 = run(_cfg())
    for name in r1["summary"]:
        for k in ("accuracy", "ci95", "n", "mean_persistent_delta",
                  "mean_state_delta"):
            assert r1["summary"][name][k] == r2["summary"][name][k], (name, k)
    assert r1["provenance"]["config_hash"] == r2["provenance"]["config_hash"]
    assert r1["diffs"] == r2["diffs"]


def test_paired_same_tasks_improve_signal():
    # context should beat frozen on linear with 4 demos (paired same tasks)
    r = run(_cfg())
    assert r["summary"]["context"]["accuracy"] > r["summary"]["frozen"]["accuracy"]
    d = r["diffs"]["context_minus_frozen"]
    assert d["diff"] > 0
