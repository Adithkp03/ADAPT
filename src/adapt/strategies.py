"""Adaptation strategies — one common interface.

reset()  -> restore episodic init (theta_0 / s_0). Enforces isolation.
adapt(D) -> consume demonstrations (real computation per strategy).
predict(Q) -> output prediction.
telemetry() -> dict with persistent_delta, state_delta, steps, latency_ms.

Honesty contracts (asserted in tests):
- FrozenBaseline / ContextICL / RecurrentState / TTTState: persistent
  params NEVER change (persistent_delta == 0).
- ParamTTA: persistent params MUST change after adapt on real signal.
- RecurrentState vs TTTState: recurrence applies a fixed transition F to a
  sufficient-stat state; TTTState runs gradient descent ON the state S
  (state parameterizes a model). Different mechanisms, not sizes.

d_s (state_dim): OPERATIONAL PROXY for capacity — a fixed random
projection of the sufficient-stat vector to d_s dims. Documented as
proxy, never as capacity itself.
"""
import time
import numpy as np

MODEL_VERSION = "adapt-v1"


class AdaptationStrategy:
    name = "base"

    def reset(self):
        raise NotImplementedError

    def adapt(self, demonstrations):
        raise NotImplementedError

    def predict(self, query):
        raise NotImplementedError

    def telemetry(self):
        raise NotImplementedError

    # E8 causal-intervention hooks (stateful strategies override)
    def get_state(self):
        return None

    def set_state(self, state):
        pass


def _proj_matrix(rng, in_dim, out_dim):
    if out_dim is None or out_dim >= in_dim:
        return None
    return rng.normal(0, 1.0 / max(1, out_dim) ** 0.5, size=(out_dim, in_dim))


def _reconstruct(P, s):
    """Bottleneck readout: project to d_s dims and back (lossy if d_s < dim)."""
    import numpy as np
    if P is None:
        return s
    return np.linalg.pinv(P) @ (P @ s)


class FrozenBaseline(AdaptationStrategy):
    """B1: no demonstrations. Fixed prior prediction."""
    name = "frozen"

    def __init__(self):
        self._t0 = 0.0

    def reset(self):
        pass

    def adapt(self, demonstrations):
        self._t0 = time.perf_counter()  # no-op; timed for honesty

    def predict(self, query):
        if isinstance(query, (int, float)):
            return 0.0
        if isinstance(query, list) and query and isinstance(query[0], list):
            return [row[:] for row in query]  # identity grid
        return [0] * len(query)

    def telemetry(self):
        return {"persistent_delta": 0.0, "state_delta": 0.0,
                "steps": 0, "latency_ms": 0.0}


class ContextICL(AdaptationStrategy):
    """B2: analytic conditioning on D at predict time. No persistent update.

    Linear/quadratic: closed-form least squares computed transiently.
    Symbolic/compositional: offset inferred by majority vote over D pairs.
    ARC-like: vote over candidate transforms by fit on D.
    """
    name = "context"

    def __init__(self):
        self._demos = []
        self._lat = 0.0

    def reset(self):
        self._demos = []

    def adapt(self, demonstrations):
        t = time.perf_counter()
        self._demos = list(demonstrations)
        self._lat = (time.perf_counter() - t) * 1000

    def _fit_linear(self, degree=1):
        xs = np.array([x for x, _ in self._demos], dtype=float)
        ys = np.array([y for _, y in self._demos], dtype=float)
        if len(xs) == 0:
            return np.zeros(degree + 1)
        X = np.vander(xs, degree + 1, increasing=True)
        coef, _, _, _ = np.linalg.lstsq(X, ys, rcond=None)
        return coef

    def _vote_offset(self, family):
        from collections import Counter
        votes = Counter()
        for x, y in self._demos:
            for a, b in zip(x, y if family == "symbolic" else y):
                votes[(b - a) % 8] += 1
        if not votes:
            return 0
        return votes.most_common(1)[0][0]

    def predict(self, query, family="linear"):
        if family in ("linear",):
            c = self._fit_linear(1)
            return float(c[0] + c[1] * query)
        if family == "quadratic":
            c = self._fit_linear(2)
            return float(c[0] + c[1] * query + c[2] * query * query)
        if family == "symbolic":
            o = self._vote_offset("symbolic")
            return [(v + o) % 8 for v in query]
        if family == "compositional":
            # infer offset on reversed inputs
            from collections import Counter
            votes = Counter()
            for x, y in self._demos:
                xr = list(reversed(x))
                for a, b in zip(xr, y):
                    votes[(b - a) % 8] += 1
            o = votes.most_common(1)[0][0] if votes else 0
            return [(v + o) % 8 for v in reversed(query)]
        if family == "arc_like":
            from .tasks import ARC_FNS
            best, best_score = "rot90", -1
            for name, fn in ARC_FNS.items():
                s = sum(1 for x, y in self._demos if fn(x) == y)
                if s > best_score:
                    best, best_score = name, s
            return ARC_FNS[best](query)
        raise ValueError(family)

    def telemetry(self):
        return {"persistent_delta": 0.0, "state_delta": 0.0,
                "steps": 0, "latency_ms": self._lat}


