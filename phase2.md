Yes. **Phase 2 is where the scientific specification becomes an actual experimental system.** We should treat it as a miniature ML research-engineering program, not “build a prototype.”

The goal is not yet to make the beautiful public website. The goal is to produce a **real computational substrate whose behavior is scientifically trustworthy enough that the final educational artifact can sit on top of it without faking anything**.

The Pathway brief is very explicit that the concept must genuinely behave inside the artifact, and that a real tiny model, replay of a real run, or live toy system is acceptable—but scripted animation presented as computation is not. It also requires meaningful manipulation, observable consequences, ground truth, and fast feedback. 

# PHASE 2 — BUILD AND VALIDATE THE SCIENTIFIC COMPUTATIONAL SUBSTRATE

## Phase 2 objective

At the end of Phase 2, we want to have a functioning research system that can answer:

> **Given a previously unseen task and demonstrations, can different inference-time adaptation mechanisms acquire the task, where does the acquired information live, what does it cost, and how well does it survive interference?**

The important phrase is **different mechanisms**.

We do not want a single model that “adapts.”

We want a controlled experimental environment in which the adaptation mechanism itself is an independent variable.

---

# 1. Phase 2 deliverables

I would define **10 formal deliverables**.

| ID        | Deliverable                         | What it proves                                                          |
| --------- | ----------------------------------- | ----------------------------------------------------------------------- |
| **D2.1**  | Reproducible experiment framework   | Experiments can be rerun exactly                                        |
| **D2.2**  | Controlled task generator           | We can create unseen tasks with exact ground truth                      |
| **D2.3**  | Frozen baseline                     | We know what happens without explicit adaptation                        |
| **D2.4**  | Parameter-TTA implementation        | We have real inference-time parameter adaptation                        |
| **D2.5**  | Recurrent-state adaptation model    | We have real state-based adaptation                                     |
| **D2.6**  | Optional learned-state/TTT model    | We distinguish simple recurrence from learned-state TTT                 |
| **D2.7**  | Measurement/telemetry system        | We can observe what changed                                             |
| **D2.8**  | Core experiment suite               | We can test acquisition, capacity, cost, and interference               |
| **D2.9**  | Reproducibility + validation report | Results are statistically and computationally trustworthy               |
| **D2.10** | Research prototype v1               | One end-to-end real experiment is ready to become the product substrate |

If D2.10 doesn't exist, we have not finished Phase 2.

---

# 2. D2.1 — Reproducible experiment framework

Create:

```text
experiments/
├── configs/
├── runners/
├── seeds/
├── outputs/
├── checkpoints/
└── analysis/
```

The experiment should be executable from a single configuration.

For example:

```yaml
task_family: linear_regression
model: recurrent_state_v1
adaptation: state
demonstrations: 4
state_dim: 32
adaptation_steps: 8
noise: 0.05
seed: 42
```

Then:

```bash
python run_experiment.py configs/exp_001.yaml
```

The result should contain:

```text
experiment_id
git_commit
config_hash
random_seed
model_version
task_generator_version
dataset_version
metrics
timing
hardware
```

This matters because later, when we show a graph in the public artifact, we need to know exactly where it came from.

---

# 3. Determinism and experiment identity

Every experiment needs an identity:

$$
ID = H(
\text{code},
\text{config},
\text{seed},
\text{task generator},
\text{model}
)
$$

We should record:

* random seed,
* PyTorch version,
* CUDA version where relevant,
* model checkpoint hash,
* task-generator version,
* configuration.

The purpose is not bureaucratic perfection.

It is so we never have:

> “I think that graph came from the earlier experiment.”

---

# 4. D2.2 — Controlled task generator

This is the foundation of the entire system.

Every episode should have:

$$
T=(R,D,Q,Y)
$$

where:

* \(R\): hidden task rule,
* \(D\): demonstrations,
* \(Q\): novel query,
* \(Y\): exact ground truth.

The model sees:

$$
D,Q
$$

but not \(R\) or \(Y\).

The evaluator has \(R,Y\).

This lets us ask:

> Did the model really acquire the rule?

rather than:

> Did the model produce something that looks reasonable?

---

# 5. Task generator requirements

It must generate:

### Novel tasks

The exact task rule shouldn't be repeated from training.

### Variable difficulty

We need difficulty to be parameterized rather than manually curated.

### Exact ground truth

No human judging.

### Controlled perturbation

