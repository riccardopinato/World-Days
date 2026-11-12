#!/usr/bin/env python3
"""Wave18: 51 individual source-linked EN/IT origin histories, without false human signoff.

This automated test checks structure, unique canonical identifiers, chronology
guards, and editorial completeness. It does NOT certify every historical claim,
qualified professional review, or native translations in six languages.
"""
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data/editorial/batches/origin_stories_wave18_20261112.json"
CATALOG = ROOT / "assets/data/official_core.json"
BOOK = ROOT / "docs/WORLD_DAYS_ORIGIN_WAVE18_51_STORIES_IT_EN_20261112.md"
AUDIT = ROOT / "docs/WORLD_DAYS_ORIGIN_WAVE18_SOURCE_AUDIT_20261112.md"
d = json.loads(WAVE.read_text(encoding="utf-8"))
catalog = {r["id"]: r for r in json.loads(CATALOG.read_text(encoding="utf-8"))["records"]}
book = BOOK.read_text(encoding="utf-8")
audit = AUDIT.read_text(encoding="utf-8")
assert d["schemaVersion"] == 1
assert d["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert d["reviewedOn"] == "2026-11-12"
assert d["count"] == len(d["records"]) == 51
assert len({r["observanceId"] for r in d["records"]}) == 51
assert book.count("\n## ") == 51
assert "ES/FR/DE/PT" in book
assert "non" in audit.lower()
previous = set()
for p in [ROOT / "data/editorial/batches/origin_stories_primary_20261111.json",
          *sorted((ROOT / "data/editorial/batches").glob("origin_stories_wave*.json"))]:
    if p == WAVE:
        continue
    previous.update(r["observanceId"] for r in json.loads(p.read_text(encoding="utf-8"))["records"])
assert not ({r["observanceId"] for r in d["records"]} & previous), "Duplicate already committed original histories"

for rec in d["records"]:
    oid = rec["observanceId"]
    assert oid in catalog, oid
    original = catalog[oid]
    assert original["scope"] == "GLOBAL", oid
    assert any(x["kind"] == "FIXED_DATE" for x in original["recurrenceRules"]), oid
    assert isinstance(rec["introducedYear"], int) and 1900 <= rec["introducedYear"] <= 2026 or rec["introducedYear"] is None
    if original.get("introducedYear") is not None:
        assert rec["introducedYear"] == original["introducedYear"], (oid, "canonical introduced year")
    if rec["firstObservedYear"] is not None:
        assert 1900 <= rec["firstObservedYear"] <= 2027
    assert len(rec["sources"]) >= 2
    assert len(set(rec["sources"])) == len(rec["sources"])
    assert all(
        urlsplit(u).scheme == "https" and urlsplit(u).hostname and
        not any(ch.isspace() for ch in u) for u in rec["sources"]
    ), oid
    assert any(urlsplit(u).hostname.endswith((
        "un.org", "unesco.org", "who.int", "fao.org", "icao.int",
        "opcw.org", "mfa", "wto.org"
    )) for u in rec["sources"]), oid
    assert set(rec["locale"]) == {"en", "it"}, "No invented six-language approvals"
    assert len(rec["sourceReviewNote"].strip()) >= 160, (oid, "research boundary")
    assert oid in book
    for lang in ("en", "it"):
        o = rec["locale"][lang]
        assert set(o) == {"heading", "origin", "promoter", "purpose", "facts"}
        assert len(o["heading"].strip()) >= 19, (oid, lang, "heading")
        assert len(o["origin"].strip()) >= 300, (oid, lang, "origin")
        assert len(o["promoter"].strip()) >= 68, (oid, lang, "promoter")
        assert len(o["purpose"].strip()) >= 70, (oid, lang, "purpose")
        assert len(o["facts"]) == 3
        assert all(len(f.strip()) >= 35 for f in o["facts"]), (oid, lang, "facts")
        assert o["origin"] in book, (oid, lang, "booklet")
        for s in (o["heading"], o["origin"], o["promoter"], o["purpose"], *o["facts"]):
            assert not re.search(r"\\b(?:undefined|todo)\\b|<placeholder>", s, re.I), (oid, lang)

by_id = {r["observanceId"]: r for r in d["records"]}
assert by_id["world-prematurity-day"]["introducedYear"] == 2025
assert "15 novembre" in by_id["world-prematurity-day"]["locale"]["it"]["origin"]
assert by_id["international-day-for-the-elimination-of-child-early-and-forced-marriage"]["introducedYear"] == 2026
assert by_id["international-day-for-the-elimination-of-child-early-and-forced-marriage"]["firstObservedYear"] is None
assert by_id["international-day-of-recognition-for-women-searchers-of-missing-persons"]["firstObservedYear"] is None
assert by_id["international-day-for-the-abolition-of-slavery"]["introducedYear"] is None
assert by_id["day-of-remembrance-for-all-victims-of-chemical-warfare"]["firstObservedYear"] is None
assert by_id["world-soil-day"]["firstObservedYear"] == 2014
assert by_id["international-civil-aviation-day"]["firstObservedYear"] == 1994
# First-event evidence must not be replaced by the first anniversary in the next year.
migrants = by_id["international-migrants-day"]
assert migrants["introducedYear"] == migrants["firstObservedYear"] == 2000
assert "www.ilo.org/resource/news/ilo-joins-celebration-united-nations-international-migrants-day" in migrants["sources"]
assert "18 dicembre 2000" in migrants["locale"]["it"]["origin"]

epidemic = by_id["international-day-of-epidemic-preparedness"]
assert epidemic["introducedYear"] == epidemic["firstObservedYear"] == 2020
assert "www.un.org/sg/en/content/sg/statements/2020-12-27/secretary-generals-message-the-international-day-of-epidemic-preparedness-scroll-down-for-french-version" in epidemic["sources"]
assert "Louis Pasteur" in epidemic["locale"]["en"]["origin"]

violence = by_id["international-day-for-the-elimination-of-violence-against-women"]
assert violence["introducedYear"] == 1999
assert violence["firstObservedYear"] == 1981  # earlier independent Latin American commemoration
assert "17 December 1999" in violence["locale"]["en"]["origin"]
assert "17 dicembre 1999" in violence["locale"]["it"]["origin"]
assert "digitallibrary.un.org/record/404761" in violence["sources"]
print("PASS: 51 source-bound original EN/IT histories, 102 narrative locales, qualified review pending")
