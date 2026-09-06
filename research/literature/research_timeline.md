# Research Timeline — ADAPT (Phase 1)

**Purpose:** Show progression, not isolated papers.

## Timeline

### 2020 — Test-Time Training introduced (Sun et al.)
Self-supervised loss at test time -> param update for distribution shift. Establishes TTT paradigm.

### 2023 — Transformer / ICL as implicit optimization
- von Oswald et al.: single linear self-attention layer <-> gradient descent for regression (controlled). Establishes: learning-like behavior without param update.
- Garg et al., Li et al.: formalize ICL as learned algorithm hypothesis construction.

### 2024 — TTT in language models (Hardt & Sun)
Test-time fine-tuning on retrieved neighbors; improvements across LM tasks. Establishes: explicit inference-time param adaptation can be useful.

### 2025 — TTT for few-shot reasoning (Akyürek et al., ICML)
Temporary param updates on ARC/BBH; 6x over fine-tuned baselines, 53% ARC val (8B), 61.9% with program synthesis. Establishes: explicit optimization helps novel structure.

### 2025 — Learned expressive states (Sun et al., TTT-Linear/MLP, ICML)
Hidden state is a learned model; update via self-supervised step. 125M-1.3B, strong long-context vs Transformer/Mamba. Establishes: substrate can be learnable state, not just weights.

### 2025 — Long-context as compression
TTT-E2E: compress context into weights via next-token prediction at test time; constant latency claim (their setup). Titans/ATLAS: learned long-term memory.

### 2025 — BDH (Pathway)
Scale-free graph, sparse positive activations, Hebbian working memory, synaptic state sigma. Brain-inspired Post-Transformer.

### 2026 — BDH-CQ (Pathway)
ICL + recurrent latent reasoning: inference inputs continuously update recurrent memory, query solved via latent iterative computation, no verbal CoT, no param update at inference (as described). 150M, 29.5% pass@2 ARC-AGI-1 @ $0.0007/task (computed cost, specific setup — not general cost).

## What this gives us

One axis: where adaptation lives (context -> fast memory -> state -> weights -> learned state -> synaptic/recurrent). Each advance adds a point on that axis with distinct cost/capacity/persistence.

## Primary-source protocol (per phase1.md)

For each paper extract: abstract, introduction, method (what mathematically changes), algorithm (what executes at inference), experimental setup, results, ablations, limitations, evidence type.
