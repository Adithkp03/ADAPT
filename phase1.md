Good. We should treat **Phase 1 as the scientific foundation of the entire project**, not as a preliminary “research before coding” step.

At the end of Phase 1, we should know exactly **what scientific phenomenon we are teaching, what we claim, what evidence supports it, what we will experimentally implement, what we will deliberately not claim, how BDH/BDH-CQ fits, and what experiment can falsify the claim**.

The Pathway brief itself requires this kind of discipline: one precise falsifiable claim, a clearly defined learner, meaningful manipulation, observable consequence, ground truth, BDH integration, limitations, recent primary literature, and explicit evidence boundaries.  

# PHASE 1 — SCIENTIFIC SPECIFICATION

## Phase 1 objective

By the end of Phase 1, the team should be able to answer these questions without ambiguity:

> **What exactly is test-time adaptation?**

> **What is the precise phenomenon we are teaching?**

> **What is our falsifiable claim?**

> **What competing mechanisms exist?**

> **Which mechanisms are we actually going to implement?**

> **What experiment distinguishes them?**

> **What variables can the learner manipulate?**

> **What is the ground truth?**

> **What failure mode will the learner observe?**

> **What does BDH actually contribute?**

> **What does BDH-CQ actually contribute?**

> **Which published claims can we legitimately make?**

> **What parts will be live, precomputed, synthetic, or illustrative?**

If we cannot answer these at the end, **Phase 1 is not complete**, regardless of how much research we have collected.

---

# 1. Deliverable map

Phase 1 should produce **nine concrete deliverables**:

| Deliverable                                        | Purpose                                                                 |
| -------------------------------------------------- | ----------------------------------------------------------------------- |
| **D1. Scientific Scope Document**                  | Defines exactly what our project is and isn't                           |
| **D2. Terminology & Concept Map**                  | Prevents conflating ICL, TTA, TTT, state adaptation, fast weights, etc. |
| **D3. Literature & Evidence Matrix**               | Converts papers into verified scientific claims                         |
| **D4. BDH / BDH-CQ Technical Dossier**             | Establishes the exact connection and evidence boundaries                |
| **D5. Central Claim Specification**                | Produces the final falsifiable sentence                                 |
| **D6. Learner & Learning-Objective Specification** | Defines who learns what and how we measure learning                     |
| **D7. Experimental Design Specification**          | Defines variables, baselines, tasks, hypotheses, metrics and ablations  |
| **D8. Computational Substrate Specification**      | Defines exactly what we will implement                                  |
| **D9. Feasibility / Go-No-Go Review**              | Prevents us from committing to an impossible system                     |

These should become actual files in the repository, not merely notes in a chat.

---

# 2. D1 — Scientific Scope Document

Create:

```text
docs/research/scientific_scope.md
```

This is our project's constitution.

It should contain:

### 2.1 Selected Pathway topic

**Test-Time Adaptation**

Supporting:

**Skill Acquisition from Demonstrations**

We should explicitly record that we are using the latter only as a supporting concept, not as an independent second project. The brief allows closely related topics only when they maintain one central claim and coherent learning journey. 

### 2.2 Core question

Proposed:

> **When a model encounters a previously unseen task at inference time, how does it acquire the task-specific rule, where is that information represented, and what trade-offs result from the chosen adaptation mechanism?**

### 2.3 Scope boundaries

We explicitly say:

**In scope**

* inference-time adaptation,
* few-shot task acquisition,
* context-based adaptation,
* recurrent-state adaptation,
* parameter-updating TTT,
* learned-state TTT where relevant,
* task retention/interference,
* adaptation compute,
* BDH/BDH-CQ as frontier case studies.

**Out of scope**

* general AGI,
* general-purpose continual learning,
* generic LLM training,
* generic RAG,
* broad survey of all memory architectures,
* explaining all of BDH,
* explaining all forms of reasoning.

This is important because the brief explicitly says not to explain an entire field. 

### Acceptance criterion

A reviewer should read the document and be able to describe the project in **two sentences** without mentioning anything outside scope.

---

# 3. D2 — Terminology & Concept Map

This is arguably the most important research artifact.

Create:

```text
docs/research/terminology.md
```

We need a rigorous map of:

### In-Context Learning

$$
y = f_\theta(D,x)
$$

