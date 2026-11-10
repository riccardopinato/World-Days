#!/usr/bin/env python3
"""Regression gate for the seven institutional catalog admissions, source-first, no rich-editorial promotion."""
import json
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "assets/data/official_core.json").read_text(encoding="utf-8"))
occ = json.loads((ROOT / "assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
title_source = json.loads((ROOT / "data/titles/institutional_wave05.json").read_text(encoding="utf-8"))
expected = {
    "international-day-of-women-in-multilateralism": ("2026-01-25", 2021, "UNESCO"),
    "world-engineering-day-for-sustainable-development": ("2026-03-04", 2019, "UNESCO"),
    "international-day-of-mathematics": ("2026-03-14", 2019, "UNESCO"),
    "world-day-of-romani-language": ("2026-11-05", None, "UNESCO"),
    "international-day-against-illicit-trafficking-in-cultural-property": ("2026-11-14", 2019, "UNESCO"),
    "international-day-of-islamic-art": ("2026-11-18", 2019, "UNESCO"),
    "world-hearing-day": ("2026-03-03", None, "WHO"),
}
assert title_source["titleStatus"] == "TRANSLATION_DRAFT_QA_NOT_NATIVE_REVIEWED"
assert catalog["datasetVersion"] == "2026.11.10.1"
records = {r["id"]: r for r in catalog["records"]}
assert len(records) == len(catalog["records"]) == 463
assert set(expected).issubset(records)
assert len({r["id"] for r in catalog["records"] if r["scope"] == "GLOBAL"}) == 289
assert len({r["id"] for r in catalog["records"] if r["scope"] == "NATIONAL"}) == 174
for rid, (day, introduced, typ) in expected.items():
    row = records[rid]
    assert row["scope"] == "GLOBAL" and not row["countries"]
    assert row["authority"]["type"] == typ
    assert row["authority"]["officiality"] == ("OFFICIAL_WHO" if typ == "WHO" else "OFFICIAL_UNESCO")
    assert row["editorialStatus"] == "STUB"  # no fabricated reviewed story
    assert row["introducedYear"] == introduced if introduced is not None else row.get("introducedYear") is None
    assert row.get("introducedYearSource") is None if introduced is None else row["introducedYearSource"] in [s["url"] for s in row["sources"]]
    assert len(row["sources"]) >= 1 and all(s["tier"] == "A_PRIMARY" for s in row["sources"])
    assert all(s["verifiedAt"] == "2026-11-10" for s in row["sources"])
    assert row["lastVerifiedAt"] == "2026-11-10"
    assert set(row["localizedTitles"]) == {"en", "it", "es", "fr", "de", "pt"}
    assert all(row["localizedTitles"][lang].strip() for lang in row["localizedTitles"])
    assert row["recurrenceRules"] == [{"kind": "FIXED_DATE", "month": int(day[5:7]), "day": int(day[8:])}]
    days = [o["startDate"] for o in occ["occurrences"] if o["observanceId"] == rid]
    assert days == [day], (rid, days)
assert "world-tuberculosis-day" in records and "world-tb-day" not in records
assert "International Ear Care Day" in records["world-hearing-day"]["aliases"]
assert any(o["startDate"] == "2026-11-15" for o in occ["occurrences"] if o["observanceId"] == "world-prematurity-day")
print("PASS: seven unique institutional observances, 5 sourced years, six title locales, 2026 dates, draft editorial gate")
