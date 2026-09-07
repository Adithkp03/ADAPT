# D5.9 — Final Scientific Results Package

**Freeze date:** 2026-09-07 | **Reference commit:** `6f8d42d`
**Level-3 regenerable:** yes — every number below is read from
`research/experiments/*/results.json` (see `repro/`), regenerated
figures verified by hash.

## No cherry-picking (policy)

Unexpected results are kept and reported, not hidden:

- **Learned recurrent state did not acquire the linear task** (`E8-learned`):
  base 0.10 ≈ frozen floor 0.11. Retained as an honest negative; no
  causal claim is made on that cell. (`009_learned_linear_s0`).
- **Quadratic family**: state reader 0.17 vs context 1.00 — a READER
  expressivity limitation (linear read of quadratic statistics), kept
  and documented, not hidden (E7, `007_complexity`).
- **Capacity probe shows a cliff, not a slope** (E4): any lossy
  bottleneck destroys the exact sufficient statistics the linear reader
  needs (recorded in `phase2_validation_report.md`).
- **R1/R2 published-number reproductions did NOT match** the claimed
  Sudoku / 150M-29.5% numbers — reported with full conditions in
  `research/bdh/reproductions/` (probes are TOY_EXPERIMENT, never
  merged with PUBLISHED labels).

## What can adapt?

In our controlled toy implementations (linear, symbolic, compositional,
ARC-like grid proxy): **a model can acquire an unseen task rule at
inference time without changing its persistent parameters, by updating
an internal adaptive state.** E1: frozen 0.11 → state 1.00 (linear, 200
tasks, paired); frozen 0.00 → state 1.00 (symbolic and ARC-like proxy).
Δθ = 0.0, Δs > 0 recorded per episode. Status: **candidate hypothesis
supported for toy scope** (see `research/claim/central_claim.md`).

## How quickly?

E2 demo scaling (linear): N_D=1 → ~0.08–0.15 (underdetermined, 1 point
cannot fix 2 continuous params — predicted), N_D≥2 → 1.00. Symbolic:
even 1 demo identifies the offset (single pair → 1.00). Saturation
point is task-dependent. (`t2_demo_scaling.csv`)

## At what cost?

- Compute: state adaptation is a **single non-iterative pass**
  (`steps=0`), 1.00 accuracy at ~0 ms. Gradient-based readers need
  K=8+ steps and reach ~0.26–0.51; E3 shows monotone-but-saturating
  gains with more inference compute. (`t3_compute_scaling.csv`)
- Memory: state_bytes grow as the stat register (dim × dtype); capacity
  sweeps (E4) show strength depends on what the readout needs.

## Where is the information stored?

- **State**: adapted value carried in `s` (Δθ=0, Δs>0) — E1.
- **Context**: the demonstrations themselves (context reader) — same
  episodes, different substrate.
- **Parameters**: for parameter-TTA, information lands in θ (Δθ>0) —
  but from zero-init underfits at K=8 (compute-bound, not a refutation).

Causal check (E8): zero/shuffle/noise/swap/nullmean perturbations
destroy state accuracy (1.00 → ~0.03–0.10) and restore recovers 1.00 —
the state is *causally necessary*, not merely correlated.
(`t6_intervention_*.csv`, fig6)

## How much can it retain?

E5 A→B→A shows a failure mode. Linear: context 0.03 / state 0.09
retention (accumulated stats mix two lines → bad fit; catastrophic).
Symbolic: context/param 0.00 (latest-only fully forget), state 0.45
(accumulated votes preserve A — graceful partial retention).
**Which substrate wins is task-dependent** (H6). (`t5_interference_*.csv`,
fig5a/b)

## What causes failure?

1. **Reader expressivity** (quadratic: 0.17 state vs 1.00 context).
2. **Capacity cliff** (E4: d_s∈{4,2,1} → ≤0.10 accuracy).
3. **Interference** (E5 retention collapse on accrued-statistics
   mechanisms for linear).
4. **Under-provisioned meta-training** (learned_recurrent negative).
5. Noise degrades gracefully (E6: 1.00 → 0.86 at eps 0.35, linear), no
   cliff in tested range for symbolic.

## How does this relate to BDH-CQ?

BDH-CQ stores task-relevant structure in recurrent memory during
demonstrations, then solves the query by iterative latent computation.
Our state strategy is the same abstract envelope (demonstrations →
state write → readout solves query) in a transparent toy substrate.
R2 probed the official implementation: **150M / 29.5% pass@2 number
not reproduced by us** — kept as PUBLISHED with a configuration-specific
scope guard; our ARC-like work uses the grid_toy proxy and is labelled
PROXY/SYNTHETIC (never presented as ARC-AGI). See
`research/bdh/reproductions/` and `docs/bdh_integrity_audit.md`.

## Confidence intervals & provenance

Accuracy values carry Wilson 95% CI in `results.json`; every payload
carries seed + split + generator/task versions + git_commit +
config_hash (schema v1). Paired same-task comparisons; results
"rerun-identical" — only wall-clock varies
(`phase2_validation_report.md`).

## Index

- `final/` — frozen figures (hashes in `final_manifest.csv`)
- `tables/` — t1..t9 machine-readable summaries (sources = results.json)