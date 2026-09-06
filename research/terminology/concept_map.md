# Concept Map — ADAPT (source for concept_map.pdf)

```mermaid
flowchart TD
    Q[New task arrives: demonstrations D, query Q, hidden rule R, ground truth Y]
    Q --> C[CONTEXT: condition on D]
    Q --> S[STATE: s_t = F(s_{t-1}, x_t)]
    Q --> W[WEIGHTS: theta_{t+1}=theta_t - eta grad L]

    C --> HYB[Hybrids: context+state, memory+weights]
    S --> HYB
    W --> HYB

    HYB --> BDH[BDH: synaptic memory sigma_{t+1}=sigma_t + eta X Y^T]
    HYB --> BDHCQ[BDH-CQ: recurrent memory + latent reasoning K steps]

    C --> ICL[ICL: y = f_theta(D,Q), delta_theta=0]
    S --> REC[Recurrent adaptation: delta_s>0 delta_theta=0]
    W --> TTT[Param TTT: delta_theta>0]
```

Export with: `mmdc -i research/terminology/concept_map.md -o research/terminology/concept_map.pdf`
