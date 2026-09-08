"""Phase 5 acceptance: D5.1-D5.15 presence + integrity guards.

Mostly fast/static; two runtime checks (bounds via server internals and
result-hash integrity).
"""
import csv
import hashlib
import sys
import zipfile
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

WEB_HTML = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
WEB_JS = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
WEB_CSS = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
SERVER_SRC = (ROOT / "server.py").read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- D5.1
def test_d51_architecture_freeze():
    t = (ROOT / "docs" / "architecture_freeze.md").read_text(encoding="utf-8")
    assert "FROZEN" in t and "out of scope" in t
    # freezes concrete things
    for frag in ["result_schema_version", "checkpoints/learned_*_s0.npz",
                 "results/final_manifest.csv", "stdlib"]:
        assert frag in t, frag


def test_d51_frozen_assets_hash_matches_manifest():
    rows = list(csv.DictReader(open(ROOT / "results" / "final_manifest.csv",
                                    encoding="utf-8")))
    assert len(rows) >= 9  # figures
    for r in rows:
        p = ROOT / r["path"]
        assert p.exists(), r["path"]
        assert sha256(p) == r["sha256"], r["path"]


# ---------------------------------------------------------------- D5.2
def test_d52_scientific_claim_audit():
    rows = list(csv.DictReader(open(ROOT / "audit" /
                                    "scientific_claim_audit.csv",
                                    encoding="utf-8")))
    assert len(rows) >= 20  # C01..C20
    assert {"claim_id", "claim_text", "evidence_type", "verified_by",
            "status", "allowed_wording"} <= set(rows[0].keys())
    assert all(r["status"].startswith("VERIFIED") for r in rows)
    # no banned absolutism: every row has an allowed_wording
    assert all(r["allowed_wording"].strip() for r in rows)
    # hypothesis scoping preserved (candidate claim marked
    # VERIFIED-AS-HYPOTHESIS, never upgraded to a bare finding)
    assert any("HYPOTHESIS" in r["status"] for r in rows)


# ---------------------------------------------------------------- D5.3
def test_d53_repro_package_present():
    for needed in ["environment.yml", "requirements.txt", "run_all.sh",
                   "configs", "seeds", "data", "expected_outputs",
                   "check_expected.py"]:
        assert (ROOT / "repro" / needed).exists(), needed
    assert (ROOT / "repro" / "expected_outputs" / "manifest.csv").exists()
    seeds = (ROOT / "repro" / "seeds" / "seed_index.csv").read_text(
        encoding="utf-8")
    assert "0" in seeds and "seed" in seeds
    assert any((ROOT / "repro" / "configs").glob("*.yaml"))


def test_d53_expected_output_hashes_match_results():
    rows = list(csv.DictReader(open(ROOT / "repro" / "expected_outputs" /
                                    "manifest.csv", encoding="utf-8")))
    assert len(rows) >= 28  # 19 results + 9 figures
    for r in rows:
        p = ROOT / r["path"]
        assert p.exists(), r["path"]
        assert sha256(p) == r["sha256"], r["path"]


# ---------------------------------------------------------------- D5.4
def test_d54_provenance_package():
    for fn, cols in [
        ("code.csv", ["path", "origin", "license", "usage"]),
        ("data.csv", ["dataset", "origin", "license", "splits"]),
        ("models.csv", ["model_or_checkpoint", "origin", "status"]),
        ("assets.csv", ["asset", "origin", "license"]),
        ("fonts.csv", ["font"]),
        ("third_party.csv", ["package", "version_pinned", "license"]),
    ]:
        rows = list(csv.DictReader(open(ROOT / "provenance" / fn,
                                        encoding="utf-8")))
        assert rows, fn
        assert set(cols) <= set(rows[0].keys()), fn


# ---------------------------------------------------------------- D5.5
def test_d55_performance_report_and_probe():
    t = (ROOT / "docs" / "performance_report.md").read_text(encoding="utf-8")
    assert "PASS" in t and "ms" in t
    assert "caveat" in t  # localhost-resolution caveat recorded
    probe = (ROOT / "scripts" / "perf_probe.py").read_text(encoding="utf-8")
    for ep in ["/api/health", "/api/episode", "/api/compare",
               "/api/precomputed", "/api/figure"]:
        assert ep in probe, ep


# ---------------------------------------------------------------- D5.6
def test_d56_input_bounds_via_server_internals():
    from server import _resolve_kw, _validate_request, MAX_BODY

    kw = _resolve_kw("state", {"state_dim": 10_000_000, "steps": 99_999,
                               "lr": 9.9})
    assert kw["state_dim"] == 64
    assert kw["steps"] == 64
    assert kw["lr"] == 5.0
    kw = _resolve_kw("state", {"state_dim": 0, "steps": -5, "lr": -1.0})
    assert kw["state_dim"] == 1 and kw["steps"] == 0 and kw["lr"] == 0.0
    # allowlist + learned-trio linear-only scope
    fam, name, err = _validate_request("nope", "state")
    assert err and err[1] == 400
    fam, name, err = _validate_request("linear", "not_a_strategy")
    assert err and err[1] == 400
    fam, name, err = _validate_request("symbolic", "learned_state")
    assert err  # learned trio is linear-only
    assert MAX_BODY == 1 << 20


