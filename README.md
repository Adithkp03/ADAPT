# ADAPT

*Where does an AI learn a new rule?* — a research-backed interactive
laboratory on inference-time adaptation, with exact ground truth,
full provenance, and a rigorous, honestly-labelled connection to the
BDH / BDH-CQ frontier.

Reference implementation commit: `66cebd7`.

## What this is

ADAPT is a self-contained experiment in what happens when a model
encounters a task it was never trained on: watch demonstrations, then
solve it — without retraining. It isolates the three places a new rule
can be stored — **context** (the examples themselves), **state** (an
internal adaptive register, Δθ = 0), and **parameters** (test-time
weight updates, Δθ > 0) — on identical episodes, with exact hidden
ground truth for every task.

The artifact is a 9-stage guided learning journey ending in an
interactive laboratory. Every learner-facing number is either produced
live by the real engine (`src/adapt/`) over HTTP or an explicitly
labelled precomputed/published research result — nothing is faked or
animated to repay a claim; badges are LIVE / PRECOMPUTED / SYNTHETIC /
PUBLISHED / ILLUSTRATIVE and mean exactly what the evidence taxonomy
says they mean (`docs/bdh_integrity_audit.md`, D5.2 audit).

## Central claim

> "Inference-time adaptation can succeed without persistent parameter
> changes, storing the new rule in evolving state — but that state's
> capacity and dynamics limit retention."

Status: **CANDIDATE HYPOTHESIS — supported for our controlled toy
scope; not claimed for frontier LMs.** See
`research/claim/central_claim.md`, `research/claim/falsification_criteria.md`.

## Intended learner

A student, engineer, or researcher who wants to *see* what
inference-time adaptation is, how it differs from retraining, and why
the mechanism you choose determines capacity, cost, and interference.
No prior ML theory required — the journey teaches it.

## Prerequisites

Python 3.11+ with numpy, pyyaml, matplotlib, pytest. The frontend is
vanilla HTML/CSS/JS (no node toolchain). Nothing else is needed for the
learner path; torch is only required for the BDH R1/R2 reproductions
and is not on the learner path.

## Learning objectives

By the end of the journey a learner can:

- **LO1** define inference-time adaptation and contrast Δθ = 0 vs Δθ > 0;
- **LO2** distinguish *state* from *weights* (a deliberately sticky
  misconception — pre/post tested);
- **LO3** show where the new rule is stored (context / state / params);
- **LO4** explain why capacity and interference bound adaptation;
- **LO5** interpret a causal intervention (why the state, not correlation);
- **LO6** locate BDH / BDH-CQ in the design space of adaptive memory.

Assessment: pre-test → guided experience → post-test + transfer
challenge, exported as anonymous session JSONs and analyzed by
`scripts/analyze_sessions.py` (`evaluation/learning_evaluation_report.md`).

## Scientific background

- Exact ground-truth task abstraction T = (R, D, Q, Y) — a hidden rule
  R, demonstrations D, query Q, answer Y
  (`docs/research/scientific_scope.md`).
- Literature: in-context learning (Garg et al., NeurIPS 2022; von
  Oswald et al., ICML 2023), test-time training (Sun et al. 2020; Akyürek
  et al. 2025; Gandelsman et al. 2024; OpenAI 2025), fast-weight
  programming (Schlag et al. 2021), counterfactual ICL (Li et al. 2023),
  and the BDH / BDH-CQ frontier (`research/literature/evidence_matrix.csv`).

## System architecture

```text
Task Generator (src/adapt/tasks.py, taskgen-v2)
       ↓
Experiment Engine (src/adapt/runner.py, adapt-v2)
       ↓
Adaptation Models (src/adapt/strategies.py + learned.py, model-v*)
       ↓
Metrics (src/adapt/telemetry.py)
       ↓
Result Store (research/experiments/*/results.json, schema v1)
       ↓
API (server.py, stdlib-only HTTP)  →  Learning Experience (web/, 9 stages)
       ↓
BDH / BDH-CQ bridge (dossiers + concept map + quizzes)
       ↓
Assessment (pre/post tests, session export, analyze_sessions.py)
```

