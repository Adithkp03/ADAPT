# D4.3 — Concept-to-BDH Mapping (every row evidenced, analogue ≠ identity)

**Rule:** our model is a controlled experimental analogue, never an
official implementation. Rows state the *shared design pressure*, not
equivalence. Sources: [P]=BDH paper 2509.26507, [R]=official BDH repo
README, [E]=Equations of Reasoning page, [C]=BDH-CQ paper 2608.09888,
[O]=our engine (`src/adapt` + vetted results).

| Our concept | Our substrate | BDH | BDH-CQ | Evidence |
|---|---|---|---|---|
| Task adaptation | state update s (Δθ=0) [O] | synaptic memory σ evolves, trained graph fixed [P][E] | recurrent memory M_t evolves, θ static [C] | TOY_EXPERIMENT ↔ PUBLISHED_EMPIRICAL |
| Inference-time information | demonstrations D [O] | incoming activity / new inputs [E §4] | input sequence tokens [C] | TOY ↔ PUBLISHED |
| Memory write | s = s + φ(x,y) per example [O] | round 4l+1: σ reweighted by outer/Hebbian X·Yᵀ [E §4] | recurrent memory update per input [C] | TOY ↔ OFFICIAL_REPORT |
| Persistent parameters | fixed θ (Δθ≡0) [O] | trained graph/parameters, slow weights [E][P] | trained weights fixed at inference [C] | TOY ↔ PUBLISHED |
| Query computation | prediction from adapted state [O] | iterative local dynamics; rounds 4l/4l+2/4l+3 [E §4] | latent recurrent computation × K [C] | TOY ↔ PUBLISHED |
| Interference | A→B→A retention drop, measured [O E5] | working-memory interference window (design implication; decay/interference lifetime) [P][E §3-v1] | recurrent memory dynamics under sequences (to be studied) | TOY measured; frontier side = interpretation, labeled as such |
| Adaptation cost | K steps ↔ accuracy/latency [O E3] | GPU-efficient formulation; sparsity ↔ predictability [E §4] | effort (low/med/high) ↔ performance; $0.0007/task @150M config [C] | TOY ↔ PUBLISHED (config-scoped) |
| Learning without weight change | flagship Δθ=0/Δs≠0 [O] | Hebbian working memory, monosemantic synapses [R][P] | ICL + latent reasoning, no param update [C] | TOY ↔ PUBLISHED |

## Explicit non-identities

- Our φ-accumulator ≠ BDH σ-dynamics (ours: hand-designed sufficient
  statistics; theirs: learned graph-local Hebbian system at scale).
- Our K gradient steps (param TTA) have NO BDH/BDH-CQ counterpart —
  the table marks this by absence, and the UI never implies one.
- BDH "similar to a standard SSM memory write" quotes [E §4] Step 2
  ONLY; architecture identity "Mamba-style SSM" is forbidden (brief).
- BDH-CQ "is TTT" is forbidden; allowed: "closely related point in the
  inference-time adaptation design space" (dossier v1 §6 relation table).
