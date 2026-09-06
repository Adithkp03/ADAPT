# Data Leakage Policy

**Status:** normative.

1. Split rule families per tier into META-TRAIN (available during model development) / ADAPTATION (unseen rules for inference) / EVAL-HELD-OUT (never inspected during development). Generator versions pinned.
2. No eval rule family may be selected, tuned, or filtered after looking at eval performance. Violation = invalid run.
3. Seeds: eval seed set fixed at freeze and never reused for development tuning.
4. ARC-like: our synthetic tasks are NEVER called "ARC" unqualified; official ARC items (if any) versioned separately with license/provenance.
5. Checkpoint selection on meta-train only; eval runs once per frozen config.
6. Any leakage suspicion -> rerun with fresh seed set + new generator version, reported alongside.
