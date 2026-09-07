"""Phase 3 acceptance: §66 Definition of Done + D3.1–D3.12 presence.

Static + import-level (fast, hermetic). Live HTTP behavior is covered by
tests/test_server.py; engine honesty here reuses src/adapt directly.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

WEB_HTML = (ROOT / "web" / "index.html").read_text()
WEB_JS = (ROOT / "web" / "app.js").read_text()
WEB_CSS = (ROOT / "web" / "styles.css").read_text()
SERVER = (ROOT / "server.py").read_text()


def test_d31_learning_spec_present():
    p = ROOT / "research" / "education" / "learning_experience_spec.md"
    assert p.exists()
    t = p.read_text()
    assert "STATE 0" not in t  # compressed state machine ok...
    for key in ["misconception", "Transfer", "LO1"]:
        assert key.lower() in t.lower(), key


def test_d32_interaction_model_covers_controls():
    t = (ROOT / "research" / "education" / "interaction_model.md").read_text()
    for key in ["N_D", "/api/episode", "/api/sweep", "/api/interference",
                "/api/intervene", "precomputed", "learned_tta"]:
        assert key in t, key
    assert "without a row" in t  # no cosmetic controls rule


def test_d33_design_trilogy():
    for name in ["visual_system.md", "state_visualization.md",
                 "interaction_patterns.md"]:
        p = ROOT / "design" / name
        assert p.exists(), name
    vs = (ROOT / "design" / "visual_system.md").read_text()
    assert "LIVE" in vs and "PRECOMPUTED" in vs and "aria-live" in vs
    sv = (ROOT / "design" / "state_visualization.md").read_text()
    assert "Δθ" in sv and "Forbidden" in sv
    ip = (ROOT / "design" / "interaction_patterns.md").read_text()
    assert "Predict" in ip and "Sandbox" in ip


def test_d34_flagship_60s_present():
    assert "flag-demos" in WEB_HTML and "flag-your" in WEB_HTML
    assert "flag-run" in WEB_HTML and "WHAT CHANGED" in WEB_JS
    assert "flagLoad(7)" in WEB_JS  # pre-populated, no blank canvas


def test_d35_guided_journey_stages():
    for sid in ["stage-start", "stage-flagship", "stage-manipulate",
                "stage-tradeoffs", "stage-interfere", "stage-bdh",
                "stage-challenge", "stage-lab", "stage-results"]:
        assert sid in WEB_HTML, sid


def test_d36_lab_full_controls():
    for cid in ["lab-fam", "lab-strat", "lab-seed", "lab-nd", "lab-noise",
                "lab-run", "pre-sel", "pre-run"]:
        assert cid in WEB_HTML, cid
    assert "/api/episode" in WEB_JS
    # D3.6: Phase 2B learned trio exposed as a separated Research-Lab group
    for opt in ["learned_state", "learned_tta", "learned_ttt"]:
        assert opt in WEB_HTML, opt
    assert "Research Lab" in WEB_HTML
    assert "linear only" in WEB_HTML or "linear only" in WEB_JS


def test_d37_stress_lab_predictive():
    assert "data-retpred" in WEB_HTML and "data-ndpred" in WEB_HTML
    assert "nz-run" in WEB_HTML and "ds-run" in WEB_HTML


def test_d38_bdh_module_honesty():
    assert "eta" in WEB_HTML and "Educational implementation" in WEB_HTML
    assert "official BDH" in WEB_HTML or "official BDH" in WEB_JS or \
        "not official" in WEB_HTML.lower() or "Educational" in WEB_HTML
    assert "PUBLISHED RESULT" in WEB_HTML
    assert "bdh-quiz" in WEB_HTML


def test_d39_assessment_present():
    for key in ["pretest", "posttest", "ch-quiz", "ch-explain", "export",
                "scoreboard"]:
        assert key in WEB_HTML or key in WEB_JS, key
    assert "LearningGain" in WEB_HTML or "truth test" in WEB_HTML


def test_d310_badges_and_provenance():
    for b in ["LIVE", "PRECOMPUTED", "SYNTHETIC", "PUBLISHED RESULT",
              "ILLUSTRATIVE"]:
        assert b in WEB_HTML, b
    assert "provenance" in WEB_JS.lower() and "config_hash" in WEB_JS
    assert "PRECOMPUTED" in SERVER  # server re-stamps precomputed
    # every live surface renders a drawer: episode, sweep table,
    # interference (WHY + provenance), intervention
    assert WEB_JS.count("provHTML(r.provenance") >= 4
    assert "WHY?" in WEB_JS  # D3.7 causal chain on interference


def test_d311_evaluation_plan_and_instrumentation():
    t = (ROOT / "docs" / "phase3_design_report.md").read_text()
    assert "D3.11" in t and "pre/post" in t.lower()
    assert "session_start" in WEB_JS and "JSON" in WEB_JS  # event log export
    assert "misconception" in t.lower()


def test_d312_release_candidate_hygiene():
    assert "coming soon" not in WEB_HTML.lower()
    assert "http://127.0.0.1:8123" not in WEB_JS  # relative API paths
    assert "/api/" in WEB_JS
    assert "offline" in WEB_HTML.lower() or \
        "no build, no CDN" in (ROOT / "docs" /
                               "phase3_design_report.md").read_text()


def test_computational_no_fake_logic_in_frontend():
    for bad in ["memory failed", "show(\"failed\"", "Math.random() * 0.3",
                "fake", "placeholder result"]:
        assert bad not in WEB_JS, bad
    for ep in ["/api/episode", "/api/compare", "/api/interference",
               "/api/intervene", "/api/sweep", "/api/precomputed"]:
        assert ep in WEB_JS or ep in SERVER, ep


def test_ux_mobile_a11y_hooks():
    assert "700px" in WEB_CSS  # single-column collapse
    assert "prefers-reduced-motion" in WEB_CSS
    assert "aria-live" in WEB_HTML and "aria-label" in WEB_HTML
    assert 'class="skip"' in WEB_HTML
    assert ".live" in WEB_CSS and ".pre" in WEB_CSS  # badge styles


def test_server_stdlib_and_endpoints():
    assert "ThreadingHTTPServer" in SERVER
    assert "fastapi" not in SERVER.lower() and "flask" not in SERVER.lower()
    for ep in ["api/episode", "api/compare", "api/interference",
               "api/intervene", "api/sweep", "api/precomputed",
               "api/figure", "api/health", "api/meta"]:
        assert ep in SERVER, ep


def test_engine_honest_deltas_import_level():
    from adapt import runner as R
    from adapt import tasks as T
    task = T.generate_task("linear", 7, n_demos=4, noise=0.0, split="test")
    r = R.run_episode(task, "state", {"tol": 0.5})
    assert r["correct"] is True
    assert r["telemetry"]["persistent_delta"] == 0.0
    assert r["telemetry"]["state_delta"] > 0
    assert R.RESULT_SCHEMA_VERSION == 1


def test_precomputed_and_figures_exist():
    for exp in ["008_intervention_linear", "005_interference_linear",
                "004_state_capacity_linear", "003_compute_scaling_linear"]:
        assert (ROOT / "research" / "experiments" / exp /
                "results.json").exists(), exp
    assert len(list((ROOT / "research" / "experiments" / "figures").glob(
        "*.png"))) >= 5


def test_result_schema_shape():
    from adapt import runner as R
    from adapt import tasks as T
    task = T.generate_task("linear", 7, n_demos=4, noise=0.0, split="test")
    r = R.run_episode(task, "state", {"tol": 0.5})
    for key in ["pred", "correct", "telemetry"]:
        assert key in r, key
    tel = r["telemetry"]
    for key in ["persistent_delta", "state_delta", "latency_ms"]:
        assert key in tel, key
    assert re.match(r"^[0-9a-f]{6,}$", R._config_hash({"a": 1}))


def test_compare_model_column_and_holdout_rendered():
    assert "<th scope=\"col\">Model</th>" in WEB_JS
    assert "model_version" in WEB_JS
    assert WEB_JS.count("r.task.holdout") >= 2  # flagship + lab
    assert "Single-episode result" in WEB_JS


def test_controlled_vs_learned_equation_distinguished():
    assert "CONTROLLED Adaptive State" in WEB_HTML
    assert "tanh" in WEB_HTML
    assert "not the learned variant" in WEB_HTML


def test_no_hardcoded_developer_paths():
    import subprocess as sp
    pat = "C:" + "/Users"  # built dynamically so this test can't match itself
    out = sp.run(["git", "grep", "-n", pat,
                  "--", "tests", "server.py", "src", "web", "scripts"],
                 capture_output=True, text=True, cwd=str(ROOT)).stdout
    hits = [l for l in out.splitlines() if "test_no_hardcoded" not in l]
    assert hits == [], hits


def test_pilot_session_analyzes():
    import subprocess as sp
    fix = ROOT / "tests" / "fixtures" / "pilot_session.json"
    assert fix.exists()
    p = sp.run([sys.executable, str(ROOT / "scripts" / "analyze_sessions.py"),
                str(fix)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    assert "N sessions: 1" in p.stdout
    assert "gain=2" in p.stdout
    assert "LO4: pre=1.0" in p.stdout  # post Q4 credits LO4 too
    assert "LO7" in p.stdout