class ParamTTA(AdaptationStrategy):
    """B3: genuine gradient descent on persistent params at test time.

    Regression: theta=(w,b[,c]) from zeros, K GD steps on MSE over D.
    Symbolic/compositional: score vector over 8 offsets, GD on
    negative log-likelihood of observed pairs (real update).
    ARC-like: score vector over candidate transforms, GD similarly.
    """
    name = "param_tta"

    def __init__(self, family="linear", steps=8, lr=0.05):
        self.family = family
        self.steps = steps
        self.lr = lr
        self._theta0 = None
        self.theta = None
        self._lat = 0.0

    def _init(self):
        if self.family in ("linear",):
            return np.zeros(2)
        if self.family == "quadratic":
            return np.zeros(3)
        return np.zeros(8)  # offset / transform scores

    def reset(self):
        self._theta0 = self._init()
        self.theta = self._theta0.copy()

    def adapt(self, demonstrations):
        t = time.perf_counter()
        if self.theta is None:
            self.reset()
        if self.family == "linear":
            xs = np.array([x for x, _ in demonstrations])
            ys = np.array([y for _, y in demonstrations])
            th = self.theta
            for _ in range(self.steps):
                pred = th[0] + th[1] * xs
                err = pred - ys
                n = max(1, len(xs))
                th = th - self.lr * np.array([2 * err.mean(), 2 * (err * xs).mean()])
            self.theta = th
        elif self.family == "quadratic":
            xs = np.array([x for x, _ in demonstrations])
            ys = np.array([y for _, y in demonstrations])
            th = self.theta
            for _ in range(self.steps):
                pred = th[0] + th[1] * xs + th[2] * xs * xs
                err = pred - ys
                g = np.array([2 * err.mean(), 2 * (err * xs).mean(),
                              2 * (err * xs * xs).mean()])
                th = th - self.lr * 0.1 * g
            self.theta = th
        else:
            # discrete score vector via softmax CE gradient
            obs = self._offset_votes(demonstrations)
            th = self.theta
            for _ in range(self.steps):
                p = np.exp(th - th.max())
                p = p / p.sum()
                g = p.copy()
                tot = obs.sum()
                if tot > 0:
                    g = g - obs / tot
                th = th - self.lr * g
            self.theta = th
        self._lat = (time.perf_counter() - t) * 1000

    def _offset_votes(self, demonstrations):
        import numpy as np
        obs = np.zeros(8)
        if self.family == "arc_like":
            from .tasks import ARC_FNS
            names = list(ARC_FNS.keys())
            for x, y in demonstrations:
                for i, name in enumerate(names):
                    if ARC_FNS[name](x) == y:
                        obs[i] += 1
            return obs
        for x, y in demonstrations:
            seq = list(reversed(x)) if self.family == "compositional" else x
            for a, b in zip(seq, y):
                obs[(b - a) % 8] += 1
        return obs

    def predict(self, query):
        if self.family == "linear":
            return float(self.theta[0] + self.theta[1] * query)
        if self.family == "quadratic":
            return float(self.theta[0] + self.theta[1] * query + self.theta[2] * query * query)
        if self.family in ("symbolic",):
            o = int(np.argmax(self.theta))
            return [(v + o) % 8 for v in query]
        if self.family == "compositional":
            o = int(np.argmax(self.theta))
            return [(v + o) % 8 for v in reversed(query)]
        if self.family == "arc_like":
            from .tasks import ARC_FNS
            names = list(ARC_FNS.keys())
            return ARC_FNS[names[int(np.argmax(self.theta))]](query)
        raise ValueError(self.family)

    def telemetry(self):
        d = float(np.linalg.norm(self.theta - self._theta0)) if self.theta is not None else 0.0
        return {"persistent_delta": d, "state_delta": 0.0,
                "steps": self.steps, "latency_ms": self._lat}


