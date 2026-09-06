# Phase 4 — BDH/BDH-CQ Integration, Frontier Validation & Research Evidence

Phase 4 is where the project stops being merely **an excellent TTA learning system** and becomes a submission that is genuinely anchored in **Pathway's frontier research**.

There is an important refinement from our earlier plan: **BDH/BDH-CQ should not be treated as a separate “module” we attach to the product after finishing the TTA system.** The Pathway brief explicitly says the BDH connection must be woven into the learning journey and must have its own learning objective, grounded in an equation, diagram, live experiment, or clearly labelled precomputed result. 

And the current research landscape makes this phase particularly valuable. BDH is now accompanied by an official open-source implementation, and BDH-CQ is a very recent 2026 system explicitly combining in-context learning, recurrent memory updates during inference, and latent reasoning. ([GitHub][1])

So Phase 4 has two jobs:

> **1. Establish exactly how our scientific concept relates to BDH/BDH-CQ.**

> **2. Build enough evidence and experimentation that the relationship is scientifically defensible rather than rhetorical.**

---

# 1. Phase 4 North Star

At the beginning of Phase 4 we have:

```text
Real adaptation engine
        ↓
Real experiments
        ↓
Observed adaptation / interference / cost
```

At the end we should have:

```text
Our controlled adaptation research
        ↓
Formal conceptual bridge
        ↓
BDH mechanism
        ↓
BDH-CQ mechanism
        ↓
Published evidence
        ↓
Selected reproductions / validations
        ↓
Learner-facing scientific experience
```

The final user should not feel that:

> “Oh, here is the BDH page.”

They should feel:

> **“I just discovered this adaptation mechanism in a controlled experiment. Now I can see a real frontier architecture that makes related design choices.”**

---

# 2. Phase 4 Deliverables

I would make Phase 4 produce **11 formal deliverables**.

| ID        | Deliverable                       | Purpose                                                   |
| --------- | --------------------------------- | --------------------------------------------------------- |
| **D4.1**  | BDH Technical Dossier             | Full technical understanding of BDH                       |
| **D4.2**  | BDH-CQ Technical Dossier          | Full technical understanding of BDH-CQ                    |
| **D4.3**  | Concept-to-BDH Mapping            | Exact connection between our concept and Pathway systems  |
| **D4.4**  | BDH Equation Lab                  | Interactive/formal representation of relevant equations   |
| **D4.5**  | BDH Evidence Ledger               | Claim-by-claim evidence classification                    |
| **D4.6**  | BDH Reproduction/Validation Suite | Reproduce selected public results where practical         |
| **D4.7**  | Frontier Comparison Study         | Compare our adaptation regimes with BDH-family mechanisms |
| **D4.8**  | ARC / Novel-Task Validation Layer | Connect our laboratory to frontier task acquisition       |
| **D4.9**  | BDH-CQ Educational Experience     | Learner-facing integration                                |
| **D4.10** | Scientific Integrity Audit        | Catch overclaims/misrepresentations                       |
| **D4.11** | Phase 4 Research Report           | Consolidated evidence and conclusions                     |

---

# 3. D4.1 — BDH Technical Dossier

Create:

```text id="dk5q8r"
research/bdh/
├── bdh_technical_dossier.md
├── architecture.md
├── equations.md
├── memory.md
├── interpretability.md
└── evidence.md
```

This should answer:

> **What exactly is BDH?**

Not:

> “BDH is brain-inspired and efficient.”

That isn't enough.

The official BDH paper describes a scale-free network of locally interacting neuron particles, with a GPU-friendly formulation and working memory based on synaptic plasticity/Hebbian learning. ([arXiv][2])

The public implementation additionally describes:

* scale-free network topology,
* local neuronal interactions,
* Hebbian working memory,
* sparse positive activations,
* GPU-oriented formulation. ([GitHub][1])

---

# 4. BDH architecture decomposition

We should decompose BDH into:

### A. Neural state

What variables represent neuron activity?

### B. Graph connectivity

How are neurons connected?

### C. Synaptic state

What information is carried by edges?

### D. Memory update

How is synaptic state modified?

### E. Activity propagation

How do local interactions create global computation?

### F. Read/write mechanism

