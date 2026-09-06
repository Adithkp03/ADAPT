# D7 — Experimental Design Specification

**Phase 1 | v1.0 2026-09-06**

> Exactly what experiment are we going to run?

---

## 1. Primary research question

> **How does the choice of adaptation substrate affect a model's ability to infer, retain, and transfer a previously unseen task rule?**

Decomposed into Acquire / Retain / Transfer.

## 2. Formal task definition

Every episode:
```
T = (R, D, Q, Y)
R: hidden rule
D = {(x_i,y_i)}_{i=1..k}: demonstrations (k = N_D)
Q: novel query x_q
Y = R(Q): exact ground truth
```
Model sees (D,Q), evaluator knows (R,Y). No leakage.

Difficulty controls:
```
N_D = demonstration count
C_R = rule complexity
d_s = state dimension / capacity
K   = adaptation steps (for param TTA or latent reasoning)
I   = interference (second task B)
eps = noise
```

## 3. Independent variables (learner controls)

| Variable | Symbol | Range | Scientific meaning |
|----------|--------|-------|--------------------|
| Demonstrations | N_D | 1..8 | evidence amount |
| Rule complexity | C_R | 1..5 tiers | task difficulty |
| State capacity | d_s | 8,32,128 | memory capacity |
| Adaptation steps | K | 0..16 | inference-time compute |
| Interference | I | none / B task | stability-plasticity |
| Noise | epsilon | 0..0.2 | robustness |

Each slider maps to one real variable (Pathway requirement).

## 4. Dependent variables

- **Accuracy** A = correct / total (exact match for symbolic/ARC, tolerance for regression)
- **Adaptation gain** G = A_adapted - A_baseline
- **Retention** R_A = A(A after B)
- **Delta_theta** = ||theta_after - theta_before||_2
- **Delta_s** = ||s_after - s_before||_2
- **Latency** ms per episode, plus FLOPs approx
- **State similarity** sim(s_A, s_B) for interference analysis

## 5. Baselines (minimum set)

| ID | Name | Equation | Delta_theta | Delta_s |
|----|------|----------|-------------|---------|
| B0 | Oracle | y=R(Q) | — | — | ceiling |
| B1 | Frozen | y=f_theta(Q) no D | 0 | 0 |
| B2 | Context / ICL | y=f_theta(D,Q) frozen | 0 | computation only |
| B3 | Param TTA | theta_{t+1}=theta_t - eta grad L_D | >0 | 0* |
| B4 | Recurrent state | s_t=F(s_{t-1},x_t), theta fixed | 0 | >0 |
| B5 | Learned-state TTT (optional) | S_t <- S - eta grad L_t(S) | 0 | >0 (learned) |

*Param TTA may also have transient state but measured theta is key.

## 6. Task suite (incremental, do not start with ARC)

### Tier 1 — Linear regression
y = a x + b, new (a,b) per episode. Calibration; optimal solution known.

### Tier 2 — Nonlinear
y = f(x) from controlled family (polynomial, piecewise). Tests beyond linear fitting.

### Tier 3 — Symbolic transformations
Input: A B C -> Output: B C D etc., per-task mapping. Intuitive "new rule".

### Tier 4 — Compositional
R = R1 o R2 (reverse + offset + conditional). Tunable complexity.

### Tier 5 — ARC-like grids
Input grid -> output grid, hidden transformation. Frontier connection; used for BDH-CQ validation.

For each family: meta-train distribution vs adaptation (unseen) vs eval (held-out combos). Never memorize eval generator.

## 7. Experiment suite (six flagship experiments)

### E1 — Teach the Model a New Rule (flagship)
Flow: Generate -> D (3 examples) -> Frozen baseline -> Adaptation (chosen substrate) -> Query -> Ground truth -> What changed? (Delta_theta vs Delta_s). This is the 60-second experience.

### E2 — Adaptation capacity: N_D sweep
Plot Accuracy(N_D). Hypothesis H1: more demos improve to saturation.

### E3 — State capacity: d_s sweep
Plot Accuracy(d_s) and Retention(d_s). H2: larger state helps on complex tasks (from meta-learning literature — state bottleneck).

### E4 — Adaptation compute: K sweep
Plot Accuracy(K) vs Latency(K). H3: more steps helps but costs; links to inference-time scaling and BDH-CQ effort.

### E5 — Interference: A -> B -> A
Measure Retention_A. H5: finite memory -> interference trade-off. Core failure experiment.

### E6 — Conflicting evidence
Demonstrations support competing rules; control conflict level. Tests robustness/ambiguity.

### E7 — Novel-task transfer
New family not in tutorial; learner predicts best substrate, runs. Tests transfer, not recognition.

## 8. Ablation matrix

| Ablation | Question |
|----------|----------|
| No adaptation | Base knowledge? |
| Context only | What can conditioning do? |
| Param update | What does explicit TTA buy? |
| State update | What can recurrent adaptation do? |
| State size | Capacity? |
| N_D | Evidence amount? |
| K | Compute? |
| Interference | Stability? |
| Noise | Robustness? |

## 9. Hypotheses (pre-registered)

- H1: More demonstrations generally improve adaptation to saturation.
- H2: Increasing state capacity improves adaptation on sufficiently complex tasks.
- H3: More adaptation compute can improve but increases latency/cost.
- H4: State-based adaptation can acquire task-specific behavior without modifying persistent parameters.
- H5: Finite adaptive memory creates interference/retention trade-offs.
- H6: Best substrate depends on task characteristics (no universal winner).

Promote to conclusions only after experiments.

## 10. Statistics & reproducibility

- Config-driven: yaml defines task_family, model, adaptation, N_D, d_s, K, noise, seed
- Single command: `python run_experiment.py configs/exp_001.yaml`
- Record: experiment_id, git_commit, config_hash, seed, model_version, task_generator_version, hardware, timing
- Determinism: Generator(seed)=same task; ID = H(code,config,seed,model)
- N >=100 episodes/condition (500 for final report), 95% CI, bootstrap/Wilson
- Versioned outputs under experiments/outputs/<id>/

## 11. Live / precomputed / synthetic / illustrative boundaries

- LIVE: small experiments (task gen, adaptation, prediction, metrics) — must be real computation
- PRECOMPUTED: large sweeps, expensive benchmarks — clearly labeled, with provenance (exp ID, commit, seed)
- SYNTHETIC: generated task distributions — labeled as synthetic
- ILLUSTRATIVE: architecture diagrams — labeled as illustrative, not claimed as measurement

UI must visibly tag each visualization (Pathway honesty requirement).

## 12. Ground truth discipline

Every chart shows truth beside estimate (model prediction vs Y). No human judging.

## 13. Exit gate Phase 2

Same task, same seed, different adaptation strategies -> results reproducibly differ (Delta_theta/Delta_s and accuracy diverge as predicted).
