#!/usr/bin/env python3
"""Fail-closed structural gate for DFAT Wave12 discovery (NOT admission approval).

DFAT is an Australian diplomatic protocol index, not independent evidence of
each foreign state's legal holiday or the date's recurrence in future years.
"""
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/market/wave12_diplomatic_158_countries_20261111.json"
LOCALES = {"en", "it", "es", "fr", "de", "pt"}
DFAT = "https://protocol.dfat.gov.au/Public/NationalDays"


def validate():
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = payload["records"]
    # The historical filename says 158, but the payload itself currently says 156.
    # Never silently infer the admitted count from a filename.
    assert payload["count"] == payload["countryCount"] == len(rows) == 156
    assert payload["source"] == DFAT
    assert payload["sourceStatus"] == "DFAT_INDEX_TRANSCRIPTION_REQUIRES_ITEM_SOURCE_AUDIT"
    assert payload["editorialStatus"] == "STUB"
    ids = [row["id"] for row in rows]
    countries = [row["country"] for row in rows]
    assert len(set(ids)) == len(ids), "duplicate canonical candidate ID"
    assert len(set(countries)) == len(countries), "repeated country; inspect semantic identity"
    assert len(payload["countries"]) == len(set(countries))
    assert {country["code"] for country in payload["countries"]} == set(countries)
    for row in rows:
        assert row["source"] == DFAT and row["sourceTier"] == "A_PRIMARY"
        assert row["country"] in countries
        assert row["scope"] == "NATIONAL"
        assert row["holidayClassification"] == "AUSTRALIAN_DIPLOMATIC_PROTOCOL_NATIONAL_DAY_NOT_INDEPENDENTLY_VERIFIED_STATUTORY_HOLIDAY"
        assert row["humanEditorialStatus"] == "SOURCE_INDEX_ONLY_LONG_FORM_NOT_REVIEWED"
        assert row["titleTranslationStatus"] == "EN_FALLBACK_NOT_NATIVE_TRANSLATION"
        assert row["proposedIntroducedYear"] is None and row["introducedYearSource"] is None
        assert set(row["localizedTitles"]) == LOCALES
        assert all(row["localizedTitles"][locale] == row["canonicalTitleEn"] for locale in LOCALES)
        assert len(row["recurrenceRules"]) == 1
        rule = row["recurrenceRules"][0]
        assert rule["kind"] == "FIXED_DATE"
        for year in (2026, 2027, 2028):
            date(year, rule["month"], rule["day"])
    print("PASS: 156 DFAT research candidates structurally valid; 0 independently admitted")
    print("BLOCKED: per-country originator/date/annual-recurrence and semantic-dedup reviews outstanding")


if __name__ == "__main__":
    validate()