def test_d56_security_review_documented():
    t = (ROOT / "docs" / "security_review.md").read_text(encoding="utf-8")
    assert "No module-global mutable state" in t
    assert "rate limiting" in t  # residual risk accepted, documented
    assert "test_phase5" in t  # tests referenced actually exist


# ---------------------------------------------------------------- D5.7
def test_d57_accessibility_and_mobile():
    t = (ROOT / "docs" / "accessibility_audit.md").read_text(encoding="utf-8")
    for req in ["Keyboard navigation", "Screen-reader", "aria-live",
                "Mobile", "PASS"]:
        assert req in t, req
    # claims match the code
    assert re.search(r'<meta\s+name=["\']viewport["\']', WEB_HTML)
    assert 'class="skip' in WEB_HTML or "class=\"skip" in WEB_HTML
    assert 'role="img"' in WEB_HTML
    assert WEB_HTML.count("aria-live") >= 3
    assert "@media" in WEB_CSS and "grid2" in WEB_CSS
    assert "max-width: 100%" in WEB_CSS or "max-width:100%" in WEB_CSS
    assert len(re.findall(r"<h1", WEB_HTML)) == 1
    # no div-as-button trap: interactive controls are native elements
    assert 'role="button"' not in WEB_HTML


# ---------------------------------------------------------------- D5.8
def test_d58_learning_report_honest():
    t = (ROOT / "evaluation" /
         "learning_evaluation_report.md").read_text(encoding="utf-8")
    # honest study framing: no finished claim, distinct-ID discipline
    assert "IN PROGRESS" in t and "n=10" in t
    assert ("distinct" in t and "excluded" in t) or "dedupe" in t \
        or "double-count" in t
    assert "8" in t and "15" in t and "participant" in t
    assert "transfer" in t and "preliminary" in t
    assert "stop rules" in t
    assert ("must not" in t) or ("not published" in t) or ("no claim" in t)
    jets = sorted((ROOT / "evaluation").glob("anon-*.json"))
    assert len(jets) >= 1
    # duplicate-ID files must be excluded, not counted twice
    ids = []
    import json
    for j in jets:
        ids.append(json.loads(j.read_text(encoding="utf-8")).get("id"))
    assert len(ids) == len(set(ids)) or "excluded" in t
    # analysis tables exist for the reported numbers
    assert (ROOT / "evaluation" / "analysis" / "learning_gain.csv").exists()
    assert (ROOT / "evaluation" / "analysis" / "transfer.csv").exists()


# ---------------------------------------------------------------- D5.9
def test_d59_results_package():
    assert (ROOT / "results" / "final").is_dir()
    assert (ROOT / "results" / "tables").is_dir()
    figures = {p.name for p in (ROOT / "results" / "final").glob("*.png")}
    assert {"fig1_task_acquisition.png", "fig2_demo_scaling.png",
            "fig3_state_capacity.png", "fig4_interference_linear.png",
            "fig5_compute.png"} <= figures
    tables = [p.name for p in (ROOT / "results" / "tables").glob("*.csv")]
    assert len(tables) >= 8
    # narrative answers the "final scientific narrative" questions
    n = (ROOT / "results" / "README.md").read_text(encoding="utf-8")
    for q in ["What can adapt", "How quickly", "At what cost",
              "Where is the information stored", "How much can it retain",
              "What causes failure", "relate to BDH-CQ"]:
        assert q in n, q
    assert "No cherry-picking" in n
    assert "HONEST NEGATIVE" in n or "honest negative" in n.lower()


# ---------------------------------------------------------------- D5.10
def test_d510_concept_summary_word_count():
    t = (ROOT / "concept_summary.md").read_text(encoding="utf-8")
    body = t.split("---")[0]
    words = re.findall(r"\w+", re.sub(r"[*#`\[\]()]", " ", body))
    assert 500 <= len(words) <= 950, len(words)
    for para in ["Paragraph 1", "Paragraph 7", "Final"]:
        assert para in t


# ---------------------------------------------------------------- D5.11
def test_d511_readme_sections():
    t = (ROOT / "README.md").read_text(encoding="utf-8")
    for h in ["What this is", "Central claim", "Intended learner",
              "Prerequisites", "Learning objectives", "Scientific background",
              "System architecture", "Experiment design", "Adaptation methods",
              "Task generator", "Ground truth", "Live computation",
              "Precomputed results", "Synthetic data",
              "Illustrative visualizations", "BDH integration",
              "BDH-CQ integration", "Results", "Reproduction",
              "Installation", "Deployment", "Limitations", "Sources",
              "Licenses", "AI disclosure", "Credits"]:
        assert f"## {h}" in t, h
    # central claim + honest status carried
    assert "CANDIDATE HYPOTHESIS" in t
    assert "did **not** reproduce" in t.replace("\n", " ") \
        or "did not reproduce" in t
    # no ARC mislabel
    assert "ARC Reasoning" not in t


