"""Phase 2 freeze gate (review patches 1-6)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from adapt.runner import run, RESULT_SCHEMA_VERSION
from adapt.strategies import STRATEGY_DISPLAY, FAMILY_DISPLAY
from adapt.tasks import generate_task


def test_result_schema_version():
    assert RESULT_SCHEMA_VERSION == 1
    cfg = {"family": "linear", "strategies": ["frozen", "state"],
           "strategy_kwargs": {"state": {}},
           "task_seeds": [0, 1, 2], "n_demos": 4,
           "noise": 0.0, "split": "test", "tol": 0.5}
    res = run(cfg)
    assert res["result_schema_version"] == 1


def test_public_display_names():
    # every strategy key has an honest public name; grid family guard
    from adapt.strategies import make_strategy  # noqa
    for k in ["frozen", "context", "param_tta", "state", "ttt_state",
              "learned_state", "learned_tta", "learned_ttt"]:
        assert k in STRATEGY_DISPLAY, k
    assert "ARC" not in FAMILY_DISPLAY["grid_toy"]
    assert FAMILY_DISPLAY["grid_toy"] == "Grid Transformation Lab"
    assert "controlled" in STRATEGY_DISPLAY["state"].lower()
    assert "toy" in STRATEGY_DISPLAY["param_tta"].lower()


def test_grid_transform_alias():
    a = generate_task("grid_transform", 3, n_demos=2, split="test")
    b = generate_task("grid_toy", 3, n_demos=2, split="test")
    assert a.hidden_rule == b.hidden_rule
    assert a.ground_truth == b.ground_truth


def test_latency_split_present():
    cfg = {"family": "linear", "strategies": ["state", "param_tta"],
           "strategy_kwargs": {"state": {},
                               "param_tta": {"steps": 8, "lr": 0.05}},
           "task_seeds": [0, 1, 2], "n_demos": 4,
           "noise": 0.0, "split": "test", "tol": 0.5}
    from adapt.runner import run_episode
    from adapt.tasks import generate_task as gt
    t = gt("linear", 0, n_demos=4, split="test")
    for name, kw in [("state", {}),
                     ("param_tta", {"steps": 8, "lr": 0.05})]:
        r = run_episode(t, name, {"tol": 0.5, **kw})
        tel = r["telemetry"]
        assert tel["t_adapt_ms"] >= 0.0 and tel["t_predict_ms"] >= 0.0
        assert abs(tel["latency_ms"] - (tel["t_adapt_ms"] + tel["t_predict_ms"])) < 1e-9
