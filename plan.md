Yes. After the deeper literature pass, I would make one important change to our earlier plan:

**We should build the project around an experimentally testable research question about inference-time adaptation, rather than around a generic “TTA explainer.”**

The Pathway brief gives us the educational constraints; the research literature gives us the scientific structure. The final product should be a **real, reproducible interactive laboratory**, with live computation wherever feasible and precomputed results only for experiments that genuinely cannot run interactively. The brief explicitly allows precomputation, but prohibits presenting animation as computation and requires clear labeling of live/precomputed/synthetic/animated components. 

# Master Plan — ADAPT

## Working title

# **ADAPT**

### *Where does an AI learn a new rule?*

**Approved Pathway topic:** Test-Time Adaptation

**Supporting concept:** Skill Acquisition from Demonstrations

**Core scientific question:**

> **When a model encounters a previously unseen task at inference time, how is the task-specific information acquired, where is it stored, and what trade-offs arise from that memory mechanism?**

The reason this framing is strong is that current research spans several distinct mechanisms rather than one monolithic notion of “test-time learning”:

* standard in-context learning,
* explicit parameter-updating TTT,
* TTT with learned/expressive hidden state,
* recurrent memory,
* fast-weight-style memory,
* and BDH-CQ's inference-time recurrent memory and latent reasoning. ([Proceedings of Machine Learning Research][1])

So our artifact becomes a controlled laboratory for comparing **where adaptation lives**.

---

# 1. The final scientific thesis

I would make the project revolve around this claim:

> **Inference-time adaptation can acquire task-specific behavior without permanently changing trained parameters, but the choice of adaptation substrate—context, recurrent state, or parameter updates—determines its capacity, cost, persistence, and susceptibility to interference.**

That is deliberately broader than our earlier “weights vs state” idea.

But we should only freeze the exact wording **after Phase 0/1 experiments validate which clauses we can demonstrate rigorously**.

The Pathway brief requires one falsifiable sentence and says the interaction must allow the learner to reproduce or challenge it. 

---

# 2. The conceptual model

The whole product will revolve around:

```text
                   A NEW TASK ARRIVES
                           │
                           ▼
                    DEMONSTRATIONS
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
           CONTEXT       STATE        WEIGHTS
              │            │            │
          condition      update      optimize
              │            │            │
              └────────────┼────────────┘
                           ▼
                     NOVEL QUERY
                           │
                           ▼
                       PREDICTION
                           │
                           ▼
                     GROUND TRUTH
                           │
                           ▼
                   SUCCESS / FAILURE
                           │
                           ▼
                      RETENTION
                           │
                           ▼
                      NEW TASK
```

The product then asks:

> **What changed?**

> **How did it change?**

> **How much information can it hold?**

> **How much compute did adaptation require?**

> **What happens when another task arrives?**

> **Does the learned rule survive?**

This gives us a coherent experimental narrative rather than a collection of unrelated visualizations.

---

# 3. Research foundation

We should organize the literature into five layers.

## Layer A — ICL as inference-time learning

The ICL literature shows that a Transformer can perform task adaptation in its forward computation without explicitly updating its trained parameters. There is even work showing an equivalence between certain linear self-attention computations and gradient descent on regression losses. ([Proceedings of Machine Learning Research][1])

**Why we need it:** establishes that “learning during inference” does not necessarily imply parameter updates.

---

## Layer B — explicit parameter adaptation

Akyürek et al. study TTT where model parameters are temporarily updated using losses formed from input examples. On ARC, they report large gains over relevant baselines, illustrating that inference-time optimization can help with structurally novel tasks. ([Proceedings of Machine Learning Research][2])

Hardt and Sun demonstrate another form of TTT by fine-tuning on retrieved neighbors at test time. ([ICLR Proceedings][3])

**Why we need it:** gives us a genuine parameter-update baseline.

---

## Layer C — learned/expressive state

Sun et al.'s TTT-Linear and TTT-MLP are especially important because the hidden state itself is a learned model, and its update rule is a self-supervised learning step. ([Proceedings of Machine Learning Research][4])

This turns “state” into something richer than a fixed-size feature vector.

