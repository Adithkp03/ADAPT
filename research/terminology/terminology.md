# D2 — Terminology & Concept Map — ADAPT

**Phase:** 1 | **Version:** 1.0 | **Date:** 2026-09-06

This document is normative. Every claim in the artifact must use terms as defined here.

---

## 1. Core equations

### In-Context Learning (frozen)
```
y = f_theta(D, x)
theta' = theta   (no change)
```
Task info via conditioning; computation changes, parameters do not.

### Meta-learning (MAML-style, for contrast)
```
theta'_T = theta - alpha grad L_T(theta)   [inner]
theta <- theta - beta grad sum_T L_T(theta'_T) [outer]
```
Training learns an initialization that adapts fast. Not our inference mechanism, but explains why some models are good ICL learners.

### Parameter-based TTT
```
theta_{t+1} = theta_t - eta grad_{theta} L_D(theta_t)
L_D = (1/k) sum_i loss(f_theta(x_i), y_i)
```

### Recurrent state adaptation
```
s_t = F_theta(s_{t-1}, x_t, y_t)
theta_{t+1}=theta_t
y_hat = G_theta(s_k, Q)
```

### Learned-state TTT (Sun et al. 2025)
```
S_t <- S_{t-1} - eta_t grad_S L_t(S_{t-1})
```
where S itself can be a linear model or MLP — state is computational machinery.

### Fast weights (historical bridge)
Linearized attention <-> fast weight programmer (Schlag et al.):
attention dynamically programs a fast associative memory.

### BDH memory (simplified educational form vs published)
Published pathway describes local cycle: read sigma -> Hebbian update -> gated readout -> state update.
Educational simplification:
```
sigma_{t+1} = sigma_t + eta * X_t Y_t^T
```
Must be labeled as simplification if not verbatim from paper.

### BDH-CQ (inference timeline)
```
demonstrations -> recurrent memory updates (no param update) -> query -> latent recurrent steps K -> answer
```
No inference-time parameter update in described mechanism; effort scales via K.

---

## 2. NOT THE SAME AS — disambiguation table

| Concept | Param update? | Changes during inference? | Stores task info in | Update rule | Example paper |
|---------|---------------|---------------------------|---------------------|-------------|---------------|
| Standard ICL | No | Computation only | Context / attention activations | Conditioning | Garg et al., Li et al. |
| Parameter TTT | Yes | Yes | Parameters theta | Gradient descent | Akyürek et al. 2025, Hardt & Sun 2024 |
| Recurrent-state adaptation | No (theta fixed) | Yes (state) | Hidden state s_t | Learned recurrence F | generic RNN/SSM |
| TTT-Linear / TTT-MLP | State-level learning | Yes | Learned state S | Self-supervised grad on S | Sun et al. 2025 |
| BDH synaptic memory | Not equivalent to generic TTT | Yes | Synaptic state sigma | Hebbian outer-product | BDH paper |
| BDH-CQ | No (params static at inference) | Yes | Recurrent memory | Recurrent update + latent reasoning | BDH-CQ 2026 |

## 3. Term glossary (alphabetical)

- **Adaptation substrate:** where transient task info lives (context/state/weights).
- **ARC (Abstraction & Reasoning Corpus):** few-shot grid-transformation benchmark; input->output demonstrations, hidden rule, exact ground truth.
- **BDH:** Brain-inspired Distributed Hebbian (?) — Pathway frontier architecture: scale-free graph, sparse positive activations, synaptic plasticity/Hebbian memory.
- **BDH-CQ:** BDH variant combining ICL with recurrent latent reasoning; 150M 29.5% pass@2 ARC-AGI-1 @ $0.0007/task (reported, specific setup — do not generalize).
- **Conditioning:** changing output by changing input, not parameters.
- **Demonstration (D):** one (x_i,y_i) example of hidden rule R.
- **Evidence type:** FORMAL / PUBLISHED_EMPIRICAL / OFFICIAL_REPORT / INDEPENDENT_REPRO / OUR_REPRO / TOY_EXPERIMENT / ILLUSTRATION
- **Fast weights:** rapidly changing memory via outer-product writes, often equivalent to linearized attention.
- **Falsifiable claim:** statement with explicit conditions under which it would be shown false (delta metrics).
- **Ground truth (Y):** exact correct output under R.
- **Hebbian update:** sigma <- sigma + eta * pre * post^T (fire together wire together).
- **Interference:** loss of prior task performance after adapting to new task.
- **Latent reasoning:** iterative computation in hidden state without verbal chain-of-thought.
- **Retention:** accuracy on task A after learning task B.
- **State capacity (d_s):** dimensionality / expressivity of adaptive state.
- **TTT (Test-Time Training):** family where inference-time learning objective drives updates (param or state).
- **TTA (Test-Time Adaptation):** umbrella — any inference-time use of test information to change subsequent computation.

## 4. Common misconceptions to correct

- "ICL is not learning; TTT is learning" -> false nuance: von Oswald et al. show linear attention can emulate GD in forward pass without param update.
- "BDH = Mamba/SSM" -> explicitly prohibited (Pathway brief warning).
- "BDH-CQ does full parameter TTT" -> false; paper describes recurrent memory updates, not param updates at inference.
- "Toy model = official BDH" -> never; label as controlled educational analogue.

## 5. Concept map (textual; companion file concept_map.md = diagram source)

```
                        WHERE DOES NEW TASK INFORMATION LIVE?
                                      |
            +---------------------------+---------------------------+
            |                           |                           |
         CONTEXT                      STATE                       WEIGHTS
            |                           |                           |
     retain examples           recurrent hidden state          update parameters
            |                           |                           |
      standard ICL             state-space / TTT-RNN           TTT / TTT-NN
            |                           |                           |
            +---------------------------+---------------------------+
                                      |
                                   HYBRIDS
                                      |
                          context + state / memory + weights
                                      |
                            BDH (synaptic) / BDH-CQ (recurrent+latent)
```

Full visual: see concept_map.pdf (exported from concept_map.md mermaid) — must be generated before Phase 1 review.

## 6. Citations (primary)

- von Oswald et al. 2023 — linear attention <-> GD
- Garg et al., Li et al. — ICL as algorithm learning
- Hardt & Sun 2024 — TTT via retrieved neighbors
- Akyürek et al. 2025 — TTT on ARC
- Sun et al. 2025 — TTT-Linear/MLP (learned state)
- BDH paper 2025 — synaptic plasticity memory
- BDH-CQ 2026 — recurrent memory + latent reasoning
- Schlag et al. — fast weights <-> attention
- Kirsch et al. — meta-learned ICL, state bottleneck

## 7. Audit rule

Search codebase for dangerous terms [learn, memory, reason, understand, adapt, train, latent, synapse, attention] — each occurrence must match this glossary or be reworded with evidence label.
