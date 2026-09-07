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
`test_bdh_audit_*` in tests/test_phase4.py (string scan over web/ +
server render paths).
