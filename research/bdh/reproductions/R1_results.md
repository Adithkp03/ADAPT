# D4.6 R1 results — 2026-09-07, torch CPU, random ids, no training

Pinned: official BDH @ `2b0d7a4` (pathwaycom/bdh); bdh-cq @ `c246f89`
(lucidrains/bdh-cq, third-party WIP). torch 2.14.0+cpu.

## Official BDH baseline: PASS
- config: n_layer=6 n_embd=256 n_head=4 vocab=256
- forward (1,64) -> logits (1, 64, 256), loss=5.5725 (finite, stochastic
  across runs since logits are uninitialized random; shape and finiteness
  are the invariant)
- memory/answer path exists as described.

## bdh-cq wrapper (third-party WIP): PASS
- BDH(dim=64) + ReasoningWrapper forward ok
- latent steps=4 -> 3 layer memories surfaced (return_memory=True)
- input-chunk -> memory -> latent-steps path exists; update_memory flag present in source.
- Label stays: third-party WIP, NOT official, NOT a reproduction of the 150M result.
