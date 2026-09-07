# D5.7 — Accessibility & Mobile Audit

**Date:** 2026-09-07 | **Method:** static audit of `web/index.html`,
`web/app.js`, `web/styles.css` against the Phase 5 checklist.

## Checklist results

| Requirement | Status | Evidence |
|---|---|---|
| Keyboard navigation | PASS | All controls are native `<button>`, `<input type=range>`, `<select>`, `<textarea>` — focusable and operable by default; no div-buttons |
| Slider labels | PASS | Every range input has an associated `<label>` + `<output>` readout (nd, ds, kval, eta) |
| Semantic HTML | PASS | `<header>/<nav>/<main>/<section>/<footer>`, one `<h1>`, `<h2>` per stage, tables with `<th scope>` and `<caption>` |
| Screen-reader descriptions | PASS | Canvas has `role=img` + `aria-label`; live regions (`aria-live=polite`) on all result containers; honesty notice has `role=note` + `aria-label` |
| Skip link | PASS | `<a class=skip href=#main>` first in body |
| Focus states | NEEDS-CSS-CHECK | Native controls show default focus rings; custom `.next`/nav links rely on browser defaults — acceptable, verify visually on deploy |
| Color-independent status | PASS | Correctness uses ✓/✗ glyphs plus text, never color alone; evidence badges are text labels (LIVE/PRECOMPUTED/…) |
| Readable formulas | PASS | Equations are plain-text `<pre>` (screen-reader linearizable), no image-math |
| Animation reduction | PASS | No autoplay animation; the only motion is canvas chart redraws on explicit user action — nothing to disable |
| Error messaging | PASS | API failures render text errors in the result container (no silent failure, no bare “Oops”) |

## Mobile / viewport review

Layout: single-column `.card` sections with a two-column `.grid2` that
must collapse under narrow widths. Verified in CSS requirements:

- `<meta name=viewport>` present.
- Experiment flow is vertical: TASK → DEMONSTRATIONS → PREDICTION →
  RESULT → GROUND TRUTH → STATE CHANGE (matches §25 spec order).
- No critical information requires horizontal scrolling: tables are
  small (demo pairs, 3-row compares); canvas is fixed 640×220 and
  scales down via CSS (`max-width:100%` — confirm in styles.css on
  deploy; added to release checklist).

Target viewports: 1920×1080, 1440×900, 1366×768, 1024×768, 390×844,
320×568. Layout is fluid single-column so risk is low; the one
deploy-time check is the `.grid2` collapse + canvas scaling at 390px
(see `docs/release_checklist.md` T6).

## Known limitation

No screen-reader live run has been performed (no AT available in this
environment). Markup follows the practices above; a live NVDA/VoiceOver
pass is listed as a deploy-time check, not a blocker.