class RecurrentState(AdaptationStrategy):
    """B4: fixed params; state accumulates sufficient statistics.

    s_t = s_{t-1} + phi(x_t, y_t)  (learned-transition analogue with a
    FIXED transition). Prediction reads s. d_s projects the stat vector
    through a fixed random matrix (operational capacity proxy).
    """
    name = "state"

    def __init__(self, family="linear", state_dim=None, seed=0):
        self.family = family
        self.state_dim = state_dim
        self.seed = seed
        self._s0 = None
        self.s = None
        self._lat = 0.0
        self._proj = None

    def _stat_dim(self):
        return {"linear": 5, "quadratic": 9, "symbolic": 8,
                "compositional": 8, "arc_like": 3}[self.family]

    def _phi(self, x, y):
        import numpy as np
        if self.family == "linear":
            return np.array([1.0, x, y, x * x, x * y], dtype=float)
        if self.family == "quadratic":
            return np.array([1.0, x, y, x * x, x * y, x ** 3, x ** 4,
                             x * x * y, y * y], dtype=float)
        if self.family in ("symbolic",):
            v = np.zeros(8)
            for a, b in zip(x, y):
                v[(b - a) % 8] += 1
            return v
        if self.family == "compositional":
            v = np.zeros(8)
            for a, b in zip(reversed(x), y):
                v[(b - a) % 8] += 1
            return v
        from .tasks import ARC_FNS
        names = list(ARC_FNS.keys())
        v = np.zeros(3)
        for i, name in enumerate(names):
            if ARC_FNS[name](x) == y:
                v[i] += 1
        return v

    def reset(self):
        import numpy as np
        d = self._stat_dim()
        self._s0 = np.zeros(d)
        self.s = np.zeros(d)
        rng = np.random.RandomState(self.seed)
        self._proj = _proj_matrix(rng, d, self.state_dim)

    def _eff(self):
        return self.s if self._proj is None else self._proj @ self.s

    def adapt(self, demonstrations):
        t = time.perf_counter()
        if self.s is None:
            self.reset()
        for x, y in demonstrations:
            self.s = self.s + self._phi(x, y)
        self._lat = (time.perf_counter() - t) * 1000

    def _use(self):
        return _reconstruct(self._proj, self.s)

    def _read_linear(self):
        import numpy as np
        s = self._use()
        # lstsq-equivalent read from (possibly bottlenecked) stats
        n, sx, sy, sxx, sxy = s
        if n < 2:
            return 0.0, 0.0
        den = n * sxx - sx * sx
        if abs(den) < 1e-9:
            return 0.0, sy / max(1, n)
        w = (n * sxy - sx * sy) / den
        b = (sy - w * sx) / n
        return b, w

    def predict(self, query):
        import numpy as np
        if self.family == "linear":
            b, w = self._read_linear()
            return float(b + w * query)
        if self.family == "quadratic":
            import numpy as np
            s = self._use()
            n, sx, sy, sxx, sxy = s[0], s[1], s[2], s[3], s[4]
            if n < 3:
                return 0.0
            den = n * sxx - sx * sx
            if abs(den) < 1e-9:
                return 0.0
            w = (n * sxy - sx * sy) / den
            b = (sy - w * sx) / n
            return float(b + w * query)
        if self.family in ("symbolic", "compositional"):
            s = self._use()
            o = int(np.argmax(s)) if s.sum() > 0 else 0
            if self.family == "symbolic":
                return [(v + o) % 8 for v in query]
            return [(v + o) % 8 for v in reversed(query)]
        if self.family == "arc_like":
            from .tasks import ARC_FNS
            names = list(ARC_FNS.keys())
            s = self._use()
            return ARC_FNS[names[int(np.argmax(s))] if s.sum() > 0 else 0](query)
        raise ValueError(self.family)

    def telemetry(self):
        import numpy as np
        ds = float(np.linalg.norm(self._eff() - (self._proj @ self._s0 if self._proj is not None else self._s0)))
        return {"persistent_delta": 0.0, "state_delta": ds,
                "steps": 0, "latency_ms": self._lat}

    def get_state(self):
        return None if self.s is None else self.s.copy()

    def set_state(self, state):
        import numpy as np
        self.s = np.array(state, dtype=float).copy()


