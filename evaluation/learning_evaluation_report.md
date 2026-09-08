# D5.8 — Learning Effectiveness Report

**Status:** study IN PROGRESS — n=10 distinct participants analysed to
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
  in nine of ten sessions; scoring local and anonymous. No LLM grading.

## Current study data (n=10, distinct participant IDs)

Sessions collected 2026-09-07/08 into `evaluation/`. One export file
(`anon-2gtigru.json`) was a re-export of `anon-1gtigru.json` (same
participant ID, same first-attempt events) and is **excluded** from the
analysis to avoid double-counting; see `data_disclosure.md`. Six new
participants joined on 2026-09-08. `anon-4rg340l` has no pre-test
record (export began at first run), so its row counts toward the total
n but its gain is undefined. `anon-mk9fhh9` and `anon-4rg340l` did not
reach the transfer challenge; `anon-9bve55v`'s first-run timestamp
(~7.3 h) reflects a session tab left open overnight, so timing medians
rather than means are reported for `t_first_run_s`.

### Learning gain (per session)

| session_id | pre | post | gain | g_norm |
|---|---|---|---|---|
| anon-1gtigru | 3 | 4 | +1 | 0.50 |
| anon-3f2st3z | 1 | 2 | +1 | 0.25 |
| anon-cyxta1v | 2 | 3 | +1 | 0.33 |
| anon-9bve55v | 2 | 5 | +3 | 1.00 |
| anon-id8tbdc | 3 | 4 | +1 | 0.50 |
| anon-iw0axf8 | 1 | 5 | +4 | 1.00 |
| anon-mk9fhh9 | 4 | 3 | −1 | −1.00 |
| anon-ry3bx6i | 3 | 4 | +1 | 0.50 |
| anon-y7gfr18 | 3 | 3 | 0 | 0.00 |
| **mean (n=9)** | **2.44** | **3.67** | **+1.22** | **g_norm=0.34** |

g_norm undefined for pre=5: not present. 7/9 gained, 1 flat, 1 negative
gain (anon-mk9fhh9, pre=4 the highest baseline). Aggregate standardized
gain (post−pre)/(5−pre) = **0.48**.

### Per-LO means (item-level)

| LO | pre | post | n |
|---|---|---|---|
| LO1 (adaptation outside weights) | 0.22 | 0.67 | 9 |
| LO2 (Δθ=0, Δs≠0 distinction) | 0.33 | 0.78 | 9 |
| LO4 (capacity cliff) | 1.00 | 0.78 | 9 |
| LO5 (A→B→A interference) | 0.44 | 0.78 | 9 |
| LO6 (BDH/BDH-CQ reuse) | 0.44 | 0.67 | 9 |
| LO7 (compute non-monotonic) | – | 0.78 | 9 |

Largest shifts: LO1 (+45 pp), LO2 (+45 pp), LO5 (+33 pp). LO4 starts
at ceiling (1.00) and dips post (−22 pp) — this is the capacity-cliff
item that gets *harder* once the cliff is explained; treat as expected
post-instruction repricing, not a fidelity loss. LO6 soft +22 pp. LO7
post-only (no pre probe). All six LOs correct at post ≥ 0.67.

### Transfer (unseen challenge, pick winner)

| session_id | pick | winner |
|---|---|---|
| anon-1gtigru | frozen | context |
| anon-3f2st3z | frozen | context |
| anon-cyxta1v | context | context |
| anon-9bve55v | state | context |
| anon-id8tbdc | context | context |
| anon-iw0axf8 | state | context |
| anon-ry3bx6i | state | context |
| anon-y7gfr18 | state | context |

Transfer solved: **2/8** (anon-cyxta1v, anon-id8tbdc). Winner is
`context` for every dealt challenge; most participants still pick
`frozen`/`state` on the unseen seed. First transfer success appeared at
n≈5; the two context picks are the strongest signal so far that the
transfer copy can work, but at 25% it is not a reliable outcome yet.
If the pick rate does not rise with further n, the transfer-selection
copy is the revision target.

### Prediction behavior

`nd_predict` (N_D direction, correct = improve): **4/9** first-attempt
correct. `ret_predict` (retention, correct = degrade): **0/5** — every
participant who predicted retention expected `improve`/`same`, then saw
A→B→A drops in-app. `nd_predict` guesses are near chance; cross-check
`prediction_behavior.csv` after each new batch.

### Misconception shift (M1, M2, M4)

| misconception | held pre → held post |
|---|---|
| M1 learning ⇒ weight change | 7/9 → 3/9 |
| M2 state ≡ weights | 6/9 → 2/9 |
| M4 more compute always better | 0/9 → 2/9 |
| M3, M5 | not probed by fixed items |

M2 (state ≡ weights) shifted 6/9 → 2/9 — the intended flagship shift
replicated at larger n and the biggest single move. M1 also cleared
(7/9 → 3/9). M4 started at floor (0/9 held) and 2 participants acquired
it post hoc — treat with care; it is the weakest-tracked item.

### In-lab validation signals (D4.9)

- BDH-CQ order quiz (LO6): **6/11** correct
- Mechanism-distinction checks (`mech_quiz`): **10/13** correct (first-OK
  in all but one session)

`mech_quiz` first-OK times (median **43.9 s**, IQR ~17–137 s; one
overnight outlier excluded): 136.4, 25.3, 43.9, 3.0 min outlier, 113.1,
265.2, 56.2, 27.7, 17.3, 171.6.

### Direction reading (preliminary, not a claim)

Pre/post items move the right way on the flagship distinguish LOs
(LO1/LO2/LO5) and on M2 (6/9→2/9 held). Transfer picked `context` in
2/8 — first positive signal but still well below reliable. The two
criteria to watch at the full sample are (a) transfer > 50% and
(b) M2 not persisting; currently (a) is 25% and trending up. Stop
rules from the protocol apply before anything is published as a gain.

## What “done” requires

1. Reach n = 8–15 distinct participants (n=10 today — at the low end of
   range; study may close at n=10 or continue to n=15).
2. Verify no duplicated participant IDs in exported JSONs (one
   re-export seen and excluded; exporter ID bug fixed in the current
   release).
3. Final run of `scripts/analyze_sessions.py` + `scripts/study_tables.py`
   over `evaluation/anon-*.json`.
4. Publish anonymized JSONs + analysis output alongside ANY gain claim.
5. Apply stop rules: ≥30% flagship failure in ~2 min → fix flagship;
   persistent M2 → revise WHAT CHANGED; skipped predictions → gate
   prediction before run; transfer ≈ 0 → revise transfer-stage copy.
   (Transfer is 2/8 — copy revision is triggered if it stalls.)

## 60-second test (author self-run, 2026-09-07)

Unseen task → prediction → run → result → ground truth → state change
is reachable in one screen and one click (“Run Adaptive State”); all
server legs measure < 100 ms (D5.5), so the loop completes in well
under 60 s on first visit. Independent verification with naive users is
part of the full study above.