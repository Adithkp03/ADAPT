# D4.2 — BDH-CQ Technical Dossier

**Version:** 2.0 (Phase 4 expansion of v1.0) | **Date:** 2026-09-07
**Primary source:** B. Engdahl, A. Kosowski, J. Chorowski, Z. Stamirowska,
P. Uznański, J. Jiang, R. Phadke, R. Kinas, R. Zhong, *BDH-CQ: In-Context
Learning with Recurrent Latent Reasoning*, arXiv:2608.09888 (2026), cs.NE.
**Third-party code (WIP, NOT official):**
https://github.com/lucidrains/bdh-cq (`pip install bdh-cq`; `BDH` +
`BDHReasoningWrapper`; tensor stages ingested, int stages = latent
reasoning steps; `return_memory` exposes memories).

## 1. What BDH-CQ is

Per the abstract (verbatim core): system evaluated on the **ARC-AGI-1
evaluation set**, using **controlled ARC-like interventions** to study
what it learns from demonstrations, consistency of the inferred
transformation, and difficult concepts. Inference-time inputs
**continuously update recurrent memory**; the query is then solved by
**iterative computation in high-dimensional latent space** — **no
verbalized chain-of-thought**, **no inference-time parameter updating**
in the described mechanism.

## 2. Computational timeline (normative)

```text
demonstration 1 → memory update
demonstration 2 → memory update
demonstration 3 → memory update
query → latent recurrent computation × K (effort) → answer
```

Static: trained parameters θ. Evolves: recurrent memory M_t. Consumed:
demonstrations D. Produced: answer ŷ. Cost: K latent steps.

## 3. Reported result (exact, configuration-scoped)

> "A 150M-parameter configuration reaches **29.5% pass@2** at a computed
> inference cost of **$0.0007 per task**. This operating point breaks
> through the previously reported ARC-AGI-1 cost-accuracy Pareto frontier,
> establishing a new state of the art in benchmark cost efficiency."

Evidence: PUBLISHED_EMPIRICAL + OFFICIAL_REPORT. Allowed wording is the
sentence above and nothing broader. NEVER: "BDH-CQ solves ARC at 29.5%"
(unscoped), never cost-generalized beyond that configuration.

## 4. Effort scaling

Paper frames low/medium/high inference effort; effort↔performance is the
paper's own cost-accuracy trade-off — the same lens as our K-sweep (E3).
Exact effort definitions to be quoted from the paper body in full
Phase 5 review; until then the UI states effort qualitatively only.

## 5. Relation to our 4 regimes (see concept_mapping.md)

Frozen ↔ BDH-CQ without memory update · Recurrent state ↔ memory update
(closest analogue) · Param TTA ↔ NOT BDH-CQ (no param update at inference
per paper) · Learned-state TTT ↔ loosely similar (learned dynamics, but
BDH-CQ memory is learned recurrent dynamics at scale). Our model is a
controlled analogue, not a reproduction.

## 6. Third-party implementation status (verified 2026-09-07)

`lucidrains/bdh-cq` README titles itself "(wip)". API: `BDH(dim,
num_tokens)` forward → logits; `BDHReasoningWrapper(model)` interleaves
token chunks and latent steps, `return_memory=True` surfaces memories,
`generate()` decodes answers. D4.6 levels: (1) architecture verification
— instantiate + forward on random ids, confirm memory/answer path exists;
(2) tiny controlled experiment — synthetic probe of memory behavior;
(3) published benchmark — NOT attempted (resources/fidelity; stated, not
hidden). Any use is labeled third-party WIP in UI and ledger.

## 7. Evidence status (see also evidence_ledger.csv)

All v1.0 rows retained with abstract-verbatim wording; added: author list
+ eprint + class (cs.NE), effort-framing row (PUBLISHED_EMPIRICAL,
qualitative-only until body quoted), third-party-API rows
(OUR_REPRO only if Level 1 passes; else TOY_EXPERIMENT/ILLUSTRATION).
