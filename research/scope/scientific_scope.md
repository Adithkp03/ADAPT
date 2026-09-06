# D1 — Scientific Scope Document — ADAPT

**Project:** ADAPT — *Where does an AI learn a new rule?*
**Approved Pathway topic:** Test-Time Adaptation (TTA / TTT)
**Supporting concept:** Skill Acquisition from Demonstrations
**Phase:** 1 — Scientific Specification
**Version:** v1.0 — 2026-09-06
**Status:** FROZEN (scope only). Central claim itself is a CANDIDATE HYPOTHESIS — see research/claim/central_claim.md. Final claim wording freezes after Phase 2 prototype validation.

---

## 1. Selected topic

**Primary:** Test-Time Adaptation — how a trained system uses information encountered during inference to change the computation it performs on subsequent inputs.

**Supporting:** Skill Acquisition from Demonstrations — the few-shot task-acquisition structure (D,Q) → Y with hidden rule R.

We use the supporting concept strictly as an evaluation scaffolding, not as an independent project. One central claim, one learning journey (Pathway brief §1).

## 2. Core research question

> **When a model encounters a previously unseen task at inference time, how is the task-specific information acquired, where is it stored, and what trade-offs arise from that memory mechanism?**

Sub-questions (decomposed):

1. What changes? — context / hidden state / weights / fast memory
2. How does it change? — conditioning / recurrence / gradient descent / Hebbian write
3. When does it change? — before / during / between examples
4. What persists? — one query / one task / sequence / session
5. What is capacity? — context length / state_dim / parameter count
6. What is failure mode? — forgetting / interference / instability / cost
7. Is update learned? — fixed rule / learned update / optimizer
8. Can we inspect it? — high / medium / low

## 3. Working thesis — CANDIDATE (not frozen; validated in Phase 2)

> **Inference-time adaptation can acquire task-specific behavior without permanently changing trained parameters, but the choice of adaptation substrate — context, recurrent state, or parameter updates — determines its capacity, cost, persistence, and susceptibility to interference.**

Frozen wording only after Phase 0/1 experiments validate which clauses we can demonstrate rigorously.

## 4. Scope boundaries

### In scope
- Inference-time adaptation (all substrates)
- Few-shot task acquisition from demonstrations
- Context-based adaptation (ICL as computation)
- Recurrent-state adaptation (s_t = F(s_{t-1}, x_t))
- Parameter-updating TTT (theta_{t+1}=theta_t - eta grad L)
- Learned-state TTT (state as learnable model, Sun et al. 2025)
- Task retention / interference / forgetting
- Adaptation compute / latency
- BDH synaptic-memory and BDH-CQ recurrent-memory + latent-reasoning as frontier case studies
- ARC-style visual rule induction as frontier evaluation family

### Out of scope
- General AGI, general continual learning, generic LLM training, generic RAG
- Broad survey of all memory architectures
- Explaining all of BDH or all forms of reasoning
- Claiming our toy model equals official BDH/BDH-CQ
- Training foundation models from scratch

## 5. Conceptual model (canonical)

```
               A NEW TASK ARRIVES
                        |
                        v
                DEMONSTRATIONS (D)
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
     CONTEXT          STATE           WEIGHTS
        |               |               |
    condition         update          optimize
        |               |               |
        +---------------+---------------+
                        |
                        v
                   NOVEL QUERY (Q)
                        |
                        v
                    PREDICTION
                        |
                        v
                  GROUND TRUTH (Y, R)
                        |
                        v
                  SUCCESS / FAILURE
                        |
                        v
                    RETENTION
                        |
                        v
                    NEW TASK (interference)
```

## 6. Definitions (normative)

| Term | Symbol | Meaning |
|------|--------|---------|
| Hidden rule | R | Task-specific mapping unknown to learner/model |
| Demonstrations | D = {(x_i,y_i)} | k examples revealing R |
| Query | Q | novel x_q |
| Ground truth | Y | R(Q), known to evaluator only |
| Frozen | f_theta(D,Q) | theta fixed |
| Param TTA | theta_{t+1}=theta_t - eta grad L_D | true tensor update |
| State adaptation | s_t = F(s_{t-1},x_t), theta fixed | delta_s>0, delta_theta=0 |
| TTT-state | S_t <- S_{t-1} - eta grad_S L_t(S) | state is learnable model |

## 7. Acceptance criterion

A reviewer reading only this document can describe ADAPT in two sentences without mentioning anything out-of-scope, and can state the independent variable (adaptation substrate) and dependent variables (accuracy, delta_theta, delta_s, latency, retention).

## 8. References to plan

- plan.md §2 conceptual model, §5 architecture, §7-8 task families
- research summary.md §1-5 (substrate taxonomy)
- phase1.md D1 template

## 9. Change log

- v1.0 2026-09-06: initial freeze
