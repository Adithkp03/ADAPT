"""Adaptation strategies — Phase 2B. Honest naming throughout.

Analytical (hand-designed, controlled) substrate — Phase 2A, kept:
- FrozenBaseline: no demonstrations, fixed prior.
- AnalyticalContext: analytic conditioning at predict time (lstsq /
  hypothesis vote). An analytical/contextual oracle baseline, NOT
  learned ICL.
- GradientTaskLearner: minimal parameterized task learner with
  inference-time gradient updates (MSE/CE). NOT an LLM undergoing TTT.
- SufficientStatState: hand-designed sufficient-statistics accumulator
  with fixed transition s_t = s_{t-1} + phi(x,y). NOT a learned
  recurrent neural model.
- TTTState (analytical): state parameterizes a tiny predictor,
  optimized at test time; persistent init fixed.

Learned neural substrate — Phase 2B (see learned.py):
- LearnedRecurrentState, LearnedParamTTA, LearnedTTTState share one
  MLP backbone, meta-trained on the train split, tuned on val,
  evaluated on test.

Common interface: reset/adapt/predict/telemetry + get_state/set_state
+ persistent_parameters. Episodic reset enforced by runner.
d_s is an OPERATIONAL PROXY (project-reconstruct bottleneck), never
capacity itself. Latency is split t_adapt/t_predict; wall-clock from
this CPU toy is NOT a neural-inference cost claim.
"""
import time
import numpy as np

MODEL_VERSION = "adapt-v2"


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

    def get_state(self):
        return None

    def set_state(self, state):
        pass

    def persistent_parameters(self):
        return None


def _proj_matrix(rng, in_dim, out_dim):
    if out_dim is None or out_dim >= in_dim:
        return None
    return rng.normal(0, 1.0 / max(1, out_dim) ** 0.5, size=(out_dim, in_dim))


def _reconstruct(P, s):
    if P is None:
        return s
    return np.linalg.pinv(P) @ (P @ s)


def _mse_loss(family, pairs, predict_fn):
    import math
    if family in ("linear", "quadratic"):
        errs = [(predict_fn(x) - y) for x, y in pairs]
        return float(sum(e * e for e in errs) / max(1, len(errs)))
    tot = sum(len(y) for _, y in pairs)
    bad = sum(a != b for x, y in pairs for a, b in zip(predict_fn(x), y))
    return bad / max(1, tot)


class FrozenBaseline(AdaptationStrategy):
    name = "frozen"

    def reset(self):
        pass

    def adapt(self, demonstrations):
        pass

    def predict(self, query):
        if isinstance(query, (int, float)):
            return 0.0
        if isinstance(query, list) and query and isinstance(query[0], list):
            return [row[:] for row in query]
        return [0] * len(query)

    def telemetry(self):
        return {"persistent_delta": 0.0, "state_delta": 0.0, "steps": 0,
                "t_adapt_ms": 0.0, "t_predict_ms": 0.0, "latency_ms": 0.0,
                "param_count": 0, "state_dim": 0, "state_bytes": 0,
                "loss_before": None, "loss_after": None, "grad_norm": 0.0}


class AnalyticalContext(AdaptationStrategy):
    """Analytical conditioning baseline (NOT learned ICL)."""
    name = "context"

    def __init__(self):
        self._demos = []

    def reset(self):
        self._demos = []

    def adapt(self, demonstrations):
        self._demos = list(demonstrations)

    def _fit_poly(self, degree):
        xs = np.array([x for x, _ in self._demos], dtype=float)
        ys = np.array([y for _, y in self._demos], dtype=float)
        if len(xs) == 0:
            return np.zeros(degree + 1)
        X = np.vander(xs, degree + 1, increasing=True)
        coef, _, _, _ = np.linalg.lstsq(X, ys, rcond=None)
        return coef

    def _best_affine(self):
        from .tasks import VOCAB, MULTS
        best, best_s = (1, 0), -1
        for a in MULTS:
            for o in range(VOCAB):
                s = sum(1 for x, y in self._demos
                        if [(a * v + o) % VOCAB for v in x] == y)
                if s > best_s:
                    best, best_s = (a, o), s
        return best

    def predict(self, query, family="linear"):
        if family == "linear":
            c = self._fit_poly(1)
            return float(c[0] + c[1] * query)
        if family == "quadratic":
            c = self._fit_poly(2)
            return float(c[0] + c[1] * query + c[2] * query * query)
        if family == "symbolic":
            from .tasks import VOCAB
            a, o = self._best_affine()
            return [(a * v + o) % VOCAB for v in query]
        if family == "compositional":
            # hypothesis vote over single ops only (honest limit: deeper
            # chains are NOT solvable by this baseline — ladder effect)
            from .tasks import VOCAB, _apply_chain
            cands = [{"op": "reverse"}] + [
                {"op": "shift", "offset": o} for o in range(VOCAB)]
            best, best_s = cands[0], -1
            for hyp in cands:
                s = sum(1 for x, y in self._demos if _apply_chain(x, [hyp]) == y)
                if s > best_s:
                    best, best_s = hyp, s
            return _apply_chain(query, [best])
        if family == "grid_toy":
            from .tasks import GRID_FNS
            best, best_s = "rot90", -1
            for name, fn in GRID_FNS.items():
                s = sum(1 for x, y in self._demos if fn(x) == y)
                if s > best_s:
                    best, best_s = name, s
            return GRID_FNS[best](query)
        raise ValueError(family)

    def telemetry(self):
        return {"persistent_delta": 0.0, "state_delta": 0.0, "steps": 0,
                "t_adapt_ms": 0.0, "t_predict_ms": 0.0, "latency_ms": 0.0,
                "param_count": 0, "state_dim": 0, "state_bytes": 0,
                "loss_before": None, "loss_after": None, "grad_norm": 0.0}


