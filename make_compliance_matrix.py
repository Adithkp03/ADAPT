"""D5.15 — generate submission/compliance_matrix.{xlsx,csv}.

Zero-dependency: writes a minimal, valid .xlsx (Excel 2010+) directly
from the workbook rows below, plus a .csv twin for quick inspection.
The rows mirror the requirements listed in phase5.md (pages 12-14 of the
Pathway brief) plus the Phase 5 Definition of Done items.

Usage: python submission/make_compliance_matrix.py
"""
import csv
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT_XLSX = ROOT / "compliance_matrix.xlsx"
OUT_CSV = ROOT / "compliance_matrix.csv"

HEADER = ["Requirement", "Evidence", "Location", "Status"]

# Status codes: DONE / PARTIAL / TODO-DEPLOY (deploy-time, requires public URL)
ROWS = [
    ("Public artifact opens without authentication", "release checklist T1-T2",
     "submission/artifact_url.txt (public URL live)", "DONE"),
    ("First visible thing is the live experiment (no marketing landing)",
     "web/index.html stage-flagship first; D5.1 gate",
     "public artifact + README", "DONE"),
    ("Preset experiment already running (no blank canvas / no long loading)",
     "web/app.js preload + /api/episode", "web/", "DONE"),
    ("Meaningful interaction (predict -> run -> truth -> change -> consequence)",
     "9-stage journey + /api/* endpoints", "web/, tests/test_server.py", "DONE"),
    ("Fast feedback (< ~60s full loop)",
     "docs/performance_report.md (D5.5: 2-84ms server-side)",
     "results, perf probe", "DONE"),
    ("Failure handling distinguishes system vs model failure",
     "web/app.js 'Experiment unavailable' + retry", "web/app.js", "DONE"),
    ("Public repository", "git remote", "submission/repository_url.txt (public)", "DONE"),
    ("README (technical-paper-style with required sections)",
     "README.md (+ Ai disclosure, sources, licenses, credits)", "README.md", "DONE"),
    ("3+ recent primary papers cited beside claims",
     "research/literature/evidence_matrix.csv, docs/sources.md", "research/", "DONE"),
    ("Source/license record",
     "provenance/{code,data,models,assets,fonts,third_party}.csv",
     "provenance/, docs/licenses.md", "DONE"),
    ("AI assistance disclosure",
     "docs/ai_disclosure.md + docs/ai_assistance.md", "docs/", "DONE"),
    ("Setup instructions",
     "README Installation + repro/README.md + docs/deployment.md", "repo", "DONE"),
    ("Reproducibility package",
     "repro/ (environment.yml, requirements.txt, run_all.sh, configs, seeds, data, expected_outputs)",
     "repro/", "DONE"),
    ("Result hashes / reproducibility identifiers",
     "repro/expected_outputs/manifest.csv + results/final_manifest.csv", "repro/, results/", "DONE"),
    ("Concept summary (500-950 words)",
     "concept_summary.md (773 words prose)", "repo root -> PDF at deploy", "DONE"),
    ("Blog PDF", "submission/blog.pdf", "submission/", "DONE"),
    ("Learning-effectiveness instrument implemented",
     "evaluation/learning_evaluation_report.md; scripts/analyze_sessions.py",
     "evaluation/, scripts/", "DONE"),
    ("Learner study (8-15 participants) — n=10 recruited; 9 complete pre/post; 8 transfer",
     "evaluation/learning_evaluation_report.md + evaluation/anon-*.json + evaluation/analysis/*",
     "evaluation/", "DONE"),
    ("BDH module (substantive, not bolted on)",
     "9-stage journey BDH section + stepper/synapse card; D5.1 gate",
     "web/, research/bdh/", "DONE"),
    ("BDH integration: official vs independent distinguished",
     "dossiers + reproductions R1/R2; evidence_ledger.csv", "research/bdh/", "DONE"),
    ("BDH-CQ integration correct, scope-guarded",
     "bdhcq_technical_dossier.md + UI scope guard + R2", "research/bdh/, web/", "DONE"),
    ("Limitation module (stress lab)",
     "interference + intervention stages (E5/E8), docs/scientific_limitations.md",
     "public artifact", "DONE"),
    ("Every major claim audited",
     "audit/scientific_claim_audit.csv (C01-C20 rows)", "audit/", "DONE"),
    ("Every result traceable to an experiment",
     "provenance envelope + repro manifest + results/*/results.json", "research/experiments/", "DONE"),
    ("No accidental state leakage",
     "docs/security_review.md + test_phase5 isolation scan", "server.py, src/adapt/", "DONE"),
    ("Resource bounds enforced",
     "server.py::_resolve_kw (steps<=64, state_dim<=64, lr<=5) + test_phase5", "server.py", "DONE"),
    ("Accessible & mobile",
     "docs/accessibility_audit.md (D5.7) + release checklist T6", "web/, docs/", "DONE"),
    ("No fake/animated results; Illustrative labels present",
     "D5.2 audit; badges taxonomy; BDH card label", "web/, audit/", "DONE"),
    ("Final compliance matrix", "submission/compliance_matrix.xlsx + .csv", "submission/", "DONE"),
]

STATUS_KEY = {
    "DONE": "done",
    "TODO-DEPLOY": "at deployment",
    "PARTIAL": "pending participants",
}


def _esc(v):
    return (str(v).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


if __name__ == "__main__":
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(list(HEADER) + ["Note"])
        for r in ROWS:
            w.writerow(list(r) + [STATUS_KEY[r[3]]])

    sheet = ["<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>",
             "<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">",
             "<sheetData>"]
    for i, row in enumerate([HEADER + ["Note"]] + [list(r) + [STATUS_KEY[r[3]]] for r in ROWS], 1):
        cells = "".join(
            f'<c r="{chr(65 + j)}{i}" t="inlineStr"><is><t xml:space="preserve">{_esc(v)}</t></is></c>'
            for j, v in enumerate(row))
        sheet.append(f'<row r="{i}">{cells}</row>')
    sheet.append("</sheetData></worksheet>")
    sheet_xml = "".join(sheet)

    files = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            "</Types>"),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"'
            ' Target="xl/workbook.xml"/>'
            "</Relationships>"),
        "xl/workbook.xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
            ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="ComplianceMatrix" sheetId="1" r:id="rId1"/></sheets>'
            "</workbook>"),
        "xl/_rels/workbook.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"'
            ' Target="worksheets/sheet1.xml"/>'
            "</Relationships>"),
        "xl/worksheets/sheet1.xml": sheet_xml,
    }
    with zipfile.ZipFile(OUT_XLSX, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    print(f"wrote {OUT_XLSX.name} and {OUT_CSV.name} "
          f"({len(ROWS)} requirement rows)")