# Phase 3 — Turn the Research Engine into a Research-Grade Learning Experience

Phase 2 answers:

> **“Can we make the science work?”**

Phase 3 answers:

> **“Can a technically competent learner use that real system to discover the science themselves?”**

This phase is where we build the **actual Pathway artifact**. But the key is that we are not making a UI around the research engine. We are designing an **experiment-driven educational system** whose interface is itself part of the scientific communication.

That distinction matters because the brief explicitly says the substrate should already behave before the learner acts, every control should map to a real variable, important state should be visible, truth should be shown beside estimate, feedback should be fast, and the learner should be guided before entering the sandbox. 

There is also useful external evidence supporting this philosophy: research on interactive ML education finds that interaction can improve learning, but the effect depends heavily on the design of the interaction rather than simply adding more controls. One study found constrained exploration could outperform open exploration, while a 2025 study of interactive ML visualizations found learning gains differed by concept rather than being universally improved by interactivity. ([ScienceDirect][1])

So **Phase 3 is not “make it interactive.” It is “design the interaction so that the learner's actions constitute an experiment.”**

---

# 1. Phase 3 Objective

By the end of Phase 3, we want a public-ready educational experience in which a learner can:

```text
Encounter an unseen task
        ↓
Make a prediction
        ↓
Choose/manipulate a real adaptation variable
        ↓
Run real computation
        ↓
Observe internal state + output
        ↓
Compare with ground truth
        ↓
Form an explanation
        ↓
Stress the system
        ↓
Observe failure/interference
        ↓
Connect the phenomenon to BDH / BDH-CQ
        ↓
Solve a new unseen task
```

The important part is that **the learner creates evidence**.

The system isn't simply telling them:

> “State-based adaptation works.”

It lets them discover:

> “I changed the number of demonstrations, the model changed its state, its parameters remained fixed, and its ability to solve the unseen task changed.”

That is the level of interaction the Pathway brief is asking for. 

---

# 2. Phase 3 Deliverables

I would make Phase 3 produce **12 formal deliverables**.

| ID        | Deliverable                       | Purpose                                           |
| --------- | --------------------------------- | ------------------------------------------------- |
| **D3.1**  | Learning Experience Specification | Defines the pedagogical journey                   |
| **D3.2**  | Interaction Model                 | Maps every learner action to a real variable      |
| **D3.3**  | Visual Language/System            | Defines how computation and state are represented |
| **D3.4**  | Flagship 60-Second Experience     | Core learning moment                              |
| **D3.5**  | Guided Learning Journey           | Full narrative flow                               |
| **D3.6**  | Interactive Experiment Lab        | Learner-facing research environment               |
| **D3.7**  | Failure/Stress Lab                | Makes limitations experimentally visible          |
| **D3.8**  | BDH/BDH-CQ Learning Module        | Integrates the frontier case study                |
| **D3.9**  | Prediction & Assessment System    | Tests conceptual understanding                    |
| **D3.10** | Transparency/Provenance Layer     | Distinguishes live/precomputed/etc.               |
| **D3.11** | Usability + Learning Evaluation   | Tests whether the artifact actually teaches       |
| **D3.12** | Public Release Candidate          | Stable, deployable Pathway artifact               |

---

# 3. D3.1 — Learning Experience Specification

Create:

```text
research/education/
└── learning_experience_spec.md
```

This document defines the experience **before implementation**.

It should answer:

> What should the learner think, see, predict, discover, and understand at every stage?

---

# 4. Start with the learner's misconception

A very strong educational experience often begins with the learner's likely incorrect intuition.

For our project, one likely misconception is:

> **“If the model learns a new task, it must have changed its weights.”**

The experience should not immediately correct this.

Instead:

### Step 1

Let the learner encounter an unseen task.

### Step 2

Let the system succeed after seeing demonstrations.

### Step 3

Ask:

> **“What changed?”**

Now the learner has a reason to care.

This is much stronger than beginning with:

> “Welcome to Test-Time Adaptation.”

---

# 5. Define the learning progression

The learner should pass through these conceptual states:

