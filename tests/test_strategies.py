import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from adapt.tasks import generate_task
from adapt.strategies import make_strategy


def test_frozen_never_changes():
    s = make_strategy("frozen")
    s.reset()
    s.adapt(generate_task("linear", 1).demonstrations)
    assert s.telemetry()["persistent_delta"] == 0.0


def test_param_tta_really_updates():
    t = generate_task("linear", 3, n_demos=4)
    s = make_strategy("param_tta", family="linear", steps=8, lr=0.05)
    s.reset()
    before = s.theta.copy()
    s.adapt(t.demonstrations)
    assert np.linalg.norm(s.theta - before) > 1e-9
    assert s.telemetry()["persistent_delta"] > 0


def test_state_never_touches_params():
    t = generate_task("linear", 3, n_demos=4)
    s = make_strategy("state", family="linear")
    s.reset()
    s.adapt(t.demonstrations)
    tel = s.telemetry()
    assert tel["persistent_delta"] == 0.0
    assert tel["state_delta"] > 0


def test_ttt_state_persistent_fixed():
    t = generate_task("linear", 3, n_demos=4)
    s = make_strategy("ttt_state", family="linear")
    s.reset()
    init = s._init.copy()
    s.adapt(t.demonstrations)
    assert np.allclose(s._init, init)
    assert s.telemetry()["state_delta"] > 0


def test_state_reset_isolation():
    tA = generate_task("linear", 1, n_demos=4)
    tB = generate_task("linear", 2, n_demos=4)
    s = make_strategy("state", family="linear")
    s.reset()
    s.adapt(tA.demonstrations)
    mid = s.get_state().copy()
    s.reset()
    assert np.allclose(s.get_state(), np.zeros_like(mid))
    s.adapt(tB.demonstrations)
    assert not np.allclose(s.get_state(), mid)


def test_param_reset_isolation():
    tA = generate_task("linear", 1, n_demos=4)
    s = make_strategy("param_tta", family="linear")
    s.reset()
    s.adapt(tA.demonstrations)
    s.reset()
    assert np.allclose(s.theta, s._theta0)
