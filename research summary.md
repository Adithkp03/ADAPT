I researched this as a **research problem**, not as a hackathon implementation exercise. I also checked the Pathway brief against current primary sources because the brief specifically requires recent evidence and because BDH-CQ was released only recently. The most important conclusion is that **“Test-Time Adaptation” is a viable topic, but our original framing needs to be sharpened substantially**.

The research landscape is richer—and more technically interesting—than simply “weights vs recurrent state.”

---

# 1. First: what exactly is “Test-Time Adaptation”?

There is a terminology problem we need to resolve early.

The original **Test-Time Training (TTT)** literature introduced a setting where a model receives test data, creates a self-supervised learning problem from it, updates its parameters, and then makes predictions. Sun et al. introduced this in 2020 for distribution shift. ([Proceedings of Machine Learning Research][1])

The current language-model research uses the phrase more broadly. For example, Akyürek et al. use TTT for **temporarily updating model parameters during inference using losses derived from the test/input examples**, and demonstrate this on ARC and BBH. ([Proceedings of Machine Learning Research][2])

Then the 2025 TTT work changes the picture again: instead of treating the *whole model's parameters* as the inference-time memory, the **hidden state itself can be a learned model** that is updated during test-time. TTT-Linear and TTT-MLP are explicit examples. ([Proceedings of Machine Learning Research][3])

And BDH-CQ introduces yet another point in this family: inference-time inputs continuously update a recurrent memory, followed by latent recurrent reasoning, without parameter updates or a verbal reasoning trace. ([arXiv][4])

So our project should **not** teach “TTT = gradient-descent at test time.”

That would already be outdated/incomplete.

A better abstraction is:

> **Test-time adaptation is about how a trained system uses information encountered during inference to change the computation it performs on subsequent inputs.**

Then the key research question becomes:

# **Where is the adaptation stored, how is it updated, and what does that choice cost?**

That is much stronger.

---

# 2. The conceptual map we need

The research landscape can be organized around a single axis:

```text
                 WHERE DOES NEW TASK INFORMATION LIVE?
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
       CONTEXT                  STATE                   WEIGHTS
          │                       │                        │
   retain examples        recurrent hidden state      update parameters
          │                       │                        │
       standard ICL       state-space / TTT-RNN      TTT / TTT-NN
          │                       │                        │
          └───────────────────────┼────────────────────────┘
                                  │
                              HYBRIDS
                                  │
                         context + state
                         state + attention
                         memory + weights
```

This is the framework I think our product should eventually teach.

But we need to be extremely precise:

**ICL itself does not automatically imply state updates.**

A standard Transformer doing ICL can produce different outputs from demonstrations without changing its parameters. Papers such as Garg et al. and Li et al. study ICL as inference-time algorithmic behavior. ([Papers with Code][5])

---

# 3. ICL vs Test-Time Adaptation vs Meta-Learning

This distinction is foundational.

## In-Context Learning

The model receives:

$$
D = \{(x_i,y_i)\}_{i=1}^k
$$

and then predicts:

$$
\hat y = f_\theta(D,x)
$$

The model's parameters \(\theta\) do not change.

The model is therefore **conditioning on examples**, rather than literally gradient-updating the parameters.

Li et al. formalize ICL as a learned algorithm in which the Transformer effectively constructs a hypothesis at inference time. ([Proceedings of Machine Learning Research][6])

And von Oswald et al. showed that, at least for some controlled regression settings, a Transformer trained for ICL can implement behavior closely related to gradient descent during its forward pass. ([Proceedings of Machine Learning Research][7])

That result is extremely relevant to us because it destroys the naive distinction:

> “ICL is not learning; TTT is learning.”

It's more subtle.

A system can **implement an optimization-like learning algorithm in its forward pass without changing the model parameters**.

---

# 4. Meta-learning is one level above this

Meta-learning means the **training process teaches the model how to adapt to tasks**.

MAML is the canonical formulation:

$$
\theta'_T =
\theta - \alpha \nabla_\theta L_T(\theta)
$$

The outer loop learns an initialization \(\theta\) from which a small number of task-specific gradient steps produce good performance. ([Proceedings of Machine Learning Research][8])

