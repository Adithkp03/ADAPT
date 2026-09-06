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


def mcnemar_exact(a_hits, b_hits):
    """Two-sided exact McNemar p-value for paired binary outcomes."""
    import math
    b = sum(1 for a, h in zip(a_hits, b_hits) if a and not h)
    c = sum(1 for a, h in zip(a_hits, b_hits) if (not a) and h)
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def cohen_h(p1, p2):
    """Effect size for two proportions."""
    import math
    return 2 * math.asin(max(0.0, min(1.0, p1)) ** 0.5) - \
        2 * math.asin(max(0.0, min(1.0, p2)) ** 0.5)


def holm_bonferroni(p_values, alpha=0.05):
    """Holm step-down correction. Returns {reject, p_adjusted} aligned to input order."""
    m = len(p_values)
    if m == 0:
        return {"reject": [], "p_adjusted": []}
    order = sorted(range(m), key=lambda i: p_values[i])
    adj = [0.0] * m
    for rank, i in enumerate(order):
        adj[i] = min(1.0, (m - rank) * p_values[i])
    # enforce monotonicity along sorted order
    run_max = 0.0
    for i in order:
        run_max = max(run_max, adj[i])
        adj[i] = run_max
    return {"reject": [p <= alpha for p in adj], "p_adjusted": adj}