We should independently control:

* noise,
* ambiguity,
* demonstration count,
* rule complexity,
* interference.

### Reproducibility

Given the same seed:

$$
Generator(seed)=same\ task
$$

---

# 6. Build task families incrementally

## Task Family 1 — Linear regression

Each episode samples:

$$
y=ax+b
$$

with new \(a,b\).

Demonstrations:

$$
(x_1,y_1),...,(x_k,y_k)
$$

Query:

$$
x_q
$$

Ground truth:

$$
y_q=ax_q+b
$$

### Why first?

Because the correct solution is mathematically known.

We can independently calculate:

* optimal parameters,
* adaptation error,
* convergence,
* generalization.

This is our scientific calibration environment.

---

# 7. Task Family 2 — Polynomial / nonlinear functions

Move to:

$$
y=f(x)
$$

where \(f\) comes from a controlled family.

Now we can test whether adaptation generalizes beyond simple linear fitting.

---

# 8. Task Family 3 — Symbolic transformations

Example:

```text
Input:  A B C
Output: B C D
```

The transformation differs per task.

This makes the notion of:

> “infer a new rule from examples”

far more intuitive.

---

# 9. Task Family 4 — Compositional rules

Generate:

$$
R=R_1 \circ R_2
$$

For example:

```text
reverse
→ offset
→ conditional replacement
```

Now the learner has to infer multiple interacting operations.

---

# 10. Task Family 5 — ARC-like tasks

Eventually introduce grid transformations.

Structure:

```text
Input grid → Output grid
Input grid → Output grid
Input grid → Output grid

           ↓

      hidden rule

           ↓

      novel input

           ↓

      predicted output
```

