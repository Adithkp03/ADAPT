# D3.3 — Visual System (what the learner sees, and why)

**Status:** normative for `web/` as built. Any visual change must keep the
guarantees below or update this file in the same commit.

## 1. Governing rule

The interface communicates **causality, not decoration** (phase3 §8, §49, §64):

```text
DEMONSTRATIONS → STATE → QUERY → PREDICTION → GROUND TRUTH
```

Every stage renders this chain top-to-bottom in one flow. Desktop
side-by-side panels (`grid2`) collapse to this single column at ≤700px; the
order never changes, so the mobile layout (§46) is the canonical layout.

## 2. Tokens (`web/styles.css`)

| Token | Value | Role |
|---|---|---|
| `--ink` `#1a1a1a` | body text, buttons | contrast ≥ 12:1 on white |
| `--dim` `#5a5a5a` | secondary text | contrast ≥ 7:1 on white |
| `--acc` `#0b5fff` | sweep bars, links-in-spirit | never the sole carrier of correctness |
| `--ok` `#0a7a2f` | ✓ correct | always paired with ✓/✗ glyph + word |
| `--bad` `#b00020` | ✗ wrong | always paired with ✓/✗ glyph + word |
| honesty panel | `#fff8e1` on 2px `--ink` border | top-of-page scope statement |

Rules: correctness is never color-only (§47) — every verdict is a glyph
plus a word ("✓ Correct" / "✗ Wrong" / "✓ within tolerance"). Charts never
stand alone: each canvas is followed by a data table with identical numbers
plus 95% CI text (§47 text equivalents). No animation conveys computation;
results appear via `aria-live="polite"` and `prefers-reduced-motion` kills
all transitions (§47 reduced-motion option).

## 3. Badges — evidence status at a glance (D3.10, §33)

Rendered by `badges()` in `web/app.js` on **every** result block:

| Badge | Class | Meaning |
|---|---|---|
| LIVE | `live` | computed now by `src/adapt` over HTTP |
| PRECOMPUTED | `pre` | vetted `research/experiments/*/results.json` |
| SYNTHETIC | `syn` | procedurally generated task, not natural data |
| PUBLISHED RESULT | `pub` | paper-reported number (BDH-CQ panel only) |
| ILLUSTRATIVE | `ill` | diagram/demo, not model output (η demo) |

The footer repeats this legend verbatim. Precomputed payloads are
re-stamped server-side (`execution_type: precomputed`,
`badges: [PRECOMPUTED, SYNTHETIC]`) so the UI cannot mislabel them.

## 4. Provenance drawer (D3.10, §34)

Every live result carries `<details><summary>Experiment details
(provenance)</summary>` with: seed, task-generator version, model version,
config hash, git commit, result-schema version. Same fields the research
runner writes; the frontend renders them, never invents them (§54).

## 5. Hierarchy per screen (§62)

1. Current task → 2. Action (one primary button) → 3. State (WHAT CHANGED
box) → 4. Result → 5. Truth beside estimate (three-row table, never below
the fold, §63) → 6. Explanation (`<details class="mech">` mechanism chain).
Secondary content (provenance, precomputed browser) always sits below the
truth table.

## 6. What we deliberately do NOT build (§50, §64)

No decorative sliders (each control has a row in
`research/education/interaction_model.md` or it is removed); no neuron
cartoons; no glowing-brain animation; no streaming for effect; no "coming
soon" panels (D3.12). If removing an element does not weaken the lesson,
it ships removed.