Architecture is frozen (D5.1: `docs/architecture_freeze.md`).

## Experiment design

Controlled, paired, seeded sweeps over synthetic task families
(linear, symbolic, compositional, ARC-like grid proxy) with exact
hidden ground truth and Wilson 95% CIs. See
`research/experiments/experimental_design.md`, `statistical_analysis_plan.md`,
`episode_protocol.md`, `data_leakage_policy.md`. Every live payload
carries a provenance envelope: seed, split, task_generator_version,
model_version, git_commit, config_hash (`server.py::_prov`).

## Adaptation methods

| Strategy | How the new rule is stored | Δθ | Δs |
|---|---|---|---|
| `frozen` | nowhere (baseline) | 0 | 0 |
| `context` | the demonstrations themselves | 0 | 0 |
| `param_tta` | gradient-updated parameters | >0 | 0 |
| `state` | controlled adaptive register `s ← s + φ(x,y)` | 0 | >0 |
| `ttt_state` | learned state parameterization | 0 | >0 |
| `learned_*` | learned recurrent / TTA checkpoints | 0 | >0 |

Public display names are frozen in `src/adapt/strategies.py`
(`STRATEGY_DISPLAY`, `FAMILY_DISPLAY`).

## Task generator

`src/adapt/tasks.py` (taskgen-v2). Families: linear (`y = ax + b`),
quadratic, symbolic (`(mx + c) mod 8`), compositional (chained ops),
grid_toy. Split discipline: symbolic/compositional/grid_toy use
*disjoint operation pools* per split; linear/quadratic draw *fresh
continuous rules per seed* (seed-disjoint — server shows this exact
holdout wording on every task card, `server.py::_holdout`).

## Ground truth

Every task exposes an exact hidden rule and the ground-truth answer
for the query; the learner sees the truth beside the estimate after
each run. Nothing is stochastic in the public claim: results are
seeded, paired, and report CIs.

## Live computation

`server.py` runs the real Phase 2 engine per learner action. Endpoints:
`/api/health, /api/meta, /api/episode, /api/compare, /api/interference,
/api/intervene, /api/sweep, /api/precomputed, /api/figure`. Live data is
badged **LIVE + SYNTHETIC** and measured < 100 ms server-side
(`docs/performance_report.md`, D5.5).

## Precomputed results

Vetted research runs are re-stamped and served with provenance as
**PRECOMPUTED** (`server.py::_prov`, `EXP_IDS`); the UI labels them
explicitly and never presents them as fresh computation.
`research/experiments/*/results.json` are the canonical source; hashes
pinned in `repro/expected_outputs/manifest.csv`.

## Synthetic data

All tasks are procedurally generated from seeded RNGs — no external
data, no licensing exposure (`repro/data/README.md`,
`provenance/data.csv`). The grid family is an *ARC-like proxy* —
always labelled **Grid Transformation Lab**, never ARC-AGI
(`research/experiments/arc_like_proxy_validation.md`).

## Illustrative visualizations

The BDH stepper and synapse card are **educational renderings** of a
published architecture — explicitly labelled "not a simulation of
BDH" (`web/index.html`, `research/bdh/equations.md`, D5.2 audit C07).
All other visuals plot measured data.

## BDH integration

BDH (Kosowski et al. 2025, arXiv:2509.26507) is a post-Transformer,
scale-free architecture whose working memory lives in a synaptic state
σ updated Hebbian-style (published form `σ ← σ + ηXYᵀ`), separate from
persistent parameters. ADAPT teaches the same abstract envelope:
demonstrations → state write → readout solves query. Connection built
in the guided journey — not bolted on at the end (D5.1 gate;
`research/bdh/bdh_technical_dossier.md`, `concept_mapping.md`,
`education/bdh_educational_validation.md`).

## BDH-CQ integration

