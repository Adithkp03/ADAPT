# D5.8 — Learning Effectiveness Report

**Status:** study IN PROGRESS — n=4 distinct participants analysed to
date (target 8–15 per `docs/evaluation_protocol.md`). The results below
are preliminary and must not be read as a finished learning-gain claim;
the protocol requires the full n plus published raw session JSONs
alongside any claim. No participant was involved in building the
artifact; all records are anonymous (`anon-xxxxxxx`).

## Instrument (frozen)

- Pre-test (5 items, LO1/LO2/LO4/LO5/LO6) → post-test (same LOs) +
  transfer challenge (unseen family, pick winner strategy).
- Misconceptions tracked M1–M5 (M2 = “state ≡ weights”, the stickiest;
  M4 = “more compute always better”) — `research/education/
  evaluation_plan.md` §5.
- Pipeline: in-app Export JSON → `scripts/analyze_sessions.py` +
  `scripts/study_tables.py` → tables below. Item-level quiz logs present
  in all four sessions; scoring local and anonymous. No LLM grading.

## Current study data (n=4, distinct participant IDs)

Sessions collected 2026-09-07 into `evaluation/`. One export file
(`anon-2gtigru.json`) was a re-export of `anon-1gtigru.json` (same
participant ID, same first-attempt events) and is **excluded** from the
analysis to avoid double-counting; see `data_disclosure.md`.

### Learning gain (per session)

| session_id  | pre | post | gain | g_norm |
|---|---|---|---|---|
| anon-1gtigru | 3 | 4 | +1 | 0.50 |
| anon-3f2st3z | 1 | 2 | +1 | 0.25 |
| anon-ry3bx6i | 3 | 4 | +1 | 0.50 |
| anon-y7gfr18 | 3 | 3 | 0 | 0.00 |
| **mean (n=4)** | **2.5** | **3.25** | **+0.75** | **g=0.27** |

g_norm undefined for pre=5: not present. All four gain rows positive or
flat; no negative gain.

### Per-LO means (item-level)

| LO | pre | post | n |
|---|---|---|---|
| LO1 (adaptation outside weights) | 0.25 | 0.50 | 4 |
| LO2 (Δθ=0, Δs≠0 distinction) | 0.25 | 0.75 | 4 |
| LO4 (capacity cliff) | 1.00 | 0.75 | 4 |
| LO5 (A→B→A interference) | 0.25 | 0.75 | 4 |
| LO6 (BDH/BDH-CQ reuse) | 0.75 | 0.50 | 4 |
| LO7 (compute non-monotonic) | – | 0.75 | 4 |

Largest shifts: LO2 (+50 pp) and LO5 (+50 pp). LO4/LO6 soft either way
(ceiling / item-diff noise at n=4). LO7 post-only (no pre probe).

### Transfer (unseen challenge, pick winner)

| session_id  | pick | winner |
|---|---|---|
| anon-1gtigru | frozen | context |
| anon-3f2st3z | frozen | context |
| anon-ry3bx6i | state | context |
| anon-y7gfr18 | state | context |

Transfer solved: **0/4**. No participant selected the winning `context`
strategy on the unseen seed. This is the single most important
honest-negative at n=4: the journey improved quiz scores but did not
yet transfer to choosing the adaptive strategy — must be re-checked as
n grows; if it persists, the transfer stage copy is the revision target.

### Prediction behavior

`nd_predict` (N_D direction, correct = improve): 2/4 first-attempt
correct. `ret_predict` (retention, correct = degrade): 0/3 (one
participant did not make a ret prediction). First-attempt ret
predictions were all `improve`/`same` — participants expected no
interference, then saw A→B→A drops in-app.

### Misconception shift (M1, M2, M4)

| misconception | held pre → held post |
|---|---|
| M1 learning ⇒ weight change | 3/4 → 2/4 |
| M2 state ≡ weights | 3/4 → 1/4 |
| M4 more compute always better | 0/4 → 1/4 |
| M3, M5 | not probed by fixed items |

M2 (state ≡ weights) shifted 3/4 → 1/4 at n=4 — direction consistent
with the pilot (n=1) and with the flagship/WHAT CHANGED design intent,
but n is far too small to claim. M1 shifted 3/4 → 2/4. M4 started at
floor and one trailing misconception appeared post — treat with care at
n=4.

### In-lab validation signals (D4.9)

- BDH-CQ order quiz (LO6): **2/5** correct
- Mechanism-distinction checks (`mech_quiz`): **4/7** correct final-attempt

`mech_quiz` first-OK times (time-to-correct-mechanism): 136.4 s, 25.3 s,
17.3 s, 171.6 s.

### Direction reading (preliminary, not a claim)

The pre/post item data moves the right way on the flagship distinguish
Lots (LO2, LO5) and on M2; the transfer stage shows zero generalization
to picking the adaptive strategy on an unseen family. At n≥8 the two
criteria to watch are (a) transfer > 0% and (b) M2 not persisting;
currently (b) looks achievable and (a) does not — the transfer-selection
copy is the planned revision if the pattern holds. Stop rules from the
protocol apply before anything is published as a gain.

## What “done” requires

1. Reach n = 8–15 distinct participants (n=4 today).
2. Verify no duplicated participant IDs in exported JSONs (one
   re-export seen and excluded; the exporter ID bug is fixed as part of
   the next release).
3. Final run of `scripts/analyze_sessions.py` + `scripts/study_tables.py`
   over `evaluation/sessions/*.json`.
4. Publish anonymized JSONs + analysis output alongside ANY gain claim.
5. Apply stop rules: ≥30% flagship failure in ~2 min → fix flagship;
   persistent M2 → revise WHAT CHANGED; skipped predictions → gate
   prediction before run; transfer ≈ 0 → revise transfer-stage copy.

## 60-second test (author self-run, 2026-09-07)

Unseen task → prediction → run → result → ground truth → state change
is reachable in one screen and one click (“Run Adaptive State”); all
server legs measure < 100 ms (D5.5), so the loop completes in well
under 60 s on first visit. Independent verification with naive users is
part of the full study above.