```text
STATE 0
"I don't know how this model learns."

STATE 1
"It learned the task."

STATE 2
"Something inside the model changed."

STATE 3
"I can see what changed."

STATE 4
"I can manipulate that change."

STATE 5
"I can predict the effect."

STATE 6
"I can make it fail."

STATE 7
"I understand the trade-off."

STATE 8
"I can recognize the same design idea in BDH-CQ."

STATE 9
"I can transfer the concept to a new task."
```

That becomes the **learning state machine** for the interface.

---

# 6. D3.2 — Interaction Model

Every UI control needs a scientific mapping.

Create:

```text
research/education/interaction_model.md
```

For every interaction:

| UI element          | Scientific variable | Computation affected | Observable output  |
| ------------------- | ------------------- | -------------------- | ------------------ |
| Demonstration count | \(N_D\)             | adaptation evidence  | accuracy           |
| State size          | \(d_s\)             | state capacity       | accuracy/retention |
| Adaptation steps    | \(K\)               | test-time compute    | accuracy/latency   |
| Noise               | \(\epsilon\)        | input quality        | robustness         |
| Interference        | \(I\)               | competing task info  | retention          |
| Adaptation strategy | method              | substrate            | performance        |

This prevents the common failure mode where an interface has many attractive sliders that don't mean anything.

The Pathway brief specifically requires every control to map to a real variable. 

---

# 7. Don't give the learner all controls immediately

The product should follow:

# **Guide → Reveal → Manipulate → Sandbox**

The brief explicitly recommends this. 

So the first screen might expose only:

**Demonstrations**

and:

**Adapt**

Later:

**State size**

appears.

Later:

**Interference**

appears.

Finally:

**Full laboratory mode**

opens everything.

This keeps cognitive load manageable.

---

# 8. D3.3 — Visual language

Create:

```text
design/
├── visual_system.md
├── state_visualization.md
└── interaction_patterns.md
```

The visual language should communicate **causality**, not decoration.

For example:

```text
DEMONSTRATION
     │
     ▼
 ┌─────────┐
 │ STATE   │
 │ ΔS = ...│
 └────┬────┘
      │
      ▼
    QUERY
      │
      ▼
 PREDICTION
      │
      ▼
GROUND TRUTH
```

The learner should immediately know:

**what entered**

**what changed**

**what came out**

---

# 9. State visualization

This will probably be the most technically delicate visualization.

We must never pretend a latent vector is inherently interpretable.

If:

$$
s\in\mathbb R^{32}
$$

then visualizing it as 32 meaningful “concept neurons” would be scientifically unjustified unless we have evidence for those semantics.

Instead, we can show measurable quantities such as:

* state norm,
* state difference,
* projection,
* similarity,
* task-conditioned trajectories,
* specific known features.

For example:

$$
\Delta s =
\|s_{after}-s_{before}\|
$$

and:

$$
sim(s_A,s_B)
$$

This is honest.

---

# 10. The flagship interaction

# **“Teach the Model a New Rule”**

This is the central experience.

It should load immediately.

The Pathway brief specifically says not to start with a blank canvas or Run button; open with a meaningful preset already running. 

---

# 11. Screen 1 — The challenge

Display:

> **This task rule was not shown during training.**

Then:

```text
Example 1
Input → Output

Example 2
Input → Output

Example 3
Input → Output
```

And:

> **What should the model do with the new query?**

---

# 12. Screen 2 — Prediction

Before revealing the model result:

> **Make your prediction.**

This is important.

The learner is now forming a hypothesis.

The interaction is no longer passive.

---

# 13. Screen 3 — Actual computation

Run the real model.

Show:

```text
Your prediction
     vs
Model output
     vs
Ground truth
```

Exactly matching the brief's **truth beside estimate** requirement. 

---

# 14. Screen 4 — Reveal adaptation

Now show:

```text
WHAT CHANGED?

Parameters
████████████████
Δθ = 0

State
████████████████
Δs = 4.81
```

Depending on the selected experiment.

The learner can literally observe:

$$
\Delta\theta=0
$$

and:

$$
\Delta s\neq0
$$

This is the first major “aha.”

---

# 15. Screen 5 — Make the learner manipulate it

Now introduce:

### Demonstrations

```text
1  ──────●──────── 8
```

The learner changes it.

The model reruns.

