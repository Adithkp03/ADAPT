# Hypotheses — Pre-registered (Phase 1)

**Date:** 2026-09-06 | **Status:** pre-registered, not yet tested

## H1 — Evidence amount
More demonstrations improve adaptation performance up to saturation.
Test: sweep N_D 1..8, plot A(N_D).

## H2 — State capacity
Increasing state dimension d_s improves adaptation on sufficiently complex tasks (Tier 3+), less effect on Tier 1 linear.
Test: d_s in {8,32,128} x Tier.

## H3 — Adaptation compute
More adaptation steps K improve accuracy but increase latency linearly; diminishing returns beyond threshold.
Test: sweep K 0..16, measure A(K) and latency.

## H4 — Substrate existence
Recurrent state adaptation can acquire unseen rule without changing persistent parameters (Delta_theta=0, Delta_s>0, G>0).
Test: compare B4 vs B1/B2 on Tier1-3.

## H5 — Interference
Learning task B after A reduces accuracy on A (Retention < Initial) for finite state.
Test: A -> B -> A protocol.

## H6 — No universal winner
Best substrate depends on task characteristics (param TTA may win on Tier1 linear; state may be more efficient on symbolic with small d_s).
Test: compare B3 vs B4 across tiers.

## Falsification note
See falsification_criteria.md — if H4 fails (no gain with Delta_theta=0), revise central claim.