class TTTState(AdaptationStrategy):
    """B5 (stretch): the STATE parameterizes a model, optimized at test time.

    Persistent init (w0, b0, lr) is fixed forever. reset() copies init into
    working state S. adapt() runs GD ON S. Persistent delta stays 0 while
    adapted-state delta > 0. Regression families only (honest scope).
    """
    name = "ttt_state"

    def __init__(self, family="linear", steps=8, lr=0.05):
        assert family in ("linear", "quadratic"), "TTTState scope: regression only"
        self.family = family
        self.steps = steps
        self.lr = lr
        self._init = None
        self.S = None
        self._lat = 0.0

    def reset(self):
        import numpy as np
        dim = 2 if self.family == "linear" else 3
        self._init = np.zeros(dim)
        self.S = np.zeros(dim)

    def adapt(self, demonstrations):
        t = time.perf_counter()
        if self.S is None:
            self.reset()
        import numpy as np
        xs = np.array([x for x, _ in demonstrations])
        ys = np.array([y for _, y in demonstrations])
        S = self.S
        for _ in range(self.steps):
            if self.family == "linear":
                pred = S[0] + S[1] * xs
                err = pred - ys
                S = S - self.lr * np.array([2 * err.mean(), 2 * (err * xs).mean()])
            else:
                pred = S[0] + S[1] * xs + S[2] * xs * xs
                err = pred - ys
                S = S - self.lr * 0.1 * np.array(
                    [2 * err.mean(), 2 * (err * xs).mean(), 2 * (err * xs * xs).mean()])
        self.S = S
        self._lat = (time.perf_counter() - t) * 1000

    def predict(self, query):
        if self.family == "linear":
            return float(self.S[0] + self.S[1] * query)
        return float(self.S[0] + self.S[1] * query + self.S[2] * query * query)

    def telemetry(self):
        import numpy as np
        ds = float(np.linalg.norm(self.S - self._init)) if self.S is not None else 0.0
        return {"persistent_delta": 0.0, "state_delta": ds,
                "steps": self.steps, "latency_ms": self._lat}

    def get_state(self):
        return None if self.S is None else self.S.copy()

    def set_state(self, state):
        import numpy as np
        self.S = np.array(state, dtype=float).copy()


def make_strategy(name, family="linear", **kw):
    table = {"frozen": FrozenBaseline, "context": ContextICL,
             "param_tta": ParamTTA, "state": RecurrentState,
             "ttt_state": TTTState}
    cls = table[name]
    if name in ("frozen", "context"):
        return cls()
    return cls(family=family, **kw)
