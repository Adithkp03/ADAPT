# D5.14 — Anticipated Questions (live defense)

Every question phase5.md §52 lists, with the precise answer we would
give, backed by evidence locations.

Q1. **Why is your topic frontier?**
Inference-time adaptation is an active 2020–2026 research front (ICML
2025 TTT papers, ICLR 2025 Titans, BDH 2025, BDH-CQ 2026). Our
contribution is a *controlled, exactly-ground-truthed* isolation of the
mechanism axis (context/state/parameters) that these systems decide
between, plus transparent toy replication of the causal signature the
frontier relies on (evidence_matrix.csv; `docs/sources.md`).

Q2. **Why does this matter?**
Deployed models meet unseen rules constantly; retraining is
expensive/slow. Knowing *where the new rule is stored* and what that
costs (capacity, interference, compute) decides between mechanisms. A
model that can absorb a new rule into state (Δθ=0) avoids catastrophic
forgetting of old weights (`central_claim.md`).

Q3. **What is your falsifiable claim?**
v2: "A model can acquire an unseen task rule at inference time without
changing its persistent parameters by updating an internal adaptive
state, but the capacity and update dynamics of that state constrain
what can be retained." Falsified by: adapted ≯ frozen on paired tests
(L1), state not causally necessary (L2), capacity clause fails cleanly
(L3), or retention unaffected by interference (L4)
(`falsification_criteria.md`; verdicts in `phase2_validation_report.md`).

Q4. **What exactly changes?**
In the state strategy: Δθ = 0, Δs > 0 — `s ← s + φ(x,y)` per demo. The
server reports both deltas per episode (WHAT CHANGED box). In
param_tta: Δθ > 0, Δs = 0. In BDH terms: memory in σ, not weights.

Q5. **Why isn't this ordinary ICL (context)?**
We *implement both* and compare. Context = no update (examples passed
with query); it wins sometimes (linear 1.00) because the examples are
the rule, but it is catastrophic under interference (ret 0.03–0.06)
because it holds only the latest demonstrations. State accumulates —
that's the difference, and it's exactly what E5 demonstrates
(`005_interference_*`).

Q6. **Why isn't this just meta-learning?**
Meta-learning adapts during a *training* phase to produce a base model;
TTA/state methods adapt at *inference* on the test-time task. Our
learned checkpoints are meta-trained once, then **frozen** (Δθ = 0 at
inference) — the adaptation happens in state at deployment
(`learned.py`, E9).

Q7. **Why is your recurrent model meaningful?**
It converts the accumulating-state idea into a learned, nonlinear
recurrence — yet keeps the causal signature (perturb/restore collapses
and recovers). Its honest failure (didn't acquire linear under budget)
is retained: it shows meta-training budget matters
(`009_learned_linear_s0`).

Q8. **How do you know the state contains task information?**
Causal intervention, not correlation: E8 zero/shuffle/noise/swap/
nullmean each destroy accuracy (1.00 → ~0.03–0.10) and *restore*
recovers 1.00. Nullmean = on-manifold removal of the task direction —
the strongest control. McNemar exact + Holm-adjusted p per comparison
(`008_intervention_*`).

Q9. **What happens under interference?**
A→B→A: linear state retains 0.09 (accumulated stats mix two lines),
symbolic retains 0.45 (votes preserve partial counts) — state wins on
symbolic, ties/loses on linear; context/parameters forget fully (≤0.06)
(`005_interference_*`, fig5).

Q10. **What is the BDH connection?**
BDH stores task structure in a *synaptic working memory* σ, updated
Hebbianly, separate from persistent parameters. Our state mechanism is
the same abstract envelope in a transparent toy — demonstrations → state
write → readout solves query (`bdh_technical_dossier.md`,
`concept_mapping.md`).

Q11. **What is actually official BDH?**
The Kosowski et al. paper, the "Equations of Reasoning" teaching text,
and the `pathwaycom/bdh` repo. **Our** stepper was absent from the
official code path — the UI stepper/synapse card is our educational
rendering (labelled), and our R1/R2 probes ran the official pinned repos
directly (`reproductions/README.md`).

Q12. **Which results did you reproduce?**
Our own E1–E9 rerun byte-identically (only wall-clock varies), and R1/R2
ran the official repos at pinned commits. We did **not** reproduce the
BDH 97.4% Sudoku nor the BDH-CQ 150M/29.5% numbers — reported with full
conditions in the reproduction logs. Those claims stay PUBLISHED with
scope guards.

Q13. **Which results are precomputed?**
All E1–E9 sweeps are PRECOMPUTED (vetted + provenance-stamped). The
flagship/modify/lab panels are LIVE per request. Every figure is
regenerated from results.json; hashes pinned (badges + provenance
envelope distinguish them).

Q14. **What is your biggest limitation?**
toy, controlled systems — no frontier-LM generalization claim; the
capacity probe is a cliff not graceful degradation; the quadratic
family exposes a readout-expressivity failure; the learned-recurrent
cell is an honest negative; learning-gain claims await the full study
(pilot n=1); and our BDH/BDH-CQ reproductions did not match the
headline numbers (`scientific_limitations.md`, `results/README.md`).