**Why we need it:** it prevents us from presenting recurrent-state adaptation as merely ordinary RNN hidden-state accumulation.

---

## Layer D — long-context and continual adaptation

Recent TTT work treats long-context modeling as continual learning, including systems that compress context into weights at test time, while other work applies test-time learning to long-context problems. ([arXiv][5])

**Why we need it:** connects adaptation to the broader current frontier.

---

## Layer E — BDH / BDH-CQ

BDH provides the brain-inspired synaptic-memory perspective; Pathway's current “Equations of Reasoning” materials explicitly frame memory and reasoning as local state dynamics, with synaptic state updated through local rules. ([Pathway][6])

BDH-CQ is even closer to our topic: it combines in-context learning with recurrent latent reasoning, with inference-time inputs continuously updating recurrent memory and subsequent query solving occurring through iterative latent computation. The reported 150M-parameter configuration reaches 29.5% pass@2 on ARC-AGI-1 at a computed cost of $0.0007 per task. ([arXiv][7])

**Why we need it:** this becomes our frontier architecture case study.

---

# 4. What the actual artifact will be

The application should be an **interactive research laboratory**, not a sequence of informational pages.

Think:

# **Experiment → observe → predict → verify → stress → explain**

The user should encounter a running experiment immediately, which is explicitly encouraged by the brief. 

---

# 5. Core platform architecture

```text
                         ADAPT
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   LEARNING UI        EXPERIMENT LAB      BDH/CQ LAB
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                    EXPERIMENT API
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
 TASK GENERATOR      ADAPTATION ENGINE    METRICS
        │                  │                  │
        │          ┌───────┼─────────┐        │
        │          ▼       ▼         ▼        │
        │       FROZEN   PARAM      STATE     │
        │                TTA        ADAPT     │
        │                                      │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                      GROUND TRUTH
                           │
                           ▼
                 REPRODUCIBLE RESULTS
```

The frontend, experiment engine, and research pipeline should be separate.

That makes the system easier to reproduce, test, and defend.

---

# 6. The research-grade task generator

This should be one of our strongest technical components.

Instead of embedding a handful of manually selected puzzles, create a **task generator**.

Each task has:

$$
T = (R,D,Q,Y)
$$

where:

* \(R\) = hidden rule,
* \(D\) = demonstrations,
* \(Q\) = query,
* \(Y\) = exact ground truth.

The learner/model sees:

$$
D,Q
$$

but never receives \(R\).

The evaluation engine knows \(R,Y\).

That means every experiment has exact ground truth.

---

# 7. Task families

We'll implement them progressively.

## Level 1 — Linear regression

Example:

$$
y=ax+b
$$

Each task has different \(a,b\).

Demonstrations reveal the task.

This gives us an analytically transparent starting point.

---

## Level 2 — Nonlinear regression

Introduce task-specific nonlinear functions.

Now simple memorization becomes less trivial.

---

## Level 3 — Symbolic transformations

For example:

```text
A → C
B → D
C → E
```

The mapping changes by task.

---

## Level 4 — Compositional transformations

Example:

```text
reverse
+
offset
+
conditional replacement
```

Now task complexity becomes tunable.

---

## Level 5 — ARC-style visual tasks

```text
input grid → output grid
```

with a hidden transformation inferred from demonstrations.

The official ARC format gives us exactly the demonstration → novel test → exact output structure we need. ([Proceedings of Machine Learning Research][2])

---

# 8. Difficulty should be a scientific variable

Rather than arbitrary difficulty levels, define measurable parameters.

```text
demonstration_count
rule_complexity
noise
ambiguity
task_similarity
state_dimension
adaptation_steps
interference
sequence_length
```

Now every slider has scientific meaning.

The brief explicitly says every control should correspond to one real variable. 

---

# 9. Four adaptation regimes

## Regime A — Frozen baseline

$$
y=f_\theta(D,Q)
$$

Parameters do not change.

Context is available.

This establishes the ICL baseline.

---

## Regime B — Parameter TTA

$$
\theta_{t+1} =
\theta_t-\eta\nabla_\theta L_t
$$

Demonstrations produce an actual gradient update.

We'll measure:

* parameter delta,
* loss,
* accuracy,
* adaptation time,
* compute.

---

