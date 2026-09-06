# Phase 1 Completion Checklist

Per phase1.md §1 deliverable map (9 deliverables)

- [x] D1 Scientific Scope — research/scope/scientific_scope.md
- [x] D2 Terminology & Concept Map — research/terminology/terminology.md + concept_map.md (pdf export pending mermaid)
- [x] D3 Literature & Evidence Matrix — research/literature/evidence_matrix.csv + research_timeline.md
- [x] D4 BDH / BDH-CQ Dossier — research/bdh/bdh_dossier.md + bdhcq_dossier.md
- [x] D5 Central Claim — research/claim/central_claim.md + falsification_criteria.md
- [x] D6 Learner Spec — research/education/learner_spec.md
- [x] D7 Experimental Design — research/experiments/experimental_design.md + hypotheses.md
- [x] D8 Computational Substrate — research/system/computational_substrate.md
- [x] D9 Go/No-Go — research/phase1/go_no_go.md

Evidence discipline: every claim tagged FORMAL / PUBLISHED_EMPIRICAL / OFFICIAL_REPORT / TOY_EXPERIMENT / ILLUSTRATION (see terminology.md §7, dossiers §6).

Live/Precomputed/Synthetic/Illustrative boundaries: defined in experimental_design.md §11 and computational_substrate.md §7.

Sixty-second test: defined in learner_spec.md §8.

Phase 1 exit question: "What exactly is TTA? Precise phenomenon? Falsifiable claim? Competing mechanisms? Which implemented? Distinguishing experiment? Variables? Ground truth? Failure mode? BDH contribution?" — answered in above docs.

Status: READY FOR REVIEW

## Hardening pass 2026-09-06 (per external review — CONDITIONAL GO)

P0 fixed:
- [x] Placeholder URLs replaced; source_validation.md added
- [x] Go/No-Go -> CONDITIONAL GO (was premature unconditional GO)
- [x] Scope FROZEN vs claim CANDIDATE split explicit
- [x] ICL definition fixed (no single-substrate claim)
- [x] BDH (?) removed -> Dragon Hatchling (BDH)
- [x] E8 causal state-intervention added as primary experiment
- [x] Reset/isolation formalized (reset_and_isolation.md + episode_protocol.md)
- [x] Matrix one-paper-per-row; recency class column added

P1 added:
- [x] assumptions.md, open_questions.md, evidence_audit.md, source_validation.md, terminology_decisions.md
- [x] statistical_analysis_plan.md (paired design, confirmatory vs exploratory, Holm), episode_protocol.md, data_leakage_policy.md
- [x] H5 conditional wording; capacity as operational proxy; 60s as design target; predict-before-inspect flow

Status: PHASE 1 CONDITIONALLY CLOSED — ready for Phase 2 protocol freeze (hash statistical plan + episode protocol + seeds before runs). No serious Phase 2 model code until freeze tag.