So:

```text
META-TRAINING
        │
        ▼
learn parameters that adapt well
        │
        ▼
NEW TASK
        │
        ▼
gradient steps
        │
        ▼
adapted parameters
```

The critical distinction:

### Meta-learning

**learn how to adapt**

### Test-time adaptation

**perform that adaptation at inference**

### ICL

**perform inference conditioned on examples without explicit parameter updates**

These can overlap.

A model can be meta-trained to become a good in-context learner.

Kirsch et al. explicitly demonstrate general-purpose ICL through meta-training and note a bottleneck imposed by the accessible state/memory size. ([arXiv][9])

---

# 5. Why this becomes fascinating for our project

Because we can ask:

> **If the model can learn a new task at inference time, does it need to change its weights?**

The answer is **no**.

That is the basic premise of ICL.

Then ask:

> **Can it literally optimize parameters at inference time?**

Yes.

That is TTT.

Then:

> **Can the “learning” machinery itself be stored in a recurrent hidden state?**

Yes.

That's the newer TTT-RNN line of work. ([Proceedings of Machine Learning Research][3])

Then:

> **Can an architecture make inference-time memory part of its native computational structure?**

That is where BDH/BDH-CQ becomes particularly interesting. ([arXiv][10])

This is a much more interesting scientific narrative than simply “TTA improves accuracy.”

---

# 6. The mathematical distinction we should teach

The simplest useful abstraction is:

## Frozen parameters + context

$$
y_t = f_\theta(x_{\le t})
$$

Nothing changes except the input context.

---

## Frozen parameters + recurrent state

$$
s_t = F_\theta(s_{t-1},x_t)
$$

$$
y_t = G_\theta(s_t)
$$

Now task information can accumulate in \(s_t\).

---

## Parameter adaptation

$$
\theta_{t+1}
=
\theta_t
-
\eta \nabla_\theta L(x_t;\theta_t)
$$

and then:

$$
y_t = f_{\theta_t}(x_t)
$$

Now task-specific information is stored in parameter changes.

---

## TTT-style learned hidden state

The interesting 2025 TTT formulation makes the state itself a model:

$$
S_t \leftarrow S_{t-1}
-
\eta_t\nabla_{S} \mathcal L_t(S_{t-1})
$$

where \(S\) can itself represent a linear model or MLP.

That means the state isn't merely a vector containing an encoded summary.

**The state is itself computational machinery.**

This is a major conceptual upgrade and one of the reasons the TTT research is important. ([Proceedings of Machine Learning Research][3])

---

# 7. This connects directly to fast weights

Fast weights are historically important because they blur the boundary between:

**memory**

and

**parameters**.

The classic fast-weight interpretation of linear attention shows that an attention mechanism can be understood as dynamically programming a rapidly changing associative memory. Schlag et al. formalized the relationship between linearized attention and fast-weight programmers. ([Proceedings of Machine Learning Research][11])

This matters because our eventual narrative can become:

```text
slow weights
      ↓
fast weights
      ↓
contextual memory
      ↓
recurrent state
      ↓
learned state
```

These aren't all the same mechanism, but they occupy related points in the **“where does transient knowledge live?”** design space.

This is exactly where BDH becomes intellectually useful.

---

# 8. BDH is not simply “another TTT method”

This is a crucial correction to our earlier framing.

The original BDH paper describes a **brain-inspired Post-Transformer architecture** with scale-free graph connectivity, sparse positive activations, synaptic plasticity, and working memory implemented through Hebbian updates to synapses. ([arXiv][10])

Pathway's current “Equations of Reasoning” material makes the connection explicit:

* neurons maintain evolving states,
* synapses carry a state \(\sigma\),
* activity reads from and updates that synaptic state,
* Hebbian outer-product updates act as memory writes,
* repeated local computation produces larger-scale inference dynamics. ([Pathway][12])

So BDH gives us a fascinating conceptual proposition:

> **Memory can be implemented as transient changes in the computational fabric itself.**

That is more specific than “the hidden state changes.”

---

# 9. BDH-CQ is closer to our selected topic

