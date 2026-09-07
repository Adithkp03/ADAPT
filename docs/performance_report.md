# D5.5 — Production Performance Report

**Measured:** 2026-09-07 | **Machine:** local dev (Windows, CPU-only) |
**Method:** `scripts/perf_probe.py` against `server.py` on 127.0.0.1
(proxy bypassed — see note) | **Commit:** `6f8d42d`

## Results (single request, warm server)

| Endpoint | Load | Measured | Budget | Verdict |
|---|---|---|---|---|
| `GET /api/health` | — | 4 ms | < 200 ms | PASS |
| `GET /api/meta` | — | 8 ms | < 200 ms | PASS |
| `POST /api/episode` (linear/state) | 1 task | 63 ms | < 1000 ms | PASS |
| `POST /api/compare` (3 strategies) | 1 task × 3 | 38 ms | < 1000 ms | PASS |
| `POST /api/interference` (A→B→A) | 1 pair | 31 ms | < 1000 ms | PASS |
| `POST /api/intervene` (perturb/restore) | 1 task | 22 ms | < 1000 ms | PASS |
| `POST /api/sweep` (flagship N_D) | 3 pts × 25 tasks | 84 ms | < 1000 ms | PASS |
| `GET /api/precomputed` | 1 exp | 22 ms | < 500 ms | PASS |
| `GET /api/figure` (25 KB PNG) | 1 file | 2 ms | < 500 ms | PASS |

Headroom: the heaviest learner interaction (flagship 75-episode sweep)
completes in < 100 ms server-side — ~12× under the 1 s brief standard.
No optimization pass required; budgets are met with margin.

## Scaling note

Sweep cost is linear in `points × n_tasks × episode_cost`. Server-side
bounds cap the blast radius: `steps ≤ 64`, `state_dim ≤ 64`,
1 MiB max body, learned trio restricted to linear. A pathological
browser request therefore degrades to a fast 400, not a hung server
(see D5.6).

## Measurement caveat (recorded honestly)

An early probe via the `localhost` hostname showed a uniform ~2 s on
every endpoint including static files. Re-probing via `127.0.0.1` with
proxy bypass gave 2–84 ms. Conclusion: the 2 s was client-side
name/proxy resolution on the test machine, not server compute. The
table above reflects server performance. Deploy check: verify no
`localhost`-style resolution penalty in the hosting environment and
prefer precomputed payloads for the heaviest views on first paint.

## Budgets (frozen)

```text
Initial interactive state: < 2 s   (static HTML + CSS, no JS bundle build)
Normal experiment:         < 1 s   (measured 22–84 ms server-side)
Visualization update:      < 200 ms (canvas redraw of ≤ 8 points)
Heavy precomputed query:   < 500 ms (measured 2–22 ms)
```

## Caching strategy (D5.1-aligned)

Identical sweep configurations hash to identical `config_hash`
provenance; the UI labels cached/vetted numbers PRECOMPUTED and never
presents them as fresh computation. Live endpoints stay live because
they are cheap (< 100 ms) — no cache-invalidation risk to manage.
