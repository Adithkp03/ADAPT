"""Phase 2B learned neural substrate (numpy, CPU).

Shared MLP backbone, meta-learned with antithetic Evolution Strategies
(Salimans et al. 2017) on the TRAIN split, selected on VAL, evaluated
on TEST. Inner-loop gradients are analytic (single-layer backprop or
linear-in-state); outer loop is gradient-free ES — simple and exact,
no autograd machinery to mistrust.

Scope: linear family only (declared; symbolic/grid learned is future).
- LearnedRecurrentState: s_t = tanh(W_s s + W_e [phi(x); y] + b_s);
  params frozen after meta-train, only s evolves. dTheta == 0.
- LearnedParamTTA: y_hat = w.phi(x)+b0; K GD steps on ALL params at
  test time (same backbone as recurrent head). dTheta > 0.
- LearnedTTTState: y_hat = S.phi(x); S updated by GD on demos from
  learned S0 with learned lr; phi fixed after meta-train.
  Persistent (phi,S0,lr) delta == 0; adapted-state delta > 0.
"""
import time
import numpy as np

H = 8
MODEL_VERSION = "learned-v1"


# ---------- param packing ----------
def pack_rec(params):
    Wf, bf, Ws, We, bs, wp, bp = (params["Wf"], params["bf"], params["Ws"],
                                  params["We"], params["bs"], params["wp"],
                                  params["bp"])
    return np.concatenate([Wf.ravel(), bf, Ws.ravel(), We.ravel(), bs,
                           wp, np.atleast_1d(bp)])


def unpack_rec(vec):
    v = np.asarray(vec, float)
    i = 0
    Wf = v[i:i + H * 1].reshape(H, 1); i += H
    bf = v[i:i + H]; i += H
    Ws = v[i:i + H * H].reshape(H, H); i += H * H
    We = v[i:i + H * (H + 1)].reshape(H, H + 1); i += H * (H + 1)
    bs = v[i:i + H]; i += H
    wp = v[i:i + 2 * H]; i += 2 * H
    bp = float(v[i])
    return {"Wf": Wf, "bf": bf, "Ws": Ws, "We": We, "bs": bs,
            "wp": wp, "bp": bp}


def pack_ptt(params):
    return np.concatenate([params["Wf"].ravel(), params["bf"],
                           params["w"], np.atleast_1d(params["b0"])])


def unpack_ptt(vec):
    v = np.asarray(vec, float)
    Wf = v[:H].reshape(H, 1)
    bf = v[H:2 * H]
    w = v[2 * H:3 * H]
    b0 = float(v[3 * H])
    return {"Wf": Wf, "bf": bf, "w": w, "b0": b0}


def pack_ttt(params):
    return np.concatenate([params["Wf"].ravel(), params["bf"],
                           params["S0"], np.atleast_1d(params["log_lr"])])


def unpack_ttt(vec):
    v = np.asarray(vec, float)
    Wf = v[:H].reshape(H, 1)
    bf = v[H:2 * H]
    S0 = v[2 * H:3 * H]
    log_lr = float(v[3 * H])
    return {"Wf": Wf, "bf": bf, "S0": S0, "log_lr": log_lr}


def init_vec(kind, rng, scale=None):
    size = {"rec": H + H + H * H + H * (H + 1) + H + 2 * H + 1,
            "ptt": 3 * H + 1, "ttt": 3 * H + 1}[kind]
    scale = {"rec": 0.15, "ptt": 0.3, "ttt": 0.3}.get(kind, 0.3) if scale is None else scale
    v = rng.normal(0, scale, size=size)
    if kind == "ttt":
        v[3 * H] = np.log(0.05)
    return v


# ---------- forward / inner loops (linear family) ----------
def phi_of(x, Wf, bf):
    return np.tanh(Wf[:, 0] * float(x) + bf)


def episode_loss_rec(vec, demos, queries):
    """queries: [(x, y)]. Returns mean MSE."""
    p = unpack_rec(vec)
    s = np.zeros(H)
    for x, y in demos:
        e = np.concatenate([phi_of(x, p["Wf"], p["bf"]), [float(y)]])
        s = np.tanh(p["Ws"] @ s + p["We"] @ e + p["bs"])
    errs = []
    for x, y in queries:
        pred = float(p["wp"] @ np.concatenate([s, phi_of(x, p["Wf"], p["bf"])]) + p["bp"])
        errs.append((pred - float(y)) ** 2)
    return float(sum(errs) / max(1, len(errs))), s


def _ptt_predict(th, x):
    return float(th["w"] @ phi_of(x, th["Wf"], th["bf"]) + th["b0"])


def _ptt_grads(th, demos):
    gw = np.zeros(H); gb0 = 0.0; gWf = np.zeros((H, 1)); gbf = np.zeros(H)
    n = max(1, len(demos))
    for x, y in demos:
        z = th["Wf"][:, 0] * float(x) + th["bf"]
        h = np.tanh(z)
        err = float(th["w"] @ h + th["b0"] - float(y))
        d = 2 * err / n
        gw += d * h
        gb0 += d
        dh = d * th["w"] * (1 - h ** 2)
        gWf[:, 0] += dh * float(x)
        gbf += dh
    return {"Wf": gWf, "bf": gbf, "w": gw, "b0": gb0}


