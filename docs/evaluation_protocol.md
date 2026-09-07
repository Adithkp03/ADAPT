# D3.11 — Learner Study Protocol (run this with 8–15 participants)

**Status:** protocol frozen; participants pending. When sessions are
collected (Export anonymous session JSON), analyze with
`scripts/analyze_sessions.py`.

## 1. Participants

- N = 8–15, ML-capable (student / engineer / researcher), unfamiliar with
  inference-time adaptation specifics, did not build the artifact.
- Consent: anonymous session IDs only (`anon-xxxxxxx`); no names, no
  accounts. Exported JSONs are the study records.

## 2. Script (10–15 min, minimal assistance)

1. Say only: **"Explore this."** Start a timer. Do not explain the science.
2. Observe silently. Note: time to first Run click, whether they predict
   before running, whether they open WHAT CHANGED, where they hesitate.
3. If stuck > 3 min on one stage, note the stage and move them on — that
   stuck point is data (a §42 usability failure), not a cue to lecture.
4. End with the two spoken checks (no peeking):
   - "Without looking back: what did changing the number of demonstrations do, and why?"
   - "Where does the new task information live in the state-based system?"

## 3. Data per participant

- Pre-test answers (in-app, before touching the lab).
- Session JSON: `events[]` (timestamped), `score`, `explain` free text.
- Post-test answers (in-app, after the journey).
- Observer notes: path, stuck points, quotes (esp. weight/state confusion).

## 4. Analysis (script does the quantitative half)

```
system-python scripts/analyze_sessions.py sessions/*.json
```

Outputs per-LO pre/post gain, normalized gain g, transfer score,
time-to-first-run / time-to-correct-mechanism, prediction accuracy per
event type, and a misconception-shift table (M1–M5 coded from pre/post
deltas; explanation rubric scored by hand and passed in as CSV).

## 5. Stop / revision rules

- If ≥ 30% cannot complete the flagship loop in ~2 min: fix the flagship
  experiment or its copy — do not add explanatory text (§58).
- If M2 (state ≡ weights) persists post-study: the WHAT CHANGED box and
  state_visualization copy failed — revise, re-test.
- If predictions are skipped (not wrong, skipped): the predict-before-run
  pattern is too easy to bypass — make prediction a gate, not a suggestion.
- Publish the raw (anonymized) session JSONs + analysis output alongside
  any learning-gain claim. No claim without the data attached.
