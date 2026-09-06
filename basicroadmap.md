# ADAPT — Master Execution Roadmap

We now have the five phases. The next step is to turn them into a **single execution system** with a critical path, parallel workstreams, ownership, milestones, engineering architecture, research gates, and final release procedure.

I would run this like a **small research/product team**, not like a hackathon team.

The Pathway brief gives us a strong constraint: one coherent central claim, a real computational substrate, immediate interaction, visible state, truth beside estimate, substantive BDH/BDH-CQ integration, recent primary research, reproducibility, and a public artifact.  

The roadmap below is built around satisfying those constraints while keeping the scientific core ahead of the UI.

---

# 1. The complete project architecture

At the highest level:

```text
                         ADAPT
            ┌───────────────────────────┐
            │ Where does an AI learn    │
            │ a new task?               │
            └─────────────┬─────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
         RESEARCH ENGINE        LEARNING EXPERIENCE
              │                       │
              │                       │
      ┌───────┴────────┐       ┌──────┴─────────┐
      │                │       │                │
  Task Generator   Adaptation  Guided Path    Sandbox
                     Engine
      │                │           │                │
      └────────┬───────┘           └────────┬───────┘
               │                            │
               ▼                            ▼
         Experiment API              Assessment
               │                            │
               └──────────┬─────────────────┘
                          ▼
                    BDH / BDH-CQ
                          │
                          ▼
                  Research Evidence
                          │
                          ▼
                    Public Artifact
```

Underneath everything:

```text
             VERSIONED EXPERIMENTS
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
    Models          Tasks          Results
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                 Provenance
```

This separation is fundamental.

---

# 2. The critical path

Not everything should happen sequentially.

We have **five major streams**:

```text
A. Scientific Research
B. ML / Experiment Engine
C. Product / Frontend
D. BDH / BDH-CQ Research
E. Documentation / Evaluation
```

Their dependencies should look like this:

```text
               SCIENTIFIC SCOPE
                     │
                     ▼
                CORE CLAIM
                     │
          ┌──────────┴───────────┐
          ▼                      ▼
    TASK SPECIFICATION      EXPERIMENT DESIGN
          │                      │
          └──────────┬───────────┘
                     ▼
              COMPUTATIONAL
                 SUBSTRATE
                     │
          ┌──────────┼───────────┐
          ▼          ▼           ▼
       BASELINE   STATE-TTA   PARAM-TTA
          │          │           │
          └──────────┼───────────┘
                     ▼
              VALIDATED RESULTS
                     │
          ┌──────────┼───────────┐
          ▼          ▼           ▼
       LEARNING     BDH        FRONTIER
       EXPERIENCE   MODULE     VALIDATION
          │          │           │
          └──────────┼───────────┘
                     ▼
                  FINAL UX
                     │
                     ▼
             EVALUATION / REDTEAM
                     │
                     ▼
                PRODUCTION
                     │
                     ▼
                 SUBMISSION
```

### Critical insight

**Frontend development is not on the true critical path until the core scientific experiment works.**

The first real milestone is not:

> “We have a website.”

It is:

> **“We can reproducibly demonstrate inference-time task adaptation on an unseen task with measurable changes in the adaptation substrate.”**

---

# 3. Team structure

For a 3–5 person team, I would use these roles.

## Role A — Scientific Lead

Owns:

* central claim,
* terminology,
* equations,
* literature,
* hypotheses,
* scientific correctness,
* final technical defense.

This person effectively owns the scientific argument.

---

## Role B — ML / Experiment Lead

Owns:

* task generator,
* models,
* adaptation mechanisms,
* experiment runner,
* metrics,
* statistical analysis.

This person owns whether the science actually works.

---

## Role C — Systems / Backend Lead

Owns:

* experiment API,
* model serving,
* caching,
* reproducibility,
* deployment,
* telemetry,
* performance.

---

## Role D — Frontend / Interaction Lead

Owns:

* learning journey,
* visualizations,
* controls,
* interaction,
* accessibility,
* responsive design.

---