The result updates.

No fake interpolation.

Actual experiment.

---

# 16. Screen 6 — Ask for prediction again

Before they move the slider:

> **Will adding demonstrations improve, hurt, or leave performance unchanged?**

Then:

**Predict**

then:

**Run**

This introduces a prediction–feedback loop.

Interactive-learning research supports this kind of purposeful interaction rather than simply increasing the number of controls. ([ScienceDirect][1])

---

# 17. D3.4 — The 60-second experience

We should formally test whether this sequence can be completed in about one minute.

Target:

### 0–10 sec

See unfamiliar task.

### 10–20 sec

See successful adaptation.

### 20–35 sec

Inspect what changed.

### 35–45 sec

Manipulate demonstrations.

### 45–55 sec

Observe consequence.

### 55–60 sec

Answer:

> **Where did the new rule go?**

If the learner can answer correctly, we have passed the core test.

The Pathway brief explicitly highlights both a “sixty-second test” and the value of an insight that can be reproduced in under a minute.  

---

# 18. D3.5 — Full guided learning journey

The entire application can now grow outward from the flagship experiment.

I recommend the following sequence.

---

# MODULE 1 — The Impossible-Looking Task

The learner sees:

> **The model has never seen this rule.**

They watch it adapt.

No equations yet.

Goal:

**Create curiosity.**

---

# MODULE 2 — What Does “Learn” Mean?

Explain the distinction between:

**training**

and:

**inference**

and:

**inference-time adaptation**

Use a timeline:

```text
TRAINING
───────────────►
parameters learned

             INFERENCE
             ─────────────►
             new task arrives
```

---

# MODULE 3 — Three Places the Rule Could Live

Present three mechanisms:

```text
CONTEXT
STATE
PARAMETERS
```

The learner can switch among them.

This becomes our core conceptual taxonomy.

---

# MODULE 4 — Parameter Adaptation

Show:

$$
\theta'=
\theta-\eta\nabla_\theta L
$$

Then visualize:

```text
loss
 ↓
gradient
 ↓
parameter update
 ↓
new prediction
```

The learner can adjust:

$$
\eta
$$

and:

$$
K
$$

but only if those variables serve the lesson.

---

# MODULE 5 — Recurrent State Adaptation

Now:

$$
s_t=F_\theta(s_{t-1},x_t)
$$

and:

$$
\theta=\text{fixed}
$$

Show demonstrations entering sequentially and state changing.

---

# MODULE 6 — The Memory Question

Ask:

> **What happens when the state is too small?**

Now introduce:

$$
d_s
$$

and let the learner change it.

This makes memory capacity experimentally visible.

---

# MODULE 7 — Interference

Teach:

**Task A**

then:

**Task B**

then return to:

**Task A**

Display:

```text
Task A accuracy
Before B: 92%
After B:  61%

Retention dropped by 31 points.
```

Then explain the mechanism.

---

# MODULE 8 — Compute

Let:

$$
K
$$

vary.

Show:

```text
Adaptation compute ↑
       │
       ├── accuracy
       └── latency
```

This introduces the adaptation-quality/cost trade-off.

---

# MODULE 9 — Break the System

Give:

* noisy examples,
* conflicting examples,
* insufficient demonstrations,
* complex transformations.

Let the learner discover failure.

---

# MODULE 10 — BDH

Only after all of the above:

> **“Now let's look at a frontier architecture built around evolving memory.”**

Introduce BDH.

---

# MODULE 11 — BDH-CQ

Now:

> **“What happens when this idea becomes part of in-context learning and latent reasoning?”**

Introduce BDH-CQ.

