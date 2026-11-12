#!/usr/bin/env python3
"""Wave02: verify eight source-linked IT/EN historical narratives and chronology.

This validates source provenance and editorial schema; it does NOT grant
human-review status to the remaining four translation locales.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
batch = json.loads((ROOT / "data/editorial/batches/origin_stories_wave02_20261112.json").read_text(encoding="utf-8"))
candidates = json.loads((ROOT / "data/editorial/candidates/wave04_sources_20261109.json").read_text(encoding="utf-8"))
wave04 = {r["id"]: r for r in candidates["records"]}
catalog = json.loads((ROOT / "assets/data/official_core.json").read_text(encoding="utf-8"))
canonical = {r["id"]: r for r in catalog["records"]}
expected = {
    "world-wetlands-day": (2021, 1997),
    "international-day-of-light": (2017, 2018),
    "world-bicycle-day": (2018, 2018),
    "international-day-of-yoga": (2014, 2015),
    "world-food-safety-day": (2018, 2019),
    "world-no-tobacco-day": (1987, 1988),
    "world-population-day": (1989, 1990),
    "world-teachers-day": (1994, 1994),
}
assert batch["schemaVersion"] == 1
assert batch["batchId"] == "ORIGIN-WAVE02-UN-UNESCO-WHO-PRIMARY-20261112"
assert batch["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert batch["reviewedOn"] == "2026-11-12"
assert batch["count"] == len(batch["records"]) == len(expected) == 8
assert set(wave04) == set(expected), "Wave04 must be complete; new sources cannot be silently dropped"
assert len({r["observanceId"] for r in batch["records"]}) == 8
for r in batch["records"]:
    oid = r["observanceId"]
    year, first = expected[oid]
    assert r["introducedYear"] == year == wave04[oid]["proposedIntroducedYear"], oid
    assert canonical[oid]["introducedYear"] == year, ("catalog year must be source-surfaced", oid)
    assert canonical[oid]["introducedYearSource"] == wave04[oid]["primarySource"], ("intro provenance", oid)
    assert r["firstObservedYear"] == first, oid
    assert r["firstObservedYear"] >= r["introducedYear"] or oid == "world-wetlands-day", oid
    assert r["sources"] and wave04[oid]["primarySource"] in r["sources"], oid
    assert len(set(r["sources"])) == len(r["sources"])
    for url in r["sources"]:
        parsed = urlsplit(url)
        assert parsed.scheme == "https" and parsed.hostname in {
            "www.un.org", "mandates.un.org", "www.unesco.org", "www.who.int",
            "fctc.who.int", "www.ramsar.org", "www.worldwetlandsday.org",
            "mfa.gov.tm",
        }, (oid, url)
    assert set(r["locale"]) == {"en", "it"}, "no unjustified six-locale reviewed claim"
    assert len(r["sourceReviewNote"]) >= 30
    for lang, entry in r["locale"].items():
        assert len(entry["heading"].strip()) >= 20, (oid, lang, "heading")
        assert len(entry["origin"].strip()) >= 170, (oid, lang, "origin")
        assert len(entry["promoter"].strip()) >= 60, (oid, lang, "promoter")
        assert len(entry["purpose"].strip()) >= 75, (oid, lang, "purpose")
        assert 2 <= len(entry["facts"]) <= 5, (oid, lang, "facts")
        assert all(len(f.strip()) >= 45 for f in entry["facts"]), (oid, lang, "fact")
assert date.fromisoformat(batch["reviewedOn"]) >= date(2026, 11, 11)
print("PASS: 8 new canonical origin histories verified against wave04 source leads and chronology, IT/EN only")
