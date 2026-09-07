"""D5.3 — verify regenerated results/figures match the pinned reference hashes.

Usage:
    python repro/check_expected.py             (all rows)
    python repro/check_expected.py results      (results.json only)
    python repro/check_expected.py figures      (figures only)

Exit code 0 if every present file matches; 1 otherwise. Files that are
absent are reported (they should be regenerated). A mismatch means the
regeneration is NOT byte-identical to the reference commit.
"""
import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = Path(__file__).resolve().parent / "expected_outputs" / "manifest.csv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    scopes = set(sys.argv[1:]) or {"results", "figures"}
    rows = list(csv.DictReader(open(MANIFEST, encoding="utf-8")))
    bad = missing = 0
    for r in rows:
        kind = r["kind"]
        if kind not in scopes:
            continue
        rel = r["path"]
        path = ROOT / rel
        label = f"{rel}"
        if not path.exists():
            print(f"  MISSING: {label}")
            missing += 1
            continue
        want, got = r["sha256"], sha256(path)
        ok = want == got
        print(f"  {'OK ' if ok else 'DIFF'} {label}")
        if not ok:
            print(f"       want {want[:16]}... got {got[:16]}...")
            bad += 1
    print(f"\n{len(rows) - bad - missing} files verified, "
          f"{bad} differ, {missing} missing")
    return 1 if (bad or missing) else 0


if __name__ == "__main__":
    sys.exit(main())