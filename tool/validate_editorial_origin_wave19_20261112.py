#!/usr/bin/env python3
"""Wave19 exact-ID, first-observance, original primary-source and archive-completion gate.

Source-linked model-authored IT/EN histories are NOT human-certified six-locale
Rich Editorial, and the historical first-100 source-index archive remains separate.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/editorial/batches"
DATA = BASE / "origin_stories_wave19_20261112.json"
BOOK = ROOT / "docs/WORLD_DAYS_ORIGIN_WAVE19_07_STORIES_IT_EN_20261112.md"
AUDIT = ROOT / "docs/WORLD_DAYS_ORIGIN_WAVE19_SOURCE_AUDIT_20261112.md"
CATALOG = ROOT / "assets/data/official_core.json"
DRAFTS = ROOT / "data/editorial/candidates/origin_100_original_bilingual_drafts_20261112.json"

data = json.loads(DATA.read_text(encoding="utf-8"))
book = BOOK.read_text(encoding="utf-8")
audit = AUDIT.read_text(encoding="utf-8")
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
catalog_by_id = {r["id"]: r for r in catalog["records"]}
archive = json.loads(DRAFTS.read_text(encoding="utf-8"))
expected = {
    "international-day-of-solidarity-with-detained-and-missing-staff-members": (None, 1986),
    "international-wellness-day": (2026, 2026),
    "international-day-of-greening-the-planet": (2026, None),
    "international-day-in-memory-of-the-victims-of-earthquakes": (2025, 2026),
    "time-of-remembrance-and-reconciliation-for-those-who-lost-their-lives-during-the-second-world-war": (2004, 2005),
    "world-oceans-day": (2008, 2009),
    "international-day-of-the-tropics": (2016, None),
}
assert data["schemaVersion"] == 1
assert data["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert data["reviewedOn"] == "2026-11-12"
assert len(data["records"]) == data["count"] == len(expected) == 7
ids = [x["observanceId"] for x in data["records"]]
assert len(ids) == len(set(ids)) == 7
assert set(ids) == set(expected)
assert book.count("\n## ") == 7
assert "qualified human" in book.lower()
assert "A/RES/70/267" in audit
assert len(catalog_by_id) == len(catalog["records"]) >= 1111
for item in data["records"]:
    oid = item["observanceId"]
    original = catalog_by_id[oid]
    assert item["introducedYear"] == expected[oid][0], oid
    assert item["firstObservedYear"] == expected[oid][1], oid
    if original.get("introducedYear") is not None:
        assert original["introducedYear"] == item["introducedYear"], oid
    assert len(item["sources"]) >= 2 and len(item["sources"]) == len(set(item["sources"])), oid
    assert all(urlsplit(url).scheme == "https" and urlsplit(url).hostname for url in item["sources"]), oid
    assert any(urlsplit(url).hostname.endswith(("un.org", "unesco.org")) for url in item["sources"]), oid
    assert len(item["sourceReviewNote"]) >= 155, oid
    assert {"it", "en"} <= set(item["locale"]) <= {"en", "it", "es", "fr", "de", "pt"}
    assert oid in book
    for lang in ("en", "it"):
        body = item["locale"][lang]
        assert set(body) == {"heading", "origin", "promoter", "purpose", "facts"}, (oid, lang)
        for key in ("heading", "origin", "promoter", "purpose"):
            assert len(body[key].strip()) >= (18 if key == "heading" else 65), (oid, lang, key)
        assert 2 <= len(body["facts"]) <= 5, (oid, lang)
        assert all(len(s) >= 30 for s in body["facts"]), (oid, lang, "facts")
        assert body["origin"] in book, (oid, lang)
        assert all(src in book for src in item["sources"]), oid

assert catalog_by_id["international-day-of-the-tropics"]["authority"]["resolution"] == "A/RES/70/267"
assert catalog_by_id["micro-small-and-medium-sized-enterprises-day"]["authority"]["resolution"] == "A/RES/71/279"
assert "A/RES/70/267" in next(r for r in data["records"] if r["observanceId"] == "international-day-of-the-tropics")["locale"]["en"]["origin"]
assert next(r for r in data["records"] if r["observanceId"] == "international-day-of-solidarity-with-detained-and-missing-staff-members")["introducedYear"] is None
assert archive["count"] == len(archive["drafts"]) == 100
assert next(r for r in archive["drafts"] if r["observanceId"] == "international-day-of-the-tropics")["resolutionOrDecision"] == "A/RES/70/267"

already = {}
for path in [BASE / "origin_stories_primary_20261111.json", *sorted(BASE.glob("origin_stories_wave*.json"))]:
    batch = json.loads(path.read_text(encoding="utf-8"))
    for rec in batch["records"]:
        oid = rec["observanceId"]
        assert oid not in already, ("duplicated source-research ID", oid, path.name)
        already[oid] = path.name
original_100 = {r["observanceId"] for r in archive["drafts"]}
assert len(original_100) == 100
assert original_100 <= set(already), ("unpromoted original-100 archive", sorted(original_100 - set(already)))
assert len(already) >= 225
print("PASS Wave19: 7 new individually sourced research histories, original 100 drafts each have source-backed successor; no six-locale human approval")