How do external tokens enter and outputs leave?

### G. Sparsity

Where does sparse positive activity matter?

### H. Graph structure

Why scale-free / heavy-tailed connectivity?

Each section should cite the primary source.

---

# 5. D4.2 — BDH-CQ Technical Dossier

Create:

```text id="0s1qne"
research/bdh/
└── bdhcq_technical_dossier.md
```

This should be even more detailed because BDH-CQ is directly relevant to our topic.

The current BDH-CQ paper describes:

1. In-context examples entering at inference.
2. Recurrent memory continuously updating.
3. A subsequent query.
4. Iterative reasoning in latent space.
5. No verbalized chain-of-thought.
6. No inference-time parameter updating in the described mechanism. ([arXiv][3])

We need to understand each component precisely.

---

# 6. BDH-CQ computational timeline

We should build an explicit execution timeline.

Conceptually:

```text id="7yk4z5"
demonstration 1
       ↓
memory update
       ↓
demonstration 2
       ↓
memory update
       ↓
demonstration 3
       ↓
memory update
       ↓
query
       ↓
latent recurrent computation × K
       ↓
answer
```

Then explicitly identify:

### What is static?

Model parameters.

### What evolves?

Recurrent memory.

### What is consumed?

Demonstrations.

### What is produced?

Candidate answer.

### Where does additional compute go?

Latent recurrent reasoning.

This directly connects the architecture to our central theme.

---

# 7. D4.3 — Concept-to-BDH Mapping

This should be one of the most important documents.

Create:

```text id="i01x75"
research/bdh/concept_mapping.md
```

We'll build something like:

| Our concept                | Our substrate    | BDH                      | BDH-CQ                      |
| -------------------------- | ---------------- | ------------------------ | --------------------------- |
| Task adaptation            | state update     | synaptic memory          | recurrent memory            |
| Inference-time information | demonstrations   | incoming activity        | input sequence              |
| Memory write               | state transition | Hebbian synaptic update  | recurrent memory update     |
| Persistent parameters      | fixed            | trained graph/parameters | trained parameters          |
| Query computation          | prediction       | iterative dynamics       | latent reasoning            |
| Interference               | measured         | relevant memory dynamics | relevant recurrent dynamics |

But every row must be backed by evidence.

We are **not** saying these systems are identical.

We're showing where the mechanisms are related.

---

# 8. Critical scientific distinction

This needs to be made explicit:

### Our recurrent-state model

is an **educational/research implementation**.

### BDH

is a specific architecture with its own neuron/synaptic dynamics.

### BDH-CQ

is a specific research model with its own recurrent memory and latent reasoning architecture.

Therefore:

> **Our model is a controlled experimental analogue, not an official BDH implementation.**

The Pathway brief explicitly requires such distinctions. 

---

# 9. D4.4 — BDH Equation Lab

This is where Phase 4 can become exceptional.

Pathway's current “Equations of Reasoning” page provides a formal local-dynamics formulation of BDH, including communication, synaptic-state updates, sparse positive activity, and recurrent state evolution. ([Pathway][4])

Rather than merely displaying those equations, we build an **interactive equation laboratory**.

---

# 10. The equation experience

Start with:

> **A model's memory does not need to be a separate database.**

Then show the relevant local dynamics.

The Pathway formulation describes a four-round cycle:

1. Communication / memory read.
2. Synaptic-state update via outer/Hebbian product.
3. Gated readout.
4. Neuronal state update. ([Pathway][4])

The learner can step through the rounds.

---

# 11. Make the memory write visible

For the educational simplification:

$$
\sigma_{t+1}
=
\sigma_t
+
\eta\,X_tY_t^\top
$$

or the exact published formulation that we settle on after studying the BDH paper.

The learner changes:

$$
\eta
$$

and sees:

$$
\Delta\sigma
$$

change.

But we must label the exact equation properly.

If it is a simplified derived representation:

> **Simplified educational form**

If directly from the paper:

> **Published BDH formulation**

No ambiguity.

---

# 12. Show memory as an evolving object

Instead of:

```text
Memory = 0.81
```

show:

