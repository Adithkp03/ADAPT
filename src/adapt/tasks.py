"""Controlled task generator: T = (R, D, Q, Y). Phase 2B edition.

Model sees (D, Q); evaluator knows (R, Y). Deterministic:
generate_task(...) with same args -> same task.
Splits: train (hyperparam/model selection) / val (tuning) / test
(final eval, never inspected during development). Disjoint rule pools.

Families: linear, quadratic, symbolic (affine y=(a*x+o)%V),
compositional (sampled op chains R1 o R2 o R3), grid_toy
(renamed from arc_like: 6-rule transformation toy, NOT ARC reasoning).

Complexity ladder metadata on every task: n_ops, depth, hypothesis
space size |H|, ambiguity, sparsity, noise. See complexity_report().
"""
from dataclasses import dataclass
import numpy as np

GENERATOR_VERSION = "taskgen-v2"
FAMILIES = ["linear", "quadratic", "symbolic", "compositional", "grid_toy"]
# back-compat alias for Phase 2A configs/results
FAMILY_ALIASES = {"arc_like": "grid_toy", "grid_transform": "grid_toy"}
SPLITS = ["train", "val", "test"]
SPLIT_ALIASES = {"eval": "test"}  # back-compat (Phase 2A)

VOCAB = 8
MULTS = [1, 3, 5]  # invertible mod 8
TRAIN_OFFSETS = [1, 2, 3]
VAL_OFFSETS = [4, 7]
TEST_OFFSETS = [5, 6]


@dataclass
class Task:
    family: str
    hidden_rule: dict
    demonstrations: list
    query: object
    ground_truth: object
    seed: int
    generator_version: str = GENERATOR_VERSION
    split: str = "test"
    complexity: dict = None


def _rng(seed):
    return np.random.RandomState(int(seed))


def _offsets(split):
    return {"train": TRAIN_OFFSETS, "val": VAL_OFFSETS, "test": TEST_OFFSETS}[split]


# ---------- linear / quadratic ----------
def _gen_linear(rng, n_demos, noise, split):
    # Continuous rule space: identical distribution across splits;
    # disjointness is by SEED (task instances never repeat across
    # train/val/test seed sets — enforced by protocol, not by region).
    a = float(rng.uniform(-3, 3))
    if abs(a) < 0.5:
        a = 0.5 if a >= 0 else -0.5
    b = float(rng.uniform(-5, 5))
    r = {"a": a, "b": b}
    xs = rng.uniform(-5, 5, size=n_demos)
    demos = [(float(x), float(a * x + b + rng.normal(0, noise))) for x in xs]
    xq = float(rng.uniform(-5, 5))
    comp = {"n_ops": 1, "depth": 1, "hypothesis_space": "continuous-2d",
            "ambiguity": "low", "sparsity": n_demos, "noise": noise}
    return r, demos, xq, float(a * xq + b), comp


def _gen_quadratic(rng, n_demos, noise, split):
    # Same-distribution note as linear (seed-disjoint, not region-split).
    sgn = -1 if int(rng.randint(0, 2)) == 0 else 1
    a = float(rng.uniform(0.3, 1.5) * sgn)
    b = float(rng.uniform(-2, 2))
    c = float(rng.uniform(-3, 3))
    r = {"a": a, "b": b, "c": c}
    xs = rng.uniform(-3, 3, size=n_demos)
    demos = [(float(x), float(a * x * x + b * x + c + rng.normal(0, noise))) for x in xs]
    xq = float(rng.uniform(-3, 3))
    comp = {"n_ops": 1, "depth": 1, "hypothesis_space": "continuous-3d",
            "ambiguity": "medium", "sparsity": n_demos, "noise": noise}
    return r, demos, xq, float(a * xq * xq + b * xq + c), comp


# ---------- symbolic affine ----------
def _rand_seq(rng, length, vocab=VOCAB):
    return [int(v) for v in rng.randint(0, vocab, size=length)]


def _gen_symbolic(rng, n_demos, noise, split, seq_len=4):
    pool = _offsets(split)
    o = int(pool[rng.randint(0, len(pool))])
    a = int(MULTS[rng.randint(0, len(MULTS))])
    r = {"mult": a, "offset": o, "vocab": VOCAB}
    def apply(s):
        return [(a * v + o) % VOCAB for v in s]
    demos = []
    for _ in range(n_demos):
        s = _rand_seq(rng, seq_len)
        t = apply(s)
        if noise > 0:
            t = [(v + (1 if rng.rand() < noise else 0)) % VOCAB for v in t]
        demos.append((s, t))
    q = _rand_seq(rng, seq_len)
    comp = {"n_ops": 1, "depth": 1, "hypothesis_space": len(MULTS) * (VOCAB - 1),
            "ambiguity": "low", "sparsity": n_demos, "noise": noise}
    return r, demos, q, apply(q), comp


# ---------- compositional op chains ----------
def _sample_chain(rng, split, max_depth=3):
    """Sample 1..max_depth ops. Depth ladder: train<=2, val<=2(new ops), test<=3."""
    cap = {"train": 2, "val": 2, "test": 3}[split]
    depth = int(rng.randint(1, min(max_depth, cap) + 1))
    ops = []
    pool = _offsets(split)
    for _ in range(depth):
        kind = str(rng.choice(["reverse", "shift", "replace", "cond_add"]))
        if kind == "reverse":
            ops.append({"op": "reverse"})
        elif kind == "shift":
            ops.append({"op": "shift", "offset": int(pool[rng.randint(0, len(pool))])})
        elif kind == "replace":
            ops.append({"op": "replace", "frm": int(rng.randint(0, VOCAB)),
                        "to": int(rng.randint(0, VOCAB))})
        else:
            ops.append({"op": "cond_add", "trigger": int(rng.randint(0, VOCAB)),
                        "add": int(pool[rng.randint(0, len(pool))])})
    return ops


