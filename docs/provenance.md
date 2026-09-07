# Provenance Audit (D3.10 research-integrity check — every UI number → source)

| UI number | Computing function | Live / precomputed | Evidence label | Vetted artifact |
|---|---|---|---|---|
| Flagship pred / truth / ✓✗ | `runner.run_episode` + `tasks.generate_task` + `telemetry.is_correct` | live | LIVE + SYNTHETIC | — (computed now) |
| Δθ / Δs | `strategy.telemetry()` (`persistent_delta`, `state_delta`) | live | LIVE + SYNTHETIC | — |
| Adapt/predict ms, steps, dims | `strategy.telemetry()` | live | LIVE + SYNTHETIC | — |
| N_D / d_s / K / noise sweep points + CI | `telemetry.accuracy_ci` over `run_episode` loop in `/api/sweep` | live | LIVE + SYNTHETIC | — |
| Compare rows (pred, Δθ, Δs) | `run_episode` × N on same task | live | LIVE + SYNTHETIC | — |
| A→B→A table | continual adapt/predict in `/api/interference` | live | LIVE + SYNTHETIC | — |
| Perturb/restore table | `get_state/set_state` counterfactuals in `/api/intervene` | live | LIVE + SYNTHETIC | — |
| Learned lab results | `learned.py` trio via `strategies.make_strategy`, `checkpoints/*.npz` | live (vetted ckpt) | LIVE + SYNTHETIC | `checkpoints/learned_{rec,ptt,ttt}_s0.npz` |
| Precomputed summaries | `experiments/run_sweeps.py` → `results.json` | precomputed | PRECOMPUTED + SYNTHETIC | `research/experiments/*/results.json` |
| Figures | `research/experiments/make_figures.py` | precomputed | PRECOMPUTED (+ SYNTHETIC ctx) | `research/experiments/figures/*.png` |
| BDH-CQ 150M / 29.5% / $0.0007 | authors' paper, via dossier | published | PUBLISHED RESULT | `research/bdh/bdhcq_dossier.md` §4 |
| BDH equation / architecture | paper + Equations of Reasoning, via dossier | published desc. | PUBLISHED RESULT | `research/bdh/bdh_dossier.md` |
| R1 / R2 reproduction outputs | `experiments/repro_r1.py`, `experiments/repro_r2.py` | reproduced (CPU, random ids) | PUBLISHED/OFFICIAL (structure) + TOY_EXPERIMENT (probe) | `research/bdh/reproductions/R1_results.md`, `R2_results.md` (pins: bdh@`2b0d7a4`, bdh-cq@`c246f89`, torch 2.14.0+cpu) |
| η → ‖Δσ‖ readout | local `η·1·1` in `app.js` | illustrative | ILLUSTRATIVE | labeled educational implementation |
| Pre/post/in-situ scores | local quiz key comparison | local | n/a (learner's own) | keys in `app.js` (`PRE`/`POST` + evaluable mapping in `research/education/evaluation_plan.md`) |

Every live payload carries `provenance {seed, task_generator_version,
model_version, git_commit, config_hash, result_schema_version}` rendered in
the Experiment-details drawer; sweeps carry `seed_base` + config hash.
Precomputed payloads are re-stamped `execution_type: precomputed`.