```text id="6jtyc4"
BEFORE

        ┌──────────────┐
        │ synapse      │
        │ σ₁₂ = 0.14   │
        └──────────────┘

AFTER

        ┌──────────────┐
        │ synapse      │
        │ σ₁₂ = 0.67   │
        └──────────────┘
```

Then:

> **A local interaction changed the synaptic state.**

This is the exact kind of visible state the brief wants. 

---

# 13. D4.5 — BDH Evidence Ledger

Create:

```text id="i8m4on"
research/bdh/evidence_ledger.csv
```

Every technical claim gets:

```text id="4jeoqc"
claim
source
paper_section
evidence_type
official_result?
independent_result?
our_reproduction?
confidence
allowed_wording
```

For example:

| Claim                                            | Evidence                               |
| ------------------------------------------------ | -------------------------------------- |
| BDH uses synaptic plasticity for working memory  | primary paper                          |
| Specific synapses can strengthen for concepts    | primary empirical result               |
| BDH has sparse positive activations              | paper/result                           |
| BDH has scale-free graph structure               | paper                                  |
| BDH-CQ updates recurrent memory during inference | primary paper                          |
| BDH-CQ performs latent recurrent reasoning       | primary paper                          |
| 29.5% pass@2 on ARC-AGI-1                        | paper/official report                  |
| Independent reproduction                         | published/publicly documented evidence |
| Our toy implementation behaves similarly         | our experiment                         |

---

# 14. Evidence labels

We should standardize them:

### FORMAL

Mathematically established.

### PUBLISHED EMPIRICAL

Reported by paper authors from an experiment.

### OFFICIAL REPORT

Published by Pathway outside the paper.

### INDEPENDENT REPRODUCTION

External team reproduced the result.

### OUR REPRODUCTION

We reran it.

### TOY EXPERIMENT

Our controlled educational model.

### ILLUSTRATION

No computational claim.

This is exactly the kind of evidence discipline the brief demands. 

---

# 15. D4.6 — BDH Reproduction/Validation Suite

The official BDH repository is public and contains the baseline implementation and training instructions. ([GitHub][1])

This gives us an opportunity.

We should **not attempt to reproduce everything**.

Instead choose a small set of scientifically useful validations.

---

# 16. Candidate BDH reproduction A — Basic execution

Run the official repository.

Verify:

* environment,
* model construction,
* training,
* inference,
* state behavior.

Document the exact commit.

---

# 17. Candidate BDH reproduction B — Working-memory behavior

Find the smallest publicly documented experiment that exposes synaptic memory.

Reproduce it.

Record:

* setup,
* input,
* output,
* state,
* memory change.

This is highly relevant to our project.

---

# 18. Candidate BDH reproduction C — Interpretability

Where possible, reproduce one public demonstration of:

* sparse activation,
* synaptic concept association,
* state interpretability.

Only one or two.

The point is not to reproduce the entire BDH paper.

---

# 19. Candidate BDH reproduction D — Benchmark result

We need to be extremely cautious.

The official GitHub repository currently states that its open-source baseline **does not reproduce the internal 97.4% Sudoku Extreme result out of the box**. ([GitHub][1])

Therefore:

### We should NOT

download the repository and say:

> “We reproduced 97.4% BDH Sudoku.”

That would be scientifically incorrect.

Instead we should write:

> **“The 97.4% result is reported for Pathway's internal BDH implementation; the public repository notes that it does not reproduce this result out of the box.”**

That's exactly the kind of evidence distinction the competition expects.

---

# 20. BDH-CQ reproduction strategy

This needs even more care.

There is now a public third-party implementation of BDH-CQ, but it explicitly identifies itself as a **work in progress** implementation rather than the official Pathway implementation. ([GitHub][5])

Therefore:

### We may use it for research exploration.

But:

### We cannot present it as an official implementation.

And unless it reproduces a documented result, we cannot call it a reproduction of the Pathway benchmark.

---

# 21. BDH-CQ validation plan

I recommend three levels.

## Level 1 — Architecture verification

Instantiate the public implementation and verify that:

```text
input chunk
→ memory
→ latent reasoning
→ answer
```

exists as described.

## Level 2 — Tiny controlled experiment

Use a small synthetic task.

Check whether the implementation exhibits inference-time recurrent memory behavior.

## Level 3 — Published benchmark