## Role E — Research/Content/QA Lead

If the team has five people:

Owns:

* BDH/BDH-CQ research,
* evidence ledger,
* documentation,
* user evaluation,
* provenance,
* final submission package.

With four people, combine this with Scientific Lead.

With three people, combine:

**Scientific + BDH**

and:

**Systems + Frontend**

---

# 4. Rules for ownership

Every critical component should have:

### Primary owner

One person responsible.

### Secondary reviewer

One person who can challenge it.

Nobody owns something nobody else understands.

This matters because the brief scores technical ownership and live defense. Judges may ask teams to trace the system and predict what changing parameters will do. 

---

# 5. Phase 1 — Scientific Specification

## Objective

Freeze:

* topic,
* question,
* claim,
* learner,
* hypotheses,
* literature,
* experiment design.

The brief explicitly asks for one falsifiable sentence and a coherent learning journey. 

## Deliverables

```text
research/
├── scope/
│   └── scientific_scope.md
├── terminology/
│   ├── terminology.md
│   └── concept_map.pdf
├── literature/
│   ├── evidence_matrix.csv
│   └── research_timeline.md
├── claim/
│   ├── central_claim.md
│   └── falsification_criteria.md
├── education/
│   └── learner_spec.md
└── experiments/
    ├── hypotheses.md
    └── experimental_design.md
```

## Exit gate

We can state:

> **One precise claim, one learner, one central experiment.**

And another team member can explain why the claim is falsifiable.

---

# 6. Phase 2 — Computational Substrate

## Objective

Build a scientific instrument capable of testing the claim.

## Deliverables

```text
core/
├── task_generator/
├── models/
│   ├── frozen/
│   ├── param_tta/
│   ├── recurrent_state/
│   └── ttt_state/
├── experiments/
├── metrics/
└── telemetry/
```

## Essential first experiment

```text
Generate unseen task
        ↓
Generate demonstrations
        ↓
Frozen baseline
        ↓
Adaptation
        ↓
Query
        ↓
Ground truth
        ↓
Measure:
Δparameter
Δstate
accuracy
latency
```

## Exit gate

Same task, same seed, different adaptation strategies.

Results reproducibly differ.

---

# 7. Phase 3 — Learning Experience

Only after Phase 2 succeeds.

## Objective

Convert the computational instrument into an educational system.

The brief explicitly says the learner should manipulate a meaningful variable, observe consequences, compare output with ground truth, and encounter a limitation. 

## Product flow

```text
HOOK
 ↓
UNSEEN TASK
 ↓
PREDICT
 ↓
ADAPT
 ↓
OBSERVE
 ↓
GROUND TRUTH
 ↓
WHAT CHANGED?
 ↓
MANIPULATE
 ↓
STRESS
 ↓
FAILURE
 ↓
BDH / BDH-CQ
 ↓
TRANSFER
```

## Exit gate

An unfamiliar technically capable user can understand the core phenomenon without us verbally walking them through it.

---

# 8. Phase 4 — BDH / Frontier Validation

## Objective

Connect the controlled experiment to actual frontier research.

The brief explicitly says the BDH connection must be substantive and integrated into the journey, with a concrete equation, diagram, live experiment, or clearly labeled precomputed result. 

## Deliverables

```text
research/bdh/
├── bdh_dossier.md
├── bdhcq_dossier.md
├── concept_mapping.md
├── evidence_ledger.csv
└── reproductions/
```

## Exit gate

We can answer:

> “Exactly why is BDH relevant to this concept?”

without handwaving.

And:

> “Exactly what is our own implementation versus official BDH behavior?”

---

# 9. Phase 5 — Production / Defense

## Objective

Freeze the science, harden the system, validate learning, and submit.

The brief explicitly evaluates robustness, accessibility, mobile usability, source quality, reproducibility, provenance and public availability. 

---

# 10. The development timeline

Because I don't want to invent a deadline we haven't established in this conversation, use **milestone-based scheduling** rather than arbitrary dates.

I recommend:

## Sprint 0 — Project setup

Deliver:

