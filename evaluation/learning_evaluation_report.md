# D5.8 — Learning Effectiveness Report

**Status:** PILOT ONLY (n=1) — full 8–15 participant study pending per
`docs/evaluation_protocol.md`. No learning-gain claim is made beyond
what the pilot data supports. This report documents the instrument,
the pilot run, and the exact procedure to complete the study.

## Instrument (frozen)

- Pre-test (5 items, LO1/LO2/LO4/LO5/LO6) → post-test (same LOs) +
  transfer challenge (unseen compositional family, free-text explanation).
- Misconceptions tracked M1–M5 (M2 = “state ≡ weights”, M5 = “more
  compute always helps”).
- Pipeline: in-app Export JSON → `scripts/analyze_sessions.py` →
  per-LO gain, normalized gain g, transfer score, time-to-first-run,
  misconception-shift table.
- Item-level quiz logs + per-LO analysis are implemented (must-fix
  close-out); scoring is local and anonymous (`anon-xxxxxxx`).

## Pilot run (n=1, `tests/fixtures/pilot_session.json`)

```
N sessions: 1
anon-pilot01: pre=2 post=4 gain=2 g_norm=0.667
Per-LO: LO1 0.0→1.0 | LO2 0.0→0.0 | LO4 1.0→1.0 | LO5 1.0→1.0 | LO6 0.0→1.0
BDH-CQ order quiz (LO6): 1/1 | mech checks: 1/2
```

Reading (pilot only, not a claim): positive gain direction (+2,
g=0.667); LO2 (parameter-vs-state distinction item) flat at 0.0 and
one mech check missed — consistent with M2 being the stickiest
misconception. If this pattern replicates at n≥8, the WHAT CHANGED box
gets revised before any gain is published (per protocol stop rules).

## What “done” requires

1. Recruit 8–15 ML-capable participants unfamiliar with
   inference-time adaptation, none involved in building the artifact.
2. Run the 10–15 min protocol verbatim (say only “Explore this.”).
3. Collect exported session JSONs into `evaluation/sessions/`.
4. Run `scripts/analyze_sessions.py evaluation/sessions/*.json`.
5. Publish anonymized JSONs + analysis output alongside ANY gain claim.
6. Apply stop rules: ≥30% flagship failure in ~2 min → fix flagship;
   persistent M2 → revise WHAT CHANGED; skipped predictions → gate
   prediction before run.

## 60-second test (author self-run, 2026-09-07)

Unseen task → prediction → run → result → ground truth → state change
is reachable in one screen and one click (“Run Adaptive State”);
all server legs measure < 100 ms (D5.5), so the loop completes in
well under 60 s on first visit. Independent verification with naive
users is part of the full study above.
