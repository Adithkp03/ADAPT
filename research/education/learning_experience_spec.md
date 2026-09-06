# D3.1 — Learning Experience Specification

**Artifact:** AdaptLab (`server.py` + `web/`) | **Learner:** ML-capable student/engineer, new to inference-time adaptation (see `research/education/learner_spec.md`, LO1–LO7)

## Central misconception (target)
“If the model learns a new task, it must have changed its weights.”
Every stage is designed to collide the learner with counterevidence, never to assert the correction up front.

## Learning state machine (one stage each)
0. Unaware → 1. “It learned the task” (flagship run, model ✓) → 2. “Something inside changed” (WHAT CHANGED box: Δθ=0, Δs≠0)
→ 3. “I can see what changed” (mechanism quiz + causal chain toggle) → 4. “I can manipulate it” (N_D slider, strategy switch)
→ 5. “I can predict the effect” (predict-then-run scored: N_D, retention) → 6. “I can make it fail” (bottleneck cliff, noise, A→B→A)
→ 7. “I understand the trade-off” (compute K vs latency, precomputed E3) → 8. “Same design idea in BDH-CQ” (concept map + ordering quiz)
→ 9. “Transfer to a new task” (compositional challenge + free-text explanation).

## Stage → LO → evidence mapping
| Stage | LOs | Learner evidence produced |
|---|---|---|
| Start / pre-test | LO1,2,5,6 | 5 scored predictions (local) |
| Flagship 001 | LO1,2,3 | own prediction vs model vs truth; mechanism answer |
| Manipulate 002 | LO4 | N_D prediction; live sweep chart |
| Tradeoffs 003/4/6 | LO4,7 | bottleneck + compute + noise sweeps |
| Interfere 005 + E8 | LO5,3 | retention prediction; perturb/restore table |
| BDH bridge | LO6 | timeline ordering answer; η→‖Δσ‖ demo |
| Challenge | LO1–7 | mechanism pick on unseen family; 2–3 sentence explanation |
| Lab + precomputed | all | free experiment + vetted research summaries |
| Results / post-test | all | 5 scored questions; session JSON export |

## Non-goals
No Transformer ICL, no LLM TTT, no ARC-AGI claims, no official BDH code. The lab teaches *mechanics of adaptation*; the bridge teaches *where the same idea appears at frontier scale*, with evidence labels separating the two.
