# D5.14 — Defense: Equations

The three equations a defender must be able to write and interpret live.

## 1. Adaptive state update (controlled model)

Demonstrations update an internal register, parameters stay fixed:

```
s ← s + φ(x, y)          per demonstration
y_hat = readout(s, x_q)  query prediction
θ'  = θ                  (Δθ = 0, Δs > 0)
```

`φ` accumulates the sufficient statistics the linear/symbolic readers
need (sum of x, sum of y, sum of x·y — least-squares sufficient stats).
Source: `src/adapt/strategies.py`; validated in E1
(`001_task_acquisition_linear`, state 1.00 with Δθ = 0).

## 2. Learned recurrent state (learned model)

```
s_t = tanh(W_s · s + W_e · [φ(x); y] + b_s)
y_hat = readout(s_t, x_q)
```

Persistent weights (W_s, W_e, b_s) meta-learned once (E9), frozen at
inference. Source: `src/adapt/learned.py` (`learned-v1`).

## 3. BDH / BDH-CQ published forms (as cited, NOT ours)

BDH synaptic-state update (published form; our educational
simplification):

```
σ ← σ + η·X·Yᵀ           (Hebbian write into working-memory synapse)
```

BDH-CQ: demonstrations write recurrent memory; query solved by
iterative latent computation. Full derivation and the round-numbering
(4l–4l+3) block structure: `research/bdh/equations.md` (labels which
lines are paper-verbatim vs "simplified educational form").

## TTA (gradient) alternate for contrast

```
θ ← θ − η·∇L(θ; D)        (persistent parameters change, Δθ > 0)
```

## Live parameter questions a judge may ask

- **Double n_demos?** Linear: 1→ insufficient (one point can't fix two
  params — theory predicts ~0.08–0.15); ≥2 → saturates at 1.00
  (`002_demo_scaling_linear`). Symbolic: even 1 demo identifies the
  offset → 1.00.
- **Halve state_dim?** The lossy project-and-reconstruct bottleneck
  destroys the sufficient statistics → cliff down to ≤0.10 acc at
  d_s ≤ 4  (`004_state_capacity_linear`, fig4).
- **Why interference?** State accumulates stats for line B on top of
  line A; readout fits a mix → retention drop (linear 0.09; symbolic
  0.45 because votes preserve partial counts). More in
  `005_interference_*`.
- **Why isn't BDH a Mamba-style SSM?** BDH's working memory is a
  *synaptic* matrix σ updated Hebbianly inside a scale-free network of
  local interactions — not a linear-time-invariant recurrence
  (dossier `bdh_technical_dossier.md`; the distinction is spelled out).
- **Did your model update weights?** Check the WHAT CHANGED box: for the
  state strategy Δθ = 0.0, Δs ≠ 0 in every payload (`telemetry.js`).
- **Is this graph live?** Badges: LIVE + SYNTHETIC = computed per
  request; PRECOMPUTED = vetted research run re-stamped; PUBLISHED =
  cited paper number; ILLUSTRATIVE = educational rendering.