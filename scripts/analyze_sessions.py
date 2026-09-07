"""Analyze exported AdaptLab session JSONs (D3.11 quantitative half).

Usage:
    system-python scripts/analyze_sessions.py sessions/*.json [--rubric rubric.csv]

rubric.csv (optional, hand-scored): session_id,explain_a,explain_b
  explain_a: names state (not weights) as storage (0/1)
  explain_b: describes interference as overwrite/competition (0/1)

Prints: N, pre/post means, per-LO gain, normalized gain, transfer score,
time-to-first-run, time-to-correct-mechanism, prediction accuracy by event.
"""
import glob
import json
import sys

PRE_ANS = [1, 1, 1, 0, 1]
POST_ANS = [1, 1, 1, 1, 1]
LO_PRE = ["LO1", "LO5", "LO2", "LO4", "LO6"]
# Post Q4 (capacity cliff) probes LO4 and LO7 by design (evaluation_plan §3)
LO_POST = [["LO1"], ["LO5"], ["LO2"], ["LO4", "LO7"], ["LO6"]]


def load(path):
    with open(path) as f:
        return json.load(f)


def event_times(session, name):
    t0 = session.get("started", "")
    return [e for e in session.get("events", []) if e.get("ev") == name]


def main(paths, rubric_path=None):
    rubric = {}
    if rubric_path:
        for line in open(rubric_path).read().strip().splitlines()[1:]:
            sid, a, b = line.split(",")[:3]
            rubric[sid.strip()] = (int(a), int(b))
    sessions = [load(p) for p in paths]
    print(f"N sessions: {len(sessions)}")
    lo_acc = {}
    for s in sessions:
        evs = s.get("events", [])
        pre = next((e["d"].get("s") for e in evs if e["ev"] == "pretest"),
                   None)
        post = next((e["d"].get("s") for e in evs if e["ev"] == "posttest"),
                    None)
        pre_d = next((e["d"].get("detail") for e in evs
                      if e["ev"] == "pretest"), None)
        post_d = next((e["d"].get("detail") for e in evs
                       if e["ev"] == "posttest"), None)
        if pre_d and post_d and len(pre_d) == 5 and len(post_d) == 5:
            for i, lo in enumerate(LO_PRE):
                lo_acc.setdefault(lo + "_pre", []).append(pre_d[i])
            for i, los in enumerate(LO_POST):
                for lo in los:
                    lo_acc.setdefault(lo + "_post", []).append(post_d[i])
        t_first_run = next(
            (e["t"] for e in evs if e["ev"] in ("flagship_run", "lab_run")),
            None)
        t_mech = next((e["t"] for e in evs if e["ev"] == "mech_quiz"
                       and e["d"].get("ok")), None)
        preds = [e for e in evs if e["ev"] in ("nd_predict", "ret_predict")]
        t0 = evs[0]["t"] if evs else None
        gain = (post - pre) if pre is not None and post is not None else None
        g = (gain / (5 - pre)) if gain is not None and pre < 5 else None
        rub = rubric.get(s.get("id"), (None, None))
        sec = lambda ms: None if ms is None else round(ms / 1000, 1)
        print(f"- {s.get('id')}: pre={pre} post={post} gain={gain} "
              f"g_norm={None if g is None else round(g, 3)} "
              f"t_first_run_s={sec(None if t_first_run is None or t0 is None else t_first_run - t0)} "
              f"t_mech_ok_s={sec(None if t_mech is None or t0 is None else t_mech - t0)} "
              f"pred_events={len(preds)} explain_rubric={rub}")
    if not sessions:
        return
    if lo_acc:
        print("\nPer-LO means (item-level log present):")
        for lo in ["LO1", "LO2", "LO4", "LO5", "LO6", "LO7"]:
            a = lo_acc.get(lo + "_pre", [])
            b = lo_acc.get(lo + "_post", [])
            if a or b:
                ma = sum(a) / len(a) if a else None
                mb = sum(b) / len(b) if b else None
                print(f"  {lo}: pre={ma} (n={len(a)}) post={mb} "
                      f"(n={len(b)})")
    else:
        print("\nNOTE: no item-level pre/post detail — totals only "
              "(sessions exported before the item-logging fix).")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rub = next((a.split("=")[1] for a in sys.argv[1:]
                if a.startswith("--rubric=")), None)
    files = [f for pat in args for f in glob.glob(pat)] or []
    if not files:
        print(__doc__)
        sys.exit(1)
    main(files, rub)
