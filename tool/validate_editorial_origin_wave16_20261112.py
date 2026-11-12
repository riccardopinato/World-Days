#!/usr/bin/env python3
"""Wave16: verify 26 unique, ID-matched historical origin research drafts.

This is a structural/provenance and chronology gate, NOT qualified human factual
certification or native-language approval.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data/editorial/batches/origin_stories_wave16_20261112.json"
ARCHIVE = ROOT / "data/editorial/candidates/origin_100_original_bilingual_drafts_20261112.json"
CATALOG = ROOT / "assets/data/official_core.json"
wave = json.loads(WAVE.read_text(encoding="utf-8"))
archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))["drafts"]
catalog = {r["id"]: r for r in json.loads(CATALOG.read_text(encoding="utf-8"))["records"]}
by_id = {r["observanceId"]: r for r in archive}

assert wave["schemaVersion"] == 1
assert wave["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert wave["reviewedOn"] == "2026-11-12"
assert wave["count"] == len(wave["records"]) == 26
assert all(r["publishedToApp"] is False for r in archive)
assert len({r["observanceId"] for r in wave["records"]}) == 26
assert {by_id[r["observanceId"]]["sequence"] for r in wave["records"]} == set(range(75, 101))

for rec in wave["records"]:
    oid = rec["observanceId"]
    baseline = by_id[oid]
    canonical = catalog[oid]
    assert canonical["authority"]["resolution"] == baseline["resolutionOrDecision"], oid
    if canonical.get("introducedYear") is not None:
        assert rec["introducedYear"] == canonical["introducedYear"], (oid, "founding year")
    assert isinstance(rec["introducedYear"], int) and 1900 <= rec["introducedYear"] <= 2026
    if rec["firstObservedYear"] is not None:
        assert 1900 <= rec["firstObservedYear"] <= 2027
    assert len(rec["sources"]) >= 2
    assert len(set(rec["sources"])) == len(rec["sources"])
    assert all(urlsplit(u).scheme == "https" and urlsplit(u).hostname for u in rec["sources"])
    assert any(urlsplit(u).hostname.endswith(("un.org", "unesco.org", "who.int")) for u in rec["sources"])
    assert set(rec["locale"]) == {"en", "it"}, "No invented native six-locale approval"
    assert len(rec["sourceReviewNote"].strip()) >= 140
    for lang in ("en", "it"):
        entry = rec["locale"][lang]
        assert set(entry) == {"heading", "origin", "promoter", "purpose", "facts"}
        assert len(entry["heading"].strip()) >= 19, (oid, lang, "heading")
        assert len(entry["origin"].strip()) >= 320, (oid, lang, "original history")
        assert len(entry["promoter"].strip()) >= 70, (oid, lang, "promoter")
        assert len(entry["purpose"].strip()) >= 75, (oid, lang, "purpose")
        assert len(entry["facts"]) == 3
        assert all(len(f.strip()) >= 45 for f in entry["facts"])
        for text in (entry["heading"], entry["origin"], entry["promoter"],
                     entry["purpose"], *entry["facts"]):
            assert all(t not in text.lower() for t in ("undefined", "todo", "<placeholder>")), oid

record = {r["observanceId"]: r for r in wave["records"]}
assert record["world-kiswahili-language-day"]["introducedYear"] == 2024
assert record["world-kiswahili-language-day"]["firstObservedYear"] == 2022
assert record["international-day-of-friendship"]["firstObservedYear"] == 1958
assert record["international-day-of-safe-secure-and-trustworthy-artificial-intelligence"]["introducedYear"] == 2026
assert record["international-day-of-safe-secure-and-trustworthy-artificial-intelligence"]["firstObservedYear"] == 2027
assert "2027" in record["international-day-of-safe-secure-and-trustworthy-artificial-intelligence"]["locale"]["it"]["origin"]
assert record["international-day-against-nuclear-tests"]["firstObservedYear"] == 2010
print("PASS: 26 ID-bound original bilingual histories with source/year review boundaries; NOT human-certified in six locales")
