# D3.3 — State Visualization (honest rendering of adaptive state)

**Scope:** how `web/` shows "what changed inside the model" (phase3 §9, §48).
Applies to the Adaptive State strategy and the BDH bridge panel.

## 1. What the engine actually reports

Per episode (`src/adapt/runner.py` + `telemetry.py`), the server exposes:

- `persistent_delta` — norm of change to persistent parameters θ (0.0 for
  state/context strategies by construction).
- `state_delta` — norm of change to the disposable adaptive state s
  (`‖s_after − s_before‖`).
- `steps`, `t_adapt_ms`, `t_predict_ms`, `latency_ms`, `param_count`,
  `state_dim`, `state_bytes`, `loss_before/after`, `grad_norm`.

The flagship WHAT CHANGED box renders exactly two of these:
`Δθ = persistent_delta`, `Δs = state_delta`. Nothing else is claimed.

## 2. Allowed visual encodings

1. **Scalar deltas** — `Δθ = 0.0000` / `Δs = 4.81` as text in the `.delta`
   box. This is the primary encoding; it is a measured statistic.
2. **Paired deltas** — the compare table's Δθ/Δs columns across the three
   substrates on the identical task (paired, same seed/demos).
3. **Perturb/restore booleans** — the E8 table (base / perturbed / restored
   ✓/✗ per perturbation). Causal weight rests on `swap` (matched
   counterfactual) and `nullmean` (on-manifold null); the UI prints the
   server's caution note verbatim: shuffle-failure alone is not claimed as
   information removal.
4. **Bottleneck cliff** — accuracy vs `d_s` sweep points with Wilson 95% CI
   whiskers plus the adjacent data table. Labeled an *operational proxy*
   (project-and-reconstruct bottleneck), never "memory capacity itself".
5. **η demo (BDH panel)** — `‖Δσ‖ = η·‖x‖·‖y‖` with `‖x‖=‖y‖=1` demo vectors,
   computed locally from the slider. Labeled **educational implementation
   inspired by the published BDH formulation**, never official BDH output.

## 3. Forbidden encodings (§48 "Bad")

- Rendering state dimensions as named concepts ("rule memory", "object
  detector", "reasoning neuron") without probing evidence.
- Cosine-similarity or projection claims not computed by the engine.
- Trajectories/heatmaps of latent dimensions presented as semantics.
- Any graphic implying persistent weight change for the state strategy
  (Δθ is identically 0; the UI must show it, not hide it).

Where a projection could be misread, the adjacent copy must state:
"This visualization shows a measured state statistic; it is not a semantic
interpretation of individual latent dimensions."

## 4. Why this set is sufficient

The learning claim needs exactly one contrast — `Δθ = 0` beside `Δs ≠ 0`
(§14) — plus necessity (E8 restore ⇒ state carried the information) and
limits (capacity cliff, interference drop). Each is a number the engine
already emits; no invented interpretability is required to teach the
mechanism honestly.

## 5. Glossary — what each quantity means (and does not mean)

- **Δθ (persistent delta):** norm of change to persistent parameters θ
  across adaptation. For `state`/`context`/`learned_state` it is
  identically 0 by construction (nothing optimizes θ). NOT a measure of
  "how much was learned" — learning lives elsewhere here.
- **Δs (state delta):** `‖s_after − s_before‖`, norm of change to the
  disposable adaptive state. Nonzero means the demonstrations moved the
  transient memory. NOT a semantic code — its magnitude, not its
  direction, carries the lesson.
- **State norm / similarity:** only shown where computed (E8 swap uses a
  matched counterfactual state from another task; nullmean uses the
  8-task mean state as an on-manifold null). We do NOT display
  cosine-similarity dashboards or "Task A ↔ state = 0.82" style claims:
  uncomputed numbers are not shown.
- **Intervention result (base / perturbed / restored):** per-perturbation
  correctness booleans. `restored = True` means returning the exact
  adapted state recovers behavior (necessity check). `swap`-failure means
  another task's state does not solve this task (specificity);
  `nullmean`-failure means the average state does not solve it either.
  `shuffle`/`noise`/`zero` failures are degradation sanity checks only —
  never claimed as information removal.
- **Retention drop (A→B→A):** single-episode correctness difference, not a
  population statistic. The sweep/precomputed E5 gives the population
  view; the live episode gives the visceral one. Both are labeled.