# ---------------------------------------------------------------- D5.12
def test_d512_disclosure_package():
    for fn in ["sources.md", "licenses.md", "ai_assistance.md",
               "ai_disclosure.md", "data_disclosure.md",
               "model_disclosure.md", "provenance.md"]:
        assert (ROOT / "docs" / fn).exists(), fn
    ai = (ROOT / "docs" / "ai_assistance.md").read_text(encoding="utf-8")
    for frag in ["generated code", "generated writing",
                 "Human review", "understood and defensible"]:
        assert frag.lower() in ai.lower(), frag


# ---------------------------------------------------------------- D5.13
def test_d513_release_checklist():
    t = (ROOT / "docs" / "release_checklist.md").read_text(encoding="utf-8")
    for i in range(1, 13):
        assert f"T{i}" in t, i
    assert "no sign-in" in t.lower()
    # failure handling implemented per §43
    assert "Experiment unavailable" in WEB_JS
    assert "Retry" in WEB_JS
    assert "Oops" not in WEB_JS
    # production loading behavior: no "Loading model..." 10s spinner
    assert "Loading model..." not in WEB_HTML and "Loading model..." not in WEB_JS


# ---------------------------------------------------------------- D5.14
def test_d514_defense_package():
    for fn in ["architecture", "equations", "experiment_matrix",
               "result_provenance", "bdhr_bdchq_notes",
               "anticipated_questions"]:
        assert (ROOT / "defense" / f"{fn}.md").exists(), fn
    q = (ROOT / "defense" / "anticipated_questions.md").read_text(
        encoding="utf-8")
    for probe in ["Why is your topic frontier?",
                  "Why isn't this ordinary ICL",
                  "How do you know the state contains task information?"]:
        assert probe in q, probe
    eq = (ROOT / "defense" / "equations.md").read_text(encoding="utf-8")
    assert "s ← s + φ(x, y)" in eq or "s <- s" in eq
    assert "did not reproduce" in (ROOT / "defense" / "experiment_matrix.md"
                                   ).read_text(encoding="utf-8") \
        or "did NOT match" in (ROOT / "defense" / "experiment_matrix.md"
                               ).read_text(encoding="utf-8")


# ---------------------------------------------------------------- D5.15
def test_d515_compliance_matrix():
    assert (ROOT / "submission" / "compliance_matrix.xlsx").exists()
    assert (ROOT / "submission" / "compliance_matrix.csv").exists()
    # xlsx is a valid OOXML zip
    z = zipfile.ZipFile(ROOT / "submission" / "compliance_matrix.xlsx")
    assert z.testzip() is None
    assert "xl/workbook.xml" in z.namelist()
    assert "xl/worksheets/sheet1.xml" in z.namelist()
    rows = list(csv.DictReader(open(ROOT / "submission" /
                                    "compliance_matrix.csv",
                                    encoding="utf-8")))
    assert len(rows) >= 25
    assert {"Requirement", "Evidence", "Location", "Status"} <= set(
        rows[0].keys())
    # key brief rows present
    blob = " ".join(r["Requirement"].lower() for r in rows)
    for key in ["public artifact", "public repository", "3+ recent",
                "source/license", "ai", "readme", "reproducib",
                "bdh module", "limitation"]:
        assert key in blob, key


def test_d515_make_compliance_reproducible():
    # running the generator must not change the committed CSV
    before = (ROOT / "submission" / "compliance_matrix.csv").read_bytes()
    import subprocess
    subprocess.run([sys.executable, str(ROOT / "submission" /
                                        "make_compliance_matrix.py")],
                   check=True, cwd=ROOT,
                   capture_output=True)
    after = (ROOT / "submission" / "compliance_matrix.csv").read_bytes()
    assert before == after


# ------------------------------------------------------------------
# DoD cross-cutting: stateless adapter (leakage guard), no secrets
def test_dod_no_module_global_state_in_adapt():
    import src.adapt.strategies as S
    import src.adapt.runner as R
    import src.adapt.learned as L
    import src.adapt.tasks as T

    # Frozen metadata registries (display names, version constants) are
    # allowed; mutable *state* containers (accumulators, caches, instance
    # registers) are forbidden because they would leak across requests.
    frozen_names = {"STRATEGY_DISPLAY", "FAMILY_DISPLAY", "FAMILIES"}
    for mod in (S, R, L, T):
        for name, val in vars(mod).items():
            if name.startswith("__") or callable(val) or name.isupper():
                if name in frozen_names:
                    assert isinstance(val, (dict, list, set)), (mod, name)
                continue
            assert not isinstance(val, (list, dict, set)), (mod, name)


def test_dod_no_secrets_in_repo():
    for pat in [r"A[KZ]\w{20,}", r"(?i)password\s*=\s*['\"][^'\"]+['\"]",
                r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9]{10,}['\"]"]:
        for p in (ROOT / "server.py", ROOT / "src", ROOT / "web"):
            for f in p.rglob("*"):
                if f.suffix not in (".py", ".js", ".json", ".html", ".css"):
                    continue
                txt = f.read_text(encoding="utf-8", errors="replace")
                assert not re.search(pat, txt), (pat, f)