Parameters fixed; task information is supplied through context.

### Meta-learning

Training a model to adapt efficiently to new tasks.

### Test-Time Adaptation

Umbrella terminology for adapting a trained system using information encountered at inference.

### Test-Time Training

A specific family where an inference-time training objective drives updates.

### Parameter-based TTT

$$
\theta_{t+1}
=
\theta_t-\eta\nabla_\theta L_t
$$

### Recurrent state adaptation

$$
s_t = F_\theta(s_{t-1},x_t)
$$

### Learned-state TTT

State itself has a trainable computational structure and is updated using a learning objective. Sun et al.'s TTT-Linear and TTT-MLP make this idea explicit. ([Proceedings of Machine Learning Research][1])

### Fast weights

Rapidly changing parameters/memory that can represent temporary information; historically related to linear-attention interpretations.

### Synaptic plasticity

Especially important for BDH.

### BDH memory

Transient synaptic changes through its architecture's plasticity mechanism. ([arXiv][2])

### BDH-CQ memory

Inference-time inputs update recurrent memory, followed by iterative latent reasoning. ([arXiv][3])

---

# 4. The terminology deliverable must include a “NOT THE SAME AS” table

This is something I strongly recommend.

| Concept                    |                        Is it parameter-updating? | Changes during inference? | What stores task info? |
| -------------------------- | -----------------------------------------------: | ------------------------: | ---------------------- |
| Standard ICL               |                                               No |          Computation only | Context/computation    |
| Parameter TTT              |                                              Yes |                       Yes | Parameters             |
| Recurrent-state adaptation |                                               No |                       Yes | State                  |
| TTT-Linear / TTT-MLP       |                             State-level learning |                       Yes | Learned state          |
| BDH synaptic memory        |                    Not equivalent to generic TTT |                       Yes | Synaptic state         |
| BDH-CQ                     | No inference parameter update in described setup |                       Yes | Recurrent memory       |

The exact BDH-CQ row must be tied to the primary paper rather than our interpretation. The paper explicitly describes recurrent memory updates at inference and no parameter changes for the inference process. ([arXiv][3])

This table will prevent us from making technically incorrect claims later.

---

# 5. D3 — Literature & Evidence Matrix

This will be our main research database.

Create:

```text
research/literature/evidence_matrix.csv
```

Every important paper gets a row.

## Mandatory columns

```text
Paper
Year
Venue
Primary Source URL
Concept
Research Question
Method
Adaptation Substrate
Training-Time Change
Inference-Time Change
Task Type
Dataset
Main Result
Relevant Equation
Relevant Figure
Limitation
Evidence Type
Reproduced by Us?
Can We Cite It?
Exact Claim We Can Make
```

---

# 6. The first research cluster

We need to deeply study the progression:

### 2023 — Transformer / ICL as implicit optimization

von Oswald et al. show an equivalence between a single linear self-attention layer and gradient descent for certain regression settings. ([Google Research][4])

This is important because it establishes:

> **Inference-time learning-like behavior can occur without explicit parameter updates.**

---

### 2024 — TTT in language models

Hardt & Sun perform actual test-time fine-tuning on retrieved neighbors and report improvements across many language-modeling tasks. ([ICLR Proceedings][5])

This establishes:

> **Inference-time parameter adaptation can be operationally useful.**

---

### 2025 — TTT for few-shot reasoning

Akyürek et al. directly study TTT for structurally novel tasks and report substantial gains on ARC and BBH. ([Proceedings of Machine Learning Research][6])

This establishes:

> **Explicit test-time optimization can improve adaptation to novel task structures.**

---

### 2025 — Learned expressive states

Sun et al. introduce TTT-Linear and TTT-MLP, where the hidden state itself is a learned model and is updated using self-supervised learning. They evaluate models at 125M–1.3B parameters and report strong long-context behavior compared with Transformer and Mamba baselines. ([Proceedings of Machine Learning Research][1])

This establishes:

> **The adaptation substrate does not have to be the model's persistent weights; the state itself can contain learnable computational structure.**

---

### 2025 — BDH

BDH introduces synaptic-plasticity-based working memory and a brain-inspired graph architecture with sparse positive activations and heavy-tailed connectivity. ([arXiv][2])

---

### 2026 — BDH-CQ

