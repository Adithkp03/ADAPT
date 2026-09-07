# D3.2 — Interaction Model (every control → real variable)

**Rule:** no UI element exists without a row below. The frontend renders
engine output; it never branches on result values and never hard-codes a
scientific conclusion (§54).

| UI element | Scientific variable | Engine parameter → call | Observable consequence |
|---|---|---|---|
| Your prediction (flagship) | learner hypothesis | none — scored vs truth, tol 0.5 | ✓/✗ beside model + truth |
| Run Adaptive State | adaptation on D | `strategy=state` → POST /api/episode | pred vs truth, Δθ = 0, Δs > 0 |
| New unseen task | task seed s | `seed` → same | fresh (D, Q, Y), same generator |
| N_D predict + sweep | demonstration count N_D | `var=n_demos` → POST /api/sweep (25 tasks/pt) | accuracy + Wilson 95% CI per point; 1→4 rise (1 demo underdetermines 2 line params) |
| Compare mechanisms | substrate, paired | `strategies=[context,param_tta,state]` → POST /api/compare, same task | per-mechanism pred, Δθ, Δs columns |
| d_s slider + sweep | state bottleneck proxy d_s | `var=state_dim` → POST /api/sweep | accuracy cliff (operational proxy, not capacity itself) |
| K slider + sweep | test-time compute K | `var=steps` on `param_tta` → POST /api/sweep | accuracy/latency trade-off |
| Noise sweep | input quality ε | `var=noise` → POST /api/sweep | robustness curve |
| Retention prediction + A→B→A | interference, continual no-reset | POST /api/interference | A-before / B / A-after + WHY causal chain |
| Intervention | state necessity | `perturbations` → POST /api/intervene | base / perturbed / restored per perturbation; weight on swap + nullmean |
| η slider (BDH panel) | Hebbian rate, educational | local ‖Δσ‖ = η·‖x‖·‖y‖ (‖x‖=‖y‖=1), labeled implementation | magnitude readout only |
| Lab family / strategy / seed / N_D / noise | full task + adapt config | POST /api/episode | full result + provenance drawer |
| Lab strategy, Learned group | learned substrate (Phase 2B) | `learned_state/learned_tta/learned_ttt` → POST /api/episode; server injects vetted `checkpoints/*.npz`; linear-only enforced (400 otherwise, UI auto-switches) | pred vs truth, Δθ/Δs per learned class |
| Precomputed selector | vetted research run | GET /api/precomputed?exp= | summary + commit/hash, PRECOMPUTED badge |
| Figures | vetted research figure | GET /api/figure?name= | PNG bytes, PRECOMPUTED context |
| Challenge deal / reveal | transfer hypothesis | POST /api/compare on compositional | winner vs pick, honest-limits note |
| Free-text explanation | learner mental model | none — stored locally for manual rubric | session JSON field |
| Export session | anonymous log | none — local JSON download | sid, events, scores, explanation |

**Removed by the §50 rule:** any control whose removal would not weaken a
lesson. Survivors above each carry exactly one scientific question, phrased
in the UI as the question (not the parameter name).