BDH-CQ (Engdahl et al., 2026, arXiv:2608.09888): demonstrations update
recurrent memory; queries solved by iterative latent computation. We
map the experience onto it, then probe the OFFICIAL implementation
ourselves and report *whether we reproduced it* — we did **not**
reproduce the headline 150M / 29.5% pass@2 figure, which stays
scoped as PUBLISHED and never merges with TOY labels
(`research/bdh/bdhcq_technical_dossier.md`, `reproductions/R1/R2`,
`docs/bdh_integrity_audit.md`).

## Results

Freeze date 2026-09-07. Highlights (full narrative + CI in
`results/README.md`, figures in `results/final/`, tables in `results/tables/`):

- E1 acquisition: frozen 0.11 → state 1.00 (linear); frozen 0.00 → 1.00 (symbolic, ARC-proxy). Δθ=0, Δs>0.
- E2 demo scaling: ≥2 demos saturate linear; 1 demo identifies symbolic offset.
- E3 compute: gradient readers improve monotonically but saturate (state needs 0 steps).
- E4 capacity: lossy state bottleneck → accuracy cliff (0.10 at d_s=4).
- E5 interference: A→B→A catastrophic on linear accrued-state; state retains 0.45 on symbolic.
- E8 intervention: perturb state → ~0.03–0.10; restore → 1.00 (causal).
- E9 learned: learned_state replicates the causal signature; learned_recurrent honest negative retained.
- BDH frontier: fig7/fig8 + dossiers connect TOY results to PUBLISHED landscape without merging labels.

## Reproduction

Three levels (`repro/README.md`): smoke (pytest), full experiment
(run_experiment.py + run_sweeps.py), artifact regeneration
(make_figures.py) — with hash verification
(`repro/check_expected.py`, `repro/expected_outputs/manifest.csv`).
Rerun-identical results confirmed on the reference machine. BDH R1/R2
reproductions: `research/bdh/reproductions/`.

## Installation

```bash
git clone <repo-url> && cd ADAPT
python -m venv .venv            # Python 3.11+
.venv\Scripts\activate          # Windows (unix: source .venv/bin/activate)
pip install -r requirements.txt
python server.py --port 8001    # open http://127.0.0.1:8001
pytest tests/ -q                # 93 tests
```

## Deployment

Stdlib-only HTTP server; single command on any Python 3.11 host with
numpy. `docs/deployment.md` covers hosting, the `localhost`-name
resolution caveat measured in D5.5, reverse-proxy rate limiting
(accepted residual risk), and the public-URL launch checklist.

## Limitations

- Toy, controlled systems — no frontier-LM generalization claim.
- Reader expressivity fails on quadratic family (0.17 state vs 1.00 context).
- Capacity probe is a proxy → cliff, not graceful degradation.
- Learned recurrent variant did not acquire linear rule under budget (honest negative).
- ARC-like pool is a small proxy; grid_toy is never ARC-AGI.
- Learning-gain claims pending the 8–15-participant study (pilot n=1).
- BDH/BDH-CQ headline numbers quoted as PUBLISHED with scope guards; our reproductions did not match them.

Full treatment: `docs/scientific_limitations.md`, `results/README.md`.

## Sources

Primary sources are cited beside the claims that use them —
`docs/sources.md`, `research/literature/evidence_matrix.csv`,
`research/bdh/evidence_ledger.csv`, and each technical dossier.

## Licenses

`docs/licenses.md`, `provenance/` (code, data, models, assets, fonts,
third-party). No webfonts, no external images, no reused paper figures
— everything is either ours or cited. License: MIT (declared in
`LICENSE`; confirm with the team at packaging time).

## AI disclosure

This project used AI assistance for code generation, documentation,
and analysis; every artifact is human-reviewed and understood. Full
record: `docs/ai_assistance.md` (models used, purpose, generated
code/writing/visuals, human review, major modifications).

## Credits

Adaptation engine, experiments, and learning experience — team ADAPT
(see `docs/ai_assistance.md` for tooling split). BDH / BDH-CQ are the
work of their respective authors (papers and repos cited throughout);
our dossiers are team synthesis of those primary sources, and our
probes of the official repos are independently documented.