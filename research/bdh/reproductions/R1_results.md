# D4.6 R1 results — 2026-09-07, torch CPU, random ids, no training

## Official BDH baseline: PASS
- config: n_layer=6 n_embd=256 n_head=4 vocab=256
- forward (1,64) -> logits (1, 64, 256), loss=5.5661 (finite)
- memory/answer path exists as described.

## bdh-cq wrapper: FAIL — ModuleNotFoundError: No module named 'einx'
