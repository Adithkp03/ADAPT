# Terminology Decisions — Phase 1

**Date:** 2026-09-06

1. TTA/TTT/ICT as ADAPT WORKING DEFINITIONS, not universal claims. Rationale: literature scopes differ per community; reviewer flagged redefinition risk.
2. ICL: "conditions computation on D without explicit param update; substrate may be activations/attention/state/algorithm" — replaces "context only" shorthand. Rationale: von Oswald + Garg/Li show optimization-like forward computation.
3. Recurrence vs TTT-state split by update type (transition F vs optimizer on S), not by size. Rationale: prevents claiming GRU demonstrates TTT-state.
4. BDH name: "Dragon Hatchling (BDH)" only; no acronym expansion beyond published name. Rationale: (?) in glossary unacceptable.
5. ARC split: ARC-AGI / ARC-AGI-1 / ARC-AGI-2 / our ARC-like synthetic — always qualified. Rationale: BDH-CQ result is ARC-AGI-1 150M-specific.
6. Capacity: d_s is OPERATIONAL PROXY, never "capacity itself". Rationale: dimension != effective capacity.
7. Every UI/content occurrence of learn/memory/reason/adapt/state audited against this file (see computational_substrate audit rule).