## Regime C — Recurrent state adaptation

$$
s_t=F_\theta(s_{t-1},x_t)
$$

Parameters remain fixed.

State changes.

We measure:

* state delta,
* retrieval/query accuracy,
* state capacity,
* retention,
* interference.

---

## Regime D — Learned state / TTT-style state

Where feasible, implement a miniature TTT-Linear-style state that is itself optimized by an update rule, reflecting the research idea of making the hidden state a learned model. ([Proceedings of Machine Learning Research][4])

This is an important distinction from a simple GRU-style baseline.

---

# 10. The flagship experiment

# **Teach the Model a Rule It Has Never Seen**

This is the experience everything else supports.

### Screen 1

Immediately running experiment.

```text
TASK 17

Example 1
Input → Output

Example 2
Input → Output

Example 3
Input → Output
```

Message:

> **The model has never been trained on this task rule.**

---

### Screen 2

User predicts:

> “What should the model output?”

---

### Screen 3

Run the selected adaptation mechanism.

Display:

```text
YOUR PREDICTION
MODEL PREDICTION
GROUND TRUTH
```

---

### Screen 4

Show what changed.

```text
PARAMETERS
████████████  unchanged

STATE
███████████  changed
```

or:

```text
PARAMETERS
████████████  changed

STATE
███████████  reset
```

---

### Screen 5

Ask:

> **Where did the new rule go?**

This is the pedagogical pivot.

---

# 11. Experiment 2 — Adaptation capacity

Change:

$$
N_D = \text{number of demonstrations}
$$

Plot:

$$
Accuracy(N_D)
$$

The learner immediately sees how much evidence the system needs.

---

# 12. Experiment 3 — State capacity

Change:

$$
d_s = \text{state dimension}
$$

Measure:

$$
Accuracy(d_s)
$$

and:

$$
Retention(d_s)
$$

This gives a tangible version of the idea that finite state can constrain adaptation.

The broader meta-learning literature already motivates state capacity as a bottleneck for in-context learning. ([Proceedings of Machine Learning Research][4])

---

# 13. Experiment 4 — Adaptation compute

Change:

$$
K=\text{adaptation steps}
$$

Measure:

$$
Accuracy(K), \quad Latency(K)
$$

This connects adaptation to inference-time scaling.

It also relates to the Pathway brief's specific instruction to examine accuracy/cost/latency trade-offs and BDH-CQ's low/medium/high-effort results. 

---

# 14. Experiment 5 — Interference

Teach:

```text
Task A
```

Then:

```text
Task B
```

Then test:

```text
Task A
```

Measure:

$$
Retention_A =
Accuracy(A_{\text{after B}})
$$

Now the learner sees:

> **Adaptation is not free. New information can interfere with old information.**

This becomes our core failure experiment.

---

# 15. Experiment 6 — Conflicting evidence

Give demonstrations that support competing rules.

Now ask:

> What will the model infer?

The learner can control the conflict.

This gives us:

* robustness,
* ambiguity,
* stability/plasticity,
* adaptation failure.

---

# 16. Experiment 7 — Novel-task transfer

This is critical.

Don't let the learner finish by merely repeating a tutorial example.

Give them a **new task family** and ask them to predict:

> Which adaptation mechanism should work best?

Then run it.

This tests transfer rather than recognition.

---

# 17. BDH integration

This should occur **after the learner has personally discovered the phenomenon**.

The transition should be:

> “You just saw a system acquire task-specific information in its state. Now let's look at a real frontier architecture where evolving internal memory is part of the model design.”

Then introduce BDH.

The Pathway brief explicitly says BDH integration must have its own learning objective and be connected using something concrete: equation, diagram, experiment, or clearly labelled precomputed result. 

---

# 18. BDH module structure

## BDH Layer 1 — Architecture

Show the official high-level structure.

## Layer 2 — Memory

Show the evolving synaptic state.

## Layer 3 — Local dynamics

Use the published “Equations of Reasoning” representation.

Pathway describes one simplified cycle as:

1. read from current synaptic state,
2. update synaptic state using a Hebbian/outer-product style rule,
3. compute gated output,
4. update the neural state. ([Pathway][6])

This can become one of the most compelling interactive diagrams in the product.

