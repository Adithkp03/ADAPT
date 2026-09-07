# D5.12 — Sources

Primary sources are cited beside the technical claims that use them
(brief requirement). This file is the canonical bibliography; each row
of `research/literature/evidence_matrix.csv` carries the URL +
circumscribed claim per paper.

## Primary papers (3+ recent requirement met and exceeded)

| Paper | Venue | Entry point |
|---|---|---|
| Sun, Y. et al. — *Test-Time Training with Self-Supervision for Generalization under Distribution Shifts* | ICML 2020 | `research/literature/evidence_matrix.csv` |
| Schlag, I. et al. — *Linear Transformers Are Secretly Fast Weight Programmers* | ICML 2021 | evidence_matrix |
| Garg, S. et al. — *What Can Transformers Learn In-Context? A Case Study of Simple Function Classes* | NeurIPS 2022 | evidence_matrix |
| von Oswald, J. et al. — *Transformers Learn In-Context by Gradient Descent* | ICML 2023 | evidence_matrix; `research summary.md` |
| Li, Y. et al. — *In-Context Algorithm Learning* | NeurIPS 2023 | evidence_matrix |
| Hardt, M. & Sun, Y. — *Test-Time Training on Nearest Neighbors for Large Language Models* | ICLR 2024 | evidence_matrix |
| Akyürek, E. et al. — *The Surprising Effectiveness of Test-Time Training for Abstract Reasoning* | ICML 2025 | evidence_matrix; arXiv:2411.07279 |
| Sun, Y. et al. — *Learning to (Learn at Test Time): RNNs with Expressive Hidden States* | ICML 2025 | evidence_matrix; arXiv:2501.06152 |
| Behrouz, A. et al. — *Titans* | ICLR 2025 | evidence_matrix |
| Behrouz, A. et al. — *ATLAS* | 2025 | evidence_matrix |
| Kosowski, A. et al. — *The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain* (**BDH**) | arXiv:2509.26507 (2025) | `research/bdh/bdh_technical_dossier.md`, `equations.md`, dossiers |
| Engdahl, B. et al. — *…Recurrent Latent Reasoning* (**BDH-CQ**) | arXiv:2608.09888 (2026) | `research/bdh/bdhcq_technical_dossier.md` |
| Sun, Y. et al. — *TTT-E2E* (End-to-End TTT for Long Context) | 2026 | evidence_matrix |
| Kirsch, L. et al. — *General-Purpose In-Context Learning* | 2026 | evidence_matrix |

## Secondary / reference materials

- Pathway — *Equations of Reasoning* (public teaching text for the BDH
  design; blocks match round numbering 4l–4l+3 in `research/bdh/equations.md`).
- Standard references for statistical testing (McNemar, Holm step-down)
  as used in `runner.py`.
- `research/bdh/reproductions/README.md` — pins for the official
  `pathwaycom/bdh` (commit `2b0d7a4`) and `pathwaycom/bdh-cq`
  (commit `c246f89`) repos used in R1/R2.

## Papers not reused

The arXiv PDFs in the repository root (`2407.04620v4.pdf` etc.) are
downloaded background reading, **not** project artifacts; none of their
figures or text is redistributed.

## Claim-level attribution

Every factual claim is cross-linked in `audit/scientific_claim_audit.csv`
and `research/bdh/evidence_ledger.csv` (per-row source = the specific
paper / repo / our own experiment).