* repository,
* branching strategy,
* issue tracker,
* experiment conventions,
* research notes system,
* citation manager,
* documentation structure.

---

## Sprint 1 — Phase 1 research

Deliver:

* literature map,
* terminology,
* central claim candidate,
* learner definition,
* initial experiment design.

No serious frontend development.

---

## Sprint 2 — Scientific prototype

Implement:

* task generator,
* frozen baseline,
* parameter TTA,
* recurrent state adaptation.

The target is the first successful experiment.

---

## Sprint 3 — Scientific validation

Run:

* demonstrations,
* state capacity,
* adaptation compute,
* interference,
* noise,
* task complexity.

Produce first figures.

---

## Sprint 4 — Frontier extension

Add:

* ARC-like task generator,
* novel-task experiments,
* selected BDH/BDH-CQ investigation.

At this point, the science should be stable.

---

## Sprint 5 — Flagship learning interaction

Build only:

> **Teach the Model a New Rule**

Nothing else.

Test it.

---

## Sprint 6 — Complete learning experience

Add:

* adaptation comparison,
* state visualization,
* stress lab,
* assessment,
* BDH transition.

---

## Sprint 7 — Evaluation

Run:

* learner study,
* usability study,
* mobile test,
* scientific red-team.

---

## Sprint 8 — Production hardening

Fix:

* performance,
* bugs,
* deployment,
* accessibility,
* provenance,
* documentation.

---

## Sprint 9 — Submission freeze

Freeze:

* science,
* figures,
* wording,
* product,
* documentation.

Only critical fixes afterward.

---

# 11. The research workstream

Research should never stop completely until final freeze.

Structure it as:

```text
Literature
   ↓
Claim
   ↓
Experiment
   ↓
Result
   ↓
Interpretation
   ↓
Product wording
```

Not:

```text
Paper
↓
ChatGPT summary
↓
website
```

---

# 12. Research paper pipeline

For each important paper:

```text
RAW PAPER
    ↓
ANNOTATED PDF
    ↓
METHOD EXTRACTION
    ↓
EQUATION EXTRACTION
    ↓
EXPERIMENT EXTRACTION
    ↓
LIMITATION EXTRACTION
    ↓
EVIDENCE LEDGER
    ↓
PROJECT RELEVANCE
```

Every important paper should answer:

> Why is this in our project?

---

# 13. The experiment pipeline

Every experiment follows the same lifecycle:

```text
HYPOTHESIS
    ↓
CONFIG
    ↓
TASK GENERATION
    ↓
EXECUTION
    ↓
RAW OUTPUT
    ↓
VALIDATION
    ↓
ANALYSIS
    ↓
FIGURE
    ↓
INTERPRETATION
    ↓
CLAIM / LIMITATION
```

No manual graph creation from memory.

---

# 14. Experiment configuration standard

Example:

```yaml
experiment_id: EXP-0042
task_family: symbolic
model: recurrent_state_v3
adaptation: recurrent
demonstrations: 4
state_dim: 32
adaptation_steps: 8
noise: 0.05
seed: 42
```

Results:

```json
{
  "experiment_id": "EXP-0042",
  "accuracy": 0.87,
  "state_delta": 4.83,
  "parameter_delta": 0.0,
  "latency_ms": 127
}
```

Every final visualization can then trace back to `EXP-0042`.

---

# 15. Git strategy

Use:

```text id="9mt1bi"
main
│
├── research/*
├── experiment/*
├── backend/*
├── frontend/*
└── docs/*
```

Protect `main`.

Scientific results that become part of the final artifact should be tagged.

For example:

```text id="bbg6p6"
research-v1
experiment-freeze-v1
artifact-v1
submission-v1
```

---

# 16. Model versioning

Each model should have:

```text id="mnnwja"
model_name
version
training_config
checkpoint_hash
dataset_version
code_commit
```

Never write:

> “our recurrent model”

when there are actually four versions.

Use:

> `recurrent_state_v3`

---

# 17. Dataset/task versioning

Likewise:

```text id="fl13mf"
task_generator_v1
task_generator_v2
arc_like_v1
```

Changing the generator changes the experiment.

It must therefore be versioned.

---

# 18. The API boundary

The frontend should never directly manipulate the model.

Use:

```text id="0jsmfn"
Frontend
   ↓
Experiment API
   ↓
Experiment Engine
   ↓
Model
```

The API should receive:

```json
{
  "task_id": "...",
  "strategy": "recurrent_state",
  "demonstrations": 4,
  "state_dim": 32
}
```

and return:

```json
{
  "prediction": "...",
  "ground_truth": "...",
  "accuracy": 1,
  "state_delta": 4.81,
  "parameter_delta": 0,
  "latency_ms": 112,
  "execution_type": "live"
}
```

---

# 19. Live vs precomputed architecture

This is important enough to make explicit.

## Live

Used for:

* small tasks,
* primary interaction,
* state changes,
* immediate predictions.

## Precomputed

Used for:

* expensive sweeps,
* large models,
* expensive benchmark runs,
* selected BDH/CQ results.

## Static

Used for:

* explanatory diagrams,
* equations,
* historical context.

The Pathway brief explicitly permits expensive precomputed experiments, provided they're labelled correctly. 

---

# 20. How the final UI accesses precomputed results

Use a canonical experiment key:

$$
K = Hash(config)
$$

Example:

```text id="z4u98p"
state_dim=32
demo_count=4
noise=0.05
steps=8
```

→

```text id="b5jpno"
EXP-8127
```

The frontend asks for `EXP-8127`.

The result includes:

> **PRECOMPUTED**

No deception.

---

# 21. The most important frontend component

Build:

# `ExperimentPanel`

Every major learning section can reuse it.

It should support:

```text id="esd6j5"
Task
Demonstrations
Adaptation Strategy
Parameter Controls
Run
Prediction
Ground Truth
State Change
Parameter Change
Latency
Evidence Status
```

This gives the project a reusable substrate.

---

# 22. The second important frontend component

# `StateInspector`

It should expose:

* before state,
* after state,
* difference,
* trajectory,
* interpretable statistics.

It should not make unjustified semantic claims.

---

# 23. The third

# `PredictionChallenge`

Before computation:

> Predict.

After:

> Reveal.

This component becomes the backbone of our pedagogy.

---

# 24. The fourth

# `EvidenceBadge`

For every result:

```text
LIVE
PRECOMPUTED
SYNTHETIC
ILLUSTRATIVE
```

Clicking opens provenance.

---

# 25. The fifth

# `MechanismView`

Shows:

```text
input
 ↓
adaptation
 ↓
state/parameter change
 ↓
query
 ↓
output
```

This becomes the bridge between intuition and equations.

---

# 26. The sixth

# `FailureLab`

The learner can deliberately:

* reduce demonstrations,
* reduce state,
* increase interference,
* increase noise,
* increase task complexity.

The system then shows actual degradation.

---

# 27. The BDH experience

The transition should not be:

> “Here's BDH.”

Instead:

> **“You have just investigated one design for where adaptation can live. BDH explores a related question by treating memory as part of the model's computational fabric.”**

Then the learner can move between:

```text
Our controlled model
        ↕
BDH mechanism
        ↕
BDH-CQ mechanism
```

---

# 28. The comparison framework

Never claim that our toy model equals BDH.

Instead compare:

| Property          | Our model            | Published BDH            | Published BDH-CQ                |
| ----------------- | -------------------- | ------------------------ | ------------------------------- |
| Task adaptation   | Experimental         | Related memory mechanism | Demonstration-driven adaptation |
| State changes     | Yes                  | Yes                      | Yes                             |
| Parameter updates | Depends on condition | Architecture-specific    | Not during described inference  |
| Synaptic memory   | Simplified           | Core mechanism           | Not equivalent                  |
| Latent reasoning  | Optional             | Related dynamics         | Core mechanism                  |
| Scale             | Tiny                 | Frontier                 | Frontier                        |
| Evidence          | Our experiment       | Published                | Published                       |