def episode_loss_ptt(vec, demos, queries, steps=5, lr=0.05):
    th = unpack_ptt(vec.copy())
    for _ in range(steps):
        g = _ptt_grads(th, demos)
        th = {k: th[k] - lr * g[k] for k in th}
    errs = [(_ptt_predict(th, x) - float(y)) ** 2 for x, y in queries]
    d = float(np.linalg.norm(pack_ptt(th) - vec))
    return float(sum(errs) / max(1, len(errs))), th, d


def episode_loss_ttt(vec, demos, queries, steps=5):
    p = unpack_ttt(vec)
    lr = float(np.exp(p["log_lr"]))
    S = p["S0"].copy()
    Phi = np.array([phi_of(x, p["Wf"], p["bf"]) for x, _ in demos])
    yv = np.array([float(y) for _, y in demos])
    for _ in range(steps):
        if len(demos):
            err = Phi @ S - yv
            S = S - lr * (2 * Phi.T @ err / len(demos))
    errs = [(float(S @ phi_of(x, p["Wf"], p["bf"])) - float(y)) ** 2 for x, y in queries]
    return float(sum(errs) / max(1, len(errs))), S


# ---------- ES meta-training ----------
def _adam_init(n):
    return {"m": np.zeros(n), "v": np.zeros(n), "t": 0}


def _adam_step(state, g, lr=0.05, b1=0.9, b2=0.999, eps=1e-8):
    state["t"] += 1
    state["m"] = b1 * state["m"] + (1 - b1) * g
    state["v"] = b2 * state["v"] + (1 - b2) * (g * g)
    mh = state["m"] / (1 - b1 ** state["t"])
    vh = state["v"] / (1 - b2 ** state["t"])
    return state, lr * mh / (np.sqrt(vh) + eps)


def es_train(kind, make_episodes, val_episodes, model_seed=0, steps=200,
             pop=64, sigma=0.02, meta_lr=0.02, log_every=50):
    """make_episodes(rng, n) -> list of (demos, queries). Returns best vec by val.

    Rank (fitness) shaping: candidate returns are replaced by centered
    ranks, which stabilizes ES scale across training.
    """
    rng = np.random.RandomState(model_seed)
    vec = init_vec(kind, rng)
    adam = _adam_init(vec.size)
    fn = {"rec": episode_loss_rec, "ptt": episode_loss_ptt, "ttt": episode_loss_ttt}[kind]
    best, best_val = vec.copy(), float("inf")
    n_half = pop // 2
    for it in range(steps):
        eps = [rng.normal(0, 1, size=vec.size) for _ in range(n_half)]
        cands, rets = [], []
        for e in eps:
            for sgn in (1, -1):
                cand = vec + sgn * sigma * e
                eps_tasks = make_episodes(rng, 8)
                r = sum(fn(cand, d, q)[0] for d, q in eps_tasks) / 8
                cands.append((e, sgn))
                rets.append(r)
        order = np.argsort(np.argsort(rets)).astype(float)  # 0=best
        shaped = (order / (len(rets) - 1)) - 0.5  # centered ranks, low loss = negative
        grad = np.zeros_like(vec)
        for (e, sgn), sh in zip(cands, shaped):
            grad += (sh * sgn * e) / (sigma * n_half)
        adam, upd = _adam_step(adam, grad, meta_lr)
        vec = vec - upd
        if (it + 1) % log_every == 0 or it == 0:
            v = sum(fn(vec, d, q)[0] for d, q in val_episodes) / len(val_episodes)
            if v < best_val:
                best_val, best = v, vec.copy()
            print(f"[es/{kind}] it={it + 1} val_mse={v:.4f} best={best_val:.4f}", flush=True)
    return best


# ---------- strategy wrappers (common interface) ----------
class _LearnedBase:
    family = "linear"

    def __init__(self, checkpoint=None, steps=5, lr=0.05, family="linear", **kw):
        assert family == "linear", "learned trio scope: linear only"
        self.steps = steps
        self.lr = lr
        self.vec = None
        if checkpoint:
            self.load(checkpoint)

    def load(self, path):
        z = np.load(path, allow_pickle=True)
        self.vec = z["vec"]

    def persistent_parameters(self):
        return None if self.vec is None else self.vec.copy()


