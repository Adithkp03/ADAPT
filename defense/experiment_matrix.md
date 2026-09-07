# D5.14 — Defense: Experiment Matrix

Every experiment a judge might reference: what it shows, where it lives,
and its honest verdict.

| Exp | Question | Design | Result (accuracy, N) | Vindicated | Location |
|---|---|---|---|---|---|
| E1 | Can a model adapt with Δθ=0? | task acquisition, paired, 200 | linear frozen 0.11 → state 1.00; symbolic/ARC-proxy 0.00 → 1.00 | L1 PASS | 001_task_acquisition_* |
| E2 | How many demos? | N_D 1..8, 100/point | linear ≥2 saturates 1.00 (1 → <0.15); symbolic 1 demo → 1.00 | H1 saturating | 002_demo_scaling_* |
| E3 | Does more compute help? | K 0..16 | GD readers 0.06→0.51 monotone; state 1.00 @0 steps | H3 SUPPORTED | 003_compute_scaling_linear |
| E4 | Capacity limit? | d_s None/4/2/1 | 1.00 / 0.10 / 0.10 / 0.05 — CLIFF, not slope | L3 weak (proxy limit stated) | 004_state_capacity_linear |
| E5 | Interference A→B→A | distinct rules, 100 | linear state ret 0.09; symbolic state ret 0.45 (best); context/param ≤0.06 | H5/H6 conditional | 005_interference_* |
| E6 | Noise | eps 0..0.35 | linear 1.00→0.86@0.35; symbolic flat 1.00 | robustness, no failure | 006_noise_* |
| E7 | Harder families | fixed configs | linear/symbolic/compositional 1.00; quadratic state 0.17 vs context 1.00 — READER limit | L5 partial | 007_complexity |
| E8 | Is the state causal? | perturb/restore, 100 | linear 1.00→~0.03–0.10→restore 1.00 (all 5 perturbations) | L2 PASS | 008_intervention_* |
| E8-lrn | Causal on learned? | learned checkpoint | learned_state L2 PASS; learned_recurrent base 0.10 ≈ floor — HONEST NEGATIVE | L2 (partial) | 009_learned_* |
| R1 | Reproduce BDH Sudoku? | official repo@2b0d7a4, torch 2.14.0+cpu | our reproduction did NOT match 97.4% — recorded | REPORTED w/ conditions | research/bdh/reproductions/R1 |
| R2 | Reproduce BDH-CQ 150M/29.5%? | official repo@c246f89 | our reproduction did NOT match — recorded (einx failure also recorded) | REPORTED w/ conditions | research/bdh/reproductions/R2 |
| ARC-proxy | Proxy validity | synthetic grid_toy, seeds 0–199, split eval→test | frozen 0.0 vs adapted 1.0; labelled PROXY | scoping | research/experiments/arc_like_proxy_validation.md |
| Learner study | Does someone learn? | 8–15 participants, pre/post + transfer | **PENDING** (pilot n=1 only) | no claim | evaluation/learning_evaluation_report.md |

Re-runs are byte-identical (only wall-clock varies)
(`phase2_validation_report.md`).

## Which results are precomputed?

All E1–E9 sweeps are precomputed research runs served with provenance
as **PRECOMPUTED**. The flagship / modify / lab live endpoints compute
fresh per request as **LIVE + SYNTHETIC**. A judge can hit "Run" and
get a new seed with the same statistical envelope.