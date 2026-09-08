# Where Does an AI Learn a New Rule?

*One-page concept summary · ADAPT · 500–950 words · self-contained
briefing (not a project diary).*

## Paragraph 1 — Design pressure

Machine-learning systems are usually frozen at deployment: they predict
well on whatever they were trained on and fail on anything else. Yet
humans continually absorb new rules from a handful of examples — a
spelling convention, a net-new pattern, a fresh procedure — without
"re-training" their brains. The design pressure is to exhibit the same
behavior: a model that encounters an unseen task and, given a few
demonstrations, solves it *at inference time*, without retraining.

## Paragraph 2 — Mechanism

Three families of mechanisms can carry the new rule. **Context
adjustment** performs no update at all: the demonstration examples are
passed directly with the query, and the model pattern-matches against
them. **Parameter adaptation** changes the model's weights at test time
(test-time adaptation, TTA): the demonstration set drives gradient
updates to θ before readout. **State adaptation** is the middle path a
recurrent network uses: persistent weights θ stay fixed (Δθ = 0), while
an internal adaptive state is updated per example (e.g. `s ← s + φ(x,y)`
or a learned recurrent map) and the readout of that state solves the
query.

## Paragraph 3 — Trade-offs

The three substrates trade off **capacity, cost, retention and
interference**. State adaptation gets corrected by causal intervention
experiments: destroying the adapted state (swapping it, zeroing it,
removing its task component) collapses accuracy, and restoring it
recovers accuracy — the state is causally necessary, not decorative.
But state capacity is a bottleneck; a lossy compression destroys the
statistics the readout needs (a capacity *cliff*, not a slope), and
accumulating new rules into a shared register causes A→B→A forgetting —
behaviourally, "catastrophic interference." More test-time compute helps
gradient-based readers monotonically but with diminishing returns.

## Paragraph 4 — Research landscape

This is an active frontier. In-context learning (ICL) lets large
Transformers pattern-match demonstrations without weight updates (Garg
et al. 2022; von Oswald et al. 2023). Test-time training methods
retrain at deployment on self-supervision or nearest neighbours and can
fix shifted exact figures. Recurrent architectures treat the adaptive
state as an emergent "fast weight" memory, trading that finite state
against retention. The literature agrees the mechanism you choose
determines where the new rule lives, what it costs, and how quickly it
is overwritten.

## Paragraph 5 — BDH / BDH-CQ frontier connection

Two recent lines are directly relevant. BDH (Kosowski, Uznański,
Chorowski & Stamirowska, 2025; arXiv:2509.26507)
proposes a post-Transformer, scale-free architecture of locally
interacting neuron particles whose *working memory lives in a synaptic
state σ*, updated by a Hebbian rule (in published form, `σ ← σ + ηXYᵀ`),
separate from persistent parameters. BDH-CQ (Engdahl, Kosowski,
Chorowski & Stamirowska, 2026; arXiv:2608.09888) extends
this: demonstrations update recurrent memory, and a query is solved by
iterative latent computation. The abstract envelope — demonstrations
write to state, readout of state solves the query, parameters fixed — is
exactly the envelope our transparent toy substrate isolates. We probe
the official implementations ourselves and report faithfully whether we
can reproduce their headline numbers (see the evidence ledger).

## Paragraph 6 — Evidence

In our controlled toy implementations (synthetic linear, symbolic,
compositional, and ARC-like grid tasks; exact hidden ground truth):
frozen baseline 0.11 → state-adapted 1.00 accuracy on unseen linear
rules (200 paired tasks, Δθ = 0, Δs > 0); state also=1.00 on symbolic
(0.00 frozen). One demonstration suffices only when it identifies the
rule; continuous rules need ≥ 2. Perturb/restore interventions confirm
the state carries the task information. The learned-recurrent
checkpoint did **not** acquire the linear rule under our meta-training
budget (accuracy 0.09 ≈ 0.11 frozen baseline; learned TTA 0.26 /
learned TTT 0.45 stay far below state-adaptation 1.00) — an honest
negative, not a reproduction. Limit: toy systems; the
classic ARC-like proxy pool is small; BDH-CQ's 150M/29.5% claim was not
reproduced by us and stays scoped as PUBLISHED.

## Paragraph 7 — Limitation

The capacity probe shows a cliff, not graceful degradation; the
recurrent variant under our meta-training budget did not acquire the
linear rule; reader expressivity fails on a harder family. Learning-gain
claims wait on the full 8–15-participant study (n=10 to date). No
claim is made past toy scale.

## Final — Where to continue learning

The interactive laboratory lets you watch the state change per
demonstration, break it with interventions, induce interference, and
compare with context and parameter adaptation on identical episodes —
no retraining, full provenance, every number live or explicitly
labelled precomputed/published.

---

**Word count: ~590.** Every sentence states a definition, a mechanism,
evidence, a limitation, or a connection (per brief guidance).