This demonstrates intellectual honesty.

---

# 29. Evaluation workstream

This runs parallel to product development.

## Scientific evaluation

Verify:

* accuracy,
* repeatability,
* intervention validity,
* absence of leakage.

## Educational evaluation

Verify:

* learning gain,
* misconception reduction,
* transfer.

## Product evaluation

Verify:

* usability,
* accessibility,
* mobile,
* performance.

---

# 30. The final learner study

Structure:

```text
Participant
    ↓
Pre-test
    ↓
Artifact
    ↓
Post-test
    ↓
Transfer task
    ↓
Short interview
```

Measure:

$$
G = Post-Pre
$$

and:

$$
T = Transfer
$$

Qualitative data captures misconceptions.

---

# 31. Scientific red team

Get someone familiar with ML but unfamiliar with our project.

Give them:

* README,
* public artifact,
* concept summary.

Ask them to attack:

> Is the claim actually supported?

> Are the baselines fair?

> Does the state intervention establish causality?

> Is the BDH connection legitimate?

> Are the comparisons valid?

---

# 32. Product red team

A different person should try to use the artifact.

Don't explain anything.

Observe:

* what they click,
* where they hesitate,
* whether they understand the controls,
* whether they understand what is live,
* whether they see the ground truth.

---

# 33. Final red-team matrix

Create:

```text
audit/final_redteam.csv
```

Columns:

```text
Issue
Category
Severity
Evidence
Owner
Fix
Regression Test
Status
```

Severity:

**P0 — submission blocker**

**P1 — major issue**

**P2 — polish**

---

# 34. P0 issues

Examples:

* wrong scientific claim,
* broken experiment,
* incorrect ground truth,
* misleading BDH claim,
* inaccessible public URL,
* broken mobile interaction,
* non-reproducible final result.

These must be fixed.

---

# 35. P1 issues

Examples:

* confusing visualization,
* slow interaction,
* unclear terminology,
* weak explanation.

Fix unless time genuinely prevents it.

---

# 36. P2 issues

Examples:

* animation polish,
* typography tweaks,
* minor spacing.

Don't let these consume the critical path.

---

# 37. The final research paper package

Even though Pathway does not require a full academic paper, maintain one internally.

Final package:

```text
paper/
├── abstract.md
├── introduction.md
├── related_work.md
├── method.md
├── experiments.md
├── results.md
├── limitations.md
└── appendix/
```

This makes the final blog and concept summary much easier to produce and forces scientific structure.

---

# 38. Final concept summary

The Pathway brief asks for approximately **500–950 words** and wants it to function as a self-contained briefing rather than a project diary or collection of paper summaries. 

We should write this only after:

* results are frozen,
* BDH wording is frozen,
* limitations are known.

---

# 39. Final blog

The blog should narrate:

### Problem

Why inference-time learning matters.

### Insight

Where adaptation can live.

### Experiments

What we measured.

### Results

What happened.

### BDH

How the frontier architecture relates.

### Limitations

What we still don't know.

This prevents the blog from becoming marketing copy.

---

# 40. Final README

It must explicitly identify:

* claim,
* audience,
* prerequisites,
* objectives,
* architecture,
* major components,
* live/precomputed/synthetic/animated portions,
* reproduction,
* licenses,
* credits. 

---

# 41. Final compliance system

Create:

```text
submission/
├── compliance.md
├── artifact_url.txt
├── repo_url.txt
├── concept_summary.pdf
└── blog.pdf
```

The compliance document maps every requirement to exact evidence.

---

# 42. The final rubric attack

We should literally fill this out before submitting:

| Criterion              | Internal evidence                    | Target |
| ---------------------- | ------------------------------------ | -----: |
| Technical correctness  | equations + experiments + citations  | 23/25+ |
| Technical ownership    | defense + architecture understanding | 14/15+ |
| Learning effectiveness | learner study                        | 13/15+ |
| Interactive substrate  | live model + controls + truth        | 14/15+ |
| BDH integration        | substantive module                   |  9/10+ |
| Craft/robustness       | production QA                        |  9/10+ |
| Concept summary        | technical audit                      |  9/10+ |