BDH-CQ explicitly combines in-context learning with recurrent latent reasoning, with inference-time inputs updating recurrent memory before latent reasoning on the query. ([arXiv][3])

This gives us a research timeline rather than isolated papers.

---

# 7. D4 — BDH / BDH-CQ Technical Dossier

Create:

```text
research/bdh/bdh_dossier.md
research/bdh/bdhcq_dossier.md
```

This should be a **technical reading document**, not a marketing summary.

---

# 8. BDH dossier

We need to extract:

### Architecture

* neuron representation,
* synaptic representation,
* local interactions,
* graph structure,
* state,
* activation mechanism.

### Memory

Exactly what is changing when information is stored?

The BDH paper describes working memory as relying on synaptic plasticity with Hebbian learning and reports concept-related synaptic strengthening. ([arXiv][2])

### Interpretability

Understand:

* sparse positive activations,
* monosemantic synapses,
* state interpretability.

### Computational formulation

Extract the equations relevant to our concept.

### Evidence status

Every statement tagged:

```text
FORMAL
EMPIRICAL
DEVELOPER-REPORTED
INDEPENDENT
OUR IMPLEMENTATION
ILLUSTRATION
```

---

# 9. BDH-CQ dossier

We need to extract:

### Input ingestion

What information enters memory?

### Recurrent memory

What changes?

### Latent reasoning

How does the query get processed after memory accumulation?

### Effort scaling

What constitutes low/medium/high inference effort?

### ARC experiments

What did they actually test?

### Intervention experiments

What do the controlled ARC-like experiments demonstrate?

### Cost

What is reported and under what setup?

The paper reports a 150M-parameter configuration at 29.5% pass@2 on ARC-AGI-1 at a computed $0.0007/task, but this number belongs to their particular experimental setup and should not be generalized to all inference or all systems. ([arXiv][3])

That is exactly the sort of evidence qualification judges will expect.

---

# 10. D5 — Central Claim Specification

Create:

```text
research/claim/central_claim.md
```

This should go through several versions.

## Claim v0

> “Models can learn at test time.”

Too vague.

Reject.

## Claim v1

> “Models can adapt to unseen tasks without changing their weights.”

Better, but doesn't specify mechanism or trade-off.

## Claim v2

> **“A model can acquire an unseen task rule at inference time without changing its persistent parameters by updating an internal adaptive state, but the capacity and update dynamics of that state constrain what can be retained.”**

Now we have something testable.

But we shouldn't freeze this until our prototype experiments confirm that our specific implementation demonstrates it.

---

# 11. Claim falsification criteria

This is crucial.

For the central claim, specify:

### Evidence supporting it

Example:

$$
Accuracy_{\text{adapted}}
>
Accuracy_{\text{frozen}}
$$

while:

$$
\Delta\theta = 0
$$

and:

$$
\Delta s \neq 0
$$

### Evidence against it

If:

* state adaptation doesn't materially improve task acquisition,
* the improvement comes from hidden parameter updates,
* or our measured state variables do not actually carry task information,

then we must revise the claim.

This is how we avoid designing the experiment to merely confirm our preferred narrative.

---

# 12. D6 — Learner specification

Create:

```text
research/education/learner_spec.md
```

## Intended learner

I recommend:

> **ML practitioners / advanced students who understand neural networks, supervised learning and the basic Transformer/attention mechanism, but have not deeply studied inference-time adaptation.**

Not beginners.

That gives us enough technical room to explain the real mechanism.

---

# 13. Prerequisites

Minimum:

* vectors/matrices,
* basic neural networks,
* training vs inference,
* gradient descent,
* basic attention,
* probability/ML evaluation.

Optional:

* recurrence,
* optimization.

---

# 14. Learning objectives

By completion, learner should be able to:

### LO1

Define inference-time adaptation.

### LO2

Distinguish ICL from explicit parameter-updating TTT.

### LO3

Explain how task information can be encoded in state.

### LO4

Predict how adaptation changes when demonstration count changes.

### LO5

Predict how adaptation changes under interference.

### LO6

Explain the relevant BDH-CQ mechanism.

### LO7

Identify at least one limitation.

These objectives directly correspond to the Pathway mission. 

---

# 15. D7 — Experimental Design Specification

This is the most important technical deliverable.

Create:

```text
research/experiments/experimental_design.md
```

It should answer:

