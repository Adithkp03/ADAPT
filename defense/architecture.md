# D5.14 — Defense: Architecture (mental model every defender must hold)

> The one thing this artifact teaches: **"Inference-time adaptation can
> succeed without persistent parameter changes, storing the new rule in
> evolving state — but that state's capacity and dynamics limit
> retention."** (CANDIDATE HYPOTHESIS, toy scope.)

## The full pipeline, top to bottom

```text
user → task → demonstrations → adaptation → state/parameter change → query
      → prediction → ground truth → metrics
```

## The adaptation branch

```text
                    ┌── state        (controlled register; Δθ = 0, Δs > 0)
adaptation ─────────┼── parameters   (param_tta / TTA; Δθ > 0)
                    └── context      (no update; examples passed with query)
```

## Frontier connection

```text
state adaptation
      ↓
BDH — synaptic working memory in σ, Hebbian update (published σ ← σ + ηXYᵀ)
BDH-CQ — demonstrations update recurrent memory; query by iterative latent computation
```

## Why this design (the "why" for every major component)

- **Why this task generator?** Exact hidden rules R give controlled
  ground truth T=(R,D,Q,Y) — every claim is checkable.
- **Why these models?** Hand-specified + meta-trained toy substrates are
  transparent: we can trace the rule to a specific state register.
- **Why compare context vs state vs parameters?** They place the task
  information in *different computational substrates* — the whole
  research question.
- **Why synthetic tasks?** Causal control: seed-disjoint splits, exact
  truth, reproducible draws.
- **Why grid_toy and not ARC?** A small synthetic proxy for abstract
  transformations, always labelled PROXY — never ARC-AGI.
- **Why BDH?** A frontier architecture whose *evolving memory is
  explicitly state-like* (synaptic state σ, Hebbian write).
- **Why BDH-CQ?** Its inference-time recurrent memory + latent reasoning
  is directly the question our state mechanism isolates.

## "Show me the code" path (UI → API → model → result)

```text
State visualization  →  server.py::/api/episode  →  src/adapt/runner.run_episode
                     →  src/adapt/strategies   (state: s ← s + φ(x,y))
                     →  src/adapt/telemetry     (persistent_delta, state_delta)
                     →  results/experiments/*/results.json
```

Full trace: `tests/test_server.py`, `tests/test_strategies.py`.

## Frozen surface (D5.1)

API paths + shapes locked (`result_schema_version = 1`); provenance
envelope on every payload; evidence badges locked; checkpoints and
figures hash-pinned (`results/final_manifest.csv`).