The official total is 100 points across these seven categories. 

---

# 43. Critical-path priorities

If schedule pressure appears, protect things in this order:

### Tier 1 — Cannot compromise

1. Scientific correctness.
2. Core experiment.
3. Ground truth.
4. Real adaptation.
5. BDH/CQ technical correctness.
6. Public artifact.
7. Submission compliance.

### Tier 2 — Very important

8. Failure experiment.
9. Learner evaluation.
10. State visualization.
11. Reproducibility.

### Tier 3 — Polish

12. Advanced animation.
13. Extra task families.
14. Decorative visuals.
15. Additional experiments.

This prevents the classic failure:

> beautiful frontend + weak science.

---

# 44. Things we should deliberately refuse to add

Even if they look impressive:

### Chatbot explaining papers

No.

### Generic AI assistant

No.

### 20 different architectures

No.

### Massive dashboard

No.

### Fake “neuron animations”

No.

### Arbitrary sliders

No.

### Huge LLM just for prestige

No.

### Reproducing every BDH benchmark

No.

### Full ARC benchmark implementation if unnecessary

No.

### Anything that doesn't improve the central learning journey

No.

The brief explicitly favors focused, coherent artifacts over broad dashboards and calls unchanged forks, generic overview content and fake computation weak submissions. 

---

# 45. The one thing we should over-invest in

# **The core experimental substrate.**

Because once this is excellent:

```text
scientifically valid engine
        ↓
powerful visualization
        ↓
strong learning experience
        ↓
good BDH integration
        ↓
research-quality documentation
```

But the reverse isn't true.

A beautiful UI cannot rescue a scientifically weak experiment.

---

# 46. The final system should have three modes

## Mode 1 — Learn

Curated, guided.

```text
60-second insight
↓
guided experiments
↓
failure
↓
BDH
```

## Mode 2 — Explore

Free scientific sandbox.

```text
task
strategy
state
compute
interference
```

## Mode 3 — Research

Advanced view.

```text
experiment IDs
configurations
metrics
figures
raw results
provenance
```

This is where the project starts behaving like an actual research tool.

---

# 47. A powerful final feature: “Research Mode”

After completing the guided path, allow an advanced user to open:

> **Research Mode**

They can:

* generate task distributions,
* choose adaptation methods,
* run parameter sweeps,
* inspect metrics,
* compare experiments,
* export results.

This shouldn't be necessary for the basic learning experience.

But it gives the artifact long-term reuse potential—exactly the kind of reusable substrate the brief identifies as exceptional. 

---

# 48. Final architecture after all five phases

The finished project should look like this:

```text id="glkaw3"
                         ┌─────────────────────┐
                         │       ADAPT         │
                         │ Where does an AI    │
                         │ learn a new rule?   │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼──────────────────────┐
              │                     │                      │
              ▼                     ▼                      ▼
           LEARN                  EXPLORE                RESEARCH
              │                     │                      │
              ▼                     ▼                      ▼
       Guided journey          Free sandbox          Experiments
              │                     │                      │
              └──────────────┬──────┴──────────────┬───────┘
                             ▼                     ▼
                    ADAPTATION ENGINE        EVIDENCE ENGINE
                             │                     │
              ┌──────────────┼─────────────┐       │
              ▼              ▼             ▼       │
           CONTEXT        STATE         WEIGHTS     │
              │              │             │        │
              └──────────────┼─────────────┘        │
                             ▼                      │
                           QUERY                    │
                             ▼                      │
                        PREDICTION                  │
                             ▼                      │
                        GROUND TRUTH                │
                             ▼                      │
                       INTERVENTION                 │
                             ▼                      │
                         FAILURE                    │
                             │                      │
                             ▼                      ▼
                           BDH                  SOURCES
                             │                      │
                             ▼                      │
                         BDH-CQ                    │
                             └──────────┬───────────┘
                                        ▼
                                  FINAL CHALLENGE
```

---

# 49. The ultimate project lifecycle

