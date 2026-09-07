# D5.12 — Model Disclosure

## What models are in the artifact

### 1. Controlled adaptation strategies (`src/adapt/strategies.py`)

Hand-specified dynamical systems. No training (Δθ = 0 by construction),
fully inspectable. `MODEL_VERSION = adapt-v2`.

- `frozen` — no adaptation.
- `context` — demonstrations passed with the query (ICL analogue).
- `param_tta` — a small toy parameterized model adapted by gradient
  steps at test time (Δθ > 0).
- `state` — controlled adaptive register: `s ← s + φ(x, y)` per
  demonstration; readout solves the query (Δθ = 0, Δs > 0).
- `ttt_state` — learned state parameterization on the same register.

### 2. Learned trio (Research Lab; `src/adapt/learned.py`)

Meta-trained by us (Phase 2B E9 protocol) on the synthetic linear
distribution, frozen at inference.

- `learned_state` (recurrent state model), `learned_tta` (parameter
  backbone), `learned_ttt` (TTT backbone).
- Checkpoints `checkpoints/learned_*_s{0,1}.npz` — frozen; hashes in
  `results/final_manifest.csv`; re-validation per E9 protocol required
  before any replacement (`docs/architecture_freeze.md`).
- The recurrent variant's honest negative (did not acquire the linear
  rule under budget) is documented, not hidden
  (`research/experiments/phase2_validation_report.md`,
  `009_learned_linear_s0/results.json`).

### 3. Frontier references — cited, NOT shipped

- **BDH** (Kosowski et al. 2025): weights belong to their authors /
  the official `pathwaycom/bdh` repo; we reference and probe at pinned
  commit `2b0d7a4` (`research/bdh/reproductions/R1_results.md`).
- **BDH-CQ** (Engdahl et al. 2026): weights at the official
  `pathwaycom/bdh-cq` repo; pinned `c246f89`
  (`R2_results.md`). Their 150M config / 29.5% result is PUBLISHED,
  scope-guarded, and **not reproduced by us**.

No BDH / BDH-CQ weights are redistributed in this repository.

## How state changes are verified

Every live payload's telemetry reports `persistent_delta` and
`state_delta`. Learnability of the state strategy requires Δθ = 0 and
Δs > 0; the server reports exactly these values and the UI shows them
(`server.py::_episode_payload`). Causal necessity of the adapted state
is checked by the E8/E9 perturb/restore protocol
(`research/experiments/008_intervention_linear/results.json`,
fig6). See `provenance/models.csv`.