> **Exactly what experiment are we going to run?**

---

# 16. Our primary experimental question

I recommend:

> **How does the choice of adaptation substrate affect a model's ability to infer, retain, and transfer a previously unseen task rule?**

This gives us three measurable behaviors:

### Acquire

Can it learn the new rule?

### Retain

Does it remember it?

### Transfer

Can it use it on a new query?

---

# 17. Independent variables

At minimum:

$$
N_D = \text{demonstration count}
$$

$$
C_R = \text{rule complexity}
$$

$$
d_s = \text{state capacity}
$$

$$
K = \text{adaptation steps}
$$

$$
I = \text{interference}
$$

$$
N = \text{noise}
$$

These become our meaningful learner controls.

---

# 18. Dependent variables

### Task accuracy

$$
A
=
\frac{\text{correct predictions}}
{\text{total predictions}}
$$

### Adaptation gain

$$
G=A_{\text{adapted}}-A_{\text{baseline}}
$$

### Retention

$$
R_A =
A(A\text{ after learning B})
$$

### Adaptation cost

Measure:

* latency,
* number of updates,
* approximate FLOPs,
* memory.

### State change

$$
\Delta s=\|s_{\text{after}}-s_{\text{before}}\|
$$

### Parameter change

$$
\Delta\theta=\|\theta_{\text{after}}-\theta_{\text{before}}\|
$$

These two measurements are especially important for teaching **where the adaptation happened**.

---

# 19. Baselines

Our minimum set:

## Baseline 0 — Oracle

Ground-truth rule supplied directly.

Establishes task ceiling.

## Baseline 1 — Frozen

No adaptation.

## Baseline 2 — Context / ICL

No explicit parameter/state update beyond ordinary forward computation.

## Baseline 3 — Parameter TTA

Actual inference-time gradient updates.

## Baseline 4 — Recurrent state

Parameters fixed, state updated.

## Baseline 5 — expressive learned state

Only if we can implement it correctly within scope.

This gives us an actual scientific comparison.

---

# 20. Task suite

We need to build the task suite **from easiest to most expressive**.

## Tier 1 — Linear regression

Hidden:

$$
y=ax+b
$$

Each episode has its own \(a,b\).

This should be the sanity-check environment.

---

## Tier 2 — Nonlinear regression

Different hidden functions.

Purpose:

test whether the adaptive mechanism is merely fitting trivial linear relationships.

---

## Tier 3 — Symbolic rule induction

Input/output symbols.

Purpose:

make the notion of “new rule” visually obvious.

---

## Tier 4 — Compositional transformations

Multiple operations.

Purpose:

increase task complexity systematically.

---

## Tier 5 — ARC-style visual transformations

Input/output grids.

Purpose:

connect the educational laboratory to the research frontier and the BDH-CQ evaluation setting.

ARC-AGI explicitly targets novel tasks and few-shot adaptation, while ARC-AGI-2 is intended to provide more demanding signals for abstract reasoning. ([ARC Prize][7])

---

# 21. Why we shouldn't start with ARC

Because if the system fails on ARC, we won't know whether:

* our adaptation mechanism failed,
* our architecture is wrong,
* our task representation is poor,
* our model can't reason,
* or the experiment itself is flawed.

The linear regression environment gives us **analytical ground truth**.

Then each subsequent environment adds complexity.

That is much more scientifically sound.

---

# 22. D8 — Computational Substrate Specification

Create:

```text
research/system/computational_substrate.md
```

The critical principle:

> **The educational experience must sit on top of a functioning experimental engine.**

The Pathway brief explicitly says the concept should behave inside the artifact and allows real tiny models, real replays, or live toy systems—but not scripted animations presented as actual behavior. 

---

# 23. Define the minimum model family

We should specify:

### Model A

Small frozen model.

### Model B

Small model + parameter TTA.

### Model C

Small recurrent model.

### Model D

Optional TTT-style expressive state.

### Model E

BDH-inspired educational mechanism, only to the extent justified by published equations.

No pretending these are official BDH models.

The brief explicitly requires independent toy implementations to be labelled as such. 

---

# 24. Define live computation boundaries

Write this before frontend work.

### LIVE

Small experiment:

* task generation,
* adaptation,
* prediction,
* metrics.

### PRECOMPUTED

Heavy:

