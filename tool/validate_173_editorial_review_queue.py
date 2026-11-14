#!/usr/bin/env python3
"""Fail closed on unapproved six-locale research: review queue is NOT approval."""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from editorial_research_handoff import load_handoff

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/editorial/reviews/ph_kr_ca_173_qualified_review_queue_20261114.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
assert d["schemaVersion"] == 1
assert d["role"] == "OPEN_QUALIFIED_REVIEW_QUEUE_NOT_PUBLICATION_APPROVAL"
handoff = load_handoff()
rows = d["records"]
assert len(rows) == 173
assert len({r["id"] for r in rows}) == 173
assert {r["id"] for r in rows} == handoff["six_locale_draft_ids"]
assert Counter(r["country"] for r in rows) == {"PH":84,"KR":57,"CA":32}
assert d["summary"]["qualifiedHistoricallyCertified"] == 0
assert d["summary"]["qualifiedSixLocaleCertified"] == 0
assert d["summary"]["publishedRichFromThisReview"] == 0
assert d["summary"]["firstPartySpotPrechecked"] == 4
assert d["summary"]["firstPartyDiscrepancyHold"] == 1
assert d["summary"]["sourceConflictsInTotalInventory"] == 14
assert d["summary"]["sourceConflictsWithinDrafts"] == 8
expected_locales = {"en","it","es","fr","de","pt"}
sample_ids = {"ph-independence-day", "kr-march-first-independence-movement-day",
              "ca-ribbon-skirt-day", "ph-ninoy-aquino-day"}
sample_count = 0
for r in rows:
    assert set(r["localeCoverage"]) == expected_locales
    assert r["sourcePr"] in (118,119,120)
    assert r["sourceHead"] and len(r["sourceHead"]) == 40
    assert r["sourceFile"].startswith("data/editorial/")
    assert r["originSourceUrls"] and all(
        urlsplit(u).scheme == "https" and urlsplit(u).hostname
        for u in r["originSourceUrls"])
    assert set(r["nativeLinguisticReview"]) == expected_locales
    assert set(r["nativeLinguisticReview"].values()) == {"PENDING"}
    assert r["qualifiedEditorSignoff"] is False
    assert r["richEditorialApproved"] is False
    assert r["reviewerName"] is None and r["reviewerDate"] is None
    if r["unresolvedSourceRisk"]:
        assert r["unresolvedSourceRisk"]["evidence"].startswith("https://")
    if r["id"] in sample_ids:
        sample_count += 1
        assert r["sourcePrecheck"].startswith(("FIRST_PARTY", "FOUR_FIRST_PARTY"))
        assert len(r["reviewSourceUrls"]) >= 2
        assert r["sixLocaleDraftStructuralSpotCheck"]["numberOfFactsPerLocale"] == 3
        assert set(r["sixLocaleDraftStructuralSpotCheck"]["originChars"]) == expected_locales
        assert min(r["sixLocaleDraftStructuralSpotCheck"]["originChars"].values()) >= 300
    else:
        assert r["sourcePrecheck"] == "PENDING"
independence = next(r for r in rows if r["id"] == "ph-independence-day")
assert independence["decision"] == "BLOCK_FIRST_OBSERVANCE_YEAR"
assert independence["historicalChronologyReview"] == "REQUIRES_CORRECTION_AND_SECOND_REVIEW"
assert "proc_28_1962.html" in " ".join(independence["reviewSourceUrls"])
assert sample_count == 4
print("PASS: 173 individual PH/KR/CA drafts in a human-signoff queue, "
      "4 first-party fact prechecks, 1 discovered chronology conflict, "
      "zero qualified approvals or publications.")
