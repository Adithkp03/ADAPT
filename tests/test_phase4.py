"""Phase 4 acceptance: D4.1–D4.11 presence + integrity guards (fast, static)."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

WEB_HTML = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
WEB_JS = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")


def test_d41_d42_technical_dossiers():
    bdh = (ROOT / "research" / "bdh" / "bdh_technical_dossier.md"
           ).read_text(encoding="utf-8")
    assert "2509.26507" in bdh and "97.4%" in bdh and "4l+1" in bdh
    assert "does NOT" in bdh or "does not reproduce" in bdh
    cq = (ROOT / "research" / "bdh" / "bdhcq_technical_dossier.md"
          ).read_text(encoding="utf-8")
    assert "2608.09888" in cq and "29.5%" in cq and "WIP" in cq


def test_d43_concept_mapping():
    t = (ROOT / "research" / "bdh" / "concept_mapping.md"
         ).read_text(encoding="utf-8")
    assert "non-identities" in t.lower() or "Non-identities" in t
    assert "TOY" in t and "PUBLISHED" in t


def test_d45_evidence_ledger_valid():
    rows = list(csv.DictReader(open(ROOT / "research" / "bdh" /
                                    "evidence_ledger.csv")))
    assert len(rows) >= 15
    assert {"claim", "evidence_type", "allowed_wording"} <= set(
        rows[0].keys())
    assert any("NEVER" in (r["evidence_type"] + r["allowed_wording"])
               for r in rows)


def test_d47_comparison_study():
    rows = list(csv.DictReader(open(ROOT / "research" / "bdh" /
                                    "frontier_comparison.csv")))
    mechs = {r["mechanism"] for r in rows}
    assert {"frozen", "state", "learned_state"} <= mechs
    assert all("adaptation_gain" in r and "retention_A" in r for r in rows)
    assert (ROOT / "research" / "experiments" / "figures" /
            "fig8_frontier_tradeoff.png").exists()
    md = (ROOT / "research" / "bdh" / "frontier_comparison.md"
          ).read_text(encoding="utf-8")
    assert "never merged" in md.lower() or "never in the same" in md.lower()


def test_d44_equation_stepper():
    assert "eor-step" in WEB_HTML and "eor-prev" in WEB_HTML
    assert "Round 4l" in WEB_JS and "sig-out" in WEB_JS
    assert "not a simulation" in WEB_HTML
    eq = (ROOT / "research" / "bdh" / "equations.md").read_text(
        encoding="utf-8")
    for name in ["4l — memory read", "4l+1 — memory write",
                 "4l+2 — gated readout", "4l+3 — state update"]:
        assert name in eq, name
    assert "simplified educational form" in eq
    assert "[E] §4" in eq  # source-section links per equation


def test_d46_reproduction_log():
    t = (ROOT / "research" / "bdh" / "reproductions" / "README.md"
         ).read_text(encoding="utf-8")
    assert "2b0d7a4" in t and "NOT attempted" in t
    assert "PENDING" not in t and "PLANNED" not in t  # R1/R2 closed out
    assert (ROOT / "research" / "bdh" / "reproductions" / "R1_results.md"
            ).exists()
    assert (ROOT / "research" / "bdh" / "reproductions" / "R2_results.md"
            ).exists()


def test_d48_arc_surfaced():
    assert "001_task_acquisition_arc" in SERVER
    assert "001_task_acquisition_arc" in WEB_HTML
    assert (ROOT / "research" / "experiments" / "001_task_acquisition_arc"
            / "results.json").exists()
    proxy = (ROOT / "research" / "experiments" /
             "arc_like_proxy_validation.md").read_text(encoding="utf-8")
    for sub in ["synthetic", "proxy", "git_commit",
                "config_hash", "n=200"]:
        assert sub.lower() in proxy.lower(), sub
    assert "ARC-AGI" in proxy and "does not run ARC-AGI" in proxy  # no benchmark reproduction implied
    # grid_toy never surfaces as "ARC Reasoning" in public UI
    assert "ARC Reasoning" not in WEB_HTML


def test_d410_audit_and_banned_wording():
    audit = (ROOT / "docs" / "bdh_integrity_audit.md").read_text(
        encoding="utf-8")
    assert "test_d410_audit_and_banned_wording" in audit  # real test name
    assert "Evidence-classification" in audit  # every number classified
    blob = WEB_HTML + WEB_JS
    for banned in ["just another Mamba", "BDH-CQ is TTT",
                   "we reproduced 97.4", "thinking about shape"]:
        assert banned not in blob, banned
    assert "do not generalize" in blob


def test_d49_educational_validation_instrumented():
    ev = (ROOT / "research" / "education" /
          "bdh_educational_validation.md").read_text(encoding="utf-8")
    assert "bdh_quiz" in ev and "equation stepper" in ev.lower()
    assert "6 mechanisms" in ev or "6-mechanism" in ev
    an = (ROOT / "scripts" / "analyze_sessions.py").read_text(
        encoding="utf-8")
    assert "bdh_quiz" in an  # D3.11 analysis consumes the BDH-CQ order quiz
    assert "bdh_order_quiz" in an
    assert "mech_quiz" in WEB_JS and "bdh_quiz" in WEB_JS  # live instrumented


def test_d411_report():
    t = (ROOT / "research" / "reports" / "phase4_bdh_frontier_report.md"
         ).read_text(encoding="utf-8")
    for h in ["## 1.", "## 5.", "## 8.", "## 10.", "## 11."]:
        assert h in t, h
    # D4.11: R1/R2 actual results present; conclusions frozen post-repro
    assert "R1 live" in t and "PASS" in t.replace("PASS:", "")
    assert "Conclusions (frozen post-reproduction" in t
    assert "did not reproduce" in t  # failed/not-attempted recorded
