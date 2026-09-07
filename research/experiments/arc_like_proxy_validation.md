# D4.8 — ARC-Like / Novel-Task Validation (grid_toy synthetic proxy)

This document records how AdaptLab's ARC-*like* task family is kept
explicitly synthetic, why it is a *frontier-task-acquisition proxy* (not
an ARC-AGI benchmark reproduction), and the exact protocol+provenance of
the flagship E1 result. Validation date: 2026-09-07.

## 1. Naming hygiene — never "ARC"

The task family that was originally named `arc_like` is **renamed
`grid_toy`** in the engine (`src/adapt/tasks.py§165`: "grid toy (honest
rename of arc_like: 6-rule transformation toy, NOT ARC reasoning)").
Back-compat aliases (`arc_like`, `grid_transform`) exist only so Phase 2A
configs/results remain loadable; the aliased name never appears in the
public UI.

Public display names (`src/adapt/strategies.py`):
- `grid_toy` → `"Grid Transformation Lab"`; the string `"ARC"` is
  **forbidden** in the display name (enforced by
  `tests/test_freeze_gate.py::test_public_display_names`).
- The UI honesty banner (`web/index.html`) states the artifact is "not a
  frontier language model, **ARC-AGI**, or official BDH software."
- The only UI mention of "ARC-like" is the precomputed-selector label
  "E1 ARC-like grid acquisition (frontier mode)", which carries
  `PRECOMPUTED + SYNTHETIC` badges.

**ARC-AGI benchmark reproduction is explicitly disclaimed.** AdaptLab
does not run ARC-AGI-1; its `grid_toy` family is a 4×4 / 6-rule
transformation toy with values mod 4. Any `grid_toy` output is
`SYNTHETIC`, never presented as an ARC-AGI result.

## 2. Why grid_toy is a frontier-task-acquisition proxy (not a benchmark)

The *research pressure* that motivates public ARC-style generated-task
benchmarks (e.g. `arc-task-gen`) is: **can a system infer a genuinely
unseen transformation from a few demonstrations, without relying on
contamination/familiarity from a static public benchmark?** That is the
same core mechanism AdaptLab isolates (acquire the new rule at inference
time from demonstrations).

grid_toy is a **proxy** for that pressure because, like ARC, it presents
a small, discrete, spatial transformation given a few input→output grid
examples and asks for the unseen query's exact output — but it is
deliberately much smaller and more controlled than ARC:
- 4×4 grids, values mod 4, a 6-rule closed hypothesis space.
- Disjoint rule pools per split: train={rot90,flip_h,transpose},
  val={rot180,flip_v}, test={shift_color} — the held-out test rule is
  **never seen in train/val**, giving a clean find-the-unseen-rule setup.
- Deterministic given seed (`generate_task`), enabling exact
  reproduction.

**What it is NOT:** an ARC-AGI-1 reproduction, a measure of general
intelligence, or a claim that our 4×4 toy generalizes to ARC's grid
grammars. It is a signed, synthetic, controlled analogue that shares
ARC's *demonstration → hidden transformation → exact output* shape. That
is the frontier-task-acquisition proxy claim — no more. (See also
`research/claim/central_claim.md` and limitations doc item 1.)

## 3. E1 protocol and provenance (recorded)

**Result file:** `research/experiments/001_task_acquisition_arc/results.json`
(the directory keeps the legacy `arc_like` name for cross-phase continuity;
the engine family is `grid_toy`).

**Protocol (from `results.json["config"]`):**
- protocol: `standard`; family: `arc_like` (→ grid_toy alias).
- strategies: `frozen`, `context`, `param_tta`, `state`;
  strategy_kwargs: param_tta {steps:8, lr:0.5}, state {state_dim:null,
  seed:0}.
- `n_demos: 3`, `noise: 0.0`, `split: "eval"` (→ test, disjoint rule
  pool = {shift_color}).
- seeds: `0..199` (n=200).

**Outcome:** frozen accuracy 0.0 (CI [0,0.019]) vs context/param_tta/
state all 1.0 (CI [0.981,1.0]); diffs mcnemar_p ≈ 1.2e-60.
evidence_type: `CONTROLLED_TOY`.

**Provenance (from `results.json["provenance"]`):**
- git_commit: `29c5bf0`; config_hash: `d2814b9b82e9`.
- model_version: `adapt-v2`; task_generator_version: `taskgen-v2`.
- platform: Windows-10-10.0.26200; python 3.11.9.
- full task_seeds list [0..199], model_seed 0.

Re-runnable config: `experiments/configs/exp_001_arc.yaml`
(family `arc_like` → grid_toy). The live/eval pathway re-stamps
`PRECOMPUTED + SYNTHETIC` badges via `server.py` for `001_task_acquisition_arc`.

## 4. Cross-checks enforced by tests

- `tests/test_phase4.py::test_d48_arc_surfaced` — asserts
  `001_task_acquisition_arc` is wired in `server.py` + `web/index.html`
  and that `results.json` exists.
- `tests/test_tasks.py` / `tests/test_tasks_v2.py` — cover the
  `arc_like`→`grid_toy` alias and the ARC-JSON export
  (`to_arc_format`, which stamps `"synthetic": True`).
- `tests/test_freeze_gate.py` — asserts no `"ARC"` in the public display
  name for grid_toy.

## 5. Conclusion

`grid_toy` is explicitly labeled synthetic, no UI or report wording
implies an ARC-AGI benchmark reproduction, this document records why it
is a frontier-task-acquisition proxy (shared demonstration→hidden-
transformation→output pressure, at controlled tiny scale), and the E1
protocol + seed/config provenance are fully recorded above and in
`results.json`. D4.8 is satisfied.
