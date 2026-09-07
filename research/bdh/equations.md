# D4.4 — BDH Equation Validation (stepper ↔ published equations)

This document validates the interactive BDH equation stepper (the
`EOR` array in `web/app.js`) against the published equations, records
every educational simplification, and links each displayed equation to
its source section. It is the supporting record for the D4.4 Definition
of Done: *"interactive/formal representation of relevant equations."*

Sources:
- **[P]** A. Kosowski et al., *The Dragon Hatchling: The Missing Link
  between the Transformer and Models of the Brain*, arXiv:2509.26507
  (2025).
- **[E]** Pathway, *The Equations of Reasoning*,
  https://pathway.com/research/the-equations-of-reasoning (local cited
  as "Equations page"). Section references below are to that page as
  verified 2026-09-07.
- **[R]** Official repo https://github.com/pathwaycom/bdh @ `2b0d7a4`.

Validation date: 2026-09-07. Stepper code: `web/app.js` lines 249–262
(`EOR` array + `eorRender`), HTML: `web/index.html` lines 167–175.

---

## 1. The four-round structure (round numbering)

**Published (verbatim structure, [E] §4 "In plain words"):**

| Round | Displayed name in stepper | Published description | Status |
|---|---|---|---|
| 1 | `Round 4l — memory read` | 4l: accumulate from beliefs + inputs + σ (modus ponens) | VERIFIED ✓ |
| 2 | `Round 4l+1 — memory write` | 4l+1: reweight σ with outer/Hebbian product of X·Yᵀ | VERIFIED ✓ |
| 3 | `Round 4l+2 — gated readout` | 4l+2: Y read out from A gated by X | VERIFIED ✓ |
| 4 | `Round 4l+3 — state update` | 4l+3: final update of X, loop closes | VERIFIED ✓ |

**Round numbering check:** the stepper uses the integer indices 0–3
(`eorI`), displayed 1-indexed as `Round {eorI+1} of 4` for the human
learner, while the *body* of each card carries the authoritative
published label `4l`, `4l+1`, `4l+2`, `4l+3`. This matches the paper's
round enumeration exactly; the 1-indexed display is purely presentational
and does not change the published numbering. Navigation is modular
(`(eorI ± 1) % 4`), so the cycle wraps from 4l+3 back to 4l — consistent
with the paper's closed local cycle.

**Source links per round:**
- Round 4l → [E] §4 "In plain words", 1st bullet.
- Round 4l+1 → [E] §4 "the update step ... outer/Hebbian product", 2nd
  bullet; [P] working-memory / synaptic-plasticity section (dossier §3).
- Round 4l+2 → [E] §4 "gated readout", 3rd bullet; [P] sparse-positive
  activations (dossier §2-G, citing paper Fig. 14).
- Round 4l+3 → [E] §4 "final update of X", 4th bullet.

## 2. The σ (memory-write) update

**Published formulation (as characterized in [E] §4, step 2):**
σ is reweighted by the outer (Hebbian) product of X and Y.

**Educational simplified form displayed in the UI (explicitly labeled):**

```
σ ← σ + η·X·Yᵀ        (simplified educational form)
```

Source of the simplification, and the label applied: `web/index.html`
labels the η panel "Educational implementation (not official BDH code)"
and "σ₁₂ = 0.14 → 0.14 + η (demo scalars ... magnitude only, no
semantics)", and the stepper card labels "Educational rendering of the
published 4-round structure ... not a simulation of BDH." The dossier
(`bdh_technical_dossier.md` §2-D) states the educational form
`σ ← σ + η·X·Yᵀ` is *always labeled* a simplified educational form —
never presented as verbatim published form. VERIFIED ✓.

**‖Δσ‖ live arithmetic:** `web/app.js` `etaUpd()` computes
`‖Δσ‖ = η·1·1` using unit vector magnitudes ‖x‖=‖y‖=1 (labeled demo
vectors). This is scalar arithmetic to illustrate *magnitude response*,
not a BDH simulation; the audit (`docs/bdh_integrity_audit.md`) marks it
ILLUSTRATIVE.

## 3. Simplification ledger (every simplification explicit)

| Simplification | Where | Marker | Status |
|---|---|---|---|
| σ ← σ + η·X·Yᵀ (order-1 outer product only) | η panel + stepper | "Educational implementation (not official BDH code)" | VERIFIED ✓ |
| ‖Δσ‖ = η·1·1 (unit vectors) | η panel | "‖x‖=‖y‖=1 demo vectors" | VERIFIED ✓ |
| σ₁₂ demo scalars 0.14 → 0.14+η | η panel | "magnitude only, no semantics" | VERIFIED ✓ |
| 4-round structure rendering | stepper | "not a simulation of BDH" | VERIFIED ✓ |
| Round 1..4 display (1-indexed) | stepper | presentational only; body uses 4l..4l+3 | VERIFIED ✓ |

No simplification is presented as verbatim published form; the UI is
consistently labeled.

## 4. Cross-checks enforced by tests

- `tests/test_phase4.py::test_d44_equation_stepper` asserts the stepper
  DOM (`eor-step`, `eor-prev`), the published round naming `Round 4l`,
  the σ output (`sig-out`), and the honesty marker `not a simulation`.
- `docs/bdh_integrity_audit.md` maps every UI sentence, including the
  EOR stepper, to a category (Published fact + Illustration) and support.

## 5. Conclusion

The interactive equation stepper is faithful to the published 4-round
structure and round numbering; the σ update is an explicitly labeled
educational simplification; every simplification is marked; and each
equation/simplification is linked to its source section above. D4.4 is
satisfied.
