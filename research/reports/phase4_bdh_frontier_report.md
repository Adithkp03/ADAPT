# D4.11 — Phase 4 BDH / Frontier Research Report

## 1. Research question

When a model adapts at inference time, where is task-specific information
acquired and stored — and do frontier Post-Transformer architectures
(BDH, BDH-CQ) make the same substrate choice our controlled experiments
isolate? (Central claim unchanged from Phase 2; Phase 4 tests its
frontier connection.)

## 2. BDH architecture

Scale-free network of locally interacting neuron particles;
excitatory/inhibitory dynamics; GPU-friendly state-space formulation;
sparse positive activations; Transformer-like scaling with GPT-2-scale
parity at 10M–1B (dossier D4.1 §§1–2; README-verified).

## 3. BDH memory

Transient synaptic state σ via Hebbian/outer-product updates (round
4l+1); rounds 4l (read), 4l+2 (gated readout), 4l+3 (state update);
X/A/Y fast, σ slow; sparsity emerges on predictable input (Equations
§4; dossier §4). Lifetime = decay/interference window.

## 4. BDH-CQ architecture

ICL inputs → continuous recurrent-memory updates → query → iterative
latent computation × K → answer; no verbal CoT; no inference-time param
updates (abstract; dossier D4.2 §§1–2). Third-party WIP exists
(lucidrains/bdh-cq) — not official.

## 5. Connection to inference-time adaptation

concept_mapping.md: 8 rows, each TOY↔PUBLISHED with explicit
non-identities (§23 mechanism-level only; no merged benchmarks).

## 6. Experimental methodology

Same paired/reset/provenance protocol as Phase 2 (schema v1). New:
frontier_comparison (N=50 acc / N=20 retention, linear) and ARC-like
grid acquisition E1 (n=200). Live + precomputed labeled throughout.

## 7. Reproduced experiments

- R0 static verification (DONE): official BDH baseline structure + bdh-cq
  memory path confirmed as described (reproductions/README).
- R1 live instantiation + forward (DONE, 2026-09-07, **PASS**): official
  BDH baseline forward (1,64)→logits (1,64,256), finite loss; bdh-cq
  wrapper (dim=64) forward ok, 3 layer memories surfaced with
  return_memory=True. NOT a benchmark reproduction. **Recorded failure:**
  the first bdh-cq run failed with `ModuleNotFoundError: No module named
  'einx'`; resolved by installing einx (see R1_results.md + git history,
  retained, not deleted).
- R2 tiny BDH-CQ memory probe (DONE, 2026-09-07, **PASS**): update=True
  vs False both produce max|Δmemory|=0 (stateless forward for random
  init); discriminant = frozen path deterministic, update flag threads
  through the memory path without error. TOY_EXPERIMENT on third-party
  code; no learned-memory-content claim.
- E1 ARC-like: frozen 0.0 vs adapters 1.0 (n=200, CI excludes overlap,
  mcnemar_p≈1e-60) — clean acquisition on a held-out rule pool
  ({shift_color}); labeled CONTROLLED_TOY, proxy, not ARC-AGI.
- D4.7: gain↔retention trade-off measured (state/context gain +0.98,
  retention ≤0.15; learned trio honest 0.08–0.40).

## 8. Non-reproduced / official-only results

97.4% Sudoku (internal-only scope), BDH-CQ 150M point (config-scoped
report), BDH-CQ training/effort body details. All cited, none claimed
as ours; ledger marks them PUBLISHED/OFFICIAL.

## 9. Comparative analysis

frontier_comparison.md: shared transient memory ⇒ shared trade-offs
(gain vs retention; cost vs accuracy). Ours measured; frontier reported.
No cross-evaluation accuracy sentence exists anywhere in the study.

## 10. Limitations

scientific_limitations.md (8 items) + §52 failure modes: learned trio
underperforms hand-designed state (kept, not hidden); single-episode
interference is visceral not statistical; d_s is a proxy; E8 weight on
swap/nullmean only.

Reproduction-specific limitations (D4.6, honest):
- R1/R2 are **not** benchmark reproductions: R1 is a shapes-flow/finiteness
  forward on random ids (official baseline) + third-party WIP forward;
  R2 is a synthetic memory-switch probe on third-party code. Neither
  validates learned behavior, accuracy, or the 150M/29.5% point.
- The bdh-cq forward is stateless for random init in this probe, so R2
  cannot demonstrate memory *content* change — it only confirms the
  update flag threads through deterministically.
- The 97.4% Sudoku and BDH-CQ 150M/29.5% results were **not** reproduced
  (public repo baseline does not reproduce 97.4% per its own README;
  150M requires frontier weights/compute). These remain
  PUBLISHED/OFFICIAL in the ledger with `our_reproduction = no`.

## 11. Educational implications

Learner now distinguishes 6 mechanisms (D4.9; §49 target); BDH bridge
carries LO6 with equation stepper + η synapse card + order quiz, all
evidence-labeled. Exit-gate experiment (§55) runs end-to-end live.
Educational-validation instruments (equation stepper, BDH-CQ order quiz,
mechanism distinction, transfer challenge) are live and wired into the
D3.11 analysis; actual 8–15 participant learner study is pending and
honestly recorded (no learning-gain claim without anonymized session
data attached).

## 12. Conclusions (frozen post-reproduction, 2026-09-07)

These conclusions are frozen as of the date R1/R2 completed; they do not
change with later phases unless the evidence changes, which would be
reported as a revision, not silently:

1. **Substrate choice is the answer to "where does the new rule go?":**
   across our controlled toy families, inference-time task information
   lives in an evolving adaptive state (Δθ=0, Δs≠0 for state/context)
   or in parameters (param TTA); frozen attains nothing on held-out rules
   (E1: frozen 0.0 vs adapters 1.0).
2. **Frontier architectures make the same broad design choice:**
   BDH stores working memory in transient synaptic σ (4l+1 Hebbian
   write); BDH-CQ updates recurrent memory during inference with no
   parameter update. This is a mechanism-level connection (concept_mapping,
   D4.3), never an identity or a merged-benchmark comparison (D4.7).
3. **Shared transient memory ⇒ shared trade-offs:** adaptation gain and
   retention trade off in our measurements; the frontier side reports
   related cost/accuracy and interference trade-offs. Ours measured,
   theirs reported; never merged into one accuracy table.
4. **Reproduction scope is narrow and honest:** we reproduced construction
   + forward (R1) and a synthetic memory-switch probe (R2) on pinned
   commits; we did not reproduce 97.4% or 29.5% (recorded, not hidden).
5. **Every BDH/BDH-CQ number is evidence-classified** (evidence_ledger,
   D4.5 + D4.10 audit); no UI overclaim survives the banned-wording scan.
