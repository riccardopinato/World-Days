#!/usr/bin/env python3
"""Verify original institutional evidence and six full locale editions."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data/editorial/batches/un_primary_2026_11_03_03.json"
batch = json.loads(path.read_text(encoding="utf-8"))
assert batch["batchId"] == "UN-PRIMARY-2026-11-03-03"
assert batch["datasetVersion"] == "2026.11.03.4"
assert batch["reviewedAt"] == "2026-11-03"
rows = batch["entries"]
assert len(rows) == 15, len(rows)
ids = [row["id"] for row in rows]
assert len(ids) == len(set(ids)), "duplicate sources"
locales = {"en", "it", "es", "fr", "de", "pt"}
hosts = {"www.un.org", "un.org", "www.unesco.org", "www.irena.org"}
milestones = {
    "international-day-of-commemoration-in-memory-of-the-victims-of-the-holocaust": ("1945","2005"),
    "international-day-of-clean-energy": ("2009","2023"),
    "world-radio-day": ("1946","2011","2012"),
    "international-day-of-forests": ("2012","2013"),
    "international-day-for-the-elimination-of-racial-discrimination": ("1960","1966"),
    "world-down-syndrome-day": ("2011","2012"),
    "international-day-of-zero-waste": ("2022","2023"),
    "international-day-of-sport-for-development-and-peace": ("1896","2013"),
    "world-press-freedom-day": ("1991","1993"),
    "world-bee-day": ("1734","2017"),
}
for row in rows:
    oid = row["id"]
    source = urlsplit(row["source"])
    assert source.scheme == "https" and source.hostname in hosts, (oid, "source_host")
    assert source.path.strip("/") and not source.username, (oid, "source")
    year = row["year"]
    assert isinstance(year, int) and 1900 <= year <= 2026, (oid,"year")
    assert set(row["translations"]) == locales, (oid, "locale_parity")
    english = row["translations"]["en"]
    curated = english.get("relatedObservanceIds", [])
    assert len(curated) == len(set(curated)), (oid, "related_duplicates")
    for locale, prose in row["translations"].items():
        assert len(prose["hook"].strip()) >= 20, (oid, locale, "hook")
        assert len(prose["summary"].strip()) >= 90, (oid, locale, "summary")
        assert len(prose["origin"].strip()) >= 170, (oid, locale, "origin")
        assert len(prose["whyThisDate"].strip()) >= 55, (oid, locale, "why_date")
        assert len(prose["whyItMatters"].strip()) >= 100, (oid, locale, "why")
        actions = prose["waysToTakePart"]
        assert len(actions) == 2 and all(len(s.strip()) >= 30 for s in actions), (oid, locale, "actions")
        assert str(year) in prose["origin"], (oid, locale, "founding_year")
        assert "https://" not in str(prose), (oid, locale, "url_inside_text")
        if locale != "en":
            assert prose["summary"] != english["summary"], (oid, locale, "untranslated")
            assert prose["origin"] != english["origin"], (oid, locale, "untranslated_origin")
        for m in milestones.get(oid, ()):
            assert m in prose["origin"], (oid, locale, "missing_milestone", m)

print(f"wave03 ok: {len(rows)} original stories x six locales; {len(rows)} source-backed years")