---

# 19. BDH-CQ module

Then transition:

> **“BDH-CQ pushes this idea into in-context task adaptation and latent reasoning.”**

Explain:

```text
demonstrations
      ↓
recurrent memory update
      ↓
query
      ↓
iterative latent reasoning
      ↓
answer
```

without implying that we have reproduced the full official 150M-parameter system.

That distinction is explicitly required by the Pathway brief. 

---

# 20. What we should build ourselves vs what we should use from research

This is crucial.

## We build

* task generator,
* tiny adaptation models,
* experiments,
* metrics,
* interactive visualization,
* educational narrative,
* user evaluation.

## We use published evidence for

* BDH architecture,
* BDH equations,
* BDH-CQ architecture,
* official benchmark results,
* published large-model experiments.

## We reproduce selectively

Only experiments that:

* can be reproduced reliably,
* materially support our central claim,
* and fit the time/resource constraints.

We must label independent reproductions as such.

---

# 21. No fake simulation

You specifically emphasized this, and I agree.

There should be **zero fake model behavior**.

For every visualization:

### Live

Real model computation occurs now.

### Precomputed

An actual experiment was executed earlier.

### Synthetic

Data was generated by our controlled task generator.

### Illustrative

A conceptual visualization is being used purely for explanation.

The UI should visibly tell the learner which is which.

That exactly follows the brief's scientific honesty requirement. 

---

# 22. Precomputation architecture

For expensive experiments:

```text
research run
      ↓
versioned experiment config
      ↓
experiment execution
      ↓
raw results
      ↓
validation
      ↓
compressed result artifact
      ↓
public application
```

Every chart should have a provenance entry:

```text
Experiment ID
Model version
Dataset/task generator version
Random seed
Hyperparameters
Hardware
Execution date
Source code commit
```

This gives us a real reproducibility chain.

---

# 23. Scientific evaluation

We should run experiments in three categories.

## A. Mechanistic experiments

What changes internally?

Examples:

* parameter deltas,
* state deltas,
* memory writes,
* adaptation dynamics.

## B. Behavioral experiments

Does task performance improve?

Examples:

* accuracy,
* exact-match,
* generalization.

## C. Resource experiments

What does adaptation cost?

Examples:

* latency,
* memory,
* FLOPs/approximate compute,
* parameter update magnitude.

---

# 24. Ablation matrix

At minimum:

| Ablation            | Question                                  |
| ------------------- | ----------------------------------------- |
| No adaptation       | How much does the base system know?       |
| Context only        | What can conditioning accomplish?         |
| Parameter update    | What does explicit TTA buy us?            |
| State update        | What can recurrent adaptation accomplish? |
| State size          | How much capacity matters?                |
| Demonstration count | How much evidence matters?                |
| Adaptation steps    | How does inference compute matter?        |
| Interference        | How stable is the learned task?           |
| Noise               | How robust is adaptation?                 |

This will form the core of our scientific report.

---

# 25. Hypotheses

Before running experiments, formulate them explicitly.

### H1

More demonstrations should generally improve adaptation performance up to a saturation point.

### H2

Increasing state capacity should improve adaptation on sufficiently complex tasks.

### H3

More adaptation compute can improve performance but increases latency/cost.

### H4

State-based adaptation can acquire task-specific behavior without modifying persistent model parameters.

### H5

Finite adaptive memory creates interference/retention trade-offs.

### H6

The best adaptation substrate depends on task characteristics rather than one mechanism dominating universally.

These are **hypotheses**, not claims. We only promote them to conclusions after experiments.

---

# 26. User-learning evaluation

The brief is unusually focused on learning effectiveness. 

So we'll measure it.

## Pre-test

Ask:

> Does an AI need to modify its weights to learn a new task?

> What happens when two tasks conflict?

> What does an inference-time gradient update actually change?

## Interaction

10–15 minutes.

## Post-test

Same concepts with different examples.

## Transfer test

Completely unseen task.

## Measure

* conceptual accuracy,
* prediction accuracy,
* transfer accuracy,
* misconception change,
* completion time.

This can become a real empirical result about the effectiveness of the artifact.

---

# 27. The sixty-second learning test