def _apply_chain(seq, ops):
    s = list(seq)
    for op in ops:
        if op["op"] == "reverse":
            s = s[::-1]
        elif op["op"] == "shift":
            s = [(v + op["offset"]) % VOCAB for v in s]
        elif op["op"] == "replace":
            s = [op["to"] if v == op["frm"] else v for v in s]
        elif op["op"] == "cond_add":
            s = [(v + op["add"]) % VOCAB if v == op["trigger"] else v for v in s]
    return s


def _gen_compositional(rng, n_demos, noise, split, seq_len=5, max_depth=3):
    ops = _sample_chain(rng, split, max_depth)
    r = {"ops": ops, "vocab": VOCAB}
    demos = []
    for _ in range(n_demos):
        s = _rand_seq(rng, seq_len)
        t = _apply_chain(s, ops)
        if noise > 0:
            t = [(v + (1 if rng.rand() < noise else 0)) % VOCAB for v in t]
        demos.append((s, t))
    q = _rand_seq(rng, seq_len)
    comp = {"n_ops": len(ops), "depth": len(ops),
            "hypothesis_space": "open-ended chains",
            "ambiguity": "high" if len(ops) > 1 else "medium",
            "sparsity": n_demos, "noise": noise}
    return r, demos, q, _apply_chain(q, ops), comp


# ---------- grid toy (honest rename of arc_like) ----------
def _rand_grid(rng, n):
    return [[int(v) for v in rng.randint(0, 4, size=n)] for _ in range(n)]


def _rot90(g):
    return [list(r) for r in zip(*g[::-1])]


def _rot180(g):
    return [row[::-1] for row in g[::-1]]


def _flip_h(g):
    return [row[::-1] for row in g]


def _flip_v(g):
    return g[::-1]


def _transpose(g):
    return [list(r) for r in zip(*g)]


def _shift_color(g):
    return [[(v + 1) % 4 for v in row] for row in g]


GRID_FNS = {"rot90": _rot90, "rot180": _rot180, "flip_h": _flip_h,
            "flip_v": _flip_v, "transpose": _transpose,
            "shift_color": _shift_color}
GRID_TRAIN = ["rot90", "flip_h", "transpose"]
GRID_VAL = ["rot180", "flip_v"]
GRID_TEST = ["shift_color"]
# legacy alias (Phase 2A results)
ARC_FNS = GRID_FNS


def _gen_grid(rng, n_demos, noise, split, n=4):
    pool = {"train": GRID_TRAIN, "val": GRID_VAL, "test": GRID_TEST}[split]
    name = str(pool[rng.randint(0, len(pool))])
    fn = GRID_FNS[name]
    r = {"rule": name, "grid": n}
    demos = []
    for _ in range(n_demos):
        g = _rand_grid(rng, n)
        t = fn(g)
        if noise > 0:
            t = [[(v + 1) % 4 if rng.rand() < noise else v for v in row] for row in t]
        demos.append((g, t))
    q = _rand_grid(rng, n)
    comp = {"n_ops": 1, "depth": 1, "hypothesis_space": len(GRID_FNS),
            "ambiguity": "medium", "sparsity": n_demos, "noise": noise}
    return r, demos, q, fn(q), comp


def to_arc_format(task):
    """Export a grid_toy task in ARC-JSON format (for future ARC-derived eval)."""
    assert task.family == "grid_toy"
    return {"train": [{"input": x, "output": y} for x, y in task.demonstrations],
            "test": [{"input": task.query, "output": task.ground_truth}],
            "rule": task.hidden_rule["rule"], "synthetic": True}


def generate_task(family, seed, n_demos=4, noise=0.0, split="test", **kw):
    family = FAMILY_ALIASES.get(family, family)
    assert family in FAMILIES, f"unknown family {family}"
    split = SPLIT_ALIASES.get(split, split)
    assert split in SPLITS, f"unknown split {split}"
    rng = _rng(seed)
    if family == "linear":
        r, d, q, y, comp = _gen_linear(rng, n_demos, noise, split)
    elif family == "quadratic":
        r, d, q, y = _gen_quadratic(rng, n_demos, noise, split)[:4]
        comp = {"n_ops": 1, "depth": 1, "hypothesis_space": "continuous-3d",
                "ambiguity": "medium", "sparsity": n_demos, "noise": noise}
    elif family == "symbolic":
        r, d, q, y, comp = _gen_symbolic(rng, n_demos, noise, split, kw.get("seq_len", 4))
    elif family == "compositional":
        r, d, q, y, comp = _gen_compositional(rng, n_demos, noise, split,
                                              kw.get("seq_len", 5), kw.get("max_depth", 3))
    else:
        r, d, q, y, comp = _gen_grid(rng, n_demos, noise, split, kw.get("grid", 4))
    return Task(family=family, hidden_rule=r, demonstrations=d, query=q,
                ground_truth=y, seed=int(seed), split=split, complexity=comp)