The new BDH-CQ paper is particularly important.

It explicitly combines:

### In-context learning

with

### recurrent latent reasoning.

The paper says that inputs presented during inference **continuously update recurrent memory**, and the model then answers the query through iterative computation in a high-dimensional latent space, without verbalizing intermediate reasoning. ([arXiv][4])

The paper also evaluates this on ARC-AGI-1 and uses **controlled ARC-like interventions** to investigate what the model learns from demonstrations, consistency of the inferred transformation, and difficult concepts. ([arXiv][4])

This is almost tailor-made for our project.

---

# 10. ARC is not just a benchmark here

ARC is critical because it creates a clean test of **task acquisition from demonstrations**.

The basic structure is:

```text
Example 1:
input grid → output grid

Example 2:
input grid → output grid

Example 3:
input grid → output grid

             ↓

       infer hidden rule

             ↓

       novel test input

             ↓

       predict output
```

ARC therefore gives us exactly what we need:

* demonstrations,
* hidden task rule,
* novel query,
* exact ground truth.

The original ARC repository defines a solved task as producing the correct output grid on the previously unseen test inputs, including the correct dimensions. ([GitHub][13])

ARC-AGI-2 has subsequently been designed to push this kind of abstract reasoning further. ([ARC Prize][14])

---

# 11. Why ARC changed the TTT conversation

This is one of the strongest pieces of evidence for choosing this topic.

Akyürek et al.'s work showed that **test-time parameter adaptation can substantially improve abstract reasoning on ARC**. Their 2025 ICML paper reports up to a 6× improvement over the relevant fine-tuned baselines, with 53.0% on ARC's public validation set using an 8B LM, and 61.9% when combined with program-synthesis methods. ([Proceedings of Machine Learning Research][2])

The significance isn't just the score.

It's that:

> **A model can use a handful of task-specific examples to perform additional learning at test time, rather than relying entirely on what was encoded in its fixed parameters.**

That is exactly the phenomenon our learner needs to understand.

---

# 12. And the field has continued moving

There are now several distinct research directions:

### TTT via parameter updates

Akyürek et al.
Hardt & Sun
TTT-NN

([Proceedings of Machine Learning Research][2])

### TTT via learned hidden states

TTT-Linear / TTT-MLP.

([Proceedings of Machine Learning Research][3])

### Long-context test-time learning

TTT-E2E.

Its authors formulate long-context modeling as continual learning and compress context into model weights through next-token prediction at test time. They report constant inference latency with context length in their setup and release checkpoints/code. ([arXiv][15])

### Learned long-term memory architectures

Titans and ATLAS.

Titans explicitly separates attention-like short-term memory from a learned long-term neural memory. ([arXiv][16])

ATLAS frames long-term memory itself as something that can be optimized over current and past tokens rather than updated only from the most recent input. ([arXiv][17])

### BDH-CQ

Recurrent memory + latent reasoning + ICL.

([arXiv][4])

This gives us a genuinely active 2023–2026 research landscape.

---

# 13. The deepest conceptual question

After reading this literature, I think our original question:

> “Where does the new rule go?”

is good, but it needs one addition:

# **“What mechanism performs the update?”**

Because two systems might both have a changing state, yet behave radically differently.

So our research framework should be:

| Question                  | Possible answer                                              |
| ------------------------- | ------------------------------------------------------------ |
| What changes?             | context / hidden state / weights / fast memory               |
| How does it change?       | conditioning / recurrence / gradient descent / Hebbian write |
| When does it change?      | before inference / during inference / between examples       |
| What persists?            | one query / one task / sequence / session                    |
| What is the capacity?     | context length / state dimension / parameter count           |
| What is the failure mode? | forgetting / interference / instability / cost               |
| Is the update learned?    | fixed rule / learned update / optimizer                      |
| Can we inspect it?        | high / medium / low                                          |

Now we have a genuine research taxonomy.

---

# 14. Candidate experiment 1 — Hidden-rule regression

This should be our **first prototype**, because the science is easy to control.

Generate a task:

$$
y = ax+b
$$

but choose a different \(a,b\) for every task.

