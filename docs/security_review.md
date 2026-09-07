# D5.6 — Security & Integrity Review

**Date:** 2026-09-07 | **Scope:** `server.py` + `src/adapt/*` (stdlib HTTP
server, no auth — public artifact by brief requirement).

## Verified controls (code references)

| Threat | Control | Location | Test |
|---|---|---|---|
| Arbitrary strategy/family injection | Allowlist reject: unknown family/strategy → 400 | `server.py::_validate_request` | `tests/test_server.py` |
| state_dim = 10,000,000 | Clamped to 1–64 | `server.py::_resolve_kw` | test_phase5 (D5.6 bounds) |
| steps explosion | Clamped to 0–64 | `server.py::_resolve_kw` | test_phase5 |
| lr abuse | Clamped to 0.0–5.0 | `server.py::_resolve_kw` | test_phase5 |
| Huge body / batch smuggling | `MAX_BODY = 1 MiB`; sweeps computed server-side, never uploaded | `server.py` | test_phase5 |
| Learned-checkpoint path traversal | Trio restricted to linear family; default vetted checkpoints injected server-side | `server.py::_validate_request`, `_resolve_kw` | `tests/test_server.py` |
| Cross-user state leakage | **No module-global mutable state** in `src/adapt` (verified by scan); every strategy instance carries its own state with `reset/get_state/set_state`; each request builds fresh task + strategy objects | `strategies.py`, `learned.py`, `runner.py` | `reset_and_isolation.md` + test_phase5 scan |
| Filesystem access via API | No path parameters except figure `name` served from a fixed directory; no `open()` on user input | `server.py` figure handler | manual review |
| Adaptive-state cross-talk (A/B) | Interference endpoint constructs independent task objects per seed; E8 perturb/restore saves and restores exact state | `server.py`, `runner.py` | `test_intervention_v2.py` |

## Per-user/per-task isolation argument

The server is stateless across requests: no sessions, no caches, no
globals. A request's full state (task draw + strategy instance) is
created inside the handler and discarded after the response. Two
concurrent users therefore cannot share adaptive state by construction
— there is no shared object to leak through. The ThreadingHTTPServer
gives each request its own thread with its own objects.

## Scientific-integrity overlap

State isolation is also a validity requirement: test-split draws are
seed-disjoint from training contexts (`reset_and_isolation.md`,
`data_leakage_policy.md`), and every payload carries `seed + split +
config_hash` so a leaked-state artifact would be detectable in
provenance, not just in code review.

## Residual risks (accepted, documented)

- No rate limiting: a flood of max-size sweeps could saturate CPU.
  Accepted for a demo artifact; deployment should sit behind a reverse
  proxy with rate limits (see `docs/deployment.md`).
- No auth by design (brief: artifact opens without sign-in).
- `figure?name=` trusts filenames within one directory — safe as long
  as the figures directory contains only vetted PNGs (frozen D5.9).