* large parameter sweeps,
* expensive benchmark experiments,
* official-model evaluation where live execution isn't practical.

### SYNTHETIC

Generated task distributions.

### ILLUSTRATIVE

Architecture explanations/animations.

The brief explicitly allows expensive precomputed experiments but requires them to be clearly identified. 

---

# 25. D9 — Feasibility / Go-No-Go Review

This is the deliverable that prevents an ambitious research plan from becoming an impossible implementation.

Create:

```text
research/phase1/go_no_go.md
```

For every major experiment:

| Experiment               | Scientific value | Implementation difficulty | Runtime |      Risk | Decision       |
| ------------------------ | ---------------: | ------------------------: | ------: | --------: | -------------- |
| Linear regression TTA    |             High |                       Low |    Fast |       Low | GO             |
| Symbolic adaptation      |             High |                    Medium |    Fast |       Low | GO             |
| ARC-like adaptation      |        Very high |                      High |  Medium |    Medium | GO             |
| Official BDH live        |    Low/uncertain |                 Very high |    High | Very high | NO             |
| BDH precomputed evidence |             High |                    Medium |       — |       Low | GO             |
| Full BDH-CQ reproduction |         Moderate |                 Very high |    High | Very high | NO/conditional |

This is where we protect the scientific scope.

---

# 26. Phase 1 research questions

I would divide the actual reading into these questions.

## Q1 — What exactly is learning during ICL?

Study the theoretical/mechanistic ICL literature.

The von Oswald result is particularly useful because it gives us a concrete mathematical bridge between attention and gradient descent in controlled settings. ([Proceedings of Machine Learning Research][8])

---

## Q2 — What exactly is different about explicit TTT?

Read Akyürek and Hardt/Sun carefully.

We need to understand:

* loss construction,
* update schedule,
* parameter subset,
* number of steps,
* inference cost,
* reset behavior,
* task assumptions. ([Proceedings of Machine Learning Research][6])

---

## Q3 — Is “state adaptation” really different from parameter adaptation?

Study TTT-Linear / TTT-MLP.

The important conceptual point is that the hidden state can itself be a learned model. ([Proceedings of Machine Learning Research][1])

---

## Q4 — What is the role of memory capacity?

Investigate:

* context length,
* state dimension,
* parameter count,
* fast-memory capacity,
* interference.

This becomes central to our experiments.

---

## Q5 — What does BDH mean by memory?

Study the actual equations and implementation.

Do **not** infer this from generic descriptions.

---

## Q6 — What exactly does BDH-CQ adapt?

Read the technical report/paper end-to-end.

Especially:

* task demonstrations,
* memory updates,
* reasoning stages,
* ablations/interventions,
* ARC evaluation.

The paper explicitly uses controlled ARC-like interventions to study what is learned from demonstrations and how consistently transformations are applied. ([arXiv][3])

---

# 27. Primary-source reading protocol

Do not read papers casually.

For every primary paper, extract:

### Abstract

What problem?

### Introduction

Why now?

### Method

What mathematically changes?

### Algorithm

What executes at inference?

### Experimental setup

What exactly was measured?

### Results

What actually improved?

### Ablations

What caused the improvement?

### Limitations

What didn't work?

### Code

Is there publicly available implementation?

### Claims we can safely reuse

Exactly what sentence can we cite?

This turns research into engineering input.

---

# 28. Don't just collect papers—build a research graph

We should eventually have something like:

```text
                    META-LEARNING
                          │
                          ▼
                   IN-CONTEXT LEARNING
                     /           \
                    /             \
                   ▼               ▼
          implicit optimization   state/computation
                   │                     │
                   ▼                     ▼
            ICL ≈ GD              recurrent memory
                   │                     │
                   ▼                     ▼
             parameter TTT          TTT-Linear/MLP
                   │                     │
                   └──────────┬──────────┘
                              ▼
                         TTA design space
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
               BDH                      BDH-CQ
                 │                         │
          synaptic memory           recurrent memory
                                        +
                                  latent reasoning
```

The graph itself may eventually become part of the educational experience.

But **during Phase 1 it is a research map**, not a UI feature.

---

# 29. The first concrete experiment we should prepare

Before the full project exists, create one notebook:

```text
experiments/001_linear_task_adaptation.ipynb
```

It should contain:

### Generate task

