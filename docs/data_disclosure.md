# D5.12 — Data Disclosure

## What datasets the artifact uses

**None from external sources.** All experiment and learner-facing task
data is generated procedurally in-repo by `src/adapt/tasks.py`
(taskgen-v2) from seeded RNGs. There is nothing to license, download,
or reproduce from external distributors. See `provenance/data.csv` and
`repro/data/README.md`.

## Task-data families

| Family | Rule form | Split discipline |
|---|---|---|
| linear | y = ax + b (continuous) | fresh continuous rule per seed (seed-disjoint) |
| quadratic | y = ax² + bx + c | same |
| symbolic | y = (mx + c) mod 8 | disjoint offset pool per split |
| compositional | chained ops | disjoint op pool; test allows depth 3 |
| grid_toy | synthetic grid transforms | disjoint transform pool (test: shift_color) |

Split discipline is enforced per-sample with `seed + split` in every
provenance envelope; the holdout policy is documented in
`research/experiments/data_leakage_policy.md`.

## Where learner data goes (consent-scoped)

Learner sessions export **anonymous** JSON (anon-IDs, no PII) via the
in-app Export button. These are research data covered by the study
consent procedure in `docs/evaluation_protocol.md`. They are **not**
published without a consent record and are **not** part of the public
artifact (`evaluation/learning_evaluation_report.md`, D5.8).

Shipped data files:
- `tests/fixtures/pilot_session.json` — de-identified pilot fixture
  (anonymous, placed solely to exercise `scripts/analyze_sessions.py`).

## ARC-AGI / BDH-CQ numbers

We do **not** evaluate on ARC-AGI. The 150M / 29.5% pass@2 figure is the
BDH-CQ authors' reported result, cited as PUBLISHED with a scope guard,
never claimed as ours (`research/bdh/bdhcq_technical_dossier.md`).
Our grid work uses the synthetic `grid_toy` proxy and is labelled
PROXY / SYNTHETIC / **Grid Transformation Lab** throughout
(`research/experiments/arc_like_proxy_validation.md`).

## Privacy

No collection of identifiers; no analytics; no third-party trackers in
the vanilla frontend (no JS dependencies at all). See
`docs/security_review.md`.