Only attempt this if resources and implementation fidelity allow it.

If it doesn't reproduce the published benchmark:

**report that honestly.**

A failed reproduction is still scientifically valuable.

---

# 22. D4.7 — Frontier Comparison Study

Now compare:

### Our controlled methods

with:

### Published frontier mechanisms.

We should compare on:

| Dimension             | Frozen ICL | Parameter TTA | State TTA | BDH | BDH-CQ |
| --------------------- | ---------: | ------------: | --------: | --: | -----: |
| Inference adaptation  |            |               |           |     |        |
| Parameters changed    |            |               |           |     |        |
| State changed         |            |               |           |     |        |
| Memory substrate      |            |               |           |     |        |
| Adaptation cost       |            |               |           |     |        |
| Long-horizon behavior |            |               |           |     |        |
| Interference          |            |               |           |     |        |
| Interpretability      |            |               |           |     |        |
| Latent reasoning      |            |               |           |     |        |

But this table must distinguish:

**our measurements**

from:

**published claims**

from:

**qualitative architectural differences**.

---

# 23. Don't compare incomparable numbers

For example:

> “Our tiny model gets 91%, BDH-CQ gets 29.5%, therefore our model is better.”

Obviously invalid.

Different:

* models,
* tasks,
* training regimes,
* task distributions,
* evaluation settings.

Comparison should be made at the **mechanism level** unless evaluation conditions genuinely match.

---

# 24. D4.8 — ARC / Novel Task Validation Layer

This is where we connect our synthetic lab to a real reasoning setting.

The public `arc-task-gen` ecosystem is particularly relevant because it is designed to produce new ARC-like tasks and complement public ARC evaluation with private generated tasks. ([GitHub][6])

This gives us a powerful route:

```text id="4n0qc0"
our task generator
      ↓
ARC-like structure
      ↓
demonstrations
      ↓
hidden transformation
      ↓
novel input
      ↓
exact output
```

---

# 25. Why this matters

Public benchmarks have potential contamination/familiarity issues.

A generated evaluation set can ask:

> **Can the system infer a genuinely unseen transformation?**

The `arc-task-gen` project explicitly identifies this motivation. ([GitHub][6])

That fits our central question extremely well.

---

# 26. Build two evaluation modes

### Controlled mode

Our own synthetic rule family.

Perfect experimental control.

### Frontier mode

ARC-style novel tasks.

Higher ecological/research relevance.

This gives us:

**mechanistic rigor + frontier relevance**

without depending entirely on ARC.

---

# 27. D4.9 — BDH-CQ Educational Experience

Now we finally integrate the research into the public product.

The narrative should be:

# **You just discovered inference-time adaptation.**

Then:

> “Now look at what a frontier architecture does with the same broad design pressure.”

---

# 28. Transition experience

The learner sees:

```text id="7l9b2c"
You saw:

DEMONSTRATIONS
      ↓
ADAPTATION
      ↓
NEW QUERY
      ↓
ANSWER
```

Then:

> **Where was the task information stored?**

They answer.

Then:

> **Now inspect a real architecture built around evolving internal memory.**

---

# 29. BDH-CQ experience

Show:

```text id="dr3mih"
DEMONSTRATION 1
       ↓
  MEMORY STATE
       ↓
DEMONSTRATION 2
       ↓
  MEMORY STATE
       ↓
DEMONSTRATION 3
       ↓
  MEMORY STATE
       ↓
      QUERY
       ↓
LATENT COMPUTATION
       ↓
     ANSWER
```

Then allow the learner to scrub through the process.

---

# 30. Don't pretend we can visualize semantic latent reasoning

This needs a strong disclaimer.

We can show:

* recurrent steps,
* state norms,
* state similarity,
* memory changes,
* output probabilities,
* timing.

We should **not** claim:

> “Step 17 means the model is thinking about shape.”

unless the paper provides evidence.

Instead:

> **“The system performs another latent computation step; the semantic content of individual hidden states is not directly interpretable from this visualization.”**

That is scientifically honest.

---

# 31. D4.10 — Scientific Integrity Audit

Before Phase 4 ends, conduct a brutal audit.

Take every sentence displayed to the learner about BDH.