This connects our controlled laboratory to the task-acquisition regime used in contemporary reasoning research and BDH-CQ evaluation. BDH-CQ explicitly studies demonstration-driven transformation learning on ARC-style tasks. ([arxiv](https://arxiv.org/abs/2608.09888?utm_source=chatgpt.com))

---

# 11. Do not train everything on everything

This is critical.

For each task family, create:

### Meta-training distribution

Rules available during training.

### Adaptation distribution

Previously unseen specific rules.

### Evaluation distribution

Rules and combinations that are held out.

The model should not simply memorize our evaluation task generator.

Otherwise we cannot claim task acquisition.

---

# 12. D2.3 — Frozen baseline

Build the simplest legitimate baseline first.

$$
\hat y=f_\theta(D,Q)
$$

No explicit updates.

Record:

* prediction,
* accuracy,
* latency,
* context length,
* failure cases.

This answers:

> **How much can the pretrained/frozen computation do before adaptation?**

Every later model is compared against this.

---

# 13. D2.4 — Parameter-TTA model

Now implement genuine test-time parameter adaptation.

For a task:

$$
D=\{(x_i,y_i)\}_{i=1}^k
$$

compute:

$$
L_D(\theta)
=
\frac{1}{k}\sum_i
\ell(f_\theta(x_i),y_i)
$$

and update:

$$
\theta_{t+1}
=
\theta_t
-
\eta
\nabla_\theta L_D(\theta_t)
$$

Then evaluate on \(Q\).

This is not an animation.

The actual tensor parameters must change.

Measure:

$$
\Delta\theta=
\|\theta_{adapted}-\theta_{base}\|
$$

---

# 14. Important engineering decision: which parameters update?

We should test at least two configurations:

### Full adaptation

All selected parameters update.

### Adapter adaptation

Only a small parameter subset updates.

This lets us distinguish:

**capacity of the adaptation mechanism**

from

**raw number of changed parameters**.

However, only keep this if it contributes directly to our claim. Do not allow parameter variants to explode scope.

---

# 15. D2.5 — Recurrent-state adaptation

Implement:

$$
s_t=F_\theta(s_{t-1},x_t,y_t)
$$

with:

$$
\theta_{t+1}=\theta_t
$$

Then:

$$
\hat y=G_\theta(s_k,Q)
$$

The central property is:

$$
\Delta\theta=0
$$

while:

$$
\Delta s>0
$$

This gives us the cleanest computational demonstration of:

> **Task adaptation without persistent parameter modification.**

---

# 16. Important: ordinary RNN ≠ learned-state TTT

We must not blur these.

A basic RNN:

$$
s_t=f_\theta(s_{t-1},x_t)
$$

is not automatically a TTT-Linear/TTT-MLP-style learned-state system.

The latter treats the state as a more expressive learned computational object and updates it using a learning objective.

Sun et al.'s 2025 TTT work is particularly relevant here. ([proceedings.mlr.press](https://proceedings.mlr.press/v267/sun25h.html?utm_source=chatgpt.com))

---

# 17. D2.6 — Learned-state TTT implementation

This is optional but highly valuable.

We should implement a miniature version of the idea:

$$
S_{t+1}
=
S_t-
\eta\nabla_S
L_t(S_t)
$$

where \(S\) represents a small learned linear/MLP function.

Then compare:

```text
ordinary recurrent state
vs
learned adaptive state
```

This prevents our project from teaching a 2010s-era RNN and calling it modern TTT.

---

# 18. D2.7 — Measurement system

Every experiment must record **what changed**.

For parameter adaptation:

```text
parameter_norm_before
parameter_norm_after
parameter_delta
loss_before
loss_after
```

For recurrent-state adaptation:

```text
state_norm_before
state_norm_after
state_delta
state_projection
```

For predictions:

```text
prediction
ground_truth
accuracy
confidence
```

For compute:

```text
adaptation_steps
wall_clock_latency
memory
approx_compute
```

For task retention:

```text
accuracy_before_interference
accuracy_after_interference
retention_drop
```

---

# 19. The telemetry should not merely collect statistics

It should support visualization later.

For example:

$$
s_0
\rightarrow
s_1
\rightarrow
s_2
\rightarrow
s_3
$$

where each \(s_i\) corresponds to another demonstration.

That lets the final UI literally show:

> **The task information is changing the state after every demonstration.**

---

# 20. D2.8 — Core Experiment Suite

Now the research program begins.

I would define **seven primary experiments**.

---

# Experiment A — Can the model acquire an unseen rule?

### Question

Does adaptation improve performance on an unseen task?

### Independent variable

Adaptation mechanism.

### Conditions

* frozen,
* context/ICL,
* parameter TTA,
* recurrent state,
* optionally learned-state TTT.

### Metric

$$
A_{test}
$$

### Expected educational output

A simple:

```text
Before adaptation     31%
After adaptation      87%
```

with exact task-level examples.

---

# Experiment B — Demonstration efficiency

### Variable

$$
N_D
$$

Sweep:

$$
1,2,3,\ldots,K
$$

Measure:

$$
A(N_D)
$$

Question:

> How much evidence does the model need?

This will likely become one of the most useful learner-facing controls.

---

# Experiment C — Adaptation compute

### Variable

$$
K=\text{adaptation steps}
$$

Measure:

$$
A(K)
$$

and:

$$
Latency(K)
$$

Question:

> Does spending more computation at inference improve adaptation?

This connects to the Pathway brief's inference-time scaling theme. 

---

# Experiment D — State capacity

### Variable

$$
d_s
$$

Measure:

$$
A(d_s)
$$

and:

$$
R(d_s)
$$

Question:

> How much adaptive state is enough?

This can become an excellent interactive experiment because the physical size of the state is directly manipulable.

---

# Experiment E — Interference

Teach:

$$
A\rightarrow B\rightarrow A
$$

Measure:

$$
R_A
=
Accuracy(A_{after B})
$$

Question:

> Does learning something new damage what was learned earlier?

This becomes our core failure-mode experiment.

---

# Experiment F — Demonstration noise

Introduce:

$$
\epsilon
$$

into demonstrations.

Measure:

$$
A(\epsilon)
$$

Question:

> How robust is inference-time adaptation to imperfect evidence?

---

# Experiment G — Task complexity

Increase rule complexity.

Measure:

$$
A(C)
$$

Question:

> How far can the adaptation mechanism extrapolate?

---

# 21. Add one research-grade experiment: adaptation/retention frontier

This is more sophisticated and could become one of our paper-quality figures.

We define:

$$
AdaptationGain
=
A_{new}-A_{baseline}
$$

and:

$$
Retention
=
A_{old,after}-A_{old,before}
$$

Then plot:

$$
Retention
\quad\text{vs}\quad
AdaptationGain
$$

Now we aren't merely asking:

> “Can it adapt?”

We're asking:

> **“How much new information can it acquire without destroying existing information?”**

That is a far more interesting scientific question.

---

# 22. The experimental pipeline

Every experiment should follow:

```text
TASK GENERATION
       ↓
TRAIN / LOAD MODEL
       ↓
FREEZE CHECK
       ↓
BASELINE EVALUATION
       ↓
ADAPTATION
       ↓
INTERNAL TELEMETRY
       ↓
QUERY EVALUATION
       ↓
GROUND TRUTH
       ↓
RETENTION TEST
       ↓
METRICS
       ↓
RAW RESULTS
       ↓
VALIDATION
       ↓
ANALYSIS
       ↓
PUBLIC RESULT ARTIFACT
```

Nothing should jump directly from model output to UI.

---

# 23. Statistical methodology

This should be a research project, so one run isn't enough.

For stochastic experiments:

$$
\{seed_1,\ldots,seed_n\}
$$

Run multiple seeds.

Report:

$$
mean \pm std
$$

or confidence intervals where appropriate.

For paired task comparisons, use the same tasks across adaptation mechanisms.

That is important.

Don't compare:

> Model A on easy Task Set 1

with:

> Model B on harder Task Set 2.

Use identical task episodes wherever possible.

---

# 24. Paired evaluation is especially important

For task \(i\):

$$
A_i^{state}
$$

and:

$$
A_i^{TTA}
$$

are evaluated on the **same query**.

Then:

$$
\Delta_i
=
A_i^{state}
-
A_i^{TTA}
$$

This reduces variation from task difficulty.

---

# 25. Prevent data leakage

This deserves its own audit.

We must ensure:

### Training rules

Not present in evaluation.

### Evaluation seeds

Not accidentally reused during training.

### ARC tasks

Do not inadvertently train/evaluate on benchmark leakage.

### Synthetic generator

Evaluation rules must be held out.

### Precomputed experiments

Configuration and generation process preserved.

---

# 26. Model-training strategy

We need to distinguish three phases:

### Meta-training

Learn general behavior over task distribution.

### Adaptation

Learn the current task.

### Evaluation

Test on a new query.

This is essential.

Otherwise we're simply doing supervised learning.

---

# 27. Example formal episode

A clean episode could be:

$$
\tau =
(D,Q,Y)
$$

where:

$$
D=\{(x_i,y_i)\}_{i=1}^{k}
$$

The adaptation mechanism receives:

$$
D
$$

and produces an adapted computational state:

$$
M(D)
$$

Then:

$$
\hat y =
f_\theta(M(D),Q)
$$

Evaluation:

$$
\mathcal L_{task}
=
\ell(\hat y,Y)
$$

This abstraction allows us to swap adaptation mechanisms while holding the task fixed.

---

# 28. Core architectural abstraction

Internally we should define one common interface:

```python
class AdaptationStrategy:
    def reset(self):
        ...

    def adapt(self, demonstrations):
        ...

    def predict(self, query):
        ...

    def telemetry(self):
        ...
```

Then:

```text
FrozenStrategy
ParameterTTAStrategy
RecurrentStateStrategy
TTTStateStrategy
```

This is a powerful engineering decision.

Now our experiment framework doesn't care how adaptation works.

It asks every strategy:

```text
adapt()
predict()
telemetry()
```

That makes comparisons clean.

---

# 29. Ground-truth interface

Similarly:

```python
class Task:
    demonstrations
    query
    ground_truth
    hidden_rule
```

This gives us:

```text
Task
 │
 ├── demonstrations
 ├── query
 ├── hidden rule
 └── exact answer
```

The hidden rule is available to the **evaluator**, never the learner.

This becomes one of the key scientific invariants.

---

# 30. Unit tests

We need serious tests.

### Task generator

Given seed → same task.

### Ground truth

Known rule → correct answer.

### Frozen model

Adaptation call must not change parameters.

### Parameter-TTA

Parameters must actually change.

### State adaptation

Parameters must remain unchanged.

### State reset

Different episodes must not leak state.

### Evaluation

Predictions compared against exact ground truth.

### Experiment runner

Same configuration → reproducible result within expected floating-point tolerance.

---

# 31. The “state leakage” test

This is extremely important.

Suppose we run:

```text
Task A
Task B
```

The state of B must not accidentally contain A's information unless the experiment explicitly intends that.

We should implement:

```text
reset()
```

and test it.

Then separately implement deliberate continual-memory experiments.

Otherwise we could accidentally create false evidence for adaptation.

---

# 32. Parameter isolation

For state-based methods:

$$
\theta_{before} = \theta_{after}
$$

must actually be verified.

Not assumed.

We should calculate:

$$
\|\theta_{before}-\theta_{after}\|
$$

and assert it's below a numerical tolerance.

This becomes part of the evidence displayed in the final artifact.

---

# 33. The most important internal experiment

I want an experiment that produces something like:

```text
                   Before       After
Parameter delta      0           0
State delta          0          4.83
Task accuracy       31%         86%
```

Then:

```text
Number of demonstrations: 4
Inference adaptation steps: 8
```

This single table can become one of the strongest educational moments.

---

# 34. D2.9 — Reproducibility and validation report

At the end of Phase 2, create:

```text
research/phase2_validation_report.pdf
```

It should contain:

## Experiment 1

Setup → results → interpretation.

## Experiment 2

Setup → results → interpretation.

etc.

For every result:

* configuration,
* seeds,
* sample count,
* model,
* task generator,
* metrics,
* result,
* variance,
* limitations.

---

# 35. Distinguish evidence levels

For our own results:

### Directly measured

We ran it.

### Reproduced

We reproduced a published experiment.

### Inspired by

Our experiment is based conceptually on a paper but isn't a reproduction.

### Toy demonstration

Controlled educational implementation.

This mirrors the evidence discipline required by Pathway. The brief specifically demands that claims be grounded and that teams distinguish formal/publicly demonstrated results from independent implementations. 

---

# 36. The public UI should not exist yet—except as a thin test harness

There should be a small internal interface around the experiment engine.

Something like:

```text
Task
[Generate]

Demonstrations
[3]

Adaptation
[Recurrent State]

State Size
[32]

Adapt

Query
[Generate]

Prediction: ___
Ground truth: ___

ΔState: ___
ΔParameters: ___
Latency: ___
```

This is not the final product.

It is an **instrument panel for the researchers**.

Once this works, the actual public interface can be designed around the science.

---

# 37. Phase 2 success criterion

The following experiment should work end-to-end:

```text
Generate unseen task
       ↓
Generate demonstrations
       ↓
Run frozen baseline
       ↓
Run adaptation strategy
       ↓
Measure what changed
       ↓
Run novel query
       ↓
Compare with ground truth
       ↓
Measure adaptation gain
       ↓
Introduce second task
       ↓
Test retention
```

And we should be able to run this with:

**at least frozen + parameter-TTA + recurrent-state adaptation**

using the same task episodes.

---

# 38. Phase 2 should produce the first actual scientific figure

Before leaving Phase 2, we should have a result figure of this general form:

```text
Accuracy
100% |                         ●
     |                   ●
 80% |             ●
     |       ●
 60% |
     |
 40% | ●
     |
 20% |
     +---------------------------
        1   2   3   4   5
          Demonstrations
```

with comparable curves for the relevant adaptation mechanisms.

The exact shape is not predetermined.

**The experiment determines the result.**

---

# 39. Then we produce the first failure figure

For example:

```text
Retention of Task A
100% | ●
     |   ●
 80% |     ●
     |       ●
 60% |         ●
     |
 40% |
     +----------------------
        Interference
```

Again, the point isn't to engineer a nice-looking curve.

It is to discover whether the mechanism actually exhibits the predicted limitation.

---

# 40. Go/No-Go gate after Phase 2

There are three possible outcomes.

## GO

The mechanisms produce measurable, interpretable differences.

Proceed to the educational artifact.

## MODIFY

The phenomenon exists, but our chosen model/task isn't sufficiently informative.

Change the substrate.

## ABANDON

The central claim cannot be demonstrated cleanly.

Change the claim/topic before wasting time on frontend.

This is critical.

We should never let sunk cost force us to teach a phenomenon our experiments don't support.

---

# 41. Team allocation during Phase 2

I would split the team roughly like this:

### Research/ML lead

Own:

* model formulations,
* adaptation algorithms,
* mathematical correctness,
* literature reproduction.

### Data/Experiment lead

Own:

* task generator,
* experiment runner,
* statistical evaluation,
* result validation.

### Systems lead

Own:

* model infrastructure,
* GPU/CPU optimization,
* checkpointing,
* telemetry,
* reproducibility.

### Product/visualization lead

Work in parallel on:

* understanding what variables will eventually need to be visible,
* early experimental UI,
* visualization prototypes.

But **nobody should be building the final marketing/product interface yet.**

---

# 42. Phase 2 timeline structure

Rather than assigning arbitrary calendar dates, I would structure it around milestones.

### Milestone 2.1

Task generator works and has exact ground truth.

### Milestone 2.2

Frozen baseline established.

### Milestone 2.3

Parameter-TTA works.

### Milestone 2.4

Recurrent-state adaptation works.

### Milestone 2.5

Measurement system verifies:

$$
\Delta\theta,\Delta s
$$

### Milestone 2.6

Demonstration-scaling experiment works.

### Milestone 2.7

Interference experiment works.

### Milestone 2.8

ARC-like task family works.

### Milestone 2.9

Cross-seed validation complete.

### Milestone 2.10

Go/no-go review.

Only after 2.10 do we formally enter Phase 3.

---

# 43. What Phase 2 gives us for the final Pathway artifact

By the end of this phase, we should have:

### Real model

Not scripted behavior.

### Real adaptation

Not a visual metaphor.

### Real state transitions

Not manually drawn arrows.

### Real ground truth

Not subjective assessment.

### Real failure modes

Not fabricated “limitations.”

### Real measured trade-offs

Not marketing claims.

### Real experimental results

Not arbitrary graphs.

That satisfies the substrate requirements that the Pathway brief emphasizes. 

---

# 44. The crucial separation between Phase 2 and Phase 3

## Phase 2 asks:

> **Does our scientific idea actually work?**

## Phase 3 will ask:

> **How do we make someone understand that scientific idea?**

That's the correct order.

We don't want to spend three days making a beautiful visualization and discover later that our state-adaptation experiment doesn't actually work.

---

# 45. Phase 2 final package

At the end, our repository should contain something close to:

```text
research/
├── experiments/
│   ├── 001_task_acquisition/
│   ├── 002_demo_scaling/
│   ├── 003_compute_scaling/
│   ├── 004_state_capacity/
│   ├── 005_interference/
│   ├── 006_noise/
│   └── 007_complexity/
│
├── models/
│   ├── frozen/
│   ├── param_tta/
│   ├── recurrent_state/
│   └── ttt_state/
│
├── tasks/
│   ├── linear/
│   ├── nonlinear/
│   ├── symbolic/
│   ├── compositional/
│   └── arc_like/
│
├── configs/
├── results/
├── figures/
├── validation/
└── phase2_validation_report.pdf
```

---

# 46. The final Phase 2 checklist

Before moving forward:

### Scientific substrate

☐ At least two genuinely different adaptation mechanisms work.

☐ The task rule can be hidden from the model.

☐ Ground truth is exact.

☐ Parameters/state can be measured.

☐ Adaptation is measurable.

☐ Failure is measurable.

### Experimental integrity

☐ Multiple seeds.

☐ Held-out task rules.

☐ Same task instances used for fair comparisons.

☐ No accidental state leakage.

☐ No parameter updates in the state-only condition.

☐ Parameter changes verified in TTA.

☐ All important configurations logged.

### Engineering

☐ Experiments reproducible.

☐ Unit tests pass.

☐ Results serialized.

☐ Model checkpoints versioned.

☐ Task generator versioned.

☐ Runtime measured.

### Research

☐ Core experiments run.

☐ Ablations run.

☐ Failure experiments run.

☐ Results analyzed rather than merely plotted.

☐ Contradictory results retained.

☐ Limitations documented.

### Pathway compliance

☐ Any synthetic task is identified as synthetic.

☐ Any toy/independent model is identified as such.

☐ No experiment is described as official BDH behavior unless it actually is.

☐ Live/precomputed boundaries are documented.

These requirements follow directly from Pathway's insistence on actual computation, transparent evidence, and clear separation between official BDH systems and independent/toy implementations. 

---

# The Phase 2 exit condition

The single most important test is this:

> **Give the system an unseen task it has never been trained on. Give it demonstrations. Let three adaptation mechanisms process exactly the same demonstrations. Then ask a genuinely novel query and determine, from actual computation, how much each mechanism learned, what changed internally, what it cost, and whether it retained the learned rule after another task intervened.**

When that works reproducibly, **we have the scientific engine**.

Then Phase 3 can turn that engine into the educational experience Pathway actually wants: a guided, visually transparent, <60-second learning interaction where the learner can manipulate the same variables we just validated scientifically. The brief explicitly says the concept should behave before the learner acts and that the important state and truth/estimate gap should be visible. 

That separation—**research engine first, learning product second**—is what will keep the project at the standard you're aiming for.
