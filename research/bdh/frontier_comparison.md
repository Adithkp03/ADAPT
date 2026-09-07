# D4.7 — Frontier Comparison Study (mechanism level, §23)

**Data:** `research/bdh/frontier_comparison.csv` (linear, test split,
N=50 accuracy / N=20 A→B→A retention, seed bases 0 / 1000).
**Figure:** `research/experiments/figures/fig8_frontier_tradeoff.png`
(gain vs retention; cost vs accuracy). Script:
`experiments/frontier_comparison.py`.

## 1. OUR measurements (same task distribution — directly comparable)

| Mechanism | acc | gain vs frozen | retention A | latency | Δθ | Δs |
|---|---|---|---|---|---|---|
| frozen | 0.020 | 0.000 | 1.000* | 0.00ms | 0 | 0 |
| context | 1.000 | +0.980 | 0.150 | 0.04ms | 0 | 0 |
| param_tta (K=8) | 0.320 | +0.300 | 0.000 | 0.13ms | 2.14 | 0 |
| state | 1.000 | +0.980 | 0.100 | 0.01ms | 0 | 69.13 |
| ttt_state | 0.320 | +0.300 | 0.000 | 0.10ms | 0 | 2.14 |
| learned_state | 0.100 | +0.080 | 0.000 | 0.07ms | 0 | 2.38 |
| learned_tta | 0.240 | +0.220 | 0.143 | 0.39ms | 2.40 | 0 |
| learned_ttt | 0.420 | +0.400 | 0.000 | 0.12ms | 0 | 3.48 |

\* Frozen "retention" is trivial (nothing adapts, nothing is forgotten).
Honest negatives kept: the learned trio underperforms hand-designed
state on linear — meta-training scope limits, not hidden.

Reading: adaptation gain and retention trade off — the two perfect-gain
methods retain ≤0.15. Retention is the price of a shared transient
substrate, for parameters (θ_B overwrites θ_A) and states alike.

## 2. Published frontier rows (NOT the same evaluation — never merged)

| System | Reported point | Source |
|---|---|---|
| BDH (internal) | 97.4% Sudoku Extreme, no CoT/tools; GPT-2-scale parity 10M–1B | README (OFFICIAL_REPORT, internal scope) |
| BDH-CQ (150M config) | 29.5% pass@2 ARC-AGI-1 @ $0.0007/task; SOTA cost-efficiency point | abstract (PUBLISHED_EMPIRICAL, config-scoped) |

No "ours vs theirs" accuracy sentence exists in this study — different
models, tasks, regimes (§23). The comparison lives one level up: BOTH
our state substrate AND BDH/BDH-CQ put task information in evolving
memory while parameters stay fixed, and BOTH pay interference/cost
trade-offs (ours measured, theirs reported). That is the mechanism-level
claim, and the only one made.
