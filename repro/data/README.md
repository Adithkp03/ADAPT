# D5.3 — data::/ (procedural data)

ADAPT uses **no external training data**. Every task family is generated
procedurally from a seeded RNG inside `src/adapt/tasks.py`
(taskgen-v2). This directory is intentionally a placeholder that
documents that fact so a fresh machine knows there are no data files to
download or license.

Generators: `src/adapt/tasks.py` (linear, quadratic, symbolic,
compositional, grid_toy). See `repro/seeds/seed_index.csv` for the
seed master list and `research/experiments/data_leakage_policy.md` for
the split/holdout rules that make the learner-path live draws
leakage-safe.

The only non-procedural data in this project is the learner-study
session evidence, which is consent-scoped and does NOT ship (see
`docs/data_disclosure.md`); the shipped fixture is the de-identified
pilot at `tests/fixtures/pilot_session.json`.