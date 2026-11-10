#!/usr/bin/env python3
"""Fail-closed structural QA for institutional index reconciliation research only."""
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/editorial/candidates/institutional_40_source_reconciliation_20261110.json"
batch = json.loads(PATH.read_text(encoding="utf-8"))
assert batch["schemaVersion"] == 1
assert batch["scope"] == "RESEARCH_CANDIDATES_ONLY_NOT_RUNTIME"
rows = batch["records"]
assert len(rows) == 40
assert len({r["candidateId"] for r in rows}) == 40
assert len({r["canonicalTitleEn"].casefold() for r in rows}) == 40
expected = {"UN": 10, "UNESCO": 11, "WHO": 15, "FAO": 4}
assert {a: sum(r["sourceInstitution"] == a for r in rows) for a in expected} == expected
hosts = {
    "UN": "www.un.org",
    "UNESCO": "www.unesco.org",
    "WHO": "www.who.int",
    "FAO": "www.fao.org",
}
for row in rows:
    assert row["sourceInstitution"] in hosts
    parsed = urlparse(row["officialIndexUrl"])
    assert parsed.scheme == "https" and parsed.hostname == hosts[row["sourceInstitution"]]
    assert parsed.path and parsed.path != "/"
    date(2028, row["month"], row["day"])
    assert row["evidenceStatus"] == "OFFICIAL_INDEX_MATCHED_ENTRY_UNREVIEWED"
    assert row["editorialStatus"] == "NOT_REVIEWED"
    assert row["establishedYear"] is None
    assert row["action"] in {"RECONCILE_EXISTING", "CHECK_CANONICAL_ID_AND_IMPORT"}
    assert row["action"] == ("RECONCILE_EXISTING" if row["foundInCurrentGeneratorByTitle"] else "CHECK_CANONICAL_ID_AND_IMPORT")
exception = batch["knownDatePolicyExceptions"]
assert len(exception) == 1
assert exception[0]["candidateId"] == "world-prematurity-day"
assert exception[0]["effectiveFromYear"] == 2026
assert exception[0]["annualDateFrom2026"] == "11-15"
assert exception[0]["historicalDate"] == "11-17"
print("PASS: 40 index-backed candidates / research-only / 4 institutions / date-transition exception")