The paper reports inference-time recurrent memory updates followed by iterative latent reasoning without changing parameters during that inference process. That is exactly the connection we should expose, while keeping official BDH-CQ behavior separate from our own substrate. ([arxiv](https://arxiv.org/abs/2608.09888?utm_source=chatgpt.com))

---

# MODULE 12 — Final Challenge

Give a completely new task.

No guidance.

Ask:

> **Which adaptation mechanism will perform best?**

Then run.

The learner must explain the result.

This tests transfer.

---

# 19. D3.6 — Interactive Experiment Lab

After the guided journey, unlock the full lab.

This is the “sandbox” portion recommended by the brief. 

Layout:

```text
┌─────────────────────────────────────────────────┐
│ TASK                                            │
│ [Generate New Task]                             │
├───────────────────────┬─────────────────────────┤
│ DEMONSTRATIONS        │ MODEL                   │
│                       │                         │
│ 1 2 3 4 5             │ Frozen                  │
│                       │ Parameter TTA           │
│ RULE COMPLEXITY       │ Recurrent State        │
│ [─────●────]          │                         │
├───────────────────────┼─────────────────────────┤
│ STATE                  │ OUTPUT                  │
│                       │                         │
│ before → after        │ prediction              │
│                       │ ground truth             │
├───────────────────────┴─────────────────────────┤
│ METRICS                                         │
│ accuracy | Δstate | Δparameters | latency      │
└─────────────────────────────────────────────────┘
```

---

# 20. But don't make it a dashboard

The lab should still be guided by scientific questions.

Instead of:

> **STATE DIMENSION: 32**

say:

> **How much adaptive memory does the model need?**

Then expose the slider.

Instead of:

> **INTERFERENCE: 0.63**

say:

> **How strongly should the new task compete with the old one?**

The UI should expose the **scientific meaning** of the variable.

---

# 21. D3.7 — Failure / Stress Lab

This deserves its own module.

Because the brief explicitly values limitations and failure cases. 

Give the user a sequence of increasingly difficult tests.

### Stress 1

Fewer demonstrations.

### Stress 2

More noise.

### Stress 3

More complex rules.

### Stress 4

Competing tasks.

### Stress 5

Repeated switching.

The user sees the degradation curve.

---

# 22. Make the failure predictive

Before running each stress test:

> **What do you think will happen?**

Choices:

**Improve**

**Stay similar**

**Degrade**

Then run.

This creates a measurable learning assessment.

---

# 23. D3.8 — BDH learning module

The BDH section should not feel like:

> “Here is another architecture.”

Instead:

> **“You just saw adaptive state. Here's how a frontier architecture makes memory part of its computational fabric.”**

---

# 24. BDH visual structure

Start broad:

```text
BDH
│
├── neurons
├── synapses
├── local computation
├── sparse activity
└── evolving memory
```

Then zoom:

```text
activity
   ↓
synaptic state
   ↓
local update
   ↓
new activity
```

The Pathway brief specifically asks for a concrete equation/diagram/live experiment/precomputed result here. 

---

# 25. BDH equation interaction

Rather than displaying a static equation:

$$
S_{t+1}=S_t+\eta xy^\top
$$

let the learner change:

$$
\eta
$$

and see the magnitude of the update change.

But we must clearly label this as:

> **Educational implementation inspired by the published BDH formulation**

unless we're literally running the corresponding official/public implementation.

---

# 26. BDH-CQ integration

Show:

```text
demonstration
       ↓
recurrent memory
       ↓
query
       ↓
latent recurrent computation
       ↓
answer
```

Then explicitly show:

```text
MODEL PARAMETERS
UNCHANGED

INFERENCE-TIME MEMORY
UPDATED
```

where supported by the published model description.

This is where our controlled experiment and the frontier system finally connect.

---

# 27. D3.9 — Prediction + assessment system

This is essential.

We shouldn't merely ask:

> “Did you enjoy it?”

We need to test whether the learner understood.

Create a lightweight assessment engine.

---

# 28. Assessment type 1 — Prediction

Before an experiment:

> What will happen?

Then compare.

---

# 29. Assessment type 2 — Mechanism

Ask:

> What changed?

Options:

**Parameters**

**Context**

**Recurrent state**

**Nothing**

---

# 30. Assessment type 3 — Trade-off

Ask:

> What happens when state capacity becomes insufficient?

Not merely a multiple-choice memorization question.

Show a novel scenario.

---

# 31. Assessment type 4 — Transfer

Give a completely new task.

Ask the learner to predict:

* whether adaptation will work,
* which mechanism is likely to perform best,
* what the failure mode will be.

This is the strongest assessment.

---

# 32. Assessment type 5 — Explain in own words

The Pathway brief explicitly requires learners to explain the concept back in their own words. 

We can ask:

> **In 2–3 sentences, explain where the new task information is stored in the state-based system and what happens when another task interferes with it.**

This response can be evaluated manually during our learner study, rather than pretending an LLM is an objective educational assessment.

---

# 33. D3.10 — Transparency layer

Every experiment result should carry a badge:

### LIVE

Computed now.

### PRECOMPUTED

Computed earlier from the actual research engine.

### SYNTHETIC

Task was procedurally generated.

### ILLUSTRATIVE

Conceptual diagram, not model output.

This should be visible, not hidden in the README.

The Pathway brief explicitly requires this distinction. 

---

# 34. Provenance drawer

Every result could have:

> **Experiment details**

Opening it shows:

```text
Experiment ID
Model
Task generator
Configuration
Seed
Commit
Execution type
Source
```

This gives the learner and judges scientific transparency.

---

# 35. D3.11 — Learning evaluation

This is where Phase 3 becomes significantly stronger.

We should run an actual learner study.

There is recent evidence that interactive educational platforms can improve outcomes relative to static material, but effects are not universal, reinforcing the need to actually evaluate the design instead of assuming interactivity works. ([Google Research][2])

---

# 36. Participant profile

Target:

**ML-capable students / engineers / researchers**

who satisfy our prerequisites but are unfamiliar with this specific topic.

---

# 37. Pre-test

Five to eight conceptual questions.

Examples:

> Can a model learn a task without updating its persistent weights?

> What does TTT change?

> What does recurrent state change?

> What causes interference?

> What does more adaptation compute buy?

---

# 38. Interaction

Give them:

**10–15 minutes**

with minimal verbal assistance.

Record:

* path taken,
* experiments used,
* predictions,
* failures,
* completion,
* time.

---

# 39. Post-test

Use structurally similar but not identical questions.

Measure:

$$
LearningGain =
PostScore-PreScore
$$

---

# 40. Transfer test

Give an unseen situation.

This matters more than memorized definitions.

Measure:

$$
TransferScore
$$

---

# 41. Misconception analysis

Track whether the learner moves from:

> “learning requires weight changes”

to:

> “adaptation can occur through context/state without persistent parameter updates.”

Also track subtler misconceptions:

* treating state as permanent weights,
* conflating ordinary recurrence with TTT,
* believing more compute always improves performance,
* interpreting latent state dimensions as human-readable concepts.

These are exactly the kinds of misconceptions our artifact should be designed to prevent.

---

# 42. Design testing

We should test the UI independently from learning.

Measure:

* Can users find the main interaction?
* Do they know what a control does?
* Do they know whether the result is live?
* Do they understand what changed?
* Do they distinguish model prediction from ground truth?
* Do they understand when an experiment has finished?

The Pathway brief's craft criterion includes accessibility, mobile usability, loading behavior and robustness. 

---

# 43. D3.12 — Public release candidate

At the end of Phase 3, we should have:

```text
PUBLIC URL
   │
   ├── Guided Experience
   ├── Interactive Lab
   ├── Stress Lab
   ├── BDH
   ├── BDH-CQ
   └── Final Challenge
```

No sign-in.

No dead-end pages.

No fake loading.

No unexplained graphs.

No “coming soon.”

---

# 44. Performance architecture

The brief demands controls respond in under one second. 

Therefore:

### Live small model

For fast experiments.

### Cached research runs

For expensive models.

### Web worker/background execution

Where appropriate.

### Preloaded initial state

So the first interaction isn't waiting for model initialization.

### Streaming only where useful

Don't make every interaction stream just because it's visually interesting.

---

# 45. Important UX principle: never make the learner wait to discover the core concept

The initial experiment should already be computed or extremely fast.

For heavy research results:

```text
PRECOMPUTED RESULT
```

must appear immediately.

The user can then change selected parameters that map to cached result families.

That satisfies the brief's fast-feedback requirement without falsifying computation.

---

# 46. Responsive/mobile design

The Pathway brief specifically scores mobile usability. 

So don't design desktop-first and shrink afterward.

The central experiment should work on a phone:

```text
TASK
↓
DEMONSTRATIONS
↓
PREDICT
↓
ADAPT
↓
OUTPUT
↓
GROUND TRUTH
↓
STATE CHANGE
```

Side-by-side desktop comparisons can collapse into sequential cards.

---

# 47. Accessibility

At minimum:

* keyboard navigation,
* readable equations,
* text equivalents for charts,
* not relying solely on color,
* accessible labels for sliders,
* sufficient contrast,
* reduced-motion option,
* screen-reader descriptions for critical states.

This contributes to the craft/robustness requirement. 

---

# 48. Visual honesty

One of the biggest dangers is making the visualization so beautiful that learners believe we know more than we actually do.

For example:

### Bad

A latent vector rendered as:

```text
"RULE MEMORY"
"OBJECT DETECTOR"
"REASONING NEURON"
```

without evidence.

### Good

```text
STATE PROJECTION
Δstate = ...

Cosine similarity
Task A ↔ current state = 0.82
```

and:

> “This visualization shows a measured state statistic; it is not a semantic interpretation of individual latent dimensions.”

That is scientific communication.

---

# 49. The interaction should expose causality

A learner should be able to see:

```text
I changed X
      ↓
model computation changed
      ↓
observable Y changed
```

This is more important than adding sophisticated animation.

The interactive-ML literature similarly emphasizes interaction as a mechanism for helping users understand/control models rather than merely making visualizations more engaging. ([PubMed Central (PMC)][3])

---

# 50. Avoid the “slider dashboard” failure mode

We should impose a hard rule:

> **If removing a control doesn't weaken the scientific lesson, remove the control.**

That directly implements the Pathway instruction to cut decorative sliders. 

---

# 51. Phase 3 engineering architecture

At this point:

```text
                  LEARNING EXPERIENCE
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
     Guided             Lab              Assessment
        │                 │                  │
        └─────────────────┼──────────────────┘
                          ▼
                    EXPERIMENT API
                          │
                   ┌──────┼──────┐
                   ▼      ▼      ▼
                LIVE   CACHED   GT
                MODEL  RESULTS  ENGINE
                          │
                          ▼
                   METADATA LAYER
                          │
              ┌───────────┼────────────┐
              ▼           ▼            ▼
            LIVE      PRECOMPUTED   SYNTHETIC
```

The metadata layer becomes extremely important because the UI needs to communicate evidence status.

---

# 52. Frontend state model

The learner experience itself should be stateful.

For example:

```text id="rlx9jz"
lesson_stage
current_task
prediction
selected_strategy
experiment_config
experiment_result
ground_truth
telemetry
assessment_state
```

But don't persist sensitive/user-identifying information unnecessarily.

For the learner study, use anonymous session IDs.

---

# 53. Experiment result schema

Every result should look conceptually like:

```json
{
  "experiment_id": "...",
  "task_id": "...",
  "strategy": "recurrent_state",
  "prediction": "...",
  "ground_truth": "...",
  "accuracy": 1,
  "state_delta": 4.83,
  "parameter_delta": 0.0,
  "latency_ms": 120,
  "execution_type": "live",
  "seed": 42
}
```

That makes the frontend consume structured scientific output instead of custom ad hoc data.

---

# 54. The UI should not contain scientific logic

Bad:

```text
if slider > 50:
   show "memory failed"
```

Good:

```text
experiment engine
       ↓
actual model result
       ↓
UI renders result
```

This is essential.

---

# 55. Phase 3 testing stages

Don't wait until the whole product is built.

## Test 1 — Prototype

Only flagship experiment.

## Test 2 — Guided journey

First three modules.

## Test 3 — Complete learning journey.

## Test 4 — Full sandbox.

## Test 5 — BDH integration.

## Test 6 — Mobile.

## Test 7 — Learning study.

Each stage gets tested before the next is built.

---

# 56. User-testing protocol

For each participant:

### Step 1

Say only:

> “Explore this.”

Don't explain the science.

### Step 2

Observe whether they discover the primary control.

### Step 3

Ask:

> “What do you think just happened?”

### Step 4

Continue.

### Step 5

At the end:

> “Where does the new task information live in the state-based system?”

This identifies whether the UI itself teaches.

---

# 57. Failure analysis from testing

If a user says:

> “The model learned because you retrained it.”

then the interface failed.

If they say:

> “The state is basically the model weights.”

then the visualization/explanation failed.

If they say:

> “I changed the slider because it looked interesting.”

then the control mapping failed.

These are actionable design failures.

---

# 58. The “one-minute truth test”

At the end of early user testing, ask:

> **Without looking back at the explanation, tell me what changing the number of demonstrations did and why.**

If the user can answer correctly after interacting, the core experience works.

If not, don't add more text.

Fix the experiment.

---

# 59. BDH module acceptance criteria

The BDH section passes only if a user can answer:

### What is BDH?

A brain-inspired Post-Transformer architecture with evolving memory/synaptic mechanisms.

### Why is it relevant?

Because its design uses adaptive internal memory as part of computation.

### What exactly changes?

The relevant state/synaptic memory, according to the documented formulation.

### Is our implementation official BDH?

No, unless it actually is.

### What does BDH-CQ add?

Inference-time recurrent memory combined with latent reasoning.

The Pathway brief explicitly demands that the BDH module be substantive, sourced, and clear about exactly what changes. 

---

# 60. A major feature I recommend: “Show me the mechanism”

Every major experiment should have a toggle:

> **Explain what just happened**

When opened:

```text
DEMONSTRATION
       ↓
LOSS
       ↓
ADAPTATION UPDATE
       ↓
STATE / PARAMETERS
       ↓
QUERY
       ↓
OUTPUT
```

The learner can progressively move from:

**black box → mechanism**

without forcing every learner to read equations immediately.

---

# 61. Another major feature: “Challenge my prediction”

This should become a recurring interaction pattern.

Before every important experiment:

> **Predict**

After:

> **Reveal**

This will make the product feel like an actual scientific laboratory.

It also gives us behavioral evidence that the learner is building a mental model.

---

# 62. The product's visual hierarchy

The interface should prioritize:

### 1. Current task

What am I solving?

### 2. Action

What can I change?

### 3. State

What changed?

### 4. Result

What happened?

### 5. Truth

Was it correct?

### 6. Explanation

Why?

Everything else is secondary.

---

# 63. Don't hide the ground truth at the bottom

The Pathway brief explicitly emphasizes **truth beside estimate**. 

So:

```text
MODEL
Output: B

GROUND TRUTH
B

✓ Correct
```

not:

```text
Model output
...
...
...
scroll
...
ground truth
```

The comparison is the pedagogical object.

---

# 64. Don't over-animate

Animations should communicate actual computation.

For example:

```text
demonstration
   ↓
state update
   ↓
query
```

Good.

But:

> “A glowing neuron discovers the concept!”

Bad unless backed by measured behavior.

The brief explicitly rejects illustrative animation being presented as live model behavior. 

---

# 65. Phase 3 output should include an internal design report

Create:

```text
docs/
└── phase3_design_report.md
```

Include:

* learning theory rationale,
* user journey,
* experiment mapping,
* interaction decisions,
* visualization decisions,
* accessibility,
* live/precomputed distinctions,
* testing results,
* revisions.

This is useful for the final README and defense.

---

# 66. Phase 3 Definition of Done

## Educational

☐ One coherent learning journey.

☐ One central scientific claim.

☐ Learner predicts before major experiments.

☐ Learner manipulates genuine variables.

☐ State is visible.

☐ Ground truth is visible.

☐ Failure mode is experienced.

☐ Learner encounters BDH naturally.

☐ Final transfer task exists.

☐ Learner can explain the concept in their own words.

---

## Computational

☐ All learner-facing experiments call the actual experiment engine.

☐ No fake result generation.

☐ No hidden parameter updates.

☐ State changes are real.

☐ Ground truth is generated independently.

☐ Result provenance is available.

---

## UX

☐ Initial experiment is already populated.

☐ Core interaction works within roughly one minute.

☐ No unnecessary controls.

☐ Feedback is fast.

☐ Mobile works.

☐ Accessibility basics work.

☐ No unexplained visual encodings.

---

## BDH

☐ BDH is embedded within the learning story.

☐ BDH-CQ is connected to the exact learned concept.

☐ Official vs independent implementation is explicit.

☐ Published evidence is cited.

☐ Evidence level is visible.

---

## Evaluation

☐ Pre-test exists.

☐ Post-test exists.

☐ Transfer test exists.

☐ Usability testing completed.

☐ Major misconceptions identified.

☐ Design changed based on evidence.

---

# 67. The Phase 3 exit test

I would give an unfamiliar technically competent learner the product with **zero verbal explanation**.

We watch them.

Within the first minute, they should:

1. notice the unseen task,
2. understand what to do,
3. make a prediction,
4. run the model,
5. see the ground truth,
6. inspect what changed,
7. answer the central question.

Then, after the full journey, they should be capable of explaining:

> **A model can adapt to a task at inference time without modifying its persistent parameters; depending on the architecture, task-specific information can be represented through context or an evolving state, with capacity, computation, and interference creating measurable trade-offs.**

The precise wording will ultimately depend on what Phase 2 actually establishes.

---

# 68. Phase 3 relationship to the Pathway rubric

This phase is where we directly attack **45 of the 100 points**:

### Learning effectiveness — 15

Claim → learner → narrative → predictions → transfer. 

### Interactive substrate — 15

Real computation → controls → visible state → truth vs estimate → fast feedback. 

### Craft / robustness — 10

UI, accessibility, mobile, loading, stability, provenance. 

### BDH integration — 10

The actual BDH module is developed here too, though its scientific foundations begin in Phase 1/2. 

That is why Phase 3 deserves almost as much rigor as the ML implementation itself.

---

# 69. The most important design principle for Phase 3

I would make this our internal rule:

> **Never tell the learner something that the learner could instead discover through a controlled experiment.**

Not everything should be discovered experimentally—definitions and context still need explanation—but whenever the central claim can be demonstrated, **show the evidence rather than merely asserting it**.

This is also consistent with the Pathway brief's emphasis on a real substrate and experimentation, and with the broader interactive-learning literature showing that carefully designed interaction can support understanding while simply adding interactivity is not enough. ([PubMed Central (PMC)][3])

---

# 70. Phase 3 final architecture

By the end, the product should effectively be:

```text
                       ADAPT
                         │
              ┌──────────┴──────────┐
              │                     │
          GUIDED PATH            LAB
              │                     │
              ▼                     ▼
       Discovery             Free Exploration
              │                     │
              └──────────┬──────────┘
                         ▼
                    EXPERIMENT
                         │
               ┌─────────┼─────────┐
               ▼         ▼         ▼
            Context    State    Parameters
               │         │         │
               └─────────┼─────────┘
                         ▼
                      QUERY
                         │
                         ▼
                    PREDICTION
                         │
                         ▼
                   GROUND TRUTH
                         │
                         ▼
                  INTERNAL STATE
                         │
                         ▼
                    STRESS TEST
                         │
                         ▼
                     FAILURE
                         │
                         ▼
                     BDH / CQ
                         │
                         ▼
                  TRANSFER TASK
                         │
                         ▼
                 LEARNER EXPLAINS
```

That is the product.

Not a dashboard.

Not an animation.

Not a paper summary.

Not a chatbot.

**A real computational laboratory wrapped in a carefully designed learning experience.**

And the key transition after Phase 3 is very clean:

**Phase 1:** We establish what is scientifically true and what we intend to teach.
**Phase 2:** We build and validate the actual computational machinery.
**Phase 3:** We make that machinery teachable, measurable, transparent, and usable.

Then **Phase 4 should be the BDH/BDH-CQ deep integration + research-grade benchmark/reproduction layer**, followed by the production hardening and final submission phases. That ordering keeps the product scientifically grounded rather than designing a polished educational shell around assumptions we haven't validated.

[1]: https://www.sciencedirect.com/science/article/pii/S0360131514002711?utm_source=chatgpt.com "When does higher degree of interaction lead to higher learning in visualizations? Exploring the role of ‘Interactivity Enriching Features’ - ScienceDirect"
[2]: https://research.google/pubs/an-experimental-evaluation-of-an-ai-powered-interactive-learning-platform/?utm_source=chatgpt.com "An experimental evaluation of an AI-powered interactive learning platform"
[3]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9995896/?utm_source=chatgpt.com "Leveraging explanations in interactive machine learning: An overview - PMC"