Ask:

> **What source supports this?**

Every sentence must fit into one category:

```text
Published fact
Our experimental result
Interpretation
Illustration
Hypothesis
```

Never allow these to blur together.

---

# 32. Specific claims we should audit

### “BDH learns at inference.”

What exactly does “learns” mean?

Does it mean:

* synaptic state update?
* temporary memory?
* parameter update?
* task acquisition?

We need precise terminology.

### “BDH is an SSM.”

The Pathway brief explicitly warns against classifying BDH as an SSM in the Mamba sense. 

So our wording must be:

> **BDH has a GPU-friendly state-space formulation**

not:

> “BDH is just another Mamba-style SSM.”

---

# 33. Another important audit

### “BDH-CQ is TTT.”

We should avoid that blanket statement.

Better:

> **BDH-CQ occupies a closely related point in the broader inference-time adaptation design space, where inputs update recurrent memory during inference without modifying model parameters in the described mechanism.**

This is accurate and nuanced.

---

# 34. Another audit

### “The state stores the rule.”

That may be too strong.

Better:

> **Task-specific information is represented in the evolving state, as evidenced by changes in task-conditioned state and subsequent behavior.**

This is empirically defensible.

---

# 35. D4.11 — Phase 4 Research Report

Create:

```text id="kmor7j"
research/reports/
└── phase4_bdh_frontier_report.pdf
```

Recommended structure:

## 1. Research question

## 2. BDH architecture

## 3. BDH memory

## 4. BDH-CQ architecture

## 5. Connection to inference-time adaptation

## 6. Experimental methodology

## 7. Reproduced experiments

## 8. Non-reproduced/official-only results

## 9. Comparative analysis

## 10. Limitations

## 11. Educational implications

This becomes one of the main sources for the final blog and one-page summary.

---

# 36. The actual Phase 4 research experiments

I would structure them into four groups.

---

# GROUP A — Mechanism validation

### A1

Our state adaptation.

### A2

Parameter adaptation.

### A3

BDH-inspired synaptic update.

### A4

BDH-CQ-style recurrent memory where practical.

Goal:

> **Show that different memory-update mechanisms produce different computational behavior.**

---

# GROUP B — Memory behavior

### B1

State capacity.

### B2

Interference.

### B3

Persistence.

### B4

Noise.

### B5

Task switching.

Goal:

> **Characterize the limits of adaptive memory.**

---

# GROUP C — Frontier validation

### C1

ARC-like tasks.

### C2

Generated novel tasks.

### C3

Selected published BDH-CQ analysis.

Goal:

> **Connect controlled observations to frontier reasoning environments.**

---

# GROUP D — Cost

### D1

Latency.

### D2

Inference compute.

### D3

Memory footprint.

### D4

Adaptation steps.

Goal:

> **Understand the cost of adaptation.**

This matters because the Pathway brief explicitly asks learners to understand inference-time scaling and cost/accuracy trade-offs where relevant. 

---

# 37. One powerful Phase 4 result

I would like us to produce a plot like:

$$
\text{Adaptation Gain}
$$

versus:

$$
\text{Retention}
$$

for each mechanism.

Conceptually:

```text
Retention
  ↑
  |
  | ●
  |   ●
  |       ●
  |          ●
  |               ●
  +----------------------→
       Adaptation Gain
```

This gives us a real scientific trade-off.

But we let the data determine the actual shape.

---

# 38. Another important result

Plot:

$$
Accuracy
$$

against:

$$
Inference\ Cost
$$

for our relevant mechanisms and, where comparable, published frontier systems.

This aligns directly with the Pathway brief's interest in cost–accuracy Pareto frontiers. 

Again, we must not merge incomparable evaluations into one misleading plot.

Where results aren't directly comparable, separate them visually.

---

# 39. A third important result

Plot:

$$
Task\ Accuracy
$$

versus:

$$
Demonstration\ Count
$$

for:

* frozen,
* parameter TTA,
* state adaptation.

This is likely to be one of the most educationally useful figures in the final product.

---

# 40. A fourth important result

State trajectory:

$$
s_0 \rightarrow s_1 \rightarrow s_2 \rightarrow ... \rightarrow s_k
$$

after demonstrations.