The learner/model receives:

$$
(x_1,y_1), (x_2,y_2), \ldots
$$

then must predict \(y_q\).

Now compare:

### Frozen ICL model

No explicit update.

### TTA

Actually update parameters using the demonstrations.

### Recurrent-state model

Update a state representation.

Because the underlying task rule is known exactly, we have perfect ground truth.

This gives us a clean mathematical environment before touching ARC.

---

# 15. Candidate experiment 2 — Rule families

Move from regression to discrete functions.

Example:

```text
A → C
B → D
C → E
```

Hidden transformation varies per task.

The model gets demonstrations and must infer the transformation.

This is visually intuitive and ideal for the educational UI.

---

# 16. Candidate experiment 3 — ARC-like grids

Then move into:

```text
GRID
↓
DEMONSTRATIONS
↓
HIDDEN TRANSFORMATION
↓
NOVEL GRID
↓
PREDICTION
↓
GROUND TRUTH
```

Now the learner sees why abstract reasoning is difficult.

The ARC benchmark is useful precisely because the examples encode the task rather than merely providing more instances of a fixed classification problem. ([GitHub][13])

---

# 17. Candidate experiment 4 — Demonstration ablation

This is scientifically essential.

Start with:

**1 demonstration**

Then:

**2**

**3**

**4**

etc.

Plot:

$$
\text{adaptation accuracy}
\quad\text{vs}\quad
\text{number of demonstrations}
$$

Now the learner can directly observe the relationship between evidence and adaptation.

This connects naturally to both ICL and TTA research. ([Proceedings of Machine Learning Research][6])

---

# 18. Candidate experiment 5 — Conflicting demonstrations

This is potentially one of our strongest experiments.

Suppose:

```text
Example A → Rule 1
Example B → Rule 1
Example C → Rule 2
Example D → Rule 2
```

Now ask the model to infer what applies.

The learner can control:

**conflict level**

and observe what happens.

For recurrent memory, this can expose:

**interference**

For parameter TTA, it can expose:

**optimization instability / catastrophic interference**

For context-based approaches, it can expose:

**attention competition**

This makes the failure mode a central scientific phenomenon rather than a disclaimer.

---

# 19. Candidate experiment 6 — Adaptation compute

Let the learner vary:

$$
K = \text{number of adaptation steps}
$$

Then measure:

$$
\text{accuracy}(K)
$$

and:

$$
\text{latency}(K)
$$

Potential result:

```text
more test-time computation
          │
          ▼
      better adaptation
          │
          └──────► higher cost
```

This connects naturally to the Pathway brief's emphasis on inference-time scaling and BDH-CQ's low/medium/high-effort results. 

---

# 20. Candidate experiment 7 — State capacity

This may become the most important recurrent-memory experiment.

Let:

$$
d_s = \text{state dimension}
$$

and measure task performance as \(d_s\) changes.

The learner gets:

```text
SMALL STATE
████

MEDIUM STATE
████████

LARGE STATE
████████████████
```

Then observe:

$$
\text{accuracy} \; \text{vs} \; d_s
$$

This is not arbitrary. The broader ICL/meta-learning literature already identifies accessible state size as an important limitation for learned in-context algorithms. ([arXiv][9])

---

# 21. Candidate experiment 8 — Retention vs interference

This is the one I would most like to investigate for the final product.

Teach the model:

**Task A**

then:

**Task B**

then ask it about **Task A** again.

Now quantify:

$$
R_A = \text{accuracy on A after learning B}
$$

This gives us a measurable version of:

> **How much does adapting to something new damage what was already learned?**

That creates a bridge to:

* recurrent memory,
* continual learning,
* synaptic plasticity,
* fast weights,
* state capacity,
* catastrophic interference.

And because the Pathway brief explicitly includes continual/online learning and stability–plasticity as a related area, this is scientifically coherent. 

---

# 22. The fast-weight connection becomes useful here

Suppose we have an associative memory represented as:

$$
M_{t+1}
=
M_t + \eta\, k_t v_t^\top
$$

