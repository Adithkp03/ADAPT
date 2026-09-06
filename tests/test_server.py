"""Server smoke tests: import-level + live HTTP (spawns server)."""
import json
import subprocess
import time
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
PY = "C:/Users/adith/AppData/Local/Programs/Python/Python311/python.exe"


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
