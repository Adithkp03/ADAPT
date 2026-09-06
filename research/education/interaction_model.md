# D3.2 — Interaction Model (every control → real variable)

| UI element | Scientific variable | Engine call | Observable output |
|---|---|---|---|
| Your prediction (flagship) | learner hypothesis | none (scored vs truth, tol 0.5) | ✓/✗ beside model + truth |
| Run Adaptive State | adaptation on D | POST /api/episode (state) | pred vs truth, Δθ, Δs |
| New unseen task | task_seed | same, new seed | fresh (D, Q, Y) |
| N_D slider 1–8 + sweep | demonstration count | POST /api/sweep var=n_demos (25 tasks/pt) | accuracy + Wilson CI per point |
| Compare mechanisms | substrate (paired) | POST /api/compare, same task | per-mechanism pred, Δθ, Δs |
| d_s slider + sweep | state bottleneck proxy | POST /api/sweep var=state_dim | accuracy cliff |
| K slider + sweep | test-time compute | POST /api/sweep var=steps (param_tta) | accuracy/latency trade |
| Noise sweep | input quality ε | POST /api/sweep var=noise | robustness curve |
| Retention prediction + A→B→A | interference (no reset) | POST /api/interference | A-before / B / A-after |
| Intervention | state necessity | POST /api/intervene | base / perturbed / restored per perturbation |
| η slider (BDH panel) | Hebbian rate (educational) | local ‖Δσ‖=η·‖x‖·‖y‖, labeled implementation | magnitude readout |
| Lab family/strategy/seed/N_D/noise | full task+adapt config | POST /api/episode | full result + provenance |
| Precomputed selector | vetted research run | GET /api/precomputed?exp= | summary + commit/hash |
| Export session | anonymous log | local JSON download | sid, events, scores, explanation |

Hard rules: no control without a row above; sliders that stop teaching get removed; the UI never branches on result values (no `if accuracy > x: show "failed"` — the engine's booleans are rendered, not interpreted).
