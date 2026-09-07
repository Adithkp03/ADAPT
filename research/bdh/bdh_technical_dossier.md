# D4.1 — BDH Technical Dossier

**Version:** 2.0 (Phase 4 expansion of v1.0) | **Date:** 2026-09-07
**Primary source:** A. Kosowski, P. Uznański, J. Chorowski, Z. Stamirowska,
M. Bartoszkiewicz, *The Dragon Hatchling: The Missing Link between the
Transformer and Models of the Brain*, arXiv:2509.26507 (2025).
**Official code:** https://github.com/pathwaycom/bdh (baseline variant).
**Official supplement:** Pathway, *The Equations of Reasoning*
(https://pathway.com/research/the-equations-of-reasoning).

Supersedes the v1.0 sketch by adding: exact authorship/claims with
locations, the verbatim 4-round cycle, reproduction-relevant repo facts,
and the Sudoku scoping correction. Every row carries an evidence label
(FORMAL / PUBLISHED_EMPIRICAL / OFFICIAL_REPORT / ILLUSTRATION).

## 1. What BDH is (and is not)

**Is** (official README + paper):
- Biologically inspired LLM architecture bridging deep learning and
  neuroscience (PUBLISHED_EMPIRICAL framing; README §Overview).
- Scale-free, locally interacting network of neuron particles with
  excitatory/inhibitory dynamics (README Key properties).
- Working memory via synaptic plasticity / Hebbian learning, displaying
  monosemanticity (README Key properties).
- GPU-friendly state-space formulation for efficient implementation
  (README Key properties).
- Sparse, positive, interpretable activations (README Key properties).
- Matches GPT-2–scale Transformers on language/translation at equivalent
  scales (10M–1B) (OFFICIAL_REPORT; README §Overview).

**Is not:**
- A Mamba-style SSM. The brief warns against this classification; the
  correct wording is **"BDH has a GPU-friendly state-space formulation"**
  (README). (The Equations page likens *one step* — the 4l+1 write — to
  "a standard state-space model (SSM) memory write"; quote with that
  scope, never as an architecture identity.)
- Generic gradient TTT (memory mechanism differs: Hebbian synaptic
  updates, not loss-driven parameter optimization).
- Standard attention-only Transformer (attention *emerges* from
  neuron-level graph interactions; README §Relation to Transformers).
- Our toy recurrent model (controlled analogue, never official).

## 2. Architecture decomposition (A–H per phase4 §4)

- **A. Neural state:** per-neuron evolving activity; fast pulse-like
  variables X, A, Y on neurons (Equations page §4; FORMAL within their
  axiomatics, ILLUSTRATION in our UI).
- **B. Graph connectivity:** scale-free topology, few hubs / many
  low-degree nodes, heavy-tailed degrees (paper + README).
- **C. Synaptic state σ:** edges carry the slower synaptic variable —
  the transient memory substrate, "analogous to the road map itself"
  (Equations page §4; urban-network analogy).
- **D. Memory update:** round 4l+1 reweights σ with the outer (Hebbian)
  product of X and Y (Equations page §4). Educational form:
  σ ← σ + η·X·Yᵀ, always labeled *simplified educational form*.
- **E. Activity propagation:** local pairwise rules (single-node compute
  or single-edge exchange) yield macroscopic reasoning — "bridge our
  axiomatics needs" via distributed-computation theory (Equations §5.1).
- **F. Read/write:** external inputs enter as activity; round 4l+2 reads
  Y from readout A gated by context X (A×X gating); round 4l+3 finalizes
  X, closing the loop.
- **G. Sparsity:** Y sparse and positive at implementation level;
  BDH-GPU neurons less active on predictable input, most active on novel
  sequences; sparsity measured by non-zero counts (Equations §4,
  citing paper Fig. 14).
- **H. Scale-free rationale:** biological connectivity mimicry with
  Transformer-like scaling laws retained (README §§Overview, Scaling).

## 3. Memory precisely

Stored in **transient synaptic state σ**, not trained parameters. Lifetime
= synaptic decay / interference window. Our mapping: STATE s_t ↔ σ;
WEIGHTS θ ↔ trained graph parameters.

## 4. The 4-round cycle (verbatim structure, educational rendering)

Per the Equations page §4 ("In plain words"):
1. **Round 4l — memory read:** update the accumulator from current
   beliefs + new inputs + causal relations in σ (modus ponens).
2. **Round 4l+1 — memory write:** reweight σ with the outer/Hebbian
   product of X and Y.
3. **Round 4l+2 — gated readout:** Y from readout A for context-relevant
   neurons (A gated by X); Y sparse and positive.
4. **Round 4l+3 — state update:** final update of X, loop closes.
Plus the implementability claim: the GPU-efficient state-space
architecture compiles into a local graph-dynamical kernel with preserved
asymptotic size, admitting a Hebbian spiking implementation (FORMAL —
proved results per the Equations page §5.1; we report, not re-prove).

## 5. Sudoku scoping correction (D4.6-relevant)

- Claim: internal BDH reaches **97.4% on ~250k Sudoku Extreme puzzles**,
  no CoT/backtracking/tools; leading LLMs (O3-mini, DeepSeek R1,
  Claude 3.7 8K) ~0% (README §Sudoku; LLM scores sourced to
  arXiv:2506.21734). Evidence: OFFICIAL_REPORT (internal data).
- **The open-source repo is the baseline paper variant and does NOT
  reproduce 97.4% out of the box** (README note, verbatim scope).
  Allowed wording: "reported for Pathway's internal BDH implementation".
  NEVER: "we reproduced 97.4%".

## 6. Reproduction surface (repo facts, verified 2026-09-07)

- Deps: `torch numpy requests` (requirements.txt). Demo: `pip install -r
  requirements.txt; python train.py` (toy dataset; repo thanks Karpathy's
  nanoGPT + tiny Shakespeare). Community ports exist (Burn, MLX) —
  third-party, not official.
- D4.6 attempt log lives in `research/bdh/reproductions/`; failures are
  recorded, never hidden.

## 7. Evidence status (see also evidence_ledger.csv)

All §6-v1.0 rows retained; added: GPT-2-scale parity (OFFICIAL_REPORT),
4-round structure (OFFICIAL_REPORT via Equations page), Sudoku numbers
(OFFICIAL_REPORT, internal-only scope), repo-does-not-reproduce-97.4
(OFFICIAL_REPORT, verbatim README note).
