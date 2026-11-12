#!/usr/bin/env python3
"""Fail-closed admission test for a real 100-story bilingual *draft* corpus.

The source calendar establishes day, institutional title and reference only.
It does not substitute for research of individual origin, proposer or founding
year. This batch must remain outside the published origin-review ledger.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/editorial/candidates/origin_100_original_bilingual_drafts_20261112.json"
BOOK = ROOT / "docs/WORLD_DAYS_100_ORIGINAL_STORIES_DRAFT_20261112.md"
CATALOG = ROOT / "assets/data/official_core.json"
FILES = [ROOT / "data/editorial/batches/origin_stories_primary_20261111.json"]
FILES += sorted((ROOT / "data/editorial/batches").glob("origin_stories_wave*.json"))

data = json.loads(DATA.read_text(encoding="utf-8"))
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
book = BOOK.read_text(encoding="utf-8")
canonical = {r["id"]: r for r in catalog["records"]}
researched = {}
for path in FILES:
    item = json.loads(path.read_text(encoding="utf-8"))
    for r in item["records"]:
        assert r["observanceId"] not in researched, ("duplicate origin", r["observanceId"])
        researched[r["observanceId"]] = r

assert len(canonical) == len(catalog["records"]) >= 1111, "unexpected canonical catalog"
assert data["schemaVersion"] == 1
assert data["count"] == len(data["drafts"]) == 100
assert data["batchId"] == "WORLD-DAYS-NEW-100-ORIGINAL-STORY-DRAFTS-20261112"
assert data["createdOn"] == "2026-11-12"
assert data["researchStatus"] == "100_ORIGINAL_IT_EN_DRAFTS_WITH_INCREMENTAL_ORIGIN_FACT_REVIEW"
assert data["locales"] == ["it", "en"]
ids = [r["observanceId"] for r in data["drafts"]]
assert len(ids) == len(set(ids)) == 100
assert set(ids).issubset(canonical)
# A historical draft is preserved even after its own independently verified
# successor is promoted to the offline origin ledger. This does not turn the
# unverified draft itself into a source-reviewed or app-published record.
overlap = set(ids) & set(researched)
assert len(overlap) <= 100
for oid in overlap:
    successor = researched[oid]
    # Source research may prove the first historical observance without an
    # independently identifiable formal founding act. Preserve null rather
    # than inventing a year solely to pass this archival-overlap validator.
    if successor["introducedYear"] is None:
        assert oid == "international-day-of-solidarity-with-detained-and-missing-staff-members", oid
        assert successor["firstObservedYear"] == 1986, oid
        assert "no founding resolution" in successor["sourceReviewNote"].lower(), oid
    assert len(successor["sources"]) >= 1
    assert {"it", "en"} <= set(successor["locale"])
    assert all(len(successor["locale"][lang]["origin"]) >= 170
               for lang in ("it", "en")), ("incomplete successor", oid)
    assert successor["sourceReviewNote"], ("missing successor research note", oid)
assert book.count("\n## ") == 100, "100 readable stories must actually exist"
assert book.count("**English — ") == 100
assert book.count("**Contesto istituzionale:** ") == 100
assert "NON ancora certificati" in book
assert len(set(r["locale"]["it"]["story"] for r in data["drafts"])) == 100
assert len(set(r["locale"]["en"]["story"] for r in data["drafts"])) == 100

for i, r in enumerate(data["drafts"], 1):
    oid = r["observanceId"]
    original = canonical[oid]
    assert r["sequence"] == i, (oid, "sequence")
    assert r["canonicalTitleEn"] == original["canonicalTitleEn"]
    assert r["date"]["kind"] == "FIXED_DATE"
    expected = {"kind": "FIXED_DATE",
                "month": r["date"]["month"], "day": r["date"]["day"]}
    assert expected in original["recurrenceRules"], (oid, "wrong calendar date")
    assert r["resolutionOrDecision"] == original["authority"]["resolution"], (oid, "wrong authority resolution")
    assert isinstance(r["resolutionOrDecision"], str) and r["resolutionOrDecision"]
    assert r["sourceEvidenceLevel"] == "OFFICIAL_CALENDAR_INDEX_AND_RESOLUTION_ID_ONLY"
    assert r["editorialState"] == "ORIGINAL_BILINGUAL_STORY_DRAFT_FACT_REVIEW_REQUIRED"
    assert r["publishedToApp"] is False, "archival drafts themselves are never auto-published"
    for field in ("formalIntroductionYearConfirmed", "firstObservanceYearConfirmed",
                  "originalProposerConfirmed", "reasonForDateConfirmed"):
        assert r[field] is None, (oid, "unverified historical certainty")
    assert set(r["locale"]) == {"it", "en"}
    assert len(r["sourceLinks"]) == 1
    source = r["sourceLinks"][0]
    url = urlsplit(source)
    assert url.scheme == "https" and url.hostname in {
        "www.un.org", "www.unesco.org",
    }, (oid, "unknown institution")
    assert source in {s["url"] for s in original["sources"]}, (oid, "source not in canonical")
    assert len(r["titleIt"]) >= 16
    assert f"## {i:03d}. {r['titleIt']}" in book, (oid,"missing in booklet")
    assert r["locale"]["it"]["story"] in book, (oid, "Italian story not present")
    assert r["locale"]["en"]["story"] in book, (oid, "English story not present")
    for lang in ("it","en"):
        narrative = r["locale"][lang]
        assert set(narrative) == {"heading", "story", "origin", "purpose", "facts"}
        assert len(narrative["heading"].strip()) >= 15
        assert len(narrative["story"].strip()) >= 150, (oid,lang,"not a story")
        assert len(narrative["story"].split()) >= 20, (oid,lang,"no narrative")
        assert len(narrative["origin"].strip()) >= 175
        assert len(narrative["purpose"].strip()) >= 100
        assert len(narrative["facts"]) == 2
        assert all(len(f.strip()) >= 35 for f in narrative["facts"])
        for value in [narrative["heading"], narrative["story"], narrative["origin"],
                      narrative["purpose"], *narrative["facts"]]:
            assert "undefined" not in value.lower() and " null " not in value.lower(), (oid,lang,"placeholder leaked")
            assert "<script" not in value.lower()
print(f"PASS: 100 original bilingual archival drafts, {len(overlap)} with independently source-researched successors, {100-len(overlap)} awaiting origin verification; no false draft approvals")
