# D5.13 — Release Checklist

Final public-artifact acceptance. Performed on a **clean browser with no
developer intervention**; the artifact opens without sign-in exactly as
the brief requires.

**Status: COMPLETE — executed 2026-09-08 against the public deployment
`https://adapt-learner.up.railway.app` using a fresh Playwright/Chromium
profile at desktop (1440×900) and mobile (390×844) viewports. Asset
hashes on the deployment are byte-identical to this repository. Zero
console/page errors.**

## Public artifact tests (clean browser)

| # | Test | Pass |
|---|---|---|
| T1 | Open URL; first visible thing is the live experiment (no marketing landing) | ☑ |
| T2 | No sign-in / no account walls anywhere | ☑ |
| T3 | Preset experiment is already populated (no blank canvas; no "Loading model…") | ☑ |
| T4 | Make a prediction | ☑ |
| T5 | Run experiment; result appears with ground truth beside it | ☑ |
| T6 | Change a parameter (n_demos / state_dim / eta) at 390px viewport: `.grid2` collapses, canvas scales (`max-width:100%`), no horizontal clipping | ☑ |
| T7 | Changing the parameter produces an actual consequence (documented by telemetry) | ☑ |
| T8 | Ground truth shown beside the estimate on every run | ☑ |
| T9 | Stress section works: interference A→B→A + intervention perturb/restore | ☑ |
| T10 | BDH section opens; stepper works; educational-rendering disclaimer present | ☑ |
| T11 | BDH-CQ section opens; scope guard on 150M / 29.5% present | ☑ |
| T12 | Final transfer challenge completes and exports a session JSON | ☑ |

Evidence: Playwright harness `T1–T12` (Chromium, clean profile),
2026-09-08; `/api/*` exercised (health OK, episode/cmp/interfere/
intervene/sweep POST 200, precomputed/figure GET 200 with valid IDs,
unknown exp → 404 as designed); no JS console errors.

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

## Deploy-time checks (executed 2026-09-08)

- Public URL: `https://adapt-learner.up.railway.app` (Railway, TLS valid
  at test date: leaf `*.up.railway.app` 2026-07-29 → 2026-10-27; openssl
  verify return 0). No `localhost`-name resolution penalty observed;
  `/api/*` round-trips 0.4–1.3 s first-paint, heaviest POST `/api/sweep`
  ~0.5 s from the test host.
- Proxy regression check: deployed `index.html` / `app.js` / `styles.css`
  are **byte-identical** to this repository (hashes match), so no proxy
  rewrite or middleware injection; `favicon.ico` 404 is by design (no
  favicon shipped). `/api/health` returns `{"ok": true, "schema": 1}`.
- Visual focus states (native rings are acceptable) and a live
  NVDA/VoiceOver pass — scripted practice documented in
  `docs/accessibility_audit.md`; not a blocker (release T-items cover
  keyboard/skip-link/aria-live statically; aria-live ×3 and skip link
  verified on the deployment).
- `submission/artifact_url.txt` → `https://adapt-learner.up.railway.app`
  and `submission/repository_url.txt` → `https://github.com/Adithkp03/ADAPT`
  (committed).