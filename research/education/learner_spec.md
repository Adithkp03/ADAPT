# D6 — Learner & Learning Objective Specification

**Phase 1 | v1.0 2026-09-06**

---

## 1. Intended learner (normative)

> **ML practitioners / advanced students who understand neural networks, supervised learning and the basic Transformer/attention mechanism, but have not deeply studied inference-time adaptation.**

**Not beginners.** This gives technical room to explain real mechanisms without oversimplifying to slogan.

## 2. Prerequisites

### Minimum
- Vectors/matrices, linear algebra basics
- Basic neural nets (layers, params, forward pass)
- Training vs inference distinction
- Gradient descent intuition
- Basic attention (query/key/value conditioning)
- Probability / ML evaluation (accuracy, train/test split)

### Optional (enables deeper)
- Recurrence / RNN / SSM intuition
- Optimization (learning rate, steps)
- Familiarity with few-shot evaluation

### Explicitly not required
- BDH internals
- ARC expertise
- Large-scale training experience

## 3. Preconceptions to address

- "If it learns a new task, weights must have changed." -> target misconception for flagship moment
- "More data always helps" -> to be stressed via noise/interference
- "Memory = database lookup" -> to be replaced via state update visualization

## 4. Learning objectives (7, per phase1.md D6)

| ID | Objective | Bloom | Assessed via |
|----|-----------|-------|--------------|
| LO1 | Define inference-time adaptation (condition/state/weight) | Understand | Pre/post quiz: choose correct definition |
| LO2 | Distinguish ICL (no param change) from param TTA (theta update) | Analyze | Prediction: delta_theta / delta_s identification |
| LO3 | Explain how task info can be encoded in state (s_t update) | Explain | Tracing: given D, describe s change |
| LO4 | Predict how adaptation changes when demonstration count N_D changes | Predict | Slider prediction -> run -> compare |
| LO5 | Predict how adaptation changes under interference (A->B->A retention) | Predict | Interference lab prediction |
| LO6 | Explain relevant BDH-CQ mechanism (recurrent memory + latent reasoning, no param update as described) | Understand | BDH-CQ timeline ordering |
| LO7 | Identify at least one limitation (capacity, forgetting, cost) | Evaluate | Failure lab: choose failure mode explanation |

## 5. Measurement plan (brief requires evaluation)

### Pre-test (5 Q)
1. Does an AI need to change weights to learn a new task? (Y/N + why)
2. What happens when two tasks conflict? (retain/forget)
3. What does an inference-time gradient update change? (theta/s/context)
4. Which has capacity limits? (state/context/params)
5. What is BDH memory? (choose among distractors)

### Interaction (10-15 min guided -> sandbox)

### Post-test (same concepts, different examples) + transfer

### Transfer test
Unseen task family (e.g., new compositional rule not in tutorial) — learner predicts which substrate should work best; run experiment.

### Metrics
- Conceptual accuracy (pre->post delta)
- Prediction accuracy (hypothesis vs observed)
- Transfer accuracy (unseen family)
- Misconception change (LO1/LO2 specifically)
- Completion time, drop-off point

Target: post > pre, transfer > chance, majority achieve LO2+LO3.

## 6. Learning progression (state machine)

```
STATE 0 "I don't know how this model learns"
STATE 1 "It learned the task" (observe success)
STATE 2 "Something inside changed" (Delta visible)
STATE 3 "I can see what changed" (theta vs s)
STATE 4 "I can manipulate that change" (sliders)
STATE 5 "I can predict the effect" (predict-then-run)
STATE 6 "I can make it fail" (interference/noise)
STATE 7 "I understand the trade-off" (capacity/cost)
STATE 8 "I recognize same idea in BDH-CQ"
STATE 9 "I can transfer to new task"
```

UI must support this progression via Guide->Reveal->Manipulate->Sandbox.

## 7. Accessibility / inclusion

- All visualizations with text alternative (delta_s numeric + visual)
- Keyboard-navigable controls
- Mobile usability (Pathway scores this)
- Color not sole encoding (use labels + patterns)
- No jargon without definition on first use (glossary linked)

## 8. Sixty-second DESIGN TARGET (not proven outcome — validated in Phase 3 usability)

0-10s: see unfamiliar task
10-25s: manipulate demonstrations
25-40s: observe model behavior vs ground truth
40-50s: compare truth/estimate
50-60s: answer "Where did new rule go?"

If artifact fails 60s test, redesign before Phase 5.