# back-compat alias (Phase 2A names)
ContextICL = AnalyticalContext


class GradientTaskLearner(AdaptationStrategy):
    """Minimal parameterized task learner, inference-time GD (NOT LLM TTT)."""
    name = "param_tta"

    def __init__(self, family="linear", steps=8, lr=0.05):
        self.family = family
        self.steps = steps
        self.lr = lr
        self._theta0 = None
        self.theta = None
        self._gnorm = 0.0

    def _init(self):
        if self.family == "linear":
            return np.zeros(2)
        if self.family == "quadratic":
            return np.zeros(3)
        if self.family == "symbolic":
            from .tasks import MULTS, VOCAB
            return np.zeros(len(MULTS) * VOCAB)
        if self.family == "grid_toy":
            from .tasks import GRID_FNS
            return np.zeros(len(GRID_FNS))
        return np.zeros(8)

    def _hyps(self):
        if self.family == "symbolic":
            from .tasks import MULTS, VOCAB
            return [(a, o) for a in MULTS for o in range(VOCAB)]
        if self.family == "grid_toy":
            from .tasks import GRID_FNS
            return list(GRID_FNS.keys())
        return None

    def reset(self):
        self._theta0 = self._init()
        self.theta = self._theta0.copy()

    def _obs(self, demonstrations):
        import numpy as np
        hyps = self._hyps()
        obs = np.zeros(len(hyps))
        if self.family == "symbolic":
            from .tasks import VOCAB
            for x, y in demonstrations:
                for i, (a, o) in enumerate(hyps):
                    if [(a * v + o) % VOCAB for v in x] == y:
                        obs[i] += 1
        elif self.family == "grid_toy":
            from .tasks import GRID_FNS
            for x, y in demonstrations:
                for i, name in enumerate(hyps):
                    if GRID_FNS[name](x) == y:
                        obs[i] += 1
        return obs

    def adapt(self, demonstrations):
        if self.theta is None:
            self.reset()
        if self.family == "compositional":
            return  # honest limit: no parametric chain learner; predict=identity-ish
        if self.family == "linear":
            xs = np.array([x for x, _ in demonstrations])
            ys = np.array([y for _, y in demonstrations])
            th = self.theta
            for _ in range(self.steps):
                err = (th[0] + th[1] * xs) - ys
                n = max(1, len(xs))
                g = np.array([2 * err.mean(), 2 * (err * xs).mean()])
                self._gnorm = float(np.linalg.norm(g))
                th = th - self.lr * g
            self.theta = th
        elif self.family == "quadratic":
            # lr documented here AND in config; tuned on val split only
            # (0.1 inner damping compensates x^4-scale gradients)
            xs = np.array([x for x, _ in demonstrations])
            ys = np.array([y for _, y in demonstrations])
            th = self.theta
            for _ in range(self.steps):
                err = (th[0] + th[1] * xs + th[2] * xs * xs) - ys
                g = np.array([2 * err.mean(), 2 * (err * xs).mean(),
                              2 * (err * xs * xs).mean()])
                self._gnorm = float(np.linalg.norm(g))
                th = th - (self.lr * 0.1) * g
            self.theta = th
        else:
            obs = self._obs(demonstrations)
            th = self.theta
            for _ in range(self.steps):
                p = np.exp(th - th.max())
                p = p / p.sum()
                tot = obs.sum()
                g = p - (obs / tot if tot > 0 else p * 0)
                self._gnorm = float(np.linalg.norm(g))
                th = th - self.lr * g
            self.theta = th

    def predict(self, query):
        if self.family == "linear":
            return float(self.theta[0] + self.theta[1] * query)
        if self.family == "quadratic":
            return float(self.theta[0] + self.theta[1] * query
                         + self.theta[2] * query * query)
        if self.family == "symbolic":
            from .tasks import VOCAB
            a, o = self._hyps()[int(np.argmax(self.theta))]
            return [(a * v + o) % VOCAB for v in query]
        if self.family == "compositional":
            return list(query)  # honest limit: no parametric chain learner here
        if self.family == "grid_toy":
            from .tasks import GRID_FNS
            return GRID_FNS[self._hyps()[int(np.argmax(self.theta))]](query)
        raise ValueError(self.family)

    def persistent_parameters(self):
        return None if self.theta is None else self.theta.copy()

    def telemetry(self):
        d = float(np.linalg.norm(self.theta - self._theta0)) if self.theta is not None else 0.0
        return {"persistent_delta": d, "state_delta": 0.0, "steps": self.steps,
                "t_adapt_ms": 0.0, "t_predict_ms": 0.0, "latency_ms": 0.0,
                "param_count": int(self.theta.size) if self.theta is not None else 0,
                "state_dim": 0, "state_bytes": 0,
                "loss_before": None, "loss_after": None, "grad_norm": self._gnorm}


