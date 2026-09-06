# Phase 2B — Learned Neural Substrate (design, frozen)

## Framing change (per review)

- Phase 2A question (answered): can CONTROLLED analytical memory substrates acquire an unseen rule with causal substrate effects? YES (see phase2_validation_report.md).
- Phase 2B question: does the same phenomenon emerge in a LEARNED neural adaptive state sharing one backbone with param-TTA and TTT-state?
- Central claim wording narrows until 2B lands: "a controlled parameterized system can acquire rules from demonstrations via transient state with persistent params unchanged." The broader "a model can..." unlocks after 2B.

## Naming honesty

Analytical strategies renamed: AnalyticalContext, GradientTaskLearner, SufficientStatState. grid_toy replaces arc_like (6 rules, ARC-JSON export; NOT ARC reasoning). Learned trio in learned.py shares an MLP backbone (h=8), meta-trained by antithetic ES on train, selected on val, evaluated on test.

## Deliverable mapping

- P0.1 quadratic fix: TRUE 3x3 normal-equation fit (test_quadratic_state_fits_quadratic).
- P0.2 renames: done, aliases kept for 2A reproducibility.
- P0.3/4 learned recurrent + proper TTT-state: learned.py (ES meta-training, analytic inner loops).
- P0.5 intervention controls: swap-with-B as matched control + nullmean population null (on-manifold task-component removal); shuffle-failure explicitly NOT claimed as information removal (coordinate-correspondence caveat); McNemar + Holm across perturbations; learned E8 wired (runner supports learned_state/learned_ttt; 009 rerun non-empty: learned_ttt L2 passes, learned_rec honest floor-effect negative).
- P0.6 train/val/test: disjoint pools per family + tuning protocol (train search, val select, test once).
- P0.7 seed taxonomy: task_seeds vs model_seed, factorial cells, provenance records both.
- P1: affine symbolic (24-hypothesis space), op-chain compositional (depth ladder 1-3), grid_toy 6 rules, rule-parameter probing, t_adapt/t_predict split, stats v2 (McNemar + Cohen h + Holm).
- P2: wider figures (frontier + probe/transfer panels), larger hidden size documented as future (h=8->32 scaling untested), no-GPU path documented (numpy CPU; wall-clock is NOT an inference-cost claim), broader benchmark = test-split 2B battery + ARC-JSON export groundwork.
