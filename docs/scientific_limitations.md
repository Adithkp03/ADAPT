# Scientific Limitations (what AdaptLab does NOT claim)

1. **Toy substrates, not frontier models.** Linear/quadratic/symbolic/
   compositional/grid tasks are procedurally generated SYNTHETIC probes
   that isolate adaptation mechanics. No claim transfers automatically to
   Transformers, LLM in-context learning, or ARC-AGI.
2. **"Adaptive State" is hand-designed** (sufficient-statistics memory),
   not a learned RNN — except the explicitly labeled Phase 2B learned
   trio (`learned_state/learned_tta/learned_ttt`, linear-only,
   `learned-v1` checkpoints, ES meta-training per `learned.py`).
3. **State bottleneck d_s is an operational proxy** (project-and-reconstruct),
   not a direct measure of memory capacity.
4. **Intervention weight rests on swap + nullmean.** Shuffle/zero/noise
   failures are degradation sanity checks, never information-removal proof.
5. **Single-episode interference is visceral, not statistical.** The
   population claim lives in precomputed E5 / sweeps with CIs.
6. **BDH/BDH-CQ panels are PUBLISHED RESULT + ILLUSTRATIVE.** The η demo is
   an educational implementation of the published update form, not official
   BDH code (repo: https://github.com/pathwaycom/bdh). The 150M / 29.5%
   pass@2 / $0.0007/task figure is configuration-specific per the BDH-CQ
   dossier — never generalized.
7. **Assessment is formative + manual.** Pre/post gains measure the
   artifact's teaching, not participant ability; free text is hand-rubriced.
   No learning-gain claim ships without anonymized session data attached.
8. **Sweep CIs are Wilson/empirical over ≤50 test-split episodes** with
   fixed seed bases — reproducible, not infinite-population guarantees.