Then after another task:

$$
s_k \rightarrow s'_1 \rightarrow ... 
$$

Show retention.

This visually connects:

**memory formation**

to:

**interference**

to:

**task adaptation**.

---

# 41. Build a causal experiment, not just correlations

Suppose we observe:

> Larger state → higher accuracy.

We should ask:

> Is state dimension actually causing the improvement?

Control:

* same tasks,
* same model,
* same training,
* same adaptation algorithm,
* same seeds,
* only state dimension changed.

This gives us a controlled intervention.

---

# 42. Phase 4 should also introduce perturbation tests

For state-based adaptation:

### Perturb state after demonstrations.

Then query again.

If performance drops:

$$
A(s+\delta)
<
A(s)
$$

that's evidence that the state is functionally involved.

Likewise:

### Restore old state.

Does prior task behavior return?

This can provide a much stronger mechanistic argument than merely observing that “the state changed.”

---

# 43. Memory intervention experiment

This could be one of our flagship research experiments.

Pipeline:

```text id="73es8w"
Task A
 ↓
adapt
 ↓
save state S_A
 ↓
Task B
 ↓
adapt
 ↓
state S_B
 ↓
restore S_A
 ↓
query Task A
```

If A recovers:

> state contains task-relevant information.

This is a **causal intervention** on the memory substrate.

That is a much stronger scientific demonstration.

---

# 44. Parameter intervention experiment

Similarly:

```text id="eom81q"
Task A
 ↓
parameter-TTA
 ↓
θ_A
 ↓
Task B
 ↓
θ_B
 ↓
restore θ_A
 ↓
query A
```

Then compare with the state mechanism.

Now our central claim is not merely descriptive.

We have actual interventions.

---

# 45. This is how we can make the project research-paper level

The core scientific contribution becomes something like:

> **A controlled experimental framework for studying inference-time task adaptation across context-, parameter-, and state-based memory substrates, with explicit interventions on memory capacity and retention, and a frontier-oriented mapping to BDH/BDH-CQ.**

That is much stronger than:

> “We made an interactive TTA explainer.”

---

# 46. Important: don't turn Phase 4 into a BDH benchmark contest

The objective isn't:

> “Beat BDH-CQ.”

That would be unrealistic and unnecessary.

We're studying the **mechanism**, not trying to become Pathway.

The brief doesn't require us to reproduce or outperform BDH-CQ; it requires a technically correct BDH/BDH-CQ connection and evidence-backed explanation. 

---

# 47. Phase 4 product integration

The final product should now have:

```text id="f9oyoa"
            ADAPT
              │
     ┌────────┴────────┐
     ▼                 ▼
  LEARN              EXPLORE
     │                 │
     ▼                 ▼
Core Experiment     Research Lab
     │                 │
     └────────┬────────┘
              ▼
         MEMORY TYPES
              │
       ┌──────┼───────┐
       ▼      ▼       ▼
    Context  State  Parameters
              │
              ▼
          STRESS TEST
              │
              ▼
             BDH
              │
              ▼
           BDH-CQ
              │
              ▼
       FRONTIER EVIDENCE
              │
              ▼
        FINAL CHALLENGE
```

---

# 48. Product wording hierarchy

The learner-facing language should progress from intuitive to technical.

### First:

> “Something changed.”

### Then:

> “The model adapted.”

### Then:

> “The state changed while the trained parameters remained fixed.”

### Then:

> “Here is the recurrence.”

### Then:

> “Here is how the corresponding idea appears in BDH-CQ.”

This controls cognitive load without compromising technical rigor.

---

# 49. What Phase 4 should add to the learner

By the end, the learner should be capable of distinguishing:

```text id="5zqsbi"
IN-CONTEXT LEARNING
≠
PARAMETER TTA
≠
ORDINARY RECURRENT STATE
≠
LEARNED TTT STATE
≠
BDH SYNAPTIC MEMORY
≠
BDH-CQ RECURRENT MEMORY
```

They are related.

They are not identical.

That distinction is one of our strongest educational contributions.

---

# 50. Phase 4 testing

We need two kinds of testing.

## Scientific testing

Can an ML researcher attack our claims?

## Educational testing

