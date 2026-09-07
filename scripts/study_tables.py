"""D3.11 study tables: emit learning_gain, transfer, timing,
prediction_behavior, and misconception_shift CSVs from exported
anonymous session JSONs.

Usage:
    python scripts/study_tables.py evaluation/anon-*.json --out evaluation/analysis

Consumes the same session schema as scripts/analyze_sessions.py. Item
mappings are reused verbatim from research/education/evaluation_plan.md
(LO table) so the two tools cannot drift.
"""
import argparse
import csv
import glob
import json
import os

PRE_ANS = [1, 1, 1, 0, 1]
POST_ANS = [1, 1, 1, 1, 1]
LO_PRE = ["LO1", "LO5", "LO2", "LO4", "LO6"]
LO_POST = [["LO1"], ["LO5"], ["LO2"], ["LO4", "LO7"], ["LO6"]]


def load(path):
    with open(path) as f:
        return json.load(f)


def first(evs, name):
    return next((e for e in evs if e["ev"] == name), None)


def main(paths, outdir):
    os.makedirs(outdir, exist_ok=True)
    sessions = [load(p) for p in paths]
    rows_gain, rows_transfer, rows_timing, rows_pred = [], [], [], []
    lo_pre, lo_post = {}, {}
    bdh_ok = bdh_n = mech_ok = mech_n = 0
    for s in sessions:
        evs = s.get("events", [])
        sid = s.get("id", "?")
        pre = first(evs, "pretest")
        post = first(evs, "posttest")
        pre_s = pre["d"].get("s") if pre else None
        post_s = post["d"].get("s") if post else None
        gain = (post_s - pre_s) if (pre_s is not None and post_s is not None) \
            else None
        g = (gain / (POST_ANS[1] * len(LO_POST) - pre_s)) \
            if gain is not None and pre_s < 5 else (None if gain is None
                                                    else 0.0)
        if pre and post and pre["d"].get("detail") and post["d"].get("detail"):
            pd, qd = pre["d"]["detail"], post["d"]["detail"]
            for i, lo in enumerate(LO_PRE):
                lo_pre.setdefault(lo, []).append(pd[i] if i < len(pd) else 0)
            for i, los in enumerate(LO_POST):
                for lo in los:
                    lo_post.setdefault(lo, []).append(qd[i] if i < len(qd)
                                                      else 0)
        rows_gain.append({"session_id": sid, "pre": pre_s, "post": post_s,
                          "gain": gain, "g_norm": ("" if g is None
                                                   else round(g, 3))})
        t0 = evs[0]["t"] if evs else None
        t_run = next((e["t"] for e in evs
                      if e["ev"] in ("flagship_run", "lab_run")), None)
        t_mech = next((e["t"] for e in evs
                       if e["ev"] == "mech_quiz" and e["d"].get("ok")), None)
        ch = [e["d"] for e in evs if e["ev"] == "challenge_run"]
        ch = ch[-1] if ch else None
        sec = lambda ms: None if (ms is None or t0 is None) \
            else round((ms - t0) / 1000, 1)
        pri = [e["d"] for e in evs if e["ev"] == "challenge_dealt"]
        rows_transfer.append({"session_id": sid,
                              "pick": (ch or {}).get("pick"),
                              "winner": (ch or {}).get("winner")})
        rows_timing.append({"session_id": sid,
                            "t_first_run_s": sec(t_run),
                            "t_first_mech_ok_s": sec(t_mech)})
        nd = [e["d"].get("v") for e in evs if e["ev"] == "nd_predict"]
        ret = [e["d"].get("v") for e in evs if e["ev"] == "ret_predict"]
        rows_pred.append({"session_id": sid,
                          "nd_predict_events": len(nd),
                          "nd_predict_first": nd[0] if nd else "",
                          "nd_correct": (1 if nd and nd[0] == "improve"
                                         else 0),
                          "ret_predict_events": len(ret),
                          "ret_predict_first": ret[0] if ret else "",
                          "ret_correct": (1 if ret and ret[0] == "degrade"
                                          else 0)})
        for e in evs:
            if e["ev"] == "bdh_quiz":
                bdh_n += 1
                bdh_ok += 1 if e["d"].get("ok") else 0
            if e["ev"] == "mech_quiz":
                mech_n += 1
                mech_ok += 1 if e["d"].get("ok") else 0

    def write(name, rows, fieldnames):
        with open(os.path.join(outdir, name), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)

    write("learning_gain.csv", rows_gain,
          ["session_id", "pre", "post", "gain", "g_norm"])
    write("transfer.csv", rows_transfer, ["session_id", "pick", "winner"])
    write("timing.csv", rows_timing,
          ["session_id", "t_first_run_s", "t_first_mech_ok_s"])
    write("prediction_behavior.csv", rows_pred,
          ["session_id", "nd_predict_events", "nd_predict_first",
           "nd_correct", "ret_predict_events", "ret_predict_first",
           "ret_correct"])

    # Misconception shift, coded per participant from item-level
    # pre/post deltas (M3 not probed by fixed items; in-lab only).
    # M1: Q1 correct=1 -> misconception held when 0. M2: held when Q3
    # (LO2) is 0 OR final mech_quiz not ok. M4: pre Q4=0 == held.
    M1_pre, M1_post, M2_pre, M2_post, M4_pre, M4_post = [], [], [], [], [], []
    for s in sessions:
        evs = s.get("events", [])
        pre = first(evs, "pretest")
        post = first(evs, "posttest")
        if not (pre and post):
            continue
        pd = pre["d"].get("detail", []) or pre["d"].get("answers", [])
        qd = post["d"].get("detail", []) or post["d"].get("answers", [])
        mech_final = [e["d"].get("ok") for e in evs
                      if e["ev"] == "mech_quiz"]
        m1_pre = (1 if not pd or pd[0] == 0 else 0) if len(pd) >= 1 else None
        m1_post = (1 if not qd or qd[0] == 0 else 0) if len(qd) >= 1 else None
        m2_pre = (1 if not pd or pd[2] == 0 else 0) if len(pd) >= 3 else None
        m2_post_q = (1 if not qd or qd[2] == 0 else 0) if len(qd) >= 3 else None
        mech_ok_final = bool(mech_final) and mech_final[-1]
        m2_post = (1 if (m2_post_q or not mech_ok_final) else 0) \
            if m2_post_q is not None else None
        m4_pre = (1 if not pd or pd[3] == 0 else 0) if len(pd) >= 4 else None
        m4_post = (1 if not qd or qd[3] == 0 else 0) if len(qd) >= 4 else None
        for dst, v in ((M1_pre, m1_pre), (M1_post, m1_post),
                       (M2_pre, m2_pre), (M2_post, m2_post),
                       (M4_pre, m4_pre), (M4_post, m4_post)):
            if v is not None:
                dst.append(v)
    held = lambda a, b: f"{sum(a)}/{len(a)} -> {sum(b)}/{len(b)}"
    with open(os.path.join(outdir, "misconception_shift.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["misconception", "defined", "probe",
                    "held_pre -> held_post"])
        w.writerow(["M1", "learning requires weight change",
                    "pre/post Q1 (LO1)", held(M1_pre, M1_post)])
        w.writerow(["M2", "state equals weights",
                    "pre/post Q3 (LO2) + final mech_quiz",
                    held(M2_pre, M2_post)])
        w.writerow(["M4", "more compute always better",
                    "pre/post Q4 (LO4/LO7 cliff)", held(M4_pre, M4_post)])
        w.writerow(["M3", "recurrence equals TTT",
                    "not probed by fixed items", "n/a"])
        w.writerow(["M5", "more dims = more concepts",
                    "not probed by fixed items", "n/a"])
    # Per-LO means (item level)
    with open(os.path.join(outdir, "per_lo_gain.csv"), "w",
              newline="") as f:
        w = csv.writer(f)
        w.writerow(["lo", "pre_mean", "post_mean", "n"])
        for lo in ["LO1", "LO2", "LO4", "LO5", "LO6", "LO7"]:
            a = lo_pre.get(lo, [])
            b = lo_post.get(lo, [])
            if a or b:
                w.writerow([lo,
                            round(sum(a) / len(a), 3) if a else "",
                            round(sum(b) / len(b), 3) if b else "",
                            max(len(a), len(b))])

    aggs = {"bdh_order_quiz_correct": bdh_ok, "bdh_order_quiz_n": bdh_n,
            "mech_correct": mech_ok, "mech_n": mech_n}
    with open(os.path.join(outdir, "signals.json"), "w") as f:
        json.dump({"n_sessions": len(sessions), **aggs}, f, indent=2)
    print(f"Wrote {outdir}: learning_gain, transfer, timing, "
          f"prediction_behavior, per_lo_gain, signals.json")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", default="evaluation/analysis")
    args = ap.parse_args()
    files = [f for p in args.paths for f in glob.glob(p)] or []
    if not files:
        print(__doc__)
        raise SystemExit(1)
    main(files, args.out)