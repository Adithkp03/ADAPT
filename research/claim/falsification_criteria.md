# Falsification Criteria — Central Claim

**Companion to central_claim.md | v1.1 hardened**

---

## 1. Supporting evidence (must all hold for claim to be considered supported)

| # | Criterion | Measurement | Pass condition |
|---|-----------|-------------|----------------|
| E1 | Adaptation gain | Accuracy adapted vs frozen | A_adapted > A_frozen + epsilon (epsilon via 95% CI, >=100 episodes) |
| E2 | No param change | L2 param delta | Delta_theta == 0 (within floating tolerance) for state model |
| E3 | State change (necessary, not sufficient) | L2 state delta | Delta_s > 0. NOTE: change alone never proves storage — requires causal intervention E8 (ablate/shuffle/swap state; accuracy must drop and recover on restore) |
| E4 | Capacity effect | Sweep d_s | Larger d_s improves accuracy on complex tasks (stat significant) |
| E5 | Retention cost | Interference test A->B->A | Retention < initial A (demonstrates trade-off) |
| E6 | Ground truth | Exact match vs Y | Truth beside estimate visible |

If any E1-E3 fails, core claim fails.

## 2. Falsification conditions (any one forces revision)

| # | Condition | Interpretation | Action |
|---|-----------|----------------|--------|
| F1 | No gain | State adaptation does not improve over frozen | Reject or reduce claim to "state adaptation insufficient in this architecture" |
| F2 | Hidden param update | Delta_theta > 0 in "state" model | Implementation bug; fix or reclassify as hybrid |
| F3 | State not carrying info | Delta_s>0 but probing shows no task information (probing accuracy = chance) | Claim about state storage false; revise to conditioning-only |
| F4 | No capacity effect | Varying d_s has no effect on any task | Remove capacity clause from claim |
| F5 | No interference | Retention ≈ initial (no forgetting) | Remove retention trade-off clause or note task too simple |

## 3. Statistical discipline

- Minimum 100 episodes per condition (Phase 2 will use 500 for report)
- Report 95% CI (bootstrap or Wilson for accuracy)
- Seed-averaged, config-hashed, git-pinned
- Pre-register hypotheses (see hypotheses.md) before running

## 4. What we will NOT do

- Post-hoc cherry-pick seeds that show gain
- Present animation as computation
- Collapse evidence types (toy vs published)

## 5. Decision procedure after Phase 2

```
Run E1-E6 -> if all pass -> freeze v2 wording
        -> if F1-F5 -> revise claim, document, re-run
        -> if partial -> narrow scope (which families substantiate claim?)
```

## Falsification hierarchy (added per review)

- Level 1 Core: can state-only adaptation improve novel-task performance with Delta_theta=0? (E1-E2)
- Level 2 Mechanistic: is changed state CAUSALLY necessary? (E8 intervention: destroy adapted state -> accuracy drops; restore -> recovers)
- Level 3 Capacity: does operational capacity proxy d_s affect performance under controlled complexity? (dimension is proxy, not capacity itself)
- Level 4 Interference: does sequential adaptation induce measurable retention effects UNDER STRESS? Absence of interference does not falsify core claim — means regime did not stress the boundary.
- Level 5 Generalization: does behavior survive across task families? (Tier 1->5)

H5 revised: "Finite adaptive memory MAY create an adaptation-retention trade-off under sufficiently demanding or interfering sequences." No-interference = boundary not stressed, not claim failure.
