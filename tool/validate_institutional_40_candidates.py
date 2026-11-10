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
statuses = {"EXISTING_EXACT_TITLE": 32, "EXISTING_ALIAS": 1, "NEW_CANONICAL_CANDIDATE": 7}
assert {s: sum(row["reconciliation"]["status"] == s for row in rows) for s in statuses} == statuses
assert batch["reconciliationSummary"]["exactExisting"] == 32
assert batch["reconciliationSummary"]["aliasExisting"] == 1
assert batch["reconciliationSummary"]["newCanonicalCandidates"] == 7
assert sum("proposedIntroducedYear" in row for row in rows) == 4
for row in rows:
    status = row["reconciliation"]["status"]
    assert status in statuses
    assert row["reconciliation"]["checkedAgainst"].startswith("tool/build_dataset.py@")
    if status == "NEW_CANONICAL_CANDIDATE":
        assert row["reconciliation"]["canonicalId"] is None
    else:
        assert row["reconciliation"]["canonicalId"]
        assert row["reconciliation"]["canonicalTitleEn"]
    if "proposedIntroducedYear" in row:
        assert row["proposedIntroducedYear"] <= 2026
        assert row["introducedYearSource"] == row["observanceSourceUrl"]
assert next(row for row in rows if row["candidateId"] == "world-tb-day")["reconciliation"]["status"] == "EXISTING_ALIAS"
assert next(row for row in rows if row["candidateId"] == "world-prematurity-day")["reconciliation"]["dateStatus"] == "2026_11_15_CONFIRMED_WHO"
print("PASS: 40 candidates / 32 exact / 1 alias / 7 new candidates / 4 sourced year proposals / no runtime promotion")
