# D5.3 — experiment configs (canonical copies)

These YAML files are byte-copies of the canonical configs used to
produce the reference results (kept in `experiments/configs/`). The
repro package copies them so a fresh machine regenerates the reference
hashes without needing the history of `experiments/configs/`.

Canonical set (matches the results pinned in `expected_outputs/`):
  exp_001_linear.yaml            linear acquisition (E1, live flagship base)
  exp_001_symbolic.yaml          symbolic acquisition (E1)
  exp_001_arc.yaml               arc-like proxy acquisition (E4.8)
  exp_005_interference_linear.yaml   E5 linear A->B->A
  exp_005_interference_symbolic.yaml E5 symbolic A->B->A
  exp_008_intervention_linear.yaml   E8 linear perturb/restore
  exp_008_intervention_symbolic.yaml E8 symbolic perturb/restore
  exp_009_learned_linear.yaml        E9 learned trio (s0/s1)
  exp_009_learned_interference.yaml  E9 learned interference
  exp_009_learned_intervention.yaml  E9 learned intervention

(The E2/E3/E4/E6/E7 sweeps are parameterized in `run_sweeps.py` and do
not need a config file per point.)