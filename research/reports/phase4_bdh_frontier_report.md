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

- R0 static verification: official BDH baseline structure + bdh-cq
  memory path confirmed as described (reproductions/README).
- R1/R2 live: pending torch CPU install (recorded on arrival).
- E1 ARC-like: frozen 0.0 vs adapters 1.0 (n=200) — clean acquisition.
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

## 11. Educational implications

Learner now distinguishes 6 mechanisms (D4.9; §49 target); BDH bridge
carries LO6 with equation stepper + η synapse card + order quiz, all
evidence-labeled. Exit-gate experiment (§55) runs end-to-end live.