We should explicitly design for this.

A person who has never seen the artifact should be able to:

**0–10 sec:** see a task being learned

**10–25 sec:** manipulate a variable

**25–40 sec:** observe model behavior

**40–50 sec:** compare to ground truth

**50–60 sec:** answer:

> “Where did the new rule go?”

The brief explicitly calls out the sixty-second test and describes exceptional submissions as those where the central insight can be reproduced in under a minute.  

---

# 28. Product architecture

I would structure the UI into:

### `/`

**The Challenge**

Immediate experiment.

### `/lab`

**Adaptation Laboratory**

Full parameter/state/context comparisons.

### `/memory`

**Where Is the Rule?**

Internal-state visualizations.

### `/stress`

**Break the Learner**

Interference, noise, conflicting tasks.

### `/bdh`

**From Adaptive State to BDH**

Published architecture/equations.

### `/bdh-cq`

**BDH-CQ**

Inference-time recurrent memory + latent reasoning.

### `/research`

**Evidence**

Paper-backed experimental results.

### `/methodology`

**How this laboratory works**

Transparency and provenance.

This is much better than a traditional “home / about / features” site.

---

# 29. Research repository structure

```text
adapt/
│
├── app/
│   ├── experiments/
│   ├── narrative/
│   ├── state_view/
│   ├── bdh/
│   └── components/
│
├── models/
│   ├── frozen/
│   ├── param_tta/
│   ├── recurrent_state/
│   └── ttt_state/
│
├── tasks/
│   ├── regression/
│   ├── symbolic/
│   ├── compositional/
│   └── arc_like/
│
├── experiments/
│   ├── configs/
│   ├── runners/
│   ├── outputs/
│   └── analysis/
│
├── bdh/
│   ├── sources/
│   ├── equations/
│   ├── diagrams/
│   └── reproduced/
│
├── evaluation/
│   ├── benchmark/
│   └── learner_study/
│
├── research/
│   ├── literature/
│   ├── evidence_ledger/
│   ├── hypotheses/
│   └── technical_report/
│
└── docs/
    ├── README.md
    ├── provenance.md
    ├── licenses.md
    ├── ai_disclosure.md
    └── concept_summary.pdf
```

---

# 30. Experiment configuration must be version controlled

Example:

```yaml
task_family: symbolic
rule_complexity: 4
demonstrations: 3
noise: 0.05
state_dimension: 32
adaptation_steps: 8
seed: 42
model: recurrent_state_v3
```

This allows us to say:

> “The result shown in the application corresponds to experiment configuration X.”

That is the level of reproducibility I want.

---

# 31. Research paper / technical report

We should maintain a paper-style internal document from the beginning.

## Abstract

## 1. Introduction

## 2. Problem formulation

## 3. Taxonomy of adaptation mechanisms

## 4. Experimental methodology

## 5. Synthetic task generator

## 6. Adaptation models

## 7. Results

## 8. Ablations

## 9. Failure modes

## 10. BDH/BDH-CQ relationship

## 11. Educational artifact

## 12. Learner evaluation

## 13. Limitations

## 14. Conclusion

This also makes the final concept summary much easier to write.

---

# 32. Evidence discipline

We should maintain an evidence matrix such as:

| Statement                                                | Primary source    | Evidence type        | Reproduced? |
| -------------------------------------------------------- | ----------------- | -------------------- | ----------- |
| ICL can perform inference-time task adaptation           | ICL paper         | published result     | —           |
| Transformer computation can implement GD-like adaptation | von Oswald et al. | formal + empirical   | possibly    |
| TTT updates parameters at inference                      | Akyürek et al.    | published experiment | yes/no      |
| TTT hidden state can be a learned model                  | Sun et al.        | published experiment | yes/no      |
| BDH uses evolving synaptic state                         | BDH               | architecture/paper   | no          |
| BDH-CQ updates recurrent memory at inference             | BDH-CQ            | published experiment | no          |
| Our toy recurrent model exhibits interference            | our experiment    | independent result   | yes         |

This prevents accidental overclaiming.

---

# 33. Three mandatory research papers

The submission requires at least three recent primary papers from 2022–2026. 

Our eventual evidence base should be substantially larger.

