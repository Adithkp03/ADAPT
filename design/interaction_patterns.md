# D3.3 — Interaction Patterns (recurring learner loops)

**Scope:** the three loops every experimental stage in `web/` must follow
(phase3 §16, §60, §61). Adding a stage that breaks these patterns requires
updating this file with rationale.

## Pattern 1 — Predict → Run → Reveal ("Challenge my prediction", §61)

Before every important experiment the learner commits to a hypothesis;
after the run the UI scores it against engine output:

| Stage | Prediction control | Scoring rule |
|---|---|---|
| Flagship 001 | numeric `flag-your` input | \|mine − truth\| ≤ tol (0.5) |
| N_D sweep 002 | Improve / Same / Degrade buttons | correct = Improve (1→4 rises: 1 demo underdetermines 2 line params) |
| Retention 005 | Improve / Same / Degrade buttons | correct = Degrade |
| Flagship mechanism | Parameters / Context / State / Nothing | correct = Adaptive state |
| BDH-CQ order (LO6) | 3-option order quiz | correct = demos → memory → query → latent compute → answer |
| Challenge transfer | Frozen / Context / State pick | correct = winner on the dealt seed |

Predictions are logged to the anonymous session (`nd_predict`,
`ret_predict`, `flagship_run`, `challenge_run`) for the D3.11 study. The UI
never reveals the answer before the run; the run always calls the engine.

## Pattern 2 — "Show me the mechanism" (black box → mechanism, §60)

Each major experiment ships a `<details class="mech">` toggle rendering the
causal chain for that substrate, e.g. flagship:

```text
DEMONSTRATIONS → state update s_t = s + phi(x,y) → QUERY → prediction
  persistent parameters θ: fixed (Δθ = 0)
  adaptive state s: changed (Δs ≠ 0)
```

Equations stay hidden until requested; the chain is always one click away,
never the default view (progressive disclosure, §7 Guide → Reveal).

## Pattern 3 — Guide → Reveal → Manipulate → Sandbox (§7)

Controls appear in lesson order, never all at once:

1. **Guide** (Start + Flagship): one input (your prediction) + one action
   (Run Adaptive State). Task pre-dealt on load (seed 7) — no blank canvas.
2. **Reveal** (WHAT CHANGED + mechanism quiz): the delta box and chain
   toggle appear as *output* of the run, not as upfront controls.
3. **Manipulate** (N_D → compare → d_s → K → noise → interference →
   intervention): one variable per sweep, each framed as a question ("How
   much evidence does it need?"), each run live against the engine.
4. **Sandbox** (Laboratory): full family × strategy × seed × N_D × noise
   matrix plus the precomputed browser — same `/api/episode` semantics as
   every guided stage, so freedom never leaves the validated engine.

## Anti-patterns (rejected)

- Slider-first dashboards with no question attached (§20, §50).
- Scientific branching in the frontend (`if slider > x: show "failed"`).
  The frontend renders engine booleans; it never interprets thresholds.
- Pre-test answers that leak into the guided stages (pre/post are
  structurally similar but non-identical item sets, §39).
- Free-text explanation graded by an LLM (§32): the challenge textarea is
  stored locally for manual rubric scoring in the learner study.
