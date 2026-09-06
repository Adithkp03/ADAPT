**Status: CONDITIONAL GO (revised 2026-09-06 per review — was incorrectly marked unconditional GO)**

# D9 — Feasibility / Go-No-Go Review — Phase 1

**Date:** 2026-09-06 | **Reviewers:** Scientific Lead + ML Lead | **Decision quorum:** Phase 1 exit

---

## 1. Review matrix

| Experiment | Scientific value | Impl. difficulty | Runtime | Risk | Decision | Rationale |
|------------|------------------|------------------|---------|------|----------|-----------|
| Linear regression TTA + state | High | Low | Fast | Low | GO | Calibration, analytic GT, proves Delta_s>0 exists |
| Symbolic adaptation (Tier3) | High | Medium | Fast | Low | GO | Makes rule induction intuitive, supports claim |
| Compositional (Tier4) | High | Medium | Fast | Medium | GO (conditional) | Needed for complexity sweep; scope-cut if time |
| ARC-like adaptation (Tier5) | Very high | High | Medium | Medium | GO (scoped) | Frontier link + BDH-CQ validation; use small grids (3x3-6x6), limited pool |
| Official BDH live | Low/uncertain | Very high | High | Very high | NO | Training cost, complexity; use precomputed evidence + repo read-through |
| BDH precomputed evidence | High | Medium | — | Low | GO | Cite paper + repo; label evidence type correctly |
| Full BDH-CQ reproduction | Moderate | Very high | High | Very high | NO / conditional | Clone repo, run basic inference only; not full training reproduction |
| TTT-state (learned state) | Medium-High | High | Medium | Medium | GO (stretch) | Distinguishes simple recurrence from learned-state; implement only after A-D work |
| Interference/retention | High | Low | Fast | Low | GO | Core failure experiment; required for trade-off clause |

## 2. Resource constraints

- Team size assumption: 3-5 (as per basicroadmap). With 1-2 implementers, keep scope to Tier1-3 + small ARC (Tier5 limited).
- Compute: CPU-only tiny models for LIVE; no GPU required for Phase 2 prototype. Precomputed sweeps can run local CPU overnight.
- Time: Phase 2 true critical path is generator + frozen + param TTA + state -> validated results (before frontend).

## 3. Go criteria (must hold to proceed to Phase 2)

- [x] Claim frozen to candidate v2 with falsification criteria
- [x] Terminology map prevents conflation (table + glossary)
- [x] Task generator spec covers T=(R,D,Q,Y) with GT
- [x] Four regimes spec'd with equations and deltas
- [x] BDH/BDH-CQ dossiers show substantive connection (not rhetorical)
- [x] Live vs precomputed boundaries defined
- [x] Hypotheses pre-registered

NOT all criteria met at review time. Status: **CONDITIONAL GO to Phase 1 closure pass (no serious Phase 2 model implementation until blockers cleared).**

Blockers: (1) citation integrity (placeholder URLs), (2) claim-freeze semantics, (3) causal state validation design, (4) reset/isolation formalization, (5) one-paper-per-row matrix, (6) statistical preregistration.

This file is updated to CONDITIONAL GO; unconditional GO was premature (claim doc itself states candidate status).

## 4. Risk mitigations

- Risk: ARC grid complexity explodes -> Mitigation: cap grid size 6x6, rule pool <20 for Phase 2.
- Risk: TTT-state too hard -> Mitigation: treat as stretch; Phase 2 success does not depend on it.
- Risk: Overclaim BDH -> Mitigation: evidence_ledger + audit, label TOY_EXPERIMENT vs PUBLISHED_EMPIRICAL.
- Risk: Frontend before science -> Mitigation: no serious frontend until D2.10 (one real experiment) passes.

## 5. Conditional triggers to downgrade scope (explicit)

- If after 2 weeks linear state model shows no gain (F1 falsification) -> revisit architecture, not expand scope.
- If ARC-like generator bugs cause non-reproducibility -> fall back to symbolic/compositional as primary frontier proxy.
- If BDH repo fails to run at pinned commit within 1 day -> switch to paper-only evidence with OFFICIAL_REPORT labeling.

## 6. Approval

Scientific Lead: ____________  ML Lead: ____________  Systems Lead: ____________

Date: 2026-09-06
