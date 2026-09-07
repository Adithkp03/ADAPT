# D4.6 R2 results — 2026-09-07, CPU, synthetic random ids

Pinned: bdh-cq @ `c246f89` (lucidrains/bdh-cq, third-party WIP).
torch 2.14.0+cpu. TOY_EXPERIMENT label; no learned-memory-content claim.

- max|Δmemory| across presentations (update=True): 0.000000
- max|Δmemory| across presentations (update=False): 0.000000
- PASS: frozen path deterministic; update flag threads through the memory path without error.
- Interpretation: wrapper exposes a controllable memory write switch (§3.3 framing); no claim about learned memory content.
