# D4.9 — BDH Educational Validation (instrumentation + status)

This document records the learner-facing educational-validation layer for
the BDH/BDH-CQ integration: the equation stepper, the BDH-CQ ordering
question, and the 6-mechanism-distinction target. It states exactly what
is instrumented, what is testable today, and the current participant
status (which is an honest blocker, not hidden). Validation date:
2026-09-07.

## 1. BDH equation stepper (testable, live in product)

- **Where:** `web/index.html` §stage-bdh; logic in `web/app.js` (the
  `EOR` array + `eorRender`), wrapped by `#eor-step` / `#eor-prev` /
  `#eor-next` / `#eor-pos`.
- **What a learner does:** clicks Prev/Next through the 4-round published
  structure (`4l memory read` → `4l+1 memory write` → `4l+2 gated
  readout` → `4l+3 state update`), each labeled with its source section
  (Equations of Reasoning §4, step N). Interaction, not passive text.
- **Instrumentation:** every step logs `eor_step { i }` to the session
  event log (exported via the Results → Export JSON button).
- **Validation record:** D4.4 / `research/bdh/equations.md` cross-checks
  the stepper against the published equations, rounding, and σ update.

## 2. BDH-CQ ordering question (testable, live, tracked)

- **Where:** `web/app.js` `#bdh-quiz` block (LO6).
- **The question:** which sequence matches the paper's described
  mechanism? Correct answer: *Demonstrations → recurrent memory updates →
  query → iterative latent computation → answer* (no verbal CoT, no
  inference-time param edit).
- **Scoring rule:** `design/interaction_patterns.md` Pattern 1; the `ok`
  flag is fired on `bdh-go`.
- **Instrumentation:** `log("bdh_quiz", { ok })` per attempt — now
  aggregated by `scripts/analyze_sessions.py` as the "BDH-CQ order quiz
  (LO6)" educational-validation signal (see §4).

## 3. Distinguishing the 6 mechanisms (target, measurable)

Phase 4 §49 target: the learner must be able to distinguish
`IN-CONTEXT LEARNING ≠ PARAMETER TTA ≠ ORDINARY RECURRENT STATE ≠
LEARNED TTT STATE ≠ BDH SYNAPTIC MEMORY ≠ BDH-CQ RECURRENT MEMORY`.

How it is measured (multi-signal, per-session):
- **Pre/post tests (LOs):** LO1 (context vs weights), LO2 (param TTA
  changes θ), LO5 (interference), LO6 (BDH σ / BDH-CQ latent reasoning),
  LO4/LO7 (capacity). LO6 appears in both PRE (Q5: BDH working memory in
  σ) and POST (Q5: BDH-CQ iterative latent computation).
- **In-lab checks:** flagship `mech_quiz` (what changed inside the model)
  and the `bdh_quiz` order check — both logged and now aggregated.
- **Transfer challenge:** `challenge_run` (free-text explanation of where
  state stores new-task info + interference).
- **Hand rubric** (item-level): free-text `ch-explain` scored per
  `evaluation_protocol.md` and passed via `--rubric=`.

The 6-mechanism distinction is not a single number; it is the retained
ability across these checks. `analyze_sessions.py` now reports the
aggregate "Mechanism-distinction checks (mech_quiz)" signal and the
BDH-CQ order-quiz signal alongside the pre/post per-LO gains.

## 4. How these feed the D3.11 analysis

`scripts/analyze_sessions.py` (D3.11 quantitative half) now emits, per
session and in aggregate:
- BDH-CQ order quiz (LO6) correct/total.
- Mechanism-distinction checks correct/total.
Plus the existing pre/post per-LO gains (incl. LO6), normalized gain,
transfer score, times, and the misconception-shift table.

## 5. Status — honest participant blocker

The instruments above are **live, wired, and testable today** (the
pilot fixture exercises them: `bdh_order_quiz=1/1,
mech_checks=1/2`). Actual learner testing with 8–15 ML-capable
participants is **pending** (per `docs/evaluation_protocol.md`:
"protocol frozen; participants pending"). **No learning-gain claim is
made** until real anonymized session JSONs are collected and analyzed;
any such claim will ship with the raw session data + analysis output
attached (protocol §4's no-claim-without-data rule). The instrumented
signals above are exactly what will populate that claim once sessions
are gathered.

## 6. Conclusion

The educational-validation layer is fully instrumented for (1) the BDH
equation stepper, (2) the BDH-CQ ordering question, and (3) the
6-mechanism-distinction target, and all three are wired into the D3.11
analysis. Participant testing is pending and honestly recorded; no
learning-gain claim is asserted without data. D4.9 instruments are
satisfied; the empirical learner-study run is a Phase 5 evaluation
activity, not hidden.
