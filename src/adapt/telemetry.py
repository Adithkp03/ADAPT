"""Correctness predicates + CI helpers (paired design)."""
import numpy as np


def l2_delta(after, before):
    a = np.asarray(after, dtype=float).ravel()
    b = np.asarray(before, dtype=float).ravel()
    return float(np.linalg.norm(a - b))


def regression_correct(pred, truth, tol=0.5):
    return abs(float(pred) - float(truth)) <= tol


def exact_correct(pred, truth):
    return list(pred) == list(truth)


def grid_correct(pred, truth):
    return [list(r) for r in pred] == [list(r) for r in truth]


def is_correct(family, pred, truth, tol=0.5):
    if family in ("linear", "quadratic"):
        return regression_correct(pred, truth, tol)
    if family in ("symbolic", "compositional"):
        return exact_correct(pred, truth)
    return grid_correct(pred, truth)


def accuracy_ci(hits, alpha=0.05):
    """Wilson 95% CI for a proportion."""
    n = len(hits)
    if n == 0:
        return 0.0, (0.0, 0.0)
    p = sum(1 for h in hits if h) / n
    z = 1.96
    den = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * ((p * (1 - p) + z * z / (4 * n)) / n) ** 0.5
    return p, (max(0.0, (c - m) / den), min(1.0, (c + m) / den))


def paired_diff_ci(a_hits, b_hits, n_boot=2000, seed=0):
    """Bootstrap 95% CI for paired accuracy difference (a - b)."""
    rng = np.random.RandomState(seed)
    a = np.array([1 if h else 0 for h in a_hits])
    b = np.array([1 if h else 0 for h in b_hits])
    d = a - b
    boots = [rng.choice(d, size=len(d), replace=True).mean() for _ in range(n_boot)]
    return float(d.mean()), (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))
