# D3.9 / D3.11 — Evaluation Plan (question → LO mapping, metrics, rubrics)

## 1. Learning objectives

| LO | Statement |
|---|---|
| LO1 | Adaptation can live outside persistent weights (context / transient state) |
| LO2 | Parameter TTA changes θ; state adaptation leaves θ fixed (Δθ = 0, Δs ≠ 0) |
| LO3 | State is necessary for the adapted behavior (perturb/restore causality) |
| LO4 | Adaptive memory has capacity limits (bottleneck cliff) |
| LO5 | Sequential tasks interfere (A→B→A retention loss) |
| LO6 | BDH/BDH-CQ reuse the same design idea at frontier scale |
| LO7 | Test-time compute buys accuracy at latency cost, non-monotonically |

## 2. Pre-test → LO (5 items, `PRE` in web/app.js)

| Q | Concept | LO |
|---|---|---|
| 1. Must persistent weights change to learn a new task? | weights-not-required | LO1 |
| 2. A→B sequence, what happens to A? | interference expectation | LO5 |
| 3. Inference-time gradient update changes… | TTA mechanism | LO2 |
| 4. Tightest capacity limit? | bottleneck | LO4 |
| 5. In BDH, working memory lives in… | synaptic state σ | LO6 |

## 3. Post-test → LO (5 items, `POST` — structurally similar, non-identical)

| Q | Concept | LO |
|---|---|---|
| 1. Where can new-task info live without changing weights? | weights-not-required (transfer wording) | LO1 |
| 2. A→B→A accuracy drop is… | interference naming | LO5 |
| 3. Δθ = 0, Δs > 0 means… | delta reading | LO2 |
| 4. Shrinking d_s below sufficient statistics… | capacity cliff | LO7* |
| 5. BDH-CQ solves queries by… | latent computation | LO6 |

\* Q4 doubles as the LO7 probe (compute/capacity trade-off); LO3 is probed
in situ by the mechanism quizzes, LO4 by the N_D/bottleneck predictions.
Post items test the same LO through a new surface (read a delta, name a
drop) — never the same sentence reworded.

## 4. In-situ scored predictions (behavioral, logged with timestamps)

| Event | Correct | LO |
|---|---|---|
| `nd_predict` (N_D direction) | improve | LO4 |
| `ret_predict` (retention) | degrade | LO5 |
| `flagship_run` numeric | \|mine − truth\| ≤ 0.5 | LO1 |
| `mech_quiz` (what changed) | Adaptive state | LO2/LO3 |
| `bdh_quiz` (CQ order) | demos → memory → query → latent → answer | LO6 |
| `challenge_run` pick | winner on dealt seed | transfer, all |

## 5. Misconception rubric (M1–M5)

M1 learning ⇒ weight change · M2 state ≡ weights · M3 recurrence ≡ TTT ·
M4 more compute always better · M5 more dims = more concepts.
Pre/post + explanation coded per-misconception (held / shifted / absent);
see `docs/evaluation_protocol.md`. Free-text explanation is scored by hand
against: (a) names state (not weights) as storage, (b) describes
interference as overwrite/competition. No LLM grading.

## 6. Metrics

- `LearningGain = Post − Pre` (per LO and total).
- Normalized gain `g = (post − pre) / (max − pre)` (undefined when pre = max → report separately).
- Transfer score (challenge pick correct + explanation rubric 0–2).
- Time-to-first-run, time-to-first-correct-mechanism (from event log).
- Usability failures coded to §42 checklist (find interaction, control
  meaning, live-ness, what-changed, pred-vs-truth, completion).
