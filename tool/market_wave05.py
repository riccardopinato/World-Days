"""Source-pinned Japanese Wave05: 3 uniquely named national holidays.

This admits catalog METADATA only, not human-reviewed long-form articles.
Source of truth: Japan Cabinet Office National Holidays Act and explanations.
"""
from calendar import monthrange
from datetime import date, timedelta
import json
from pathlib import Path
from urllib.parse import urlsplit

SOURCE = Path(__file__).resolve().parents[1] / "data/market/wave05_japan_20261109.json"
LOCALES = {"en", "it", "es", "fr", "de", "pt"}
EXPECTED = {
    "japan-coming-of-age-day": {
        "title": "Coming of Age Day — Japan",
        "year": 1948,
        "dates": ["2026-01-12", "2027-01-11", "2028-01-10"],
    },
    "japan-emperors-birthday": {
        "title": "Emperor's Birthday — Japan",
        "year": None,
        "dates": ["2026-02-23", "2027-02-23", "2028-02-23"],
    },
    "japan-showa-day": {
        "title": "Showa Day — Japan",
        "year": 2007,
        "dates": ["2026-04-29", "2027-04-29", "2028-04-29"],
    },
}
SOURCE_URLS = {
    "https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html",
    "https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku.html",
}

def occurrence(rule, year):
    month = rule["month"]
    if rule["kind"] == "FIXED_DATE":
        return date(year, month, rule["day"])
    assert rule["kind"] == "NTH_WEEKDAY"
    first = date(year, month, 1)
    weekday = rule["weekday"] - 1
    day = 1 + (weekday - first.weekday()) % 7 + 7 * (rule["occurrence"] - 1)
    assert day <= monthrange(year, month)[1]
    return date(year, month, day)

def load_wave05_japan():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert data["schemaVersion"] == 1
    assert data["datasetId"] == "world-days-market-wave05-japan-2026-11-09"
    assert data["sourceReviewDate"] == "2026-11-09"
    assert set(data["locales"]) == LOCALES
    assert data["count"] == len(data["records"]) == 3
    assert data["countryCounts"] == {"JP": 3}
    assert data["reviewStatus"] == "SOURCE_VERIFIED_METADATA_ONLY_HUMAN_EDITORIAL_NOT_APPROVED"
    by_id = {x["id"]: x for x in data["records"]}
    assert len(by_id) == 3 and set(by_id) == set(EXPECTED)
    assert len({x["canonicalTitleEn"] for x in by_id.values()}) == 3
    for rid, item in by_id.items():
        expected = EXPECTED[rid]
        assert item["id"] == rid and item["country"] == "JP"
        assert item["canonicalTitleEn"] == expected["title"]
        assert set(item["localizedTitles"]) == LOCALES
        assert item["localizedTitles"]["en"] == item["canonicalTitleEn"]
        assert all(
            isinstance(s, str) and len(s.strip()) >= 8
            for s in item["localizedTitles"].values()
        )
        assert item["authority"] == "Cabinet Office, Government of Japan"
        assert item["authorityType"] == "GOVERNMENT"
        assert item["officiality"] == "OFFICIAL_INSTITUTIONAL"
        assert item["sourceTier"] == "A_PRIMARY"
        assert item["humanEditorialStatus"] == "METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert item["holidayClassification"] == "STATUTORY_NATIONAL_HOLIDAY"
        assert item["sourceReviewedOn"] == data["sourceReviewDate"]
        urls = [item["source"], *item.get("additionalSources", [])]
        assert len(urls) == len(set(urls))
        assert set(urls) == SOURCE_URLS
        for url in urls:
            parts = urlsplit(url)
            assert parts.scheme == "https" and parts.hostname == "www8.cao.go.jp"
        assert item["proposedIntroducedYear"] == expected["year"]
        if expected["year"] is None:
            assert item["introducedYearSource"] is None
        else:
            assert item["introducedYearSource"] in urls
        assert len(item["chronologyNote"]) >= 130
        assert len(item["dateRationale"]) >= 110
        assert len(item["researchSummary"]) >= 130
        assert len(item["recurrenceRules"]) == 1
        rule = item["recurrenceRules"][0]
        assert rule["kind"] in ("FIXED_DATE", "NTH_WEEKDAY")
        assert 1 <= rule["month"] <= 12
        if rule["kind"] == "FIXED_DATE":
            assert 1 <= rule["day"] <= monthrange(2028, rule["month"])[1]
        else:
            assert 1 <= rule["weekday"] <= 7 and 1 <= rule["occurrence"] <= 5
        dates = [occurrence(rule, year).isoformat() for year in (2026, 2027, 2028)]
        assert dates == expected["dates"], (rid, dates, expected["dates"])
    return data["records"]

if __name__ == "__main__":
    print(f"Wave05 Japan OK: {len(load_wave05_japan())} distinct dates")