ParamTTA = GradientTaskLearner


class SufficientStatState(AdaptationStrategy):
    """Hand-designed sufficient-statistics memory (NOT a learned RNN)."""
    name = "state"

    def __init__(self, family="linear", state_dim=None, seed=0):
        self.family = family
        self.state_dim = state_dim
        self.seed = seed
        self._s0 = None
        self.s = None
        self._proj = None

    def _stat_dim(self):
        return {"linear": 5, "quadratic": 8, "symbolic": 24,
                "compositional": 8, "grid_toy": 6}[self.family]

    def _phi(self, x, y):
        if self.family == "linear":
            return np.array([1.0, x, y, x * x, x * y], dtype=float)
        if self.family == "quadratic":
            # full 2nd-order sufficient stats: n,sx,sx2,sx3,sx4,sy,sxy,sx2y
            return np.array([1.0, x, x * x, x ** 3, x ** 4, y, x * y,
                             x * x * y], dtype=float)
        if self.family == "symbolic":
            from .tasks import VOCAB, MULTS
            v = np.zeros(len(MULTS) * VOCAB)
            for ia, a in enumerate(MULTS):
                for o in range(VOCAB):
                    if [(a * t + o) % VOCAB for t in x] == y:
                        v[ia * VOCAB + o] += 1
            return v
        if self.family == "compositional":
            v = np.zeros(8)
            for a, b in zip(x, y):
                v[(b - a) % 8] += 1
            return v
        from .tasks import GRID_FNS
        names = list(GRID_FNS.keys())
        v = np.zeros(len(names))
        for i, name in enumerate(names):
            if GRID_FNS[name](x) == y:
                v[i] += 1
        return v

    def reset(self):
        d = self._stat_dim()
        self._s0 = np.zeros(d)
        self.s = np.zeros(d)
        self._proj = _proj_matrix(np.random.RandomState(self.seed), d, self.state_dim)

    def _use(self):
        return _reconstruct(self._proj, self.s)

    def adapt(self, demonstrations):
        if self.s is None:
            self.reset()
        for x, y in demonstrations:
            self.s = self.s + self._phi(x, y)

    def _fit_quad(self, s):
        # solve 3x3 normal equations from sufficient stats (TRUE quadratic fit)
        n, sx, sx2, sx3, sx4, sy, sxy, sx2y = s
        M = np.array([[n, sx, sx2], [sx, sx2, sx3], [sx2, sx3, sx4]])
        v = np.array([sy, sxy, sx2y])
        try:
            c0, c1, c2 = np.linalg.solve(M, v)
        except np.linalg.LinAlgError:
            return 0.0, 0.0, 0.0
        return float(c0), float(c1), float(c2)

    def predict(self, query):
        if self.family == "linear":
            s = self._use()
            n, sx, sy, sxx, sxy = s
            if n < 2:
                return 0.0
            den = n * sxx - sx * sx
            if abs(den) < 1e-9:
                return 0.0
            w = (n * sxy - sx * sy) / den
            return float((sy - w * sx) / n + w * query)
        if self.family == "quadratic":
            c0, c1, c2 = self._fit_quad(self._use())
            return float(c0 + c1 * query + c2 * query * query)
        if self.family == "symbolic":
            from .tasks import VOCAB, MULTS
            s = self._use()
            if s.sum() <= 0:
                return list(query)
            i = int(np.argmax(s))
            a, o = MULTS[i // VOCAB], i % VOCAB
            return [(a * v + o) % VOCAB for v in query]
        if self.family == "compositional":
            s = self._use()
            o = int(np.argmax(s)) if s.sum() > 0 else 0
            return [(v + o) % 8 for v in query]  # honest limit: shift-only read
        if self.family == "grid_toy":
            from .tasks import GRID_FNS
            names = list(GRID_FNS.keys())
            s = self._use()
            return GRID_FNS[names[int(np.argmax(s))] if s.sum() > 0 else 0](query)
        raise ValueError(self.family)

    def persistent_parameters(self):
        return np.zeros(0)

    def telemetry(self):
        ds = float(np.linalg.norm(self._use() - _reconstruct(self._proj, self._s0)))
        return {"persistent_delta": 0.0, "state_delta": ds, "steps": 0,
                "t_adapt_ms": 0.0, "t_predict_ms": 0.0, "latency_ms": 0.0,
                "param_count": 0, "state_dim": int(self.s.size),
                "state_bytes": int(self.s.nbytes),
                "loss_before": None, "loss_after": None, "grad_norm": 0.0}

    def get_state(self):
        return None if self.s is None else self.s.copy()

    def set_state(self, state):
        self.s = np.array(state, dtype=float).copy()


RecurrentState = SufficientStatState


class TTTState(AdaptationStrategy):
    """Analytical TTT-state: state parameterizes predictor, GD on state."""
    name = "ttt_state"

    def __init__(self, family="linear", steps=8, lr=0.05):
        assert family in ("linear", "quadratic")
        self.family = family
        self.steps = steps
        self.lr = lr
        self._init = None
        self.S = None

    def reset(self):
        self._init = np.zeros(2 if self.family == "linear" else 3)
        self.S = np.zeros_like(self._init)

    def adapt(self, demonstrations):
        if self.S is None:
            self.reset()
        xs = np.array([x for x, _ in demonstrations])
        ys = np.array([y for _, y in demonstrations])
        S = self.S
        for _ in range(self.steps):
            if self.family == "linear":
                err = (S[0] + S[1] * xs) - ys
                S = S - self.lr * np.array([2 * err.mean(), 2 * (err * xs).mean()])
            else:
                err = (S[0] + S[1] * xs + S[2] * xs * xs) - ys
                S = S - self.lr * 0.1 * np.array(
                    [2 * err.mean(), 2 * (err * xs).mean(), 2 * (err * xs * xs).mean()])
        self.S = S

    def predict(self, query):
        if self.family == "linear":
            return float(self.S[0] + self.S[1] * query)
        return float(self.S[0] + self.S[1] * query + self.S[2] * query * query)

    def persistent_parameters(self):
        return None if self._init is None else self._init.copy()

    def telemetry(self):
        ds = float(np.linalg.norm(self.S - self._init)) if self.S is not None else 0.0
        return {"persistent_delta": 0.0, "state_delta": ds, "steps": self.steps,
                "t_adapt_ms": 0.0, "t_predict_ms": 0.0, "latency_ms": 0.0,
                "param_count": 0, "state_dim": int(self.S.size),
                "state_bytes": int(self.S.nbytes),
                "loss_before": None, "loss_after": None, "grad_norm": 0.0}

    def get_state(self):
        return None if self.S is None else self.S.copy()

    def set_state(self, state):
        self.S = np.array(state, dtype=float).copy()


def make_strategy(name, family="linear", **kw):
    table = {"frozen": FrozenBaseline, "context": AnalyticalContext,
             "param_tta": GradientTaskLearner, "state": SufficientStatState,
             "ttt_state": TTTState,
             # Phase 2B learned (lazy import to avoid cycles)
             "learned_state": None, "learned_tta": None, "learned_ttt": None}
    if name in ("learned_state", "learned_tta", "learned_ttt"):
        from .learned import LearnedRecurrentState, LearnedParamTTA, LearnedTTTState
        ltab = {"learned_state": LearnedRecurrentState,
                "learned_tta": LearnedParamTTA, "learned_ttt": LearnedTTTState}
        cls = ltab[name]
        return cls(family=family, **kw)
    cls = table[name]
    if name in ("frozen", "context"):
        return cls()
    return cls(family=family, **kw)
