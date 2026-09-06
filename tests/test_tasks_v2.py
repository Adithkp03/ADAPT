import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from adapt.tasks import (generate_task, _apply_chain, to_arc_format,
                         GRID_FNS)


def test_affine_symbolic_gt():
    t = generate_task("symbolic", 11, n_demos=3, split="test")
    a, o = t.hidden_rule["mult"], t.hidden_rule["offset"]
    assert t.ground_truth == [(a * v + o) % 8 for v in t.query]


def test_compositional_chain_gt():
    t = generate_task("compositional", 11, n_demos=3, split="test")
    assert t.ground_truth == _apply_chain(t.query, t.hidden_rule["ops"])
    assert 1 <= len(t.hidden_rule["ops"]) <= 3
    assert t.complexity["depth"] == len(t.hidden_rule["ops"])


def test_grid_toy_six_rules_and_arc_format():
    seen = {generate_task("grid_toy", s, split="train").hidden_rule["rule"]
            for s in range(60)}
    assert len(seen) >= 2
    t = generate_task("grid_toy", 5, split="test")
    assert t.hidden_rule["rule"] == "shift_color"
    j = to_arc_format(t)
    assert j["synthetic"] is True and "train" in j and "test" in j


def test_val_split_disjoint_for_grids():
    va = {generate_task("grid_toy", s, split="val").hidden_rule["rule"]
          for s in range(30)}
    te = {generate_task("grid_toy", s, split="test").hidden_rule["rule"]
          for s in range(30)}
    assert va.isdisjoint(te)


def test_aliases():
    assert generate_task("arc_like", 3, split="eval").family == "grid_toy"
