#!/usr/bin/env bash
# ADAPT Phase 5 — Level 1→3 reproducibility orchestration (bash).
# Fresh-machine flow:  clone -> env (see import steps in README)
#                      -> run_experiment -> generate result -> compare.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[1/4] smoke test (pipeline executes)"
python -m pytest tests/ -q

echo "[2/4] full experiment (original metrics re-derived)"
python run_experiment.py experiments/configs/exp_001_linear.yaml
python experiments/run_sweeps.py 002 003 004 006 007

echo "[3/4] artifact regeneration (public figures)"
python research/experiments/make_figures.py

echo "[4/4] compare generated outputs against pinned reference hashes"
python repro/check_expected.py

echo "reproduction OK"