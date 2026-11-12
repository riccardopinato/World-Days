#!/usr/bin/env python3
"""Wave17: check 28 new individually sourced bilingual origin research drafts.

This validates canonical IDs, provenance/chronology structure, uniqueness and
editorial boundaries. It does not assert qualified human research or six native
language approvals.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data/editorial/batches/origin_stories_wave17_20261112.json"
CATALOG = ROOT / "assets/data/official_core.json"
BOOK = ROOT / "docs/WORLD_DAYS_ORIGIN_WAVE17_28_STORIES_IT_EN_20261112.md"
b = json.loads(WAVE.read_text(encoding="utf-8"))
catalog = {r["id"]: r for r in json.loads(CATALOG.read_text(encoding="utf-8"))["records"]}
book = BOOK.read_text(encoding="utf-8")
assert b["schemaVersion"] == 1
assert b["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert b["reviewedOn"] == "2026-11-12"
assert len(b["records"]) == b["count"] == 28
ids = [x["observanceId"] for x in b["records"]]
assert len(set(ids)) == 28
assert set(ids) <= set(catalog)
assert book.count("\n## ") == 28
assert "Non" in book or "non" in book
assert "ES/FR/DE/PT" in book
previous = set()
for path in (ROOT / "data/editorial/batches").glob("origin_stories_*.json"):
    if path.name == WAVE.name:
        continue
    for r in json.loads(path.read_text(encoding="utf-8"))["records"]:
        previous.add(r["observanceId"])
assert not (set(ids) & previous), "No duplicated publication proposals in committed batches"
for rec in b["records"]:
    oid = rec["observanceId"]
    original = catalog[oid]
    assert any(r["kind"] == "FIXED_DATE" for r in original["recurrenceRules"]), oid
    assert original["scope"] == "GLOBAL", oid
    assert isinstance(rec["introducedYear"], int) and 1900 <= rec["introducedYear"] <= 2026
    if original.get("introducedYear") is not None:
        assert rec["introducedYear"] == original["introducedYear"], (oid, "introduced year")
    if rec["firstObservedYear"] is not None:
        assert 1900 <= rec["firstObservedYear"] <= 2027
    assert len(rec["sources"]) >= 2
    assert len(set(rec["sources"])) == len(rec["sources"])
    assert all(urlsplit(u).scheme == "https" and urlsplit(u).hostname for u in rec["sources"])
    assert any(urlsplit(u).hostname.endswith(("un.org", "unesco.org", "who.int", "fao.org", "wto.org")) for u in rec["sources"])
    assert set(rec["locale"]) == {"en", "it"}, "No invented native six-locale review"
    assert len(rec["sourceReviewNote"]) > 135
    assert oid in book
    for lang in ("en", "it"):
        d = rec["locale"][lang]
        assert set(d) == {"heading", "origin", "promoter", "purpose", "facts"}
        assert len(d["heading"].strip()) >= 19, (oid, lang, "heading")
        assert len(d["origin"].strip()) >= 270, (oid, lang, "origin")
        assert len(d["promoter"].strip()) >= 65, (oid, lang, "promoter")
        assert len(d["purpose"].strip()) >= 65, (oid, lang, "purpose")
        assert len(d["facts"]) == 3
        assert all(len(f.strip()) >= 38 for f in d["facts"])
        assert d["origin"] in book, (oid, lang, "book")
        for s in (d["heading"], d["origin"], d["promoter"], d["purpose"], *d["facts"]):
            assert not any(x in s.lower() for x in ("undefined", "todo", "<placeholder>")), (oid, lang, "placeholder")

by_id = {x["observanceId"]: x for x in b["records"]}
assert by_id["united-nations-day-for-south-south-cooperation"]["introducedYear"] == 2003
assert by_id["united-nations-day-for-south-south-cooperation"]["firstObservedYear"] == 2004
assert by_id["international-day-of-the-world-s-indigenous-women-and-girls"]["firstObservedYear"] == 2026
assert by_id["international-day-of-sign-languages"]["firstObservedYear"] == 2018
assert by_id["world-food-day"]["firstObservedYear"] == 1981
assert by_id["international-day-for-universal-access-to-information"]["introducedYear"] == 2019
assert by_id["international-day-for-universal-access-to-information"]["firstObservedYear"] == 2016
print("PASS: 28 new canonical September-October bilingual origin histories; 56 narratives; human and four additional locale reviews pending")
