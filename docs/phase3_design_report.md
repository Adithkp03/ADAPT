# docs — Phase 3 Design Report (D3.3 visual system + D3.11 evaluation + §65)

## 1. Architecture
`server.py` (stdlib only: http.server + json + numpy engine) serves `web/` (no build, no CDN, works offline).
Every learner number is LIVE from `src/adapt` (same paired/reset/provenance semantics as the research runner) or PRECOMPUTED
vetted `results.json`. BDH panels are PUBLISHED RESULT (dossier wording) + ILLUSTRATIVE (η demo, labeled educational implementation).

## 2. Visual language decisions
- Causality chain, not decoration: DEMONSTRATIONS → STATE → QUERY → PREDICTION → GROUND TRUTH, one vertical flow per stage.
- State honesty (§9/48): only measured statistics shown (Δs norm, Δθ, cosine-free per-episode deltas, perturb/restore booleans). No neuron semantics; disclaimer inline where a projection could be misread.
- Truth beside estimate (§63): three-row table (yours / model / truth) with tolerance stated; never below the fold.
- Badges on every result: LIVE / PRECOMPUTED / SYNTHETIC / PUBLISHED RESULT / ILLUSTRATIVE (footer legend + §33).
- Provenance: native `<details>` drawer per result (seed, generator/model versions, config hash, commit, schema v1).
- Chart: canvas bars + CI whiskers with adjacent data table (text equivalent, §47).
- Motion: none conveys computation; results appear with `aria-live="polite"`; `prefers-reduced-motion` disables transitions.

## 3. Guide → Reveal → Manipulate → Sandbox
Stages unlock top-down via anchor nav (no gating — guidance by order, per brief's "guided before sandbox").
Flagship opens pre-populated (seed 7, computed on demand in ms — no fake loading, honest "computing" only during real fetch).

## 4. Assessment (D3.9)
Predict-then-run scored inline (N_D direction, retention direction, flagship numeric, challenge mechanism pick);
mechanism checks (what-changed, BDH-CQ order); free-text explanation stored locally for the learner study
(no LLM grading — manual evaluation). Pre/post 5Q mapped to LO1/2/4/5/6/7; session JSON export (anonymous sid).

## 5. Learning evaluation plan (D3.11 — instrumented, participants pending)
Protocol: 10–15 min unassisted → pre/post gain + transfer (challenge pick + explanation rubric) + misconception shift
(weight-change → context/state; state≠weights; recurrence≠TTT; compute≠always-better; dims≠concepts).
Design testing checklist (§42): find interaction, control meaning, live-ness, what-changed, pred-vs-truth, completion.
In-app metrics: event log with timestamps enables path/failure/time analysis once participants run.

## 6. Definition-of-Done status (§66)
Educational: journey ✓ claim ✓ predictions ✓ real variables ✓ visible state ✓ visible truth ✓ failure ✓ BDH ✓ transfer ✓ explain ✓.
Computational: engine-backed ✓ no fakes ✓ no hidden updates ✓ real state ✓ independent GT ✓ provenance ✓.
UX: pre-populated ✓ ~1-min core ✓ minimal controls ✓ fast (local ms) ✓ mobile (single-column ≤700px) ✓ a11y basics ✓ no unexplained encodings ✓.
BDH: embedded ✓ CQ-linked ✓ official-vs-ours explicit ✓ cited ✓ evidence labels ✓.
Evaluation: pre/post/transfer ✓ usability protocol + in-app instrumentation ✓ (live participants pending) misconceptions ✓.
