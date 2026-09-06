# Episode Protocol (frozen at Phase 2 start)

**Version:** candidate 2026-09-06

## Episode
```
seed -> Generator(seed, family, C_R, noise) -> T=(R,D,Q,Y)
model.reset(theta_0, s_0)   # episodic reset default
present D (k=N_D) in fixed order unless order-ablation
adapt per regime (none / context / param-TTA K steps / state update)
query Q -> y_pred
evaluator compares y_pred vs Y (exact / tolerance per tier)
record: y_pred, Y, correct, Delta_theta, Delta_s, latency, config hash, seed
```

## Ordering
Demonstration order fixed by seed; order-robustness is a separate ablation, not default variation.

## Query discipline
One query per episode default. Multi-query only in retention/interference mode with explicit mode flag.

## Logging
Every episode logs: experiment_id, git_commit, config_hash, seed, model_version, task_generator_version, hardware, timing. ID = H(code, config, seed, generator, model).
