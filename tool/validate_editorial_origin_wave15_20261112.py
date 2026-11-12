#!/usr/bin/env python3
"""Validate Wave15 bulk origin histories without conflating draft research with human review.

Structural/source-integrity gate; an automated PASS cannot certify source factual
truth or qualified native-linguistic approval.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data/editorial/batches/origin_stories_wave15_20261112.json"
DRAFTS = ROOT / "data/editorial/candidates/origin_100_original_bilingual_drafts_20261112.json"
CATALOG = ROOT / "assets/data/official_core.json"
wave = json.loads(WAVE.read_text(encoding="utf-8"))
drafts = json.loads(DRAFTS.read_text(encoding="utf-8"))["drafts"]
canonical = {r["id"]: r for r in json.loads(CATALOG.read_text(encoding="utf-8"))["records"]}
by_id = {r["observanceId"]: r for r in drafts}
expected_positions = set(range(41, 75)) - {55, 72}

assert wave["schemaVersion"] == 1
assert wave["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert wave["count"] == len(wave["records"]) == len(expected_positions) == 32
assert wave["reviewedOn"] == "2026-11-12"
assert len({r["observanceId"] for r in wave["records"]}) == 32
assert {by_id[r["observanceId"]]["sequence"] for r in wave["records"]} == expected_positions
assert all(d["publishedToApp"] is False for d in drafts)
assert not any(r["observanceId"] == "world-oceans-day" for r in wave["records"])
assert not any(r["observanceId"] == "international-day-of-the-tropics" for r in wave["records"])

# The UN contemporaneous report identifies 19 June 2016 as inaugural,
# distinct from the adoption of A/RES/69/293 on 19 June 2015.
sexual_violence = next(r for r in wave["records"] if r["observanceId"] == "international-day-for-the-elimination-of-sexual-violence-in-conflict")
assert sexual_violence["introducedYear"] == 2015
assert sexual_violence["firstObservedYear"] == 2016
assert "childrenandarmedconflict.un.org/en/on-world-day-ban-declares-era-of-impunity-over-for-sexual-violence-in-war" in "\\n".join(sexual_violence["sources"])

for rec in wave["records"]:
    oid = rec["observanceId"]
    draft = by_id[oid]
    source = canonical[oid]
    assert draft["resolutionOrDecision"] == source["authority"]["resolution"], oid
    assert draft["date"] and draft["observanceId"] == oid
    if source.get("introducedYear") is not None:
        assert rec["introducedYear"] == source["introducedYear"], (oid, "year mismatch")
    assert rec["introducedYear"] is None or 1800 <= rec["introducedYear"] <= 2026
    if rec["firstObservedYear"] is not None:
        assert rec["firstObservedYear"] >= 1800
        # Pre-UN celebrations (e.g., elder-abuse awareness, metrology) are valid.
    assert len(rec["sources"]) >= 2
    assert len(set(rec["sources"])) == len(rec["sources"])
    assert all(urlsplit(u).scheme == "https" and urlsplit(u).hostname for u in rec["sources"])
    assert any(
        urlsplit(u).hostname.endswith((
            "un.org", "unesco.org", "bipm.org", "fao.org",
        )) for u in rec["sources"]
    ), oid
    assert set(rec["locale"]) == {"en", "it"}, "No fraudulent six-locale REVIEWED status"
    assert len(rec["sourceReviewNote"]) >= 140
    for lang in ("en", "it"):
        item = rec["locale"][lang]
        assert set(item) == {"heading", "origin", "promoter", "purpose", "facts"}
        assert len(item["heading"].strip()) >= 19, (oid, lang, "heading")
        assert len(item["origin"].strip()) >= 320, (oid, lang, "origin")
        assert len(item["promoter"].strip()) >= 70, (oid, lang, "promoter")
        assert len(item["purpose"].strip()) >= 70, (oid, lang, "purpose")
        assert len(item["facts"]) == 3, (oid, lang, "facts")
        assert all(len(x.strip()) >= 40 for x in item["facts"])
        for value in (item["heading"], item["origin"], item["promoter"], item["purpose"], *item["facts"]):
            assert not any(x in value.lower() for x in ("undefined", "todo", "<placeholder>")), (oid, lang)
print("PASS: Wave15 32 unique ID-bound IT/EN origin research drafts and language-review boundary; factual approval remains human gate")
