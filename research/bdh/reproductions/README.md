# D4.6 — Reproduction / Validation Log (failures recorded, never hidden)

Pinned references (verified 2026-09-07):
- Official BDH repo: https://github.com/pathwaycom/bdh @ `2b0d7a4`
  (2026-05-16, "Update README.md"). Local mirror: Temp/bdh_repo (not
  vendored — clone at the pinned sha to repeat).
- Third-party BDH-CQ: https://github.com/lucidrains/bdh-cq (WIP, NOT
  official). API verified from README + source.

## R0 — Static architecture verification (DONE, both repos)

Official BDH (`bdh.py`): `BDHConfig(n_layer=6, n_embd=256, n_head=4,
vocab_size=256)` + `BDH(nn.Module).forward(idx, targets)`; RoPE-style
`Attention` with `K is Q` self-attention assertion; nanoGPT-lineage
`train.py` (seed 1337, GradScaler, tf32, cuda→cpu fallback, tiny
Shakespeare via `requests`). Deps: `torch numpy requests`.
Matches the paper's "baseline variant" description — consistent with the
README's explicit non-reproduction of the internal 97.4%.

bdh-cq (`bdh_cq/bdh_cq.py`): `BDH` + `BDHReasoningWrapper` with
`update_memory` freeze flag (§3.3 of the paper's framing),
`combine_memories` (additive order-1 memory per layer),
`return_memory=True` surfacing, `generate()` decoding. The
input-chunk → memory → latent-steps → answer path exists as described.

## R1 — Live instantiation + forward (PENDING torch CPU install)

Plan: CPU-only `pip install torch`; instantiate official `BDH` at default
config + forward on random `(1, 64)` ids (loss, no training); instantiate
`BDH(dim=64, num_tokens=256)` + wrapper `generate` on random ids with
`return_memory=True` (confirm memories surface). Success = shapes flow,
no NaN; NOT a benchmark reproduction. Results appended here when torch
lands (background job proc_cb41cff3df09).

## R2 — Tiny controlled memory probe (PLANNED, only if R1 passes)

Same random prompt twice, `update_memory=True` vs `False`: memories must
differ in the first case and equal the frozen path in the second. Tiny,
synthetic, labeled TOY_EXPERIMENT on third-party code.

## NOT attempted (stated, not hidden)

- Internal 97.4% Sudoku Extreme (officially not reproducible from the
  public repo — README note; attempting it would be theater).
- BDH-CQ 150M / ARC-AGI-1 (needs frontier weights/compute; reported,
  not reproduced — ledger rows stay PUBLISHED_EMPIRICAL).
- Any training run beyond default toy configs.
