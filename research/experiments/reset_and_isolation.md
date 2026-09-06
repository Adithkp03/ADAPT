# Reset and Isolation Policy

**Status:** normative from Phase 2 onward.

## Modes
1. EPISODIC (default): theta_i^(0)=theta_0, s_i^(0)=s_0. No cross-task leakage. All acquisition/capacity/compute claims use this mode.
2. CONTINUAL (explicit): state and/or params carry over A->B. Only for interference/retention experiments. Mode flag `continual: true` in config + logged.

## Invariants
- Param TTA: theta_A must never silently become init for Task B in episodic mode. Reset enforced in runner (assert theta==theta_0 at episode start).
- State: s_0 fixed init; continual mode sets s_B^(0)=s_A (logged).
- Oracle never touches model state.
- B1 (no D) vs B2 (with D) run on same seeds with same theta_0 — isolates value of D.

## Implementation note (Phase 2)
Runner must assert resets and log mode; violation fails the run.
