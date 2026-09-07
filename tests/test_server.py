"""Server smoke tests: import-level + live HTTP (spawns server)."""
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
PY = sys.executable


def test_meta_imports():
    import sys
    sys.path.insert(0, str(ROOT / "src"))
    from adapt.strategies import STRATEGY_DISPLAY, FAMILY_DISPLAY
    assert STRATEGY_DISPLAY["state"].startswith("Adaptive State")
    assert FAMILY_DISPLAY["grid_toy"] == "Grid Transformation Lab"


@pytest.fixture(scope="module")
def srv():
    p = subprocess.Popen([PY, str(ROOT / "server.py"), "--port", "8123"],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        for _ in range(100):
            time.sleep(0.2)
            try:
                urllib.request.urlopen("http://127.0.0.1:8123/api/health",
                                       timeout=2).read()
                break
            except Exception:
                continue
        yield "http://127.0.0.1:8123"
    finally:
        p.terminate()


def _post(base, path, body):
    req = urllib.request.Request(
        base + path, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def test_episode_honest_deltas(srv):
    r = _post(srv, "/api/episode",
              {"family": "linear", "strategy": "state",
               "strategy_kwargs": {"state": {}}, "seed": 7, "n_demos": 4})
    assert r["correct"] is True
    assert r["telemetry"]["persistent_delta"] == 0.0
    assert r["telemetry"]["state_delta"] > 0
    assert r["provenance"]["result_schema_version"] == 1
    assert "LIVE" in r["badges"]


def test_compare_paired(srv):
    r = _post(srv, "/api/compare",
              {"family": "linear",
               "strategies": ["context", "param_tta", "state"],
               "strategy_kwargs": {"param_tta": {"steps": 8, "lr": 0.05}},
               "seed": 21, "n_demos": 4})
    assert set(r["rows"]) == {"context", "param_tta", "state"}
    assert r["rows"]["context"]["correct"] is True


def test_interference_and_intervention(srv):
    r = _post(srv, "/api/interference",
              {"family": "linear", "strategy": "state", "seed": 33})
    assert r["A"]["correct_before"] is True
    i = _post(srv, "/api/intervene",
              {"family": "linear", "strategy": "state", "seed": 33,
               "perturbations": ["zero", "swap", "nullmean"]})
    assert i["rows"]["swap"]["restored"] is True


def test_precomputed_labeled(srv):
    u = srv + "/api/precomputed?exp=008_intervention_linear"
    r = json.loads(urllib.request.urlopen(u, timeout=30).read())
    assert r["execution_type"] == "precomputed"
    assert "PRECOMPUTED" in r["badges"]


def _post_raw(base, path, payload, raw_bytes=None):
    data = raw_bytes if raw_bytes is not None else json.dumps(
        payload).encode()
    req = urllib.request.Request(
        base + path, data=data,
        headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    except urllib.error.HTTPError as e:
        return {"__status__": e.code,
                "__body__": json.loads(e.read() or b"{}")}


def test_validation_rejects_bad_inputs(srv):
    import urllib.error  # noqa: F401 (ensures handler above catches)
    ep = {"family": "linear", "strategy": "state",
          "strategy_kwargs": {}, "seed": 7, "n_demos": 4}
    assert _post_raw(srv, "/api/episode",
                     {**ep, "family": "nope"})["__status__"] == 400
    assert _post_raw(srv, "/api/episode",
                     {**ep, "strategy": "nope"})["__status__"] == 400
    assert _post_raw(srv, "/api/compare",
                     {"family": "linear", "strategies": ["state", "nope"],
                      "seed": 1})["__status__"] == 400
    assert _post_raw(srv, "/api/sweep",
                     {"family": "linear", "strategy": "state",
                      "var": "nope", "values": [1]})["__status__"] == 400
    assert _post_raw(srv, "/api/sweep",
                     {"family": "linear", "strategy": "state",
                      "var": "n_demos", "values": [],
                      })["__status__"] == 400
    assert _post_raw(srv, "/api/intervene",
                     {"family": "linear", "strategy": "state", "seed": 1,
                      "perturbations": ["nope"]})["__status__"] == 400
    assert _post_raw(srv, "/api/episode", "not-json",
                     raw_bytes=b"{bad")["__status__"] == 400


def test_bounds_are_clamped_not_fatal(srv):
    r = _post_raw(srv, "/api/episode",
                  {"family": "linear", "strategy": "state",
                   "strategy_kwargs": {}, "seed": 7, "n_demos": 9999,
                   "noise": 5.0})
    assert r["correct"] is True and "__status__" not in r


def test_learned_defaults_and_scope(srv):
    r = _post_raw(srv, "/api/episode",
                  {"family": "linear", "strategy": "learned_state",
                   "strategy_kwargs": {}, "seed": 7, "n_demos": 4})
    assert r["telemetry"]["persistent_delta"] == 0.0
    assert r["telemetry"]["state_delta"] > 0
    assert _post_raw(
        srv, "/api/episode",
        {"family": "symbolic", "strategy": "learned_state",
         "strategy_kwargs": {}, "seed": 7})["__status__"] == 400


def test_provenance_on_all_live_endpoints(srv):
    ep = _post_raw(srv, "/api/episode",
                   {"family": "linear", "strategy": "state",
                    "strategy_kwargs": {}, "seed": 7})
    assert ep["provenance"]["result_schema_version"] == 1
    it = _post_raw(srv, "/api/interference",
                   {"family": "linear", "strategy": "state", "seed": 33})
    assert it["provenance"]["result_schema_version"] == 1
    iv = _post_raw(srv, "/api/intervene",
                   {"family": "linear", "strategy": "state", "seed": 33,
                    "perturbations": ["swap"]})
    assert iv["provenance"]["result_schema_version"] == 1
    sw = _post_raw(srv, "/api/sweep",
                   {"family": "linear", "strategy": "state",
                    "strategy_kwargs": {}, "var": "n_demos",
                    "values": [1, 4], "episodes": 5, "seed_base": 0})
    assert sw["provenance"]["result_schema_version"] == 1
    assert sw["provenance"]["config_hash"]
