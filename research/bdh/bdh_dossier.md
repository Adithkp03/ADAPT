# D4 — BDH Technical Dossier

**Version:** 1.0 | **Date:** 2026-09-06 | **Status:** Draft for Phase 1 review

> This dossier is a technical reading document, not a marketing summary. Every row must cite primary source. Labels: FORMAL / PUBLISHED_EMPIRICAL / OFFICIAL_REPORT / INDEPENDENT_REPRO / OUR_REPRO / TOY_EXPERIMENT / ILLUSTRATION

---

## 1. What BDH is (and is not)

**Is:**
- Brain-inspired Post-Transformer architecture
- Scale-free graph of locally interacting neuron particles
- GPU-friendly formulation of that graph
- Working memory via synaptic plasticity / Hebbian updates
- Sparse positive activations
- Heavy-tailed / scale-free connectivity

**Is not:**
- Mamba-style SSM (explicitly distinct — Pathway warning)
- Generic TTT (not automatically; memory mechanism differs)
- Standard attention-only Transformer
- Our toy recurrent model (we are an analogue, not official)

Sources: BDH paper (arXiv 2025), Pathway "Equations of Reasoning", public BDH repo https://github.com/pathwaycom/bdh

## 2. Architecture decomposition

### A. Neural state
Per-neuron evolving state vector(s). Paper defines neuron particles with state variables updated via local interactions. Detail: see equations.md (to be filled with verbatim equations from paper).

### B. Graph connectivity
Scale-free network topology: few hubs, many low-degree nodes; heavy-tailed degree distribution. Implication: efficient sparse communication vs dense all-to-all attention.

### C. Synaptic state sigma
Edges carry state sigma_{ij}. Not just weights — carries transient memory.

### D. Memory update
Core: Hebbian / outer-product
```
sigma_{t+1} = sigma_t + eta * X_t Y_t^T   (educational simplification)
```
Verbatim published form to be copied into equations.md with section reference. Evidence: BDH reports concept-related synaptic strengthening (PUBLISHED_EMPIRICAL).

### E. Activity propagation
Local interactions propagate globally via iterative dynamics; not single attention pass.

### F. Read/write
External tokens enter as activity patterns; outputs read via gated readout from current state + synaptic state.

### G. Sparsity
Sparse positive activations -> interpretability (monosemantic synapses) claim.

### H. Graph structure rationale
Scale-free -> robustness, efficiency, biological inspiration.

## 3. Memory precisely

What changes when information is stored?
- **Synaptic state sigma** (transient)
- NOT persistent trained parameters (those are slow weights)
- Working memory lifetime = synaptic decay / interference window

Compare to our taxonomy:
- Our STATE s_t  <-->  BDH synaptic sigma
- Our WEIGHTS theta <--> BDH trained graph parameters

## 4. Interpretability

Claims to verify:
- Sparse positive activations enable monosemantic synapses?
- State interpretability via synaptic inspection?
Evidence type: PUBLISHED_EMPIRICAL (paper reports); INDEPENDENT_REPRO = pending.

## 5. Computational formulation (placeholder for Equations Lab)

Pathway "Equations of Reasoning" describes 4-round cycle:
1. Communication / memory read
2. Synaptic-state update (Hebbian/outer)
3. Gated readout
4. Neuronal state update

Learner steps through rounds; equation visible and labeled. See research/bdh/equations.md.

## 6. Evidence status table

| Claim | Source | Section | Evidence type | Allowed wording |
|-------|--------|---------|---------------|-----------------|
| BDH uses synaptic plasticity for working memory | BDH paper | §Memory | PUBLISHED_EMPIRICAL | "BDH paper describes working memory as relying on synaptic plasticity with Hebbian learning" |
| Concept-related synaptic strengthening | BDH paper | Results | PUBLISHED_EMPIRICAL | "Authors report concept-related synaptic strengthening" |
| Sparse positive activations | BDH paper | Arch | PUBLISHED_EMPIRICAL | "Paper reports sparse positive activations" |
| Scale-free graph | BDH paper + repo | Arch | PUBLISHED_EMPIRICAL | "Paper describes scale-free network topology" |
| GPU-friendly formulation | BDH paper/repo | Impl | OFFICIAL_REPORT | "Authors describe GPU-oriented formulation" |
| Our toy == official BDH | — | — | — | NEVER claim |

## 7. What we will NOT do

- Claim official BDH live reproduction without actually running repo at documented commit.
- Generalize BDH-CQ 29.5% / $0.0007 to all inference.
- Conflate BDH synaptic memory with generic gradient TTT.

## 8. Next steps (Phase 4)

- Fill equations.md verbatim from paper
- Clone official BDH repo at pinned commit; run basic execution (D4.6)
- Build evidence_ledger.csv

## 9. References

- BDH arXiv 2025 (primary)
- Pathway Equations of Reasoning (official supplement)
- https://github.com/pathwaycom/bdh (code)