Can a technically competent learner correctly distinguish the mechanisms afterward?

Both are necessary.

---

# 51. Scientific red-team questions

A reviewer should ask:

> Are your three mechanisms really comparable?

> Are your tasks testing adaptation or memorization?

> Are your synthetic tasks too easy?

> Does state change actually encode task information?

> Are your state visualizations misleading?

> Is your BDH connection substantive?

> Are you confusing BDH with TTT?

> Are your benchmark comparisons apples-to-apples?

> Are your claims stronger than the evidence?

These should become explicit checks.

---

# 52. Phase 4 failure conditions

This phase can fail scientifically.

### Failure A

Our state adaptation provides no meaningful advantage.

Then revisit the mechanism.

### Failure B

Our task generator is too easy.

Increase compositional complexity.

### Failure C

Our “memory visualization” isn't causally related to performance.

Don't present it as meaningful.

### Failure D

We cannot faithfully connect our mechanism to BDH-CQ.

Then narrow the connection rather than inventing one.

### Failure E

A reproduction doesn't work.

Document the failure and its conditions rather than hiding it.

---

# 53. Phase 4 Definition of Done

### BDH

☐ BDH architecture fully understood.

☐ Relevant equations mapped.

☐ Memory mechanism validated.

☐ Official repository examined.

☐ At least one useful public BDH behavior reproduced or inspected directly.

☐ Internal-only results clearly distinguished.

---

### BDH-CQ

☐ Primary paper fully understood.

☐ Inference-time memory process mapped.

☐ Latent reasoning process understood.

☐ Demonstration/ICL behavior understood.

☐ ARC evaluation methodology understood.

☐ Official reported results correctly cited.

☐ Third-party implementations, if used, clearly identified as third-party.

---

### Scientific comparison

☐ Same task distributions used where comparisons are direct.

☐ Intervention experiments complete.

☐ State capacity tested.

☐ Interference tested.

☐ Demonstration scaling tested.

☐ Adaptation compute tested.

☐ Retention tested.

☐ Novel-task/ARC-like validation performed.

---

### Educational integration

☐ BDH appears naturally in the narrative.

☐ BDH has its own learning objective.

☐ At least one equation/diagram/live experiment/precomputed result is integrated.

☐ Official vs independent implementation clearly labelled.

☐ Evidence status visible.

☐ Learner can explain the BDH connection afterward.

---

### Scientific integrity

☐ Every claim has evidence.

☐ No unsupported semantic interpretation of latent states.

☐ No fake BDH reproduction.

☐ No apples-to-oranges benchmark comparison.

☐ Failed experiments documented.

☐ Limitations documented.

---

# 54. Phase 4 final package

The repository should now contain:

```text id="yh8l4y"
research/
│
├── bdh/
│   ├── bdh_technical_dossier.md
│   ├── bdhcq_technical_dossier.md
│   ├── concept_mapping.md
│   ├── equations/
│   ├── evidence_ledger.csv
│   └── reproductions/
│
├── experiments/
│   ├── mechanism/
│   ├── state_capacity/
│   ├── interference/
│   ├── retention/
│   ├── compute/
│   └── arc_like/
│
├── results/
│   ├── raw/
│   ├── processed/
│   ├── figures/
│   └── tables/
│
└── reports/
    └── phase4_bdh_frontier_report.pdf
```

---

# 55. The Phase 4 exit gate

We should not move to the final production-hardening phase until this experiment is working:

```text id="5tn3gy"
          UNSEEN TASK
               │
               ▼
        DEMONSTRATIONS
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    FROZEN   PARAM    STATE
             TTA       TTA
       │       │        │
       └───────┼────────┘
               ▼
          NOVEL QUERY
               │
               ▼
          GROUND TRUTH
               │
               ▼
       ┌───────────────┐
       │ INTERVENTION  │
       │               │
       │ alter/restore │
       │ memory state  │
       └───────┬───────┘
               ▼
          RETENTION
               │
               ▼
             BDH
               │
               ▼
           BDH-CQ
               │
               ▼
      RESEARCH EVIDENCE
```

And we should be able to tell the judges:

> **Here is our claim.**

> **Here is the experiment.**

> **Here is what changed.**

> **Here is the ground truth.**