Randomly choose \(a,b\).

### Generate demonstrations

$$
D = \{(x_i, ax_i+b)\}
$$

### Generate query

$$
x_q
$$

### Ground truth

$$
y_q=ax_q+b
$$

### Frozen baseline

Prediction without adaptation.

### Parameter adaptation

Perform gradient updates.

### State adaptation

Update state.

### Measure

* prediction,
* accuracy,
* parameter delta,
* state delta,
* adaptation steps,
* runtime.

This is **not the final artifact**.

It is the scientific instrument that validates our research question.

---

# 30. Expected result of the first experiment

We should ideally observe something like:

```text
                     Frozen     Parameter-TTA    State
Task accuracy          X              ↑           ↑
Parameter change      0              >0           0
State change           —              —           >0
Adaptation cost        low          higher       moderate
Retention              ...           ...          ...
```

But critically:

**We do not predetermine the numbers.**

We formulate the experiment and let the data determine what survives.

---

# 31. The second experiment should target interference

Notebook:

```text
experiments/002_adaptation_interference.ipynb
```

Sequence:

```text
Task A
 ↓
adapt
 ↓
Task B
 ↓
adapt
 ↓
test Task A
```

Measure:

$$
R_A
$$

Then vary:

$$
d_s
$$

and:

$$
I
$$

This gives us the limitation experiment.

---

# 32. The third experiment should target demonstration efficiency

Notebook:

```text
experiments/003_demonstration_scaling.ipynb
```

Sweep:

$$
N_D=1,\ldots,N_{\max}
$$

Measure accuracy.

This is ideal for the interactive product because it will respond quickly after precomputation.

---

# 33. The fourth experiment should target adaptation compute

Notebook:

```text
experiments/004_adaptation_compute.ipynb
```

Sweep:

$$
K
$$

Measure:

$$
Accuracy(K)
$$

and

$$
Cost(K)
$$

This potentially connects our product to inference-time scaling without changing our central topic.

The Pathway brief specifically highlights inference-time compute allocation as a related concept and mentions BDH-CQ's effort levels. 

---

# 34. Phase 1 should end with the experiment matrix

The final matrix should look roughly like:

| Experiment            | Research question                  | Variable            | Baselines    | Metric             | Live?       | Learner-facing? |
| --------------------- | ---------------------------------- | ------------------- | ------------ | ------------------ | ----------- | --------------- |
| Hidden-rule learning  | Can task be acquired?              | adaptation strategy | frozen       | accuracy           | Yes         | Yes             |
| Demonstration scaling | How much evidence?                 | \(N_D\)             | all          | accuracy           | Cached/live | Yes             |
| State capacity        | How much memory?                   | \(d_s\)             | state models | accuracy/retention | Cached      | Yes             |
| Adaptation steps      | Does more compute help?            | \(K\)               | state/TTA    | accuracy/cost      | Cached      | Yes             |
| Interference          | Can old task survive?              | \(I\)               | state/TTA    | retention          | Yes         | Yes             |
| Noise                 | Robustness?                        | noise               | all          | accuracy           | Cached      | Maybe           |
| ARC-like transfer     | Does this extend?                  | rule family         | selected     | exact-match        | Precomputed | Yes             |
| BDH comparison        | How does BDH embody related ideas? | architecture        | —            | evidence           | Precomputed | Yes             |

---

# 35. What Phase 1 should NOT produce

This is just as important.

At this stage we should **not** have:

* polished landing page,
* elaborate animations,
* marketing copy,
* dozens of UI screens,
* arbitrary visualizations,
* production backend,
* massive model training,
* generic chatbot,
* presentation slides.

We want **scientific certainty before product implementation**.

---

# 36. Phase 1 acceptance review

At the end, conduct a formal review.

Have one team member who did not lead the literature work read only the Phase 1 documents and answer:

### Science

**What exactly is our claim?**

**What would falsify it?**

**What is the difference between ICL and TTT?**

**What exactly does our state model change?**

**What exactly does parameter TTT change?**

### BDH

**Why is BDH relevant?**

**Why is BDH-CQ relevant?**

**What is officially documented?**

**What have we implemented ourselves?**

### Experiment

**What is the independent variable?**

**What is the dependent variable?**

**What is ground truth?**

**What happens if the result contradicts our hypothesis?**

