# D5 — Central Claim Specification

**Phase 1 | v1.1 2026-09-06 | Status: CANDIDATE HYPOTHESIS / PREREGISTRATION PENDING — NOT frozen. Final wording freezes after Phase 2 prototype validation per go_no_go CONDITIONAL GO.**

---

## Evolution

### v0 — rejected (too vague)
> "Models can learn at test time."
Issues: no mechanism, no falsifiability, conflates all adaptation.

### v1 — rejected (better but incomplete)
> "Models can adapt to unseen tasks without changing their weights."
Issues: true for ICL but doesn't specify where info goes or trade-off.

### v2 — candidate (testable)
> **"A model can acquire an unseen task rule at inference time without changing its persistent parameters by updating an internal adaptive state, but the capacity and update dynamics of that state constrain what can be retained."**

Why v2 is sufficient:
- Specifies substrate (adaptive state, not params)
- Specifies condition (unseen rule, inference-time)
- Specifies trade-off (capacity/dynamics constrain retention)
- Is falsifiable (see falsification_criteria.md)

## Formal statement

Let task T=(R,D,Q,Y), model f_theta with state s.

Claim: exists recurrent mechanism F such that:

```
theta' = theta  (Delta_theta = 0)
s' = F(s, D)    (Delta_s > 0)
A_adapted = Acc(f_theta(s', Q), Y)
A_frozen  = Acc(f_theta(s, Q), Y)   or f without D
```
and

```
A_adapted > A_frozen + epsilon   (epsilon = statistically meaningful margin)
```

and increasing state capacity d_s or interference conditions changes retention as per hypotheses.

## Scope of claim

- We claim this for our **controlled toy implementations** (recurrent state model) on **synthetic task families** (linear->symbolic->ARC-like).
- We do NOT claim this establishes general LLM behavior; we cite published results for frontier models.
- BDH/BDH-CQ are **case studies** illustrating related design choices in frontier architectures (synaptic state, recurrent memory), not proof of our claim.

## What would strengthen claim (Phase 2)

- Reproducible demonstration across linear, symbolic, compositional families
- Ablations: no adaptation, context only, param TTA, state size sweep
- Retention under interference showing failure mode
- Live computation labeling (not animation)

## What would weaken / force revision

See falsification_criteria.md

## One-sentence version for Brief compliance

> "Inference-time adaptation can succeed without persistent parameter changes, storing the new rule in evolving state — but that state's capacity and dynamics limit retention."

(52 words; brief requires one precise falsifiable sentence — this is the short form of v2)

## Claim-freeze semantics (added per review)

- Frozen: scientific scope (topic, question, boundaries, task abstraction T=(R,D,Q,Y)).
- Candidate: this claim (v2). It is a preregistration candidate, not a finding.
- Writing "pre-registered" in markdown does not constitute preregistration; formal freeze occurs when statistical plan + episode protocol + reset rules are reviewed and hashed (see research/experiments/statistical_analysis_plan.md).