> **Here is the limitation.**

> **Here is the published BDH mechanism that provides the frontier connection.**

> **Here is exactly what we reproduced ourselves.**

> **Here is what we did not reproduce.**

> **Here is how the learner discovers all of this inside the artifact.**

That is what makes Phase 4 valuable.

---

# 56. The deeper purpose of Phase 4

There is an especially interesting opportunity here because Pathway's own current framing of the **Equations of Reasoning** is explicitly about connecting microscopic local dynamics with macroscopic memory, adaptation and reasoning, including studying stability and failure regimes rather than relying only on benchmark snapshots. ([Pathway][4])

That aligns beautifully with what our project is trying to do:

```text
MODEL OUTPUT
     ↓
INTERNAL STATE
     ↓
STATE UPDATE
     ↓
MEMORY
     ↓
ADAPTATION
     ↓
BEHAVIOR
```

So Phase 4 can elevate the project from:

> **“Here's an interactive TTA explanation.”**

to:

> **“Here's an experimentally grounded way to inspect how inference-time memory changes computation, and here's how that design question appears in one of the current Post-Transformer research programs.”**

That is a much more credible research narrative.

---

# 57. Recommended Phase 4 priority order

There is a lot we *could* do here, but I would prioritize:

### Priority 1

**BDH-CQ primary-paper reconstruction**

Understand exactly what the system does.

### Priority 2

**BDH equations / synaptic-memory mechanism**

Make the connection mathematically concrete.

### Priority 3

**Memory intervention experiments**

Prove that our adaptive state actually matters causally.

### Priority 4

**ARC-like novel-task experiments**

Connect controlled adaptation to a frontier reasoning regime.

### Priority 5

**Selective BDH reproduction**

Only reproduce results that genuinely illuminate our claim.

### Priority 6

**Full educational integration**

Convert the validated material into the final learner journey.

This order keeps us from wasting time reproducing irrelevant benchmark numbers.

---

# 58. One thing I would add that wasn't explicit in our earlier phases

## Build a **Mechanism Provenance Graph**

For every important statement in the application:

```text
UI statement
     ↓
scientific claim
     ↓
equation / experiment
     ↓
source
     ↓
evidence type
     ↓
version
```

Example:

```text
"State changed after demonstrations"
           ↓
Δs = ||s_after - s_before||
           ↓
Experiment #0042
           ↓
Model: recurrent_state_v3
           ↓
Seed: 17
           ↓
Code commit: abc123
```

This is extremely powerful for a research-grade product.

It means every major visualization can ultimately be traced to a real computation.

---

# 59. Phase 4 in one sentence

If I had to summarize the entire phase:

> **Phase 4 takes our validated adaptation engine, rigorously maps its mechanisms to BDH and BDH-CQ, validates the relationship through primary-source analysis, controlled interventions and carefully selected reproductions, and then embeds that evidence into the learner's experience without overclaiming what the research demonstrates.**

That is the right level of seriousness for this submission.

And once Phase 4 is complete, the scientific core is essentially locked. **Phase 5 should then be production hardening, evaluation, documentation, and submission engineering—where we turn the research artifact into a robust public product and systematically attack every one of the Pathway judging criteria before submission.**

[1]: https://github.com/pathwaycom/bdh/?utm_source=chatgpt.com "GitHub - pathwaycom/bdh: BDH (Dragon Hatchling) – Architecture and Code · GitHub"
[2]: https://arxiv.org/abs/2509.26507?utm_source=chatgpt.com "The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain"
[3]: https://arxiv.org/abs/2608.09888?utm_source=chatgpt.com "BDH-CQ: In-Context Learning with Recurrent Latent Reasoning"
[4]: https://pathway.com/research/the-equations-of-reasoning?utm_source=chatgpt.com "The Equations of Reasoning | Pathway"
[5]: https://github.com/lucidrains/bdh-cq/blob/main/README.md?utm_source=chatgpt.com "bdh-cq/README.md at main · lucidrains/bdh-cq · GitHub"
[6]: https://github.com/pathwaycom/arc-task-gen/blob/main/README.md?utm_source=chatgpt.com "arc-task-gen/README.md at main · pathwaycom/arc-task-gen · GitHub"