### Education

**Who is the learner?**

**What should they understand after 10 minutes?**

**What will they manipulate?**

**What will they observe?**

**What failure will they experience?**

If anyone cannot answer these without referring to the researcher who wrote the documents, Phase 1 isn't complete.

---

# 37. Final Phase 1 folder

I would have this structure:

```text
research/
│
├── scope/
│   └── scientific_scope.md
│
├── terminology/
│   ├── terminology.md
│   └── concept_map.pdf
│
├── literature/
│   ├── evidence_matrix.csv
│   ├── paper_notes/
│   └── research_timeline.md
│
├── bdh/
│   ├── bdh_dossier.md
│   ├── bdhcq_dossier.md
│   ├── equations/
│   └── evidence/
│
├── claim/
│   ├── central_claim.md
│   └── falsification_criteria.md
│
├── education/
│   ├── learner_spec.md
│   └── learning_objectives.md
│
├── experiments/
│   ├── experimental_design.md
│   ├── hypotheses.md
│   ├── experiment_matrix.csv
│   └── notebooks/
│
├── system/
│   └── computational_substrate.md
│
└── review/
    └── go_no_go.md
```

This becomes the scientific backbone of the project.

---

# 38. The Phase 1 → Phase 2 gate

We move to Phase 2 only when we can demonstrate:

$$
\boxed{
D
\rightarrow
\text{adaptation}
\rightarrow
Q
\rightarrow
\hat{Y}
\rightarrow
Y
}
$$

for at least one controlled task family, using at least two genuinely different adaptation mechanisms, with measurable internal changes.

And we must know:

$$
\boxed{
\Delta\theta
\quad\text{and}\quad
\Delta s
}
$$

so we can determine **where adaptation actually occurred**.

At that point, Phase 2 is not speculative anymore.

We have a scientific phenomenon to build the product around.

---

# 39. The most important deliverable of Phase 1

Although there are nine deliverables, the real output is this:

# **A scientifically defensible experiment specification**

It should read something like:

> We study whether a model can acquire an unseen task rule from demonstrations using different inference-time adaptation substrates. We compare frozen-context inference, parameter-updating TTT, and recurrent-state adaptation on controlled task families with exact ground truth. We measure adaptation accuracy, state/parameter change, inference cost, and retention under interference. We then connect the state-based mechanism to the documented memory mechanism of BDH and BDH-CQ, explicitly distinguishing our educational implementation from the official systems.

When we can write a paragraph like that and defend **every sentence with either a primary source or our own experiment**, Phase 1 has succeeded.

And that is the standard I would set. The Pathway brief rewards exactly this combination: technical correctness/depth, ownership, learning effectiveness, a real computational substrate, substantive BDH integration, and scientific evidence discipline. 

**So Phase 1 is essentially our mini research program. Phase 2 should only begin once that research program has produced a validated computational phenomenon worth teaching.**

[1]: https://proceedings.mlr.press/v267/sun25h.html?utm_source=chatgpt.com "Learning to (Learn at Test Time): RNNs with Expressive Hidden States"
[2]: https://arxiv.org/abs/2509.26507?utm_source=chatgpt.com "The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain"
[3]: https://arxiv.org/abs/2608.09888?utm_source=chatgpt.com "BDH-CQ: In-Context Learning with Recurrent Latent Reasoning"
[4]: https://research.google/pubs/transformers-learn-in-context-by-gradient-descent/?utm_source=chatgpt.com "Transformers learn in-context by gradient descent"
[5]: https://proceedings.iclr.cc/paper_files/paper/2024/hash/f02f1185b97518ab5bd7ebde466992d3-Abstract-Conference.html?utm_source=chatgpt.com "Test-Time Training on Nearest Neighbors for Large Language Models"
[6]: https://proceedings.mlr.press/v267/akyurek25a.html?utm_source=chatgpt.com "The Surprising Effectiveness of Test-Time Training for Few-Shot Learning"
[7]: https://arcprize.org/blog/arc-agi-2-technical-report?utm_source=chatgpt.com "ARC-AGI-2 A New Challenge for Frontier AI Reasoning Systems | ARC Prize"
[8]: https://proceedings.mlr.press/v202/von-oswald23a.html?utm_source=chatgpt.com "Transformers Learn In-Context by Gradient Descent"
