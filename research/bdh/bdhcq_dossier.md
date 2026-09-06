# D4 — BDH-CQ Technical Dossier

**Version:** 1.0 | **Date:** 2026-09-06

---

## 1. What BDH-CQ is

Per current BDH-CQ paper (arXiv 2026, 2608.09888):

- Combines **in-context learning** with **recurrent latent reasoning**
- Inference-time inputs continuously update **recurrent memory**
- Query then solved via **iterative computation in high-dimensional latent space**
- **No verbalized chain-of-thought**
- **No inference-time parameter updating** in described mechanism (params static; memory evolves)
- Evaluated on **ARC-AGI-1** with controlled ARC-like interventions studying what is learned from demonstrations, consistency, difficult concepts.

This is **directly relevant** to our topic: adaptation substrate = recurrent memory, query compute = latent reasoning.

## 2. Computational timeline (normative)

```
demonstration 1  -> memory update
demonstration 2  -> memory update
demonstration 3  -> memory update
                -> query arrives
                -> latent recurrent computation x K (effort = K)
                -> answer
```

- Static: trained parameters theta
- Evolves: recurrent memory M_t
- Consumed: demonstrations D
- Produced: answer y_hat
- Compute spent: K latent steps

## 3. Effort scaling

Paper reports low/medium/high inference effort. We must reproduce exact definitions from paper in Phase 4; placeholder:

- Low: K small
- Medium: K medium
- High: K large
Performance vs effort tradeoff is central to Pathway brief's cost/latency requirement.

## 4. ARC experiments

- Evaluation: ARC-AGI-1
- Result reported: **150M, 29.5% pass@2 @ computed $0.0007/task** — this is a configuration-specific reported number.
- Interventions: controlled ARC-like transformations to test: what model learns from demos, how consistently it applies transformation, difficulty concepts.

We must not claim: general BDH-CQ solves 29.5% ARC; claim exactly as qualified.

## 5. What BDH-CQ adaptively stores

| Our concept | BDH-CQ equivalent |
|-------------|-------------------|
| Demonstrations D | input sequence tokens |
| Memory write | recurrent memory update |
| Query computation | latent iterative reasoning |
| Persistent params | trained weights (fixed at inference) |
| Interference | recurrent memory dynamics (to be studied) |

## 6. Relation to our 4 regimes

- Frozen baseline  <--> BDH-CQ without memory update (no adaptation)
- Recurrent state  <--> BDH-CQ memory update (closest analogue)
- Param TTA      <--> NOT BDH-CQ (BDH-CQ does not param-update at inference per paper)
- Learned-state TTT <--> loosely similar (state is learned, but BDH-CQ memory is learned recurrent dynamics)

Our model is **controlled analogue**, not reproduction.

## 7. Evidence ledger (subset)

| Claim | Evidence type | Allowed wording |
|-------|---------------|-----------------|
| Recurrent memory updated during inference | PUBLISHED_EMPIRICAL | "Paper says inputs presented during inference continuously update recurrent memory" |
| Latent recurrent reasoning | PUBLISHED_EMPIRICAL | "Paper describes subsequent query solving through iterative latent computation without verbal trace" |
| 29.5% pass@2 150M @ $0.0007 | PUBLISHED_EMPIRICAL + OFFICIAL_REPORT | "Authors report 29.5% pass@2 on ARC-AGI-1 for 150M config at computed $0.0007/task in their setup" |
| No param update at inference | PUBLISHED_EMPIRICAL | "Described inference mechanism does not involve parameter updates; memory evolves" |
| Our toy reproduces full BDH-CQ | — | NEVER |

## 8. Open questions for Phase 4 implementation

- Exact equations for memory update (copy verbatim)
- Latent reasoning cell architecture
- Effort definition (K? steps? flops?)
- How to build educational analogue that preserves no-param-update property

## 9. References

- BDH-CQ paper arXiv 2608.09888 (primary)
- Pathway Equations of Reasoning (supplement)
