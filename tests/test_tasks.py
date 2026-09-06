import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from adapt.tasks import generate_task, FAMILIES


def test_determinism():
    for fam in FAMILIES:
        a = generate_task(fam, 42, n_demos=4)
        b = generate_task(fam, 42, n_demos=4)
        assert a.demonstrations == b.demonstrations
        assert a.query == b.query
        assert a.ground_truth == b.ground_truth


def test_ground_truth_linear():
    t = generate_task("linear", 7, n_demos=3)
    a, b = t.hidden_rule["a"], t.hidden_rule["b"]
    assert abs(t.ground_truth - (a * t.query + b)) < 1e-9


def test_ground_truth_symbolic():
    t = generate_task("symbolic", 7, n_demos=3)
    o = t.hidden_rule["offset"]
    assert t.ground_truth == [(v + o) % 8 for v in t.query]


def test_ground_truth_arc():
    from adapt.tasks import ARC_FNS
    t = generate_task("arc_like", 7, n_demos=2)
    assert t.ground_truth == ARC_FNS[t.hidden_rule["rule"]](t.query)


def test_leakage_splits_disjoint():
    tr = {generate_task("symbolic", s, split="train").hidden_rule["offset"] for s in range(50)}
    ev = {generate_task("symbolic", s, split="eval").hidden_rule["offset"] for s in range(50)}
    assert tr.isdisjoint(ev), f"leakage: {tr & ev}"
