# D5.14 — Defense: BDH / BDH-CQ Notes

Compressed technical facts for live defense. Full detail lives in the
technical dossiers (`research/bdh/*_technical_dossier.md`) and the
reproduction logs (`research/bdh/reproductions/`).

## BDH (Kosowski et al. 2025, arXiv:2509.26507)

- Post-Transformer, scale-free architecture of locally interacting
  **neuron particles**.
- Working memory lives in **synaptic state σ** — updated, not replaced.
- Published Hebbian-style update form: `σ ← σ + ηXYᵀ`
  (educational simplification in our UI; equation card labels this).
- Sparse positive activations; "Equations of Reasoning" (§4) documents
  the 4l–4l+3 round structure (memory read / write / gated readout /
  state update) — mirrored in `research/bdh/equations.md`.
- Public repo: `pathwaycom/bdh`, pinned at `2b0d7a4` for R1.
- **Not a Mamba-style SSM**: working memory is a synaptic matrix updated
  Hebbianly within a scale-free graph, not a linear-time-invariant
  recurrence. (Distinction spelled out in the dossier — a judge will ask.)

## BDH-CQ (Engdahl et al. 2026, arXiv:2608.09888)

- Demonstrations update **recurrent memory**; query solved by
  **iterative latent computation** (multiple latent steps before readout).
- Reported: 150M-parameter config, **29.5% pass@2 on ARC-AGI-1** at a
  computed cost ~$0.0007/task.
- Scope guard is mandatory and present in the UI: config-specific,
  computed-cost, authors' result — always PUBLISHED.
- Public repo: `pathwaycom/bdh-cq`, pinned at `c246f89` for R2.
- `lucidrains/bdh-cq` is third-party WIP — **not** the official
  implementation (evidence ledger row; we pin the official repo).

## What we reproduced (R1/R2)

| Probe | Pin | Headline claim | Our result | Verdict |
|---|---|---|---|---|
| R1 BDH Sudoku | bdh@2b0d7a4 | 97.4% | did NOT match | PUBLISHED stays; our TOY probe recorded with conditions |
| R2 BDH-CQ 150M/29.5% | bdh-cq@c246f89 | 29.5% pass@2 | did NOT match (einx failure also recorded) | PUBLISHED stays scoped; our TOY probe recorded with conditions |

We do not claim to falsify the papers — we report that *our* probes on
the pinned official repos did not reproduce the headline numbers, and we
never merge that with the papers' PUBLISHED claims
(`docs/bdh_integrity_audit.md`).

## The conceptual bridge (what the learner is taught)

```text
demonstrations → state write → readout solves query   (our state model)
      maps onto
BDH:  inputs → synaptic σ write → readout               (synaptic working memory)
BDH-CQ: demonstrations → recurrent memory → latent computations → readout
```

The ejection seat if asked "is this official BDH?": **no** — our
stepper/synapse card is an educational rendering; the dossiers
summarize the papers; the R1/R2 probes ran the official repos
directly.