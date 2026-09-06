"""Controlled task generator: T = (R, D, Q, Y).

Every episode: model sees (D, Q); evaluator knows (R, Y).
Deterministic: generate_task(family, seed, ...) is pure.
Splits: split='train' | 'eval' selects disjoint rule pools so eval
rules are never seen during development (see data_leakage_policy.md).

GT is always computed from the hidden rule WITHOUT observation noise;
demos may carry noise (robustness variable epsilon).
"""
from dataclasses import dataclass, field
import numpy as np

GENERATOR_VERSION = "taskgen-v1"
FAMILIES = ["linear", "quadratic", "symbolic", "compositional", "arc_like"]

# Disjoint rule pools (leakage policy enforcement)
TRAIN_OFFSETS = [1, 2, 3]
EVAL_OFFSETS = [5, 6]
TRAIN_ARC_RULES = ["rot90", "flip_h"]
EVAL_ARC_RULES = ["shift_color"]
VOCAB = 8


@dataclass
class Task:
    family: str
    hidden_rule: dict
    demonstrations: list  # [(x, y)]
    query: object
    ground_truth: object
    seed: int
    generator_version: str = GENERATOR_VERSION
    split: str = "eval"


def _rng(seed):
    return np.random.RandomState(seed)


def _linear_params(rng, split):
    a = float(rng.uniform(-3, -0.5) if split == "train" else rng.uniform(0.5, 3))
    if a == 0:
        a = 1.0
    b = float(rng.uniform(-5, 5))
    return {"a": a, "b": b}


def _gen_linear(rng, n_demos, noise, split):
    r = _linear_params(rng, split)
    xs = rng.uniform(-5, 5, size=n_demos)
    demos = [(float(x), float(r["a"] * x + r["b"] + rng.normal(0, noise))) for x in xs]
    xq = float(rng.uniform(-5, 5))
    return r, demos, xq, float(r["a"] * xq + r["b"])


def _gen_quadratic(rng, n_demos, noise, split):
    sgn = -1 if split == "train" else 1
    a = float(rng.uniform(0.3, 1.5) * sgn)
    b = float(rng.uniform(-2, 2))
    c = float(rng.uniform(-3, 3))
    r = {"a": a, "b": b, "c": c}
    xs = rng.uniform(-3, 3, size=n_demos)
    demos = [(float(x), float(a * x * x + b * x + c + rng.normal(0, noise))) for x in xs]
    xq = float(rng.uniform(-3, 3))
    return r, demos, xq, float(a * xq * xq + b * xq + c)


def _rand_seq(rng, length):
    return [int(v) for v in rng.randint(0, VOCAB, size=length)]


def _shift(seq, o):
    return [(v + o) % VOCAB for v in seq]


def _gen_symbolic(rng, n_demos, noise, split, seq_len=4):
    pool = TRAIN_OFFSETS if split == "train" else EVAL_OFFSETS
    o = int(pool[rng.randint(0, len(pool))])
    r = {"offset": o, "vocab": VOCAB}
    demos = []
    for _ in range(n_demos):
        s = _rand_seq(rng, seq_len)
        t = _shift(s, o)
        if noise > 0:
            t = [(v + (1 if rng.rand() < noise else 0)) % VOCAB for v in t]
        demos.append((s, t))
    q = _rand_seq(rng, seq_len)
    return r, demos, q, _shift(q, o)


def _gen_compositional(rng, n_demos, noise, split, seq_len=4):
    pool = TRAIN_OFFSETS if split == "train" else EVAL_OFFSETS
    o = int(pool[rng.randint(0, len(pool))])
    r = {"offset": o, "ops": ["reverse", "shift"], "vocab": VOCAB}
    def apply(s):
        return _shift(list(reversed(s)), o)
    demos = []
    for _ in range(n_demos):
        s = _rand_seq(rng, seq_len)
        t = apply(s)
        if noise > 0:
            t = [(v + (1 if rng.rand() < noise else 0)) % VOCAB for v in t]
        demos.append((s, t))
    q = _rand_seq(rng, seq_len)
    return r, demos, q, apply(q)


# ---- ARC-like grids ----
def _rand_grid(rng, n):
    return [[int(v) for v in rng.randint(0, 4, size=n)] for _ in range(n)]


def _rot90(g):
    return [list(r) for r in zip(*g[::-1])]


def _flip_h(g):
    return [row[::-1] for row in g]


def _shift_color(g):
    return [[(v + 1) % 4 for v in row] for row in g]


ARC_FNS = {"rot90": _rot90, "flip_h": _flip_h, "shift_color": _shift_color}


def _gen_arc(rng, n_demos, noise, split, n=4):
    pool = TRAIN_ARC_RULES if split == "train" else EVAL_ARC_RULES
    name = str(pool[rng.randint(0, len(pool))])
    fn = ARC_FNS[name]
    r = {"rule": name, "grid": n}
    demos = []
    for _ in range(n_demos):
        g = _rand_grid(rng, n)
        t = fn(g)
        if noise > 0:  # flip cells with prob noise
            t = [[(v + 1) % 4 if rng.rand() < noise else v for v in row] for row in t]
        demos.append((g, t))
    q = _rand_grid(rng, n)
    return r, demos, q, fn(q)


def generate_task(family, seed, n_demos=4, noise=0.0, split="eval", **kw):
    """Deterministic task generation. Same args -> same task."""
    assert family in FAMILIES, f"unknown family {family}"
    rng = _rng(int(seed))
    if family == "linear":
        r, d, q, y = _gen_linear(rng, n_demos, noise, split)
    elif family == "quadratic":
        r, d, q, y = _gen_quadratic(rng, n_demos, noise, split)
    elif family == "symbolic":
        r, d, q, y = _gen_symbolic(rng, n_demos, noise, split, kw.get("seq_len", 4))
    elif family == "compositional":
        r, d, q, y = _gen_compositional(rng, n_demos, noise, split, kw.get("seq_len", 4))
    else:
        r, d, q, y = _gen_arc(rng, n_demos, noise, split, kw.get("grid", 4))
    return Task(family=family, hidden_rule=r, demonstrations=d,
                query=q, ground_truth=y, seed=int(seed), split=split)
