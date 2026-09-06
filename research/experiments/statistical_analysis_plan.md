# Statistical Analysis Plan — v2 (Phase 2B, frozen for 2B eval)

**Status:** FROZEN 2026-09-06 for Phase 2B test-split evaluation. Preregistration: this file + episode_protocol + reset_and_isolation + seed lists hashed at commit before test runs.

## Seed taxonomy (review fix)

- `task_seeds`: task/episode identity (which rule + demos + query). Paired across strategies.
- `model_seed`: model randomness (init, ES sampling, projection draws). Recorded in provenance.
- Never conflate: one model_seed x full task_seed set = one factorial cell. Learned results reported per model_seed (0,1) then averaged.

## Splits

- train: meta-training / hyperparameter search. val: checkpoint/HP selection. test: final eval, inspected only through frozen configs. Tuning on test invalidates the run.

## Outcomes

- Primary: exact task success / accuracy per episode.
- Secondary: gain over frozen, retention, latency split (t_adapt/t_predict), intervention drop, probe MSE ratio.

## Tests

- Accuracy with Wilson 95% CI.
- Paired strategy contrasts: bootstrap 95% CI on differences (paired by task_seed) + exact McNemar two-sided p (paired binary) + Cohen's h effect size.
- Confirmatory set (Holm-corrected across the set): L1 core gain (learned_state vs frozen), L2 intervention drop, L4 retention drop. Everything else exploratory (CIs only, no binary claims).

## Multiplicity

7+ experiments x strategies: only the 3 confirmatory contrasts carry corrected p-values; sweeps report CIs without significance claims.

## Reproducibility

Rerun-identical required: accuracies/deltas/diffs byte-identical across reruns (wall-clock exempt). Provenance: git commit, config hash, model/task versions, task_seeds, model_seed.
