# D5.3 — Experiment Reproducibility Package

A fresh machine should be able to go `clone → install → run experiment →
generate result → compare with reference` for the ADAPT learner-path
experiments (levels 1–3 below). The BDH R1/R2 reproductions are separate
(pinned external repos) and documented in `research/bdh/reproductions/`.

## Levels

| Level | What it does | Command |
|---|---|---|
| 1 — Smoke | Pipeline executes | `pytest tests/ -q` |
| 2 — Full experiment | Re-derives original metrics | `run_experiment.py experiments/configs/exp_001_linear.yaml` |
| 3 — Full artifact regeneration | Rebuilds the public figures | `run_all.sh` (or step 3 below) |

## Quick start (conda)

```bash
conda env create -f repro/environment.yml
conda activate adapt-repro
pip install -r repro/requirements.txt
```

or plain venv:

```bash
python -m venv .venv                      # Python 3.11+
.venv\Scripts\activate                    # Windows   (unix: source .venv/bin/activate)
pip install -r repro/requirements.txt
```

## Level 1 — smoke test

```bash
pytest tests/ -q
```

## Level 2 — full experiment

```bash
python run_experiment.py experiments/configs/exp_001_linear.yaml
python experiments/run_sweeps.py 002 003 004 006 007
```

## Level 3 — artifact regeneration (figures)

```bash
python research/experiments/make_figures.py
```

then compare regenerated PNGs against the pinned hashes:

```bash
python repro/check_expected.py
```

## Expected-output verification

`repro/expected_outputs/manifest.csv` pins a SHA-256 for every
`research/experiments/*/results.json` and every figure. The reference
hashes in the manifest were produced from commit `6f8d42d`; a fresh run
should reproduce results byte-identically on the same platform because
all randomness is seeded and all sweeps are run from identical configs
(only wall-clock time varies — see `phase2_validation_report.md`).

`scripts/analyze_sessions.py` is optional and requires the learner-study
session JSONs, which do not ship (consent-scoped — see `docs/data_disclosure.md`).