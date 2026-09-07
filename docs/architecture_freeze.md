# D5.1 — Production Architecture Freeze

**Status:** FROZEN | **Date:** 2026-09-07 | **Commit:** `6f8d42d`

No major feature may be added past this point. Bug fixes, copy
corrections, and performance work only. Every proposed change must pass
the gate: *does this make the central claim easier to understand?*
Yes → consider. Maybe/no → reject.

## Frozen pipeline

```text
Task Generator (src/adapt/tasks.py, taskgen-v2)
       ↓
Experiment Engine (src/adapt/runner.py, adapt-v2)
       ↓
Adaptation Models (src/adapt/strategies.py + learned.py, model-v*)
       ↓
Metrics (src/adapt/telemetry.py)
       ↓
Result Store (research/experiments/*/results.json, schema v*)
       ↓
API (server.py, stdlib-only HTTP)
       ↓
Learning Experience (web/index.html + app.js, 9 stages)
       ↓
BDH / BDH-CQ bridge (dossiers + concept map + quizzes)
       ↓
Assessment (pre/post tests, session export, analyze_sessions.py)
```

## Frozen surfaces

- HTTP API: `/api/health, /meta, /episode, /compare, /interference,
  /intervene, /sweep, /precomputed, /figure` — request/response shapes
  locked; any change requires a `result_schema_version` bump.
- Provenance envelope on every live payload: seed, split,
  task_generator_version, model_version, git_commit, config_hash.
- Evidence badges: LIVE / PRECOMPUTED / SYNTHETIC / PUBLISHED RESULT /
  ILLUSTRATIVE — meanings locked (see D5.2 audit).
- Learned trio checkpoints (`checkpoints/learned_*_s0.npz`) — frozen;
  new checkpoints need re-validation per E9 protocol.
- 9 frozen figures (`research/experiments/figures/fig*.png`, hashes in
  `results/final_manifest.csv`).

## Explicitly out of scope (rejected by the gate)

- New task families, new strategies, new figures.
- Backend framework migration (stdlib server is a feature: zero-dependency
  deploy).
- Marketing landing page — the artifact opens directly on the experiment.
