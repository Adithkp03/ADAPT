# Phase 2 Completion Checklist (per phase2.md D2.1-D2.10 + §46)

## Deliverables
- [x] D2.1 Reproducible framework — src/adapt/runner.py (paired, provenance: commit+hash+versions+seeds), run_experiment.py CLI, experiments/configs/*.yaml
- [x] D2.2 Task generator — src/adapt/tasks.py (T=(R,D,Q,Y), 5 families, determinism, train/eval disjoint pools, GT clean of noise)
- [x] D2.3 Frozen baseline — FrozenBaseline (B1, no D)
- [x] D2.4 Param TTA — ParamTTA (real GD, persistent delta verified >0; full-theta only, adapter variant deferred as non-claim-relevant)
- [x] D2.5 Recurrent state — RecurrentState (fixed params, dTheta=0 asserted, dS>0, E8 get/set_state hooks)
- [x] D2.6 Learned-state TTT — TTTState (GD on state S, persistent init fixed; regression scope honestly declared)
- [x] D2.7 Telemetry — persistent_delta/state_delta/steps/latency/retention + trajectory-capable state hooks
- [x] D2.8 Core suite — 001 acquisition, 002 scaling, 003 compute, 004 capacity, 005 interference, 006 noise, 007 complexity, 008 intervention + gain-vs-retention frontier
- [x] D2.9 Validation report — research/experiments/phase2_validation_report.md + 8 figures
- [x] D2.10 Prototype v1 — end-to-end real experiment, thin CLI harness (no public UI per §36), exit test passes reproducibly

## §46 gates
- Scientific substrate: 4 genuinely different mechanisms work; rule hidden; GT exact; deltas measurable; failure measurable — YES
- Integrity: multi-seed (100-200); held-out rules; paired episodes; reset isolation tested; no param updates in state condition (asserted); TTA change verified; configs logged — YES
- Engineering: reproducible (byte-identical minus clock); 13 unit tests green; results serialized; versions pinned; runtime measured — YES
- Research: core+ablation+failure run; analyzed; contradictory results retained (quadratic reader, noise exception, capacity cliff); limitations documented — YES
- Pathway compliance: synthetic labeled; toy labeled TOY_EXPERIMENT; nothing claimed as official BDH; live/precomputed boundaries in place (all current results LIVE computation) — YES

## Milestones 2.1-2.10: all met. Gate: GO -> Phase 3.

## Freeze patches (review gate, applied)
- P1 quadratic predictor: TRUE 3x3 normal-equation fit (test_quadratic_state_fits_quadratic) — verified present.
- P2 honest naming: AnalyticalContext / GradientTaskLearner / SufficientStatState + STRATEGY_DISPLAY public names (frontend MUST use); FAMILY_DISPLAY pins "Grid Transformation Lab".
- P3 grid alias: grid_transform -> grid_toy (arc_like kept back-compat); NEVER "ARC Reasoning" in public surface.
- P4 config-driven hyperparams: steps/lr/state_dim/seed/tol all flow config -> strategy_kwargs; quadratic 0.1 inner damping is a documented model-definition constant, not a tunable.
- P5 latency split: t_adapt_ms / t_predict_ms / latency_ms (= sum) asserted in test_freeze_gate; CPU wall-clock is NOT a neural-inference cost claim.
- P6 result_schema_version: 1 on all three protocols (standard/interference/intervention).
