#!/usr/bin/env python3
"""Fail-closed Wave21 cohort freezer, using the existing canonical queue builder.

Usage: python tool/freeze_editorial_wave21.py --output data/editorial/waves/wave21_cohort.json
Run on up-to-date main. Commit the generated cohort separately; never regenerate
an already committed cohort to silently change its membership.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from editorial_origin_completion_waves import build

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "data/editorial/waves/wave21_cohort.json"

def freeze(output: Path, allow_dirty: bool = False):
    if not allow_dirty:
        subprocess.run(["git", "diff", "--quiet"], cwd=ROOT, check=True)
        subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT, check=True)
        untracked = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True
        ).splitlines()
        if untracked:
            raise SystemExit(f"Untracked files present; clean main before freezing: {untracked[:10]}")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    remote = subprocess.check_output(
        ["git", "ls-remote", "--exit-code", "origin", "refs/heads/main"],
        cwd=ROOT, text=True, timeout=30
    ).split()[0]
    if remote != head:
        raise SystemExit(f"Local main {head} differs from origin/main {remote}; fetch and fast-forward first")
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    if branch != "main":
        raise SystemExit("Freeze must be generated from up-to-date main, not a PR branch")
    index, batches = build()
    if not batches:
        raise SystemExit("No remaining canonical research IDs; do not create an empty wave")
    if "batch_001.json" not in batches:
        raise SystemExit("Canonical queue missing batch_001.json")
    first = batches["batch_001.json"]
    ids = [d["observanceId"] for d in first["dossiers"]]
    if len(ids) != min(100, index["outstandingOriginResearch"]) or len(ids) != len(set(ids)):
        raise SystemExit("Wave21 requires exactly 100 distinct IDs, except the final residual")
    if any(not isinstance(x, str) or not x.strip() for x in ids):
        raise SystemExit("Canonical queue contains empty/non-string observance IDs")
    if first["recordCount"] != len(ids):
        raise SystemExit("Cohort record count mismatch")
    payload = {
        "schemaVersion": 1,
        "wave": 21,
        "frozenFromMainSha": head,
        "catalogVersion": index["datasetVersion"],
        "catalogTotal": index["catalogTotal"],
        "originResearchedAtFreeze": index["individuallyOriginResearched"],
        "remainingAtFreeze": index["outstandingOriginResearch"],
        "cohortIdSha256": hashlib.sha256("\n".join(ids).encode()).hexdigest(),
        "recordCount": len(ids),
        "observanceIds": ids,
        "editorialStatus": "RESEARCH_PENDING_NOT_CERTIFIED",
        "humanFactReview": "PENDING",
        "humanSixLocaleReview": "PENDING",
        "runtimeRichEditorialApproved": False
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output.exists() and output.read_text(encoding="utf-8") != serialized:
        raise SystemExit(f"Existing immutable cohort differs: {output}")
    output.write_text(serialized, encoding="utf-8")
    print(json.dumps({"wave": 21, "count": len(ids), "main": head,
                      "sha256": payload["cohortIdSha256"], "output": str(output)}))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=DEFAULT)
    args = p.parse_args()
    freeze(args.output)
