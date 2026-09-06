# Evidence Audit — Phase 1 closure pass

**Date:** 2026-09-06

## Fixes applied in this pass
- [x] All placeholder URLs replaced (250x.xxxxx / 250x.bdh / 250x.titans removed). Verify: no `250x` remains in evidence_matrix.csv.
- [x] One row = one paper (Garg and Li split; Titans and ATLAS split; von Oswald separate).
- [x] Recency class column added: Recent (2022-2026, counts toward Pathway 3-paper requirement) vs Historical/foundational (2020-2021, background only).
- [x] BDH source corrected to arXiv:2509.26507 (Dragon Hatchling); BDH-CQ confirmed arXiv:2608.09888; Titans 2501.00663; ATLAS 2505.23735; TTT-E2E 2512.23675; Akyurek 2411.07279; Hardt&Sun 2305.18466.
- [x] Akyurek result kept as setup-specific (53.0% / 61.9% with synthesis, 8B, vs compared baselines) — not universal.
- [x] BDH-CQ 29.5% pass@2 @ $0.0007 scoped to 150M config, computed cost, ARC-AGI-1 public eval.
- [x] ATLAS/Titans long-context numbers marked setup-specific.

## Remaining for Phase 2 freeze
- [ ] Section/table-level source anchors for each Main Result (Source section/table column).
- [ ] Exact source quote/paraphrase per row.
- [ ] Machine-readable citation IDs + experiment schema (P2).
