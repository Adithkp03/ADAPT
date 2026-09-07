"""Throwaway live smoke for Phase 3 close-out (not part of the suite)."""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
URL = "http://127.0.0.1:8132"


def post(path, body):
    req = urllib.request.Request(
        URL + path, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=120).read()), 200
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}"), e.code


p = subprocess.Popen([sys.executable, str(ROOT / "server.py"), "--port",
                      "8132"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
try:
    for _ in range(100):
        time.sleep(0.2)
        try:
            urllib.request.urlopen(URL + "/api/health", timeout=2).read()
            break
        except Exception:
            continue
    r, c = post("/api/episode", {"family": "linear",
                                 "strategy": "learned_state",
                                 "strategy_kwargs": {}, "seed": 7,
                                 "n_demos": 4})
    print("learned_state", c, r["telemetry"]["persistent_delta"],
          round(r["telemetry"]["state_delta"], 2))
    r, c = post("/api/episode", {"family": "linear",
                                 "strategy": "learned_tta",
                                 "strategy_kwargs": {}, "seed": 7,
                                 "n_demos": 4})
    print("learned_tta", c, r.get("correct"),
          r["telemetry"]["persistent_delta"])
    r, c = post("/api/episode", {"family": "symbolic",
                                 "strategy": "learned_ttt",
                                 "strategy_kwargs": {}, "seed": 7})
    print("learned_nonlinear", c, r)
    r, c = post("/api/episode", {"family": "linear", "strategy": "bogus",
                                 "strategy_kwargs": {}, "seed": 7})
    print("bad_strategy", c)
    r, c = post("/api/sweep", {"family": "linear", "strategy": "state",
                               "strategy_kwargs": {}, "var": "n_demos",
                               "values": [1, 4], "episodes": 5,
                               "seed_base": 0})
    print("sweep_prov", c, sorted(r["provenance"].keys()))
    r, c = post("/api/interference", {"family": "linear",
                                      "strategy": "state", "seed": 33})
    print("interference_prov", c, "provenance" in r)
    r, c = post("/api/compare", {"family": "linear",
                                 "strategies": ["state", "learned_state"],
                                 "strategy_kwargs": {}, "seed": 21,
                                 "n_demos": 4})
    print("compare_learned", c,
          {k: v["correct"] for k, v in r["rows"].items()})
finally:
    p.terminate()