This is the basic outer-product/Hebbian-style write idea underlying fast-weight interpretations of linear attention. ([Proceedings of Machine Learning Research][11])

Now a learner can literally watch:

```text
before demonstration
M = ...

after demonstration
M = M + ΔM
```

Then ask:

> Which associations were written?

That is far more pedagogically powerful than a paragraph saying “the model stores information in memory.”

And it provides a clean conceptual bridge into BDH's synaptic memory formulation.

---

# 23. BDH gives us a microscopic interpretation

The Pathway material is unusually useful here.

Their “Equations of Reasoning” describe a local process in which:

1. current activity reads the existing synaptic state,
2. synaptic state gets updated through an outer/Hebbian product,
3. activity is transformed/gated,
4. the neural state is updated again. ([Pathway][12])

That suggests a beautiful conceptual bridge:

```text
MACRO
"the model learned the task"

        ↓

MESO
"its internal memory changed"

        ↓

MICRO
"specific interactions / synaptic states changed"
```

The project's most ambitious educational contribution could be to let a learner move between these levels.

---

# 24. What I would NOT claim about BDH

We need to be strict.

We should **not** say:

> “BDH performs test-time training in the same sense as Akyürek et al.”

That's an unjustified equivalence.

BDH's architecture has synaptic plasticity as its working-memory mechanism. ([arXiv][10])

BDH-CQ specifically describes inference-time input-driven recurrent-memory updates and latent reasoning. ([arXiv][4])

Those mechanisms are **related to** the broader theme of test-time adaptation but are not identical to every parameter-updating TTT algorithm.

Our artifact needs that distinction.

---

# 25. The most promising scientific framing

After this research, I think our project's central scientific question should evolve to:

# **Where does a model put a newly learned task—and what determines whether that adaptation survives?**

And our narrower approved-topic label remains:

**Test-Time Adaptation**

Supporting concepts:

**Skill Acquisition from Demonstrations**

and, selectively,

**Recurrent Memory / Fast Weights**

for interpretation.

That gives us a single coherent story while letting us discuss the necessary neighboring mechanisms.

---

# 26. Proposed research hypothesis

We can formulate a genuinely testable hypothesis:

> **When adapting to a novel task from demonstrations, the location and update rule of task-specific information create measurable trade-offs between adaptation speed, memory capacity, interference, inference cost, and retention.**

This is much better than simply:

> “TTT improves performance.”

Because our artifact can test it across several controlled dimensions.

---

# 27. Experimental matrix

I would build the research around this:

| Independent variable | Measurement          |
| -------------------- | -------------------- |
| Demonstration count  | adaptation accuracy  |
| Task complexity      | adaptation accuracy  |
| Noise                | robustness           |
| State capacity       | accuracy / retention |
| Adaptation steps     | accuracy / latency   |
| Interference         | retention            |
| Task similarity      | transfer             |
| Adaptation mechanism | accuracy / cost      |
| Sequence length      | memory degradation   |
| Query distance       | persistence          |

Then compare:

**Frozen ICL**

**Parameter TTA**

**Recurrent-state adaptation**

and, where scientifically justified:

**fast-weight / associative memory**

This becomes our actual research framework.

---

# 28. Proposed model family for our own implementation

I recommend we do **not** begin by trying to reproduce a huge language model.

Instead build progressively:

### Model A — linear learner

Extremely interpretable.

### Model B — tiny MLP

Nonlinear task acquisition.

### Model C — recurrent-state learner

Explicit state.

### Model D — learned-state/TTT layer

State itself is a small model.

### Model E — BDH-inspired memory mechanism

A carefully scoped educational implementation based on published equations.

### Model F — official BDH evidence

Use published/precomputed evidence where appropriate.

### BDH-CQ

Use the published architecture/results/code as a case study rather than claiming reproduction unless we actually reproduce a specific experiment.

This progression gives us scientific control.

---

# 29. Why this is actually better than starting with an LLM

A huge model would hide the phenomenon.

Consider:

$$
\theta \in \mathbb R^{8B}
$$

Good luck showing a learner what changed.

Instead:

$$
\theta \in \mathbb R^{100}
$$

and:

