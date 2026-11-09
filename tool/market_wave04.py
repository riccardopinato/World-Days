"""Governance for the 15-country source-bound Wave04 batch (83 records).

A national public holiday, an official flag day, and an institutionally recognized
customary flag day have different designations. 2026 source calendars do not
establish the first-ever celebration year unless they state it explicitly.
No artificial UN/national duplicates; source-only metadata, not Rich Editorial.
"""
from __future__ import annotations
from calendar import monthrange
from datetime import date, timedelta
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BATCHES = (
    ROOT / "data/market/wave04_europe_20261109.json",
    ROOT / "data/market/wave04_global_20261109.json",
)
COUNTRY_COUNTS = {
    "CZ": 7, "SK": 6, "NO": 5, "FI": 15, "SE": 1,
    "PL": 5, "IE": 2, "NL": 2, "ZA": 6, "PH": 7,
    "NZ": 3, "SG": 2, "KR": 7, "AR": 8, "PE": 7,
}
LOCALES = ("en", "it", "es", "fr", "de", "pt")
SOURCE_HOSTS = {
    "e-sbirka.gov.cz", "www.vlada.gov.sk", "www.regjeringen.no",
    "almanakka.helsinki.fi", "www.finlex.fi", "government.se",
    "www.gov.pl", "www.workplacerelations.ie", "www.gov.ie",
    "www.government.nl", "www.gov.za", "pco.gov.ph",
    "www.employment.govt.nz", "www.mom.gov.sg", "www.mindef.gov.sg",
    "english.visitkorea.or.kr", "www.argentina.gob.ar", "www.gob.pe",
}
RULE_KINDS = {"FIXED_DATE", "NTH_WEEKDAY", "LAST_WEEKDAY"}
DESIGNATIONS = {
    "OFFICIAL_NATIONAL_COMMEMORATION", "OFFICIAL_FLAG_DAY",
    "CUSTOMARY_FLAG_DAY", "RECOMMENDED_FLAG_DAY",
    "NATIONAL_CIVIC_OR_STATUTORY_OBSERVANCE",
    "SPECIAL_WORKING_COMMENCEMENT", "OFFICIAL_CIVIC_COMMENCEMENT",
}
COUNTRY_SOURCE_AUTHORITY = {"GOVERNMENT", "UNIVERSITY"}


def _validate_rule(r):
    assert r["kind"] in RULE_KINDS, r
    assert 1 <= r["month"] <= 12, r
    if r["kind"] == "FIXED_DATE":
        assert 1 <= r["day"] <= monthrange(2028, r["month"])[1], r
        assert set(r) == {"kind", "month", "day"}
    else:
        assert 1 <= r["weekday"] <= 7
        if r["kind"] == "NTH_WEEKDAY":
            assert 1 <= r["occurrence"] <= 5
            assert set(r) == {"kind", "month", "weekday", "occurrence"}
        else:
            assert set(r) == {"kind", "month", "weekday"}


def _resolved_date(rule, year):
    """Prove dates for fixed/nth/last weekdays in 2026–2028, never workplace substitutes."""
    month = rule["month"]
    if rule["kind"] == "FIXED_DATE":
        return date(year, month, rule["day"])
    first = date(year, month, 1)
    weekday = rule["weekday"] - 1  # ISO Monday = 1, Python Monday = 0
    if rule["kind"] == "NTH_WEEKDAY":
        first_offset = (weekday - first.weekday()) % 7
        day = 1 + first_offset + (rule["occurrence"] - 1) * 7
    else:
        last_day = monthrange(year, month)[1]
        last = date(year, month, last_day)
        day = last_day - (last.weekday() - weekday) % 7
    assert 1 <= day <= monthrange(year, month)[1], rule
    return date(year, month, day)