class LearnedRecurrentState(_LearnedBase):
    name = "learned_state"

    def reset(self):
        self._s = np.zeros(H)
        self._p = unpack_rec(self.vec)

    def adapt(self, demonstrations):
        t0 = __import__("time").perf_counter()
        p = self._p
        s = np.zeros(H)
        for x, y in demonstrations:
            e = np.concatenate([phi_of(x, p["Wf"], p["bf"]), [float(y)]])
            s = np.tanh(p["Ws"] @ s + p["We"] @ e + p["bs"])
        self._s = s
        self._s0 = np.zeros(H)
        self._ta = (__import__("time").perf_counter() - t0) * 1000
        before = sum((float(p["wp"] @ np.concatenate([np.zeros(H), phi_of(x, p["Wf"], p["bf"])]) + p["bp"]) - float(y)) ** 2 for x, y in demonstrations)
        after = sum((self.predict(x) - float(y)) ** 2 for x, y in demonstrations)
        self._lb, self._la = before / max(1, len(demonstrations)), after / max(1, len(demonstrations))

    def predict(self, query):
        p = self._p
        return float(p["wp"] @ np.concatenate([self._s, phi_of(query, p["Wf"], p["bf"])]) + p["bp"])

    def telemetry(self):
        ds = float(np.linalg.norm(self._s - self._s0))
        return {"persistent_delta": 0.0, "state_delta": ds, "steps": 0,
                "t_adapt_ms": getattr(self, "_ta", 0.0), "t_predict_ms": 0.0,
                "latency_ms": getattr(self, "_ta", 0.0),
                "param_count": int(self.vec.size), "state_dim": H,
                "state_bytes": int(self._s.nbytes),
                "loss_before": getattr(self, "_lb", None),
                "loss_after": getattr(self, "_la", None), "grad_norm": 0.0}

    def get_state(self):
        return self._s.copy()

    def set_state(self, state):
        self._s = np.array(state, float).copy()


class LearnedParamTTA(_LearnedBase):
    name = "learned_tta"

    def reset(self):
        self._th0 = unpack_ptt(self.vec.copy())
        self._th = unpack_ptt(self.vec.copy())

    def adapt(self, demonstrations):
        import time
        t0 = time.perf_counter()
        lb = sum((_ptt_predict(self._th, x) - float(y)) ** 2 for x, y in demonstrations) / max(1, len(demonstrations))
        th = self._th
        for _ in range(self.steps):
            g = _ptt_grads(th, demonstrations)
            self._gn = float(np.linalg.norm(np.concatenate([g["Wf"].ravel(), g["bf"], g["w"], [g["b0"]]])))
            th = {k: th[k] - self.lr * g[k] for k in th}
        self._th = th
        la = sum((_ptt_predict(self._th, x) - float(y)) ** 2 for x, y in demonstrations) / max(1, len(demonstrations))
        self._ta = (time.perf_counter() - t0) * 1000
        self._lb, self._la = lb, la

    def predict(self, query):
        return _ptt_predict(self._th, query)

    def persistent_parameters(self):
        return None if self.vec is None else pack_ptt(self._th)

    def telemetry(self):
        d = float(np.linalg.norm(pack_ptt(self._th) - self.vec))
        return {"persistent_delta": d, "state_delta": 0.0, "steps": self.steps,
                "t_adapt_ms": getattr(self, "_ta", 0.0), "t_predict_ms": 0.0,
                "latency_ms": getattr(self, "_ta", 0.0),
                "param_count": int(self.vec.size), "state_dim": 0, "state_bytes": 0,
                "loss_before": getattr(self, "_lb", None),
                "loss_after": getattr(self, "_la", None),
                "grad_norm": getattr(self, "_gn", 0.0)}


class LearnedTTTState(_LearnedBase):
    name = "learned_ttt"

    def reset(self):
        p = unpack_ttt(self.vec)
        self._p = p
        self._S0 = p["S0"].copy()
        self._S = p["S0"].copy()

    def adapt(self, demonstrations):
        import time
        t0 = time.perf_counter()
        p = self._p
        lr = float(np.exp(p["log_lr"]))
        Phi = np.array([phi_of(x, p["Wf"], p["bf"]) for x, _ in demonstrations])
        yv = np.array([float(y) for _, y in demonstrations])
        lb = (float(np.mean((Phi @ self._S - yv) ** 2)) if len(demonstrations) else 0.0)
        S = self._S
        for _ in range(self.steps):
            if len(demonstrations):
                S = S - lr * (2 * Phi.T @ (Phi @ S - yv) / len(demonstrations))
        self._S = S
        la = (float(np.mean((Phi @ self._S - yv) ** 2)) if len(demonstrations) else 0.0)
        self._ta = (time.perf_counter() - t0) * 1000
        self._lb, self._la = lb, la

    def predict(self, query):
        return float(self._S @ phi_of(query, self._p["Wf"], self._p["bf"]))

    def telemetry(self):
        ds = float(np.linalg.norm(self._S - self._S0))
        return {"persistent_delta": 0.0, "state_delta": ds, "steps": self.steps,
                "t_adapt_ms": getattr(self, "_ta", 0.0), "t_predict_ms": 0.0,
                "latency_ms": getattr(self, "_ta", 0.0),
                "param_count": int(self.vec.size), "state_dim": H,
                "state_bytes": int(self._S.nbytes),
                "loss_before": getattr(self, "_lb", None),
                "loss_after": getattr(self, "_la", None), "grad_norm": 0.0}

    def get_state(self):
        return self._S.copy()

    def set_state(self, state):
        self._S = np.array(state, float).copy()