$$
s \in \mathbb R^{16}
$$

Now we can literally visualize the adaptation.

The Pathway brief explicitly encourages reducing the system until the important state variables become visible. 

That's not “less serious.”

It is **better experimental design**.

---

# 30. The product could then expose the entire causal chain

Something like:

```text
DEMONSTRATION
       │
       ▼
┌─────────────────┐
│ Adaptation Rule │
└────────┬────────┘
         │
         ▼
┌────────────────────┐
│ Where is information│
│ being written?      │
├────────────────────┤
│ Context             │
│ State               │
│ Parameters          │
└─────────┬──────────┘
          │
          ▼
      NEW QUERY
          │
          ▼
      PREDICTION
          │
          ▼
     GROUND TRUTH
          │
          ▼
    FAILURE / SUCCESS
          │
          ▼
   RETENTION TEST
```

This is already a substantially more sophisticated learning system.

---

# 31. A particularly strong final experiment

I would like the final artifact to end with:

> **You have 3 demonstrations. You have never seen this task family before. Choose where you think the system should store the rule.**

The learner selects:

**context**

**recurrent state**

**weights**

Then we run the controlled experiment.

Afterward:

> **Now predict what happens when we introduce a second task.**

Then run the interference test.

Then:

> **Now explain why.**

This tests actual conceptual transfer.

---

# 32. Research landscape we should anchor the project around

At minimum, our literature backbone should include:

### Foundational adaptation

Sun et al., *Test-Time Training with Self-Supervision for Generalization under Distribution Shifts* — ICML 2020. ([Proceedings of Machine Learning Research][1])

### ICL as an algorithm

Li et al., *Transformers as Algorithms: Generalization and Stability in In-context Learning* — ICML 2023. ([Proceedings of Machine Learning Research][6])

### ICL and gradient descent

von Oswald et al., *Transformers Learn In-Context by Gradient Descent* — ICML 2023. ([Proceedings of Machine Learning Research][7])

### Language-model TTT

Hardt & Sun, *Test-Time Training on Nearest Neighbors for Large Language Models* — ICLR 2024. ([ICLR Proceedings][18])

### Abstract reasoning TTT

Akyürek et al., *The Surprising Effectiveness of Test-Time Training for Few-Shot Learning* — ICML 2025. ([Proceedings of Machine Learning Research][2])

### Learned hidden-state TTT

Sun et al., *Learning to (Learn at Test Time): RNNs with Expressive Hidden States* — ICML 2025. ([Proceedings of Machine Learning Research][3])

### Long-context TTT

Tandon et al., *End-to-End Test-Time Training for Long Context* — 2025/2026 research line. ([arXiv][15])

### BDH

Kosowski et al., *The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain*. ([arXiv][10])

### BDH-CQ

Engdahl et al., *BDH-CQ: In-Context Learning with Recurrent Latent Reasoning*. ([arXiv][4])

### ARC

Chollet et al./ARC Prize materials and ARC-AGI-2. ([GitHub][13])

That's already a strong research backbone.

---

# 33. One correction to our original project plan

After the literature review, I would **not make “weights vs recurrent state” the entire project**.

That's too narrow.

Instead:

# **The real object of study is transient task memory.**

And the mechanisms become competing implementations:

$$
\boxed{
\text{Context}
\quad
\text{State}
\quad
\text{Fast memory}
\quad
\text{Parameters}
}
$$

Then the main scientific question is:

$$
\boxed{
\text{How does the choice of memory substrate affect adaptation?}
}
$$

This connects:

* ICL,
* TTT,
* TTT-RNN,
* fast weights,
* recurrent memory,
* continual adaptation,
* BDH,
* BDH-CQ,

without turning the artifact into a survey.

---

# 34. What I now think our actual project should be

## **ADAPT — A Laboratory for Test-Time Learning**

The learner encounters unfamiliar tasks and investigates four questions:

### 1. Can the system learn the task?

### 2. Where is the task information stored?

### 3. How does the update mechanism affect learning?

### 4. What happens when memory is stressed or interfered with?

The BDH/BDH-CQ section then becomes:

