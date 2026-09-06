# D8 — Computational Substrate Specification

**Phase 1 | v1.0 2026-09-06**

> The educational experience must sit on a functioning experimental engine.

---

## 1. Principle

Brief allows: real tiny models, real replays, live toy systems — but NOT scripted animations presented as computation. All visualizations tagged LIVE / PRECOMPUTED / SYNTHETIC / ILLUSTRATIVE.

## 2. System architecture

```
                 ADAPT
                   |
    +--------------+--------------+
    |              |              |
 Learning UI   Experiment Lab  BDH/CQ Lab
    |              |              |
    +--------------+--------------+
                   |
            Experiment API
                   |
    +--------------+--------------+
    |              |              |
Task Generator  Adaptation    Metrics
    |             Engine          |
    |        +----+----+          |
    |        |    |    |          |
    |     FROZEN PARAM STATE        |
    |              |              |
    +--------------+--------------+
                   |
              Ground Truth
                   |
            Reproducible Results
```

## 3. Experiment framework (D2.1)

```
experiments/
  configs/       # yaml per experiment
  runners/       # run_experiment.py
  seeds/         # seed sets
  outputs/       # versioned results
  checkpoints/   # model hashes
  analysis/      # notebooks for figures
```

Config example:
```yaml
task_family: linear_regression
model: recurrent_state_v1
adaptation: state
demonstrations: 4
state_dim: 32
adaptation_steps: 8
noise: 0.05
seed: 42
```

Execution:
```bash
python run_experiment.py configs/exp_001.yaml
```
Output includes: experiment_id, git_commit, config_hash, seed, model_version, task_generator_version, metrics, timing, hardware.

ID = H(code, config, seed, task_generator, model)

## 4. Task generator (D2.2)

```
T=(R,D,Q,Y) with evaluator knowing R,Y
Generator(seed)=same task
```
Requirements: novel tasks, parameterized difficulty, exact ground truth, controlled perturbation (noise/ambiguity/N_D/complexity/I), reproducibility.

Families: linear -> nonlinear -> symbolic -> compositional -> ARC-like (incremental).

## 5. Model family (minimum)

| Model | Description | Adaptation | Live? |
|-------|-------------|------------|-------|
| A | Small frozen | none | yes |
| B | + param TTA | theta update | yes |
| C | Recurrent state | s_t update | yes |
| D | TTT-state (optional) | S_t learned update | if feasible |
| E | BDH-inspired educational analogue | sigma-like | labeled TOY_EXPERIMENT |

Model E must never claim to be official BDH.

## 6. Measurement / telemetry (D2.7)

Per episode:
- y_pred, Y, accuracy
- Delta_theta, Delta_s
- latency, steps, FLOPs approx, memory
- state trajectory (optional low-dim projection)

Aggregated: mean, 95% CI, retention, gain.

## 7. Live boundaries

- LIVE: task gen, adaptation, prediction, metrics (small models, <1s response target per brief)
- PRECOMPUTED: large sweeps, expensive benchmarks, official-model eval — with provenance (exp ID, commit, seed, date, hardware)
- SYNTHETIC: generated distributions
- ILLUSTRATIVE: architecture animations

## 8. Tech choices (to be finalized Phase 2 Sprint 2)

- Language: Python 3.11
- DL: PyTorch (CPU-friendly tiny models), Deterministic seeds
- API: FastAPI (Experiment API) + Next.js frontend
- Repro: git + config hash + seed; requirements.txt / environment.yml
- Deploy: Vercel/Next.js frontend + Python API (or edge toy models in WASM if latency requires)

## 9. Non-functional

- Controls respond <1s (brief standard)
- Reproducible Rerun from config
- No secrets in repo (.gitignore covers .env, checkpoints)
- AI disclosure tracked in docs/ai_disclosure.md

## 10. What we build vs borrow

- We build: generator, tiny models, experiments, metrics, narrative, viz, evaluation
- We cite: BDH/BDH-CQ architecture/equations/official results
- We reproduce selectively: only experiments that support claim and are feasible; label as OUR_REPRO

## 11. Exit gate

One end-to-end real experiment: generate unseen task -> demonstrations -> state adaptation (Delta_theta=0, Delta_s>0) -> query -> Y comparison -> measurable gain over frozen. That is Research Prototype v1 (D2.10).
