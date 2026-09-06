# Statistical Analysis Plan — candidate (freeze with episode protocol before Phase 2 runs)

**Status:** CANDIDATE 2026-09-06 | Formal preregistration occurs at freeze (config + seed set + this file hashed).

## Primary outcome
Exact task success / accuracy per episode (tolerance for regression tiers, exact-match for symbolic/ARC-like). All claims evaluated on this first.

## Secondary outcomes
Adaptation gain G, retention R_A, latency, Delta_theta / Delta_s, state-intervention effect (A(s_A)-A(s_tilde)).

## Design
Paired: every condition evaluated on IDENTICAL task+seed sets. Exploit pairing (paired tests / paired bootstrap CIs), not independent-sample tests.

## Comparisons
- Core: A_state vs A_frozen (paired).
- Mechanistic: A(s_A) vs A(s_tilde) per intervention type (paired).
- Capacity: trend over d_s proxy within tier (report as proxy, not capacity proof).

## Sample size
N>=100 episodes/condition pilot; N=500 for final report figures. Report 95% CIs (bootstrap for means, Wilson for proportions; paired bootstrap for differences).

## Multiplicity
Many experiments planned: designate CONFIRMATORY (E1 core gain, E8 intervention, E5 interference under stress) vs EXPLORATORY (all sweeps). Confirmatory tested at alpha with Holm correction across the three; exploratory reported with CIs only, no binary claims.

## Preregistration rule
Freeze = this file + episode_protocol.md + reset_and_isolation.md + seed list + config hashes committed and tagged BEFORE runs. Any deviation logged as post-hoc.