At minimum, the core set should include:

**Akyürek et al., ICML 2025 — The Surprising Effectiveness of Test-Time Training for Few-Shot Learning.** ([Proceedings of Machine Learning Research][2])

**Sun et al., ICML 2025 — Learning to (Learn at Test Time): RNNs with Expressive Hidden States.** ([Proceedings of Machine Learning Research][4])

**von Oswald et al., ICML 2023 — Transformers Learn In-Context by Gradient Descent.** ([Proceedings of Machine Learning Research][1])

Then:

**Hardt & Sun, ICLR 2024 — Test-Time Training on Nearest Neighbors for Large Language Models.** ([ICLR Proceedings][3])

**BDH.** ([Hugging Face][8])

**BDH-CQ.** ([arXiv][7])

And the relevant long-context TTT work. ([arXiv][5])

---

# 34. What makes this genuinely different from an existing explainer

Our novelty should not be:

> “We explain test-time training more beautifully.”

It should be:

> **“We provide a controlled environment where a learner can manipulate the location and dynamics of inference-time adaptation and observe its consequences under controlled task distributions.”**

The novelty therefore comes from the **experimental substrate + educational interpretation**, not merely UI.

This is important because the brief explicitly warns against generic explanations and static resources. 

---

# 35. What can become our reusable research asset

The most valuable technical component may actually be:

# **Adaptive Task Laboratory**

A reusable engine that can generate unseen tasks and compare adaptation mechanisms.

Then the Pathway artifact becomes the first application of a more general system.

Potential future uses:

* studying ICL,
* TTA,
* recurrent memory,
* continual learning,
* state capacity,
* interference,
* latent reasoning.

But the public product should **not expose all of those as independent topics**, because the brief demands one central claim.

Under the hood, the substrate can be general.

On the surface, the educational journey remains focused.

---

# 36. Project phases

## Phase 0 — Scientific specification

**Goal:** freeze the question.

Deliver:

* terminology map,
* literature map,
* hypothesis set,
* candidate claim,
* experiment matrix.

No product UI.

---

## Phase 1 — Minimal scientific prototype

Implement:

* synthetic task generator,
* frozen baseline,
* parameter TTA,
* recurrent-state model.

Demonstrate:

$$
D \rightarrow adaptation \rightarrow Q \rightarrow Y
$$

with measurable results.

---

## Phase 2 — Research validation

Run:

* demonstration ablations,
* state-capacity experiments,
* adaptation-step experiments,
* noise,
* interference,
* transfer.

Generate publication-quality figures.

---

## Phase 3 — TTT-style state research

Implement a minimal expressive-state mechanism inspired by the TTT literature.

Determine exactly what it adds compared with a conventional recurrent state. ([Proceedings of Machine Learning Research][4])

---

## Phase 4 — BDH scientific module

Build:

* official-paper evidence map,
* equation visualizations,
* architecture explanation,
* carefully labelled educational implementation,
* BDH-CQ evidence section.

---

## Phase 5 — Educational prototype

Build only the flagship 60-second experiment.

User-test it.

Fix the learning experience.

---

## Phase 6 — Complete product

Add:

* adaptation lab,
* stress lab,
* state visualization,
* BDH,
* BDH-CQ,
* final challenge.

---

## Phase 7 — Learner evaluation

Run pre/post/transfer study.

---

## Phase 8 — Production hardening

* responsive UI,
* deployment,
* performance,
* failure handling,
* reproducibility,
* provenance.

---

## Phase 9 — Documentation

Finalize:

* README,
* technical report,
* concept summary,
* citations,
* sources,
* licenses,
* AI disclosure.

---

## Phase 10 — Red-team

Have someone challenge:

* scientific claims,
* implementation,
* evidence,
* UX,
* reproducibility,
* BDH interpretation.

---

# 37. Definition of Done

I would use this as the final gate.

### Scientific

☐ Central claim is falsifiable.

☐ Claim is supported by our experiments.

☐ We know exactly what is demonstrated versus hypothesized.

☐ At least three recent primary papers are incorporated.

☐ Competing approaches are understood.

☐ Major limitation is experimentally demonstrated.

---

### Computational

☐ Core behavior is actual computation.