def load_wave04():
    rows = []
    for file, length, allowed in (
        (BATCHES[0], 43, {"CZ", "SK", "NO", "FI", "SE", "PL", "IE", "NL"}),
        (BATCHES[1], 40, {"ZA", "PH", "NZ", "SG", "KR", "AR", "PE"}),
    ):
        data = json.loads(file.read_text(encoding="utf-8"))
        assert data["schemaVersion"] == 1
        assert data["count"] == len(data["records"]) == length, file
        assert set(data["locales"]) == set(LOCALES)
        assert set(data["countryCounts"]) == allowed
        assert data["sourceReviewedOn"] == "2026-11-09"
        for entry in data["records"]:
            assert entry["country"] in allowed
            assert entry["humanEditorialStatus"] == "METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
            assert entry["sourceReviewedOn"] == "2026-11-09"
            assert entry["id"].startswith(entry["country"].lower() + "-")
            assert entry["canonicalTitleEn"].strip()
            assert set(entry["localizedTitles"]) == set(LOCALES)
            assert entry["localizedTitles"]["en"] == entry["canonicalTitleEn"]
            assert all(entry["localizedTitles"][loc].strip() for loc in LOCALES)
            assert len(entry["recurrenceRules"]) == 1
            _validate_rule(entry["recurrenceRules"][0])
            host = urlsplit(entry["source"])
            assert host.scheme == "https" and host.hostname in SOURCE_HOSTS
            assert host.path not in ("", "/")
            assert entry["authority"].strip()
            assert entry["authorityType"] in COUNTRY_SOURCE_AUTHORITY
            assert entry["designation"] in DESIGNATIONS
            assert entry["category"].strip()
            assert entry["sourceTier"] in {"A_PRIMARY", "D_ORIGINATOR"}
            assert entry["officiality"] in {
                "OFFICIAL_INSTITUTIONAL", "RECOGNIZED_INSTITUTIONAL",
            }
            if entry["officiality"] == "OFFICIAL_INSTITUTIONAL":
                assert entry["sourceTier"] == "A_PRIMARY"
            else:
                assert entry["sourceTier"] == "D_ORIGINATOR"
                assert entry["authorityType"] == "UNIVERSITY"
                assert entry["designation"] in {
                    "CUSTOMARY_FLAG_DAY", "RECOMMENDED_FLAG_DAY",
                }
            year = entry["proposedIntroducedYear"]
            if year is None:
                assert entry["introducedYearSource"] is None
            else:
                assert 1850 <= year <= 2026
                assert entry["introducedYearSource"] == entry["source"]
            assert len(entry["researchSummary"]) >= 130
            assert len(entry["dateRationale"]) >= 120
            rows.append(entry)
        for country in allowed:
            assert data["countryCounts"][country] == sum(
                x["country"] == country for x in data["records"]
            ), country
    ids = [r["id"] for r in rows]
    titles = [r["canonicalTitleEn"] for r in rows]
    assert len(rows) == len(set(ids)) == len(set(titles)) == 83
    assert {x: sum(r["country"] == x for r in rows) for x in COUNTRY_COUNTS} == COUNTRY_COUNTS
    for item in rows:
        for year in (2026, 2027, 2028):
            observed = _resolved_date(item["recurrenceRules"][0], year)
            assert observed.year == year, (item["id"], year)
    by_id = {item["id"]: item for item in rows}
    expected_vectors = {
        "fi-finnish-nature-day": ("2026-08-29", "2027-08-28", "2028-08-26"),
        "ph-national-heroes-day": ("2026-08-31", "2027-08-30", "2028-08-28"),
        "nz-labour-day": ("2026-10-26", "2027-10-25", "2028-10-23"),
        "ie-st-brigids-day": ("2026-02-01", "2027-02-01", "2028-02-01"),
    }
    for rid, want in expected_vectors.items():
        got = tuple(_resolved_date(by_id[rid]["recurrenceRules"][0], year).isoformat()
                    for year in (2026, 2027, 2028))
        assert got == want, (rid, got, want)
    assert sum(r["proposedIntroducedYear"] is not None for r in rows) == 1
    return rows


if __name__ == "__main__":
    entries = load_wave04()
    print(f"Wave04 source-bound: {len(entries)} canonical identities, {len(COUNTRY_COUNTS)} new markets")
