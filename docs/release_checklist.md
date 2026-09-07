# D5.13 — Release Checklist

Final public-artifact acceptance. Performed on a **clean browser with no
developer intervention**; the artifact opens without sign-in exactly as
the brief requires.

## Public artifact tests (clean browser)

| # | Test | Pass |
|---|---|---|
| T1 | Open URL; first visible thing is the live experiment (no marketing landing) | ☐ |
| T2 | No sign-in / no account walls anywhere | ☐ |
| T3 | Preset experiment is already populated (no blank canvas; no "Loading model…") | ☐ |
| T4 | Make a prediction | ☐ |
| T5 | Run experiment; result appears with ground truth beside it | ☐ |
| T6 | Change a parameter (n_demos / state_dim / eta) at 390px viewport: `.grid2` collapses, canvas scales (`max-width:100%`), no horizontal clipping | ☐ |
| T7 | Changing the parameter produces an actual consequence (documented by telemetry) | ☐ |
| T8 | Ground truth shown beside the estimate on every run | ☐ |
| T9 | Stress section works: interference A→B→A + intervention perturb/restore | ☐ |
| T10 | BDH section opens; stepper works; educational-rendering disclaimer present | ☐ |
| T11 | BDH-CQ section opens; scope guard on 150M / 29.5% present | ☐ |
| T12 | Final transfer challenge completes and exports a session JSON | ☐ |

## Failure handling

- Any system error must render **"Experiment unavailable"** with a retry
  and explanation — never "Oops!" (`web/app.js`), and must distinguish
  system failure from model failure (phase5.md §43).
- Evidence badges (LIVE / PRECOMPUTED / SYNTHETIC / PUBLISHED RESULT /
  ILLUSTRATIVE) correct on every visible number (D5.2).

## Clean-machine test

- Repository clones; no local secrets; no absolute local paths
  (`tests` guard against hardcoded paths).
- `pip install -r requirements.txt` succeeds; `pytest tests/ -q`
  green; `python server.py --port 8001` serves the lab.
- No hidden APIs: `/api/*` surface is exactly the documented set.
- Rendering verified at 1920×1080, 1440×900, 1366×768, 1024×768,
  390×844, 320×568 (fluid single-column layout; canvas is the only
  fixed-size element and scales via CSS).

## Deploy-time checks deferred from earlier phases

- Verify no `localhost`-name resolution penalty in hosting env; prefer
  precomputed payloads for the heaviest views on first paint
  (`docs/performance_report.md`).
- Visual focus states (native rings are acceptable) and a live
  NVDA/VoiceOver pass — scripted practice documented in
  `docs/accessibility_audit.md`; not a blocker on this machine.
- Public URL + repository URL recorded in `submission/artifact_url.txt`
  and `submission/repository_url.txt` at deploy.