☐ Adaptation changes something real.

☐ Ground truth is exact.

☐ State/parameter changes are measurable.

☐ Experiment configurations are reproducible.

☐ Results are versioned.

---

### Educational

☐ Audience is explicitly defined.

☐ Prerequisites are documented.

☐ Learning objectives are measurable.

☐ Learner manipulates real variables.

☐ Learner predicts before seeing result.

☐ Ground truth is visible.

☐ Failure mode is visible.

☐ Final transfer task exists.

☐ Central insight can be discovered rapidly.

---

### BDH

☐ BDH is integrated into the learning flow.

☐ BDH/CQ connection is technically correct.

☐ Published equations/results are cited.

☐ Official behavior is never confused with our implementation.

☐ Evidence type is labelled.

---

### Product

☐ Public URL with no sign-in.

☐ Fast interaction.

☐ Mobile usable.

☐ Stable deployment.

☐ No fake animations presented as computation.

☐ Live/precomputed/synthetic/illustrative components are labelled.

---

### Submission

☐ Public repository.

☐ Complete README.

☐ Setup instructions.

☐ Concept-summary PDF.

☐ Three+ recent primary papers.

☐ Source/license record.

☐ AI/code/data/asset disclosure.

All of those map directly to the Pathway submission requirements and judging criteria.  

---

# 38. The most important strategic decision

We should **not make the final product a comparison dashboard**.

The dashboard can exist internally.

The public educational experience should be a **story of discovery**:

```text
"I've never seen this task."

        ↓

"Yet the model learned it."

        ↓

"Where did the rule go?"

        ↓

"Nothing changed here..."

        ↓

"It changed here."

        ↓

"What if I shrink that memory?"

        ↓

"What if I teach another rule?"

        ↓

"It forgot the first."

        ↓

"So adaptation has a capacity/interference trade-off."

        ↓

"Does a real frontier architecture
use the same idea?"

        ↓

"Here's BDH."

        ↓

"Here's BDH-CQ."

        ↓

"Now solve a new one yourself."
```

That is the educational experience.

The experimental engine underneath is rigorous enough that every major step has real computation behind it.

---

# 39. What I would consider our first milestone

Before writing the polished web application, we should reach this exact state:

> **Given an automatically generated unseen task, our system can present demonstrations, run at least two genuinely different adaptation mechanisms, perform a novel query, compare against exact ground truth, record what changed internally, and quantify adaptation, cost, and retention.**

Once we have that running **for real**, we have the scientific core.

Everything afterward—visualization, narrative, BDH, deployment, documentation—is built around a proven substrate.

That is the approach I would take for a **research-paper-level Pathway submission**, and it stays tightly aligned with the brief's fundamental requirement: one precise claim, real interaction, observable computation, honest evidence, meaningful BDH integration, and a learner who actually discovers the phenomenon rather than merely reading about it. 

[1]: https://proceedings.mlr.press/v202/von-oswald23a.html?utm_source=chatgpt.com "Transformers Learn In-Context by Gradient Descent"
[2]: https://proceedings.mlr.press/v267/akyurek25a.html?utm_source=chatgpt.com "The Surprising Effectiveness of Test-Time Training for Few-Shot Learning"
[3]: https://proceedings.iclr.cc/paper_files/paper/2024/hash/f02f1185b97518ab5bd7ebde466992d3-Abstract-Conference.html?utm_source=chatgpt.com "Test-Time Training on Nearest Neighbors for Large Language Models"
[4]: https://proceedings.mlr.press/v267/sun25h.html?utm_source=chatgpt.com "Learning to (Learn at Test Time): RNNs with Expressive Hidden States"
[5]: https://arxiv.org/abs/2512.23675?utm_source=chatgpt.com "End-to-End Test-Time Training for Long Context"
[6]: https://pathway.com/research/the-equations-of-reasoning?utm_source=chatgpt.com "The Equations of Reasoning | Pathway"
[7]: https://arxiv.org/abs/2608.09888?utm_source=chatgpt.com "BDH-CQ: In-Context Learning with Recurrent Latent Reasoning"
[8]: https://huggingface.co/papers/2509.26507?utm_source=chatgpt.com "Paper page - The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain"
