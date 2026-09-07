# D4.10 — BDH Scientific Integrity Audit (every UI sentence → category)

Categories: Published fact / Our experimental result / Interpretation /
Illustration / Hypothesis. Source for each: evidence_ledger.csv row or
engine function. Audit date: 2026-09-07.

| UI sentence (web/) | Category | Support |
|---|---|---|
| "small, interpretable toy systems… NOT a frontier LM, ARC-AGI, or official BDH software" (header) | Published fact + Our scope | dossiers v2; limitations doc |
| "Scale-free graph of locally interacting neuron particles" | Published fact | README Overview + paper; ledger row 1 |
| "Working memory in synaptic state σ via Hebbian updates" | Published fact | README key properties + paper; ledger row 2 |
| "Sparse positive activations" | Published fact | paper + Equations §4; ledger row 4 |
| "Sources: BDH paper (arXiv 2025), Equations of Reasoning, pathwaycom/bdh" | Published fact | full citations in bdh_technical_dossier |
| "Educational implementation (not official BDH code)" (η panel) | Illustration (labeled) | ledger: NEVER-claim row; computes η·1·1 only |
| "0.14 + η demo scalars… magnitude only, no semantics" | Illustration (labeled) | no engine/paper number; arithmetic only |
| EOR stepper rounds 4l–4l+3 | Published fact (structure) + Illustration (rendering) | Equations page §4 verbatim structure; labeled "not a simulation" |
| "150M, 29.5% pass@2 … $0.0007/task (do not generalize…)" | Published fact (config-scoped) | abstract verbatim; ledger row 13 |
| "no verbal chain-of-thought … parameters static during inference" | Published fact | abstract; ledger rows 11–12 |
| Concept-map rows (s↔σ, D↔writes, K↔effort, A→B→A↔window) | Interpretation (labeled analogue) | concept_mapping.md; "same design idea", never identity |
| "The rule was acquired…" flagship copy | Our experimental result | run_episode Δθ=0/Δs≠0, this seed |
| "Holdout: …" lines | Our experimental result + Published scope | _holdout() per family; split=test |
| "Single-episode result — population claim lives in sweeps" | Our scope (anti-overclaim) | E2–E6 precomputed + live sweeps |
| BDH-CQ order quiz + "memory evolves, parameters static" | Published fact | abstract timeline; dossier §2 |
| Challenge "honest limits (single-op vote, shift-only read…)" | Our experimental result (limits) | challenge_run output; limitations doc |

## Banned-wording scan (all PASS — none present in web/)

"BDH is just (another) Mamba/SSM" · "BDH-CQ is TTT" (blanket) · "we
reproduced 97.4%" · "state stores the rule" (unqualified) · "Step N
means thinking about X" · any unscoped "29.5%". Enforced by
`test_d410_audit_and_banned_wording` (string scan over web/ + server
render paths).

## Evidence-classification coverage (every BDH/BDH-CQ number has a label)

Every BDH/BDH-CQ number shown in the UI is cross-banded by
`research/bdh/evidence_ledger.csv` (PASS, verified 2026-09-07):
- "150M / 29.5% pass@2 / $0.0007/task" → PUBLISHED_RESULT + ILLUSTRATIVE,
  ledger row 13 (config-scoped).
- "97.4% Sudoku Extreme" → OFFICIAL_REPORT (internal-only),
  ledger row 9; repro-does-not-97.4 → row 10.
- "4-round cycle / σ update" → OFFICIAL_REPORT (+ ILLUSTRATIVE for the
  η demo), ledger row 8.
- Our Δθ/Δs state result → TOY_EXPERIMENT, ledger row 17.
- "BDH-CQ order quiz" and "memory evolves, parameters static" →
  PUBLISHED_RESULT, ledger rows 11–13.
Every number the audit lists carries its ledger row or engine function as
the Support column; no UI BDH/BDH-CQ number is unclassified.

## Reproduction numbers have evidence classification (D4.6-D4.10 cross-check)

The R1/R2 reproduction outputs (`research/bdh/reproductions/R1_results.md`,
`R2_results.md`) are evidence-labeled: R1 = OFFICIAL baseline structure +
third-party WIP forward (NOT a benchmark reproduction); R2 = TOY_EXPERIMENT
on third-party code, no learned-memory-content claim. The `evidence_ledger.csv`
`our_reproduction` column is "no" for every PUBLISHED/OFFICIAL row (we did
not reproduce 97.4% or 29.5%), and "yes (controlled)" only for our
TOY_EXPERIMENT rows — an explicit, ledger-wide rule that no
published-number reproduction is claimed.