> **“Here is a real frontier architecture that makes one particular answer to these design questions.”**

That is scientifically much stronger than:

> “Here is a toy model that looks like BDH.”

---

# 35. What we should do next

We are now at the point where **we should stop broad ideation and start locking the science**.

The next concrete research task should be:

## **Build the formal specification of the experiment.**

That means I would next work out, in detail:

**A.** the exact definitions of ICL, meta-learning, TTT, test-time adaptation, TTT-RNN and recurrent-state adaptation;

**B.** the exact equations for the minimal models;

**C.** a mathematically clean toy task family;

**D.** the experimental baselines;

**E.** the metrics;

**F.** the ablation matrix;

**G.** which parts can be run live under the <1-second requirement;

**H.** which published BDH/BDH-CQ results should be precomputed;

**I.** exactly which statements about BDH/BDH-CQ we can and cannot make;

**J.** the final one-sentence claim we can genuinely falsify.

Only after those ten things are pinned down should we design the final interface.

That is the point where this stops being “an AI education hackathon idea” and becomes a **small, controlled research program whose results happen to be presented as an interactive educational artifact**.

[1]: https://proceedings.mlr.press/v119/sun20b.html?utm_source=chatgpt.com "Test-Time Training with Self-Supervision for Generalization under Distribution Shifts"
[2]: https://proceedings.mlr.press/v267/akyurek25a.html?utm_source=chatgpt.com "The Surprising Effectiveness of Test-Time Training for Few-Shot Learning"
[3]: https://proceedings.mlr.press/v267/sun25h.html?utm_source=chatgpt.com "Learning to (Learn at Test Time): RNNs with Expressive Hidden States"
[4]: https://arxiv.org/abs/2608.09888?utm_source=chatgpt.com "BDH-CQ: In-Context Learning with Recurrent Latent Reasoning"
[5]: https://paperswithcode.com/paper/what-can-transformers-learn-in-context-a-case?utm_source=chatgpt.com "What Can Transformers Learn In-Context? A Case Study of Simple Function Classes | Papers With Code"
[6]: https://proceedings.mlr.press/v202/li23l.html?utm_source=chatgpt.com "Transformers as Algorithms: Generalization and Stability in In-context Learning"
[7]: https://proceedings.mlr.press/v202/von-oswald23a.html?utm_source=chatgpt.com "Transformers Learn In-Context by Gradient Descent"
[8]: https://proceedings.mlr.press/v70/finn17a?utm_source=chatgpt.com "Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks"
[9]: https://arxiv.org/abs/2212.04458?utm_source=chatgpt.com "General-Purpose In-Context Learning by Meta-Learning Transformers"
[10]: https://arxiv.org/abs/2509.26507?utm_source=chatgpt.com "The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain"
[11]: https://proceedings.mlr.press/v139/schlag21a.html?utm_source=chatgpt.com "Linear Transformers Are Secretly Fast Weight Programmers"
[12]: https://pathway.com/research/the-equations-of-reasoning?utm_source=chatgpt.com "The Equations of Reasoning | Pathway"
[13]: https://github.com/fchollet/arc-agi?utm_source=chatgpt.com "GitHub - fchollet/ARC-AGI: The Abstraction and Reasoning Corpus · GitHub"
[14]: https://arcprize.org/blog/arc-agi-2-technical-report?utm_source=chatgpt.com "ARC-AGI-2 A New Challenge for Frontier AI Reasoning Systems | ARC Prize"
[15]: https://arxiv.org/abs/2512.23675?utm_source=chatgpt.com "End-to-End Test-Time Training for Long Context"
[16]: https://arxiv.org/abs/2501.00663?utm_source=chatgpt.com "Titans: Learning to Memorize at Test Time"
[17]: https://arxiv.org/abs/2505.23735?utm_source=chatgpt.com "ATLAS: Learning to Optimally Memorize the Context at Test Time"
[18]: https://proceedings.iclr.cc/paper_files/paper/2024/hash/f02f1185b97518ab5bd7ebde466992d3-Abstract-Conference.html?utm_source=chatgpt.com "Test-Time Training on Nearest Neighbors for Large Language Models"
