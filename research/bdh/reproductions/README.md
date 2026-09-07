# D4.6 — Reproduction / Validation Log (failures recorded, never hidden)

Pinned references (verified 2026-09-07):
- Official BDH repo: https://github.com/pathwaycom/bdh @ `2b0d7a4`
  (2026-05-16, "Update README.md"). Local mirror: Temp/bdh_repo (not
  vendored — clone at the pinned sha to repeat).
- Third-party BDH-CQ: https://github.com/lucidrains/bdh-cq (WIP, NOT
  official) @ `c246f89` (2026-09-07, latest main). API verified from
  README + source.

Environment recorded for reproduction (2026-09-07, date of R1/R2):
- Python 3.11 (cp1252 code page; UTF-8 forced on all writes).
- torch 2.14.0+cpu (CPU-only build), no CUDA.
- numpy, requests (per repo requirements); einx installed to satisfy the
  bdh-cq dependency (see R1 FAIL record below).

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

## R1 — Live instantiation + forward (DONE, 2026-09-07, PASS)

Plan (as executed): CPU-only `pip install torch`; instantiate official
`BDH` at default config + forward on random `(1, 64)` ids (loss, no
training); instantiate `BDH(dim=64, num_tokens=256)` + wrapper forward on
random ids with `return_memory=True` (confirm memories surface). Success
= shapes flow, no NaN; NOT a benchmark reproduction.

Result: **PASS** — see `R1_results.md`:
- Official BDH baseline: forward `(1,64) -> logits (1,64,256)`, loss
  finite; config n_layer=6 n_embd=256 n_head=4 vocab=256.
- bdh-cq wrapper: `BDH(dim=64)` + `BDHReasoningWrapper` forward ok, 3
  layer memories surfaced with `return_memory=True`.

**Recorded failure during R1 (not hidden):** the first bdh-cq run
(committed `0902893`) FAILED with `ModuleNotFoundError: No module named
'einx'` — the third-party wrapper's `einx` dependency was not installed.
This was resolved by installing `einx`; subsequent runs PASS. The FAIL
record is retained in git history (commit `0902893`) rather than deleted,
so the failure and its condition are reproducible.

## R2 — Tiny controlled memory probe (DONE, 2026-09-07, PASS)

Same random prompt twice, `update_memory=True` vs `False`: the
discriminant is that `update_memory=False` is deterministic (frozen path)
and the flag threads through without error. Tiny, synthetic, labeled
TOY_EXPERIMENT on third-party code.

Result: **PASS** — see `R2_results.md`. Both `update=True` and
`update=False` produce `max|Δmemory| = 0.000000` across presentations
(the wrapper's forward is stateless for random init), so the discriminant
recorded is: frozen path deterministic; update flag threads through the
memory path without error. No claim about learned memory content.

## NOT attempted (stated, not hidden)

- Internal 97.4% Sudoku Extreme (officially not reproducible from the
  public repo — README note; attempting it would be theater).
- BDH-CQ 150M / ARC-AGI-1 (needs frontier weights/compute; reported,
  not reproduced — ledger rows stay PUBLISHED_EMPIRICAL). D4.6 Level 3
  (published benchmark) is **NOT attempted** per the bdh-cq dossier §6.
- Any training run beyond default toy configs.
