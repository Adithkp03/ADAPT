import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from adapt.tasks import generate_task
from adapt.strategies import make_strategy
from adapt.runner import run


def test_quadratic_state_fits_quadratic():
    t = generate_task("quadratic", 9, n_demos=8, split="test")
    s = make_strategy("state", family="quadratic")
    s.reset()
    s.adapt(t.demonstrations)
    assert abs(s.predict(t.query) - t.ground_truth) < 1.0


def test_symbolic_affine_state():
    t = generate_task("symbolic", 9, n_demos=4, split="test")
    s = make_strategy("state", family="symbolic")
    s.reset()
    s.adapt(t.demonstrations)
    assert s.predict(t.query) == t.ground_truth


def test_new_names_resolve():
    assert make_strategy("context", family="linear").name == "context"
    assert make_strategy("param_tta", family="linear").name == "param_tta"
    assert make_strategy("state", family="linear").name == "state"


def test_split_latency_fields():
    r = run({"protocol": "standard", "family": "linear",
             "strategies": ["state"], "strategy_kwargs": {},
             "seeds": list(range(5)), "n_demos": 4, "split": "test"})
    tel = r["summary"]["state"]
    assert "mean_latency_ms" in tel
    assert r["evidence_type"] == "CONTROLLED_TOY"


def test_mcnemar_present_in_diffs():
    r = run({"protocol": "standard", "family": "symbolic",
             "strategies": ["frozen", "state"], "strategy_kwargs": {},
             "seeds": list(range(20)), "n_demos": 4, "split": "test"})
    d = r["diffs"]["state_minus_frozen"]
    assert "mcnemar_p" in d and "cohen_h" in d
    assert d["mcnemar_p"] < 0.05