The entire program becomes:

```text
QUESTION
   ↓
LITERATURE
   ↓
CLAIM
   ↓
HYPOTHESIS
   ↓
EXPERIMENT
   ↓
REAL COMPUTATION
   ↓
VALIDATION
   ↓
LEARNING DESIGN
   ↓
INTERACTIVE PRODUCT
   ↓
BDH / BDH-CQ CONNECTION
   ↓
USER STUDY
   ↓
SCIENTIFIC AUDIT
   ↓
PRODUCTION QA
   ↓
RED TEAM
   ↓
DOCUMENTATION
   ↓
SUBMISSION
```

That is the sequence I would follow.

---

# 50. The three most important gates

To keep us disciplined, I would establish three **hard gates**.

## Gate A — Scientific Gate

Before substantial frontend work:

> **Can we demonstrate the central phenomenon with real computation?**

If no → stay in Phase 2.

---

## Gate B — Educational Gate

Before production:

> **Can an unfamiliar learner discover the central phenomenon and explain it?**

If no → stay in Phase 3.

---

## Gate C — Submission Gate

Before final release:

> **Can a technically sophisticated reviewer verify every major claim, reproduce the important results, understand the BDH connection, and use the public artifact without assistance?**

If no → stay in Phase 5.

---

# 51. The ideal final demonstration

The final presentation should essentially be the project itself.

### Start

> “This model has never seen this task.”

Run.

It succeeds.

### Ask

> “Where did the new rule go?”

Show state/parameter change.

### Manipulate

Reduce demonstrations.

Run again.

### Stress

Introduce another task.

Show interference.

### Explain

Reveal the mechanism.

### Connect

> “This design question appears in frontier architectures like BDH and BDH-CQ.”

Show the published mechanism.

### Finish

Give a completely unseen task to the learner/judge.

Ask them to predict.

Run.

Reveal.

That is a far stronger presentation than a conventional slide deck followed by a software demo.

---

# 52. What the final repository should look like

```text
adapt/
│
├── app/
│   ├── learn/
│   ├── lab/
│   ├── research/
│   ├── bdh/
│   └── components/
│
├── backend/
│   ├── api/
│   ├── experiment_engine/
│   ├── task_generator/
│   └── models/
│
├── experiments/
│   ├── configs/
│   ├── runners/
│   ├── results/
│   └── analysis/
│
├── research/
│   ├── literature/
│   ├── claim/
│   ├── bdh/
│   ├── hypotheses/
│   └── reports/
│
├── evaluation/
│   ├── learner_study/
│   ├── usability/
│   └── red_team/
│
├── docs/
│   ├── README.md
│   ├── methodology.md
│   ├── reproduction.md
│   ├── provenance.md
│   ├── licenses.md
│   └── ai_disclosure.md
│
├── submission/
│   ├── blog.pdf
│   ├── concept_summary.pdf
│   └── compliance.md
│
└── tests/
```

---

# 53. The single highest-priority next action

Now that the full roadmap is established, I would **not jump into Phase 2 implementation yet**.

The next concrete work item is:

# **Execute Phase 1 completely and freeze the scientific specification.**

Specifically, we need to produce these five things first:

```text
1. Definitive terminology map
2. Literature/evidence matrix
3. Final candidate central claim
4. Exact experimental hypotheses
5. Exact minimal computational substrate
```

Then we can implement the smallest experiment capable of falsifying the claim.

That gives us a very clean transition:

**Phase 1 → scientific blueprint**

**Phase 2 → verified research engine**

**Phase 3 → learning product**

**Phase 4 → frontier/BDH integration**

**Phase 5 → production, evaluation and submission**

And this remains tightly aligned with the Pathway brief: one central claim, meaningful manipulation, observable behavior, ground truth, a substantive BDH/BDH-CQ connection, explicit limitations, recent primary research, and a robust public artifact.  

The next execution task, therefore, is **Phase 1 deliverable D1: the definitive scientific scope + terminology + research map**, after which we can freeze the experiment architecture and start building the real substrate.
