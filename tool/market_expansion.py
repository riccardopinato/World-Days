"""Source-pinned national and civic observances, separately from global days.

No substitute public-holiday dates, no inferred founding years, no runtime AI.
The six localized titles live in the same reviewed source payload.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "market" / "expansion_2026_11_09.json"
WAVE02_SOURCE = ROOT / "data" / "market" / "expansion_wave02_2026_11_09.json"
LOCALES = ("en", "it", "es", "fr", "de", "pt")
COUNTRIES = ("IT", "ES", "FR", "DE", "PT", "GB", "US")
SOURCE_HOSTS = {
    "presidenza.governo.it", "www.gazzettaufficiale.it",
    "www.boe.es", "www.cheminsdememoire.gouv.fr",
    "www.legifrance.gouv.fr", "www.bundesregierung.de",
    "diariodarepublica.pt", "portugal.gov.pt", "www.gov.uk",
    "insidemca.blog.gov.uk", "www.opm.gov", "www.archives.gov",
    "www.lamoncloa.gob.es", "boe.es", "www.executiveoffice-ni.gov.uk",
    "www.cps.gov.uk",
}
VALID_RULES = {"FIXED_DATE", "NTH_WEEKDAY", "LAST_WEEKDAY"}


def load_expansion():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert data["schemaVersion"] == 1
    assert data["count"] == len(data["records"]) == 43
    assert set(data["locales"]) == set(LOCALES)
    assert set(data["countryCounts"]) == set(COUNTRIES)
    ids = set()
    titles = set()
    for item in data["records"]:
        ident = item["id"]
        title = item["canonicalTitleEn"]
        assert ident not in ids and title not in titles, (ident, title, "duplicate")
        ids.add(ident)
        titles.add(title)
        cc = item["country"]
        assert cc in COUNTRIES, ident
        assert item["humanEditorialStatus"] == "METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert set(item["localizedTitles"]) == set(LOCALES)
        assert item["localizedTitles"]["en"] == title
        assert all(item["localizedTitles"][loc].strip() for loc in LOCALES), ident
        rules = item["recurrenceRules"]
        assert len(rules) == 1
        rule = rules[0]
        assert rule["kind"] in VALID_RULES
        assert 1 <= rule["month"] <= 12
        if rule["kind"] == "FIXED_DATE":
            assert 1 <= rule["day"] <= 31
        else:
            assert 1 <= rule["weekday"] <= 7
            if rule["kind"] == "NTH_WEEKDAY":
                assert 1 <= rule["occurrence"] <= 5
        source = urlsplit(item["source"])
        assert source.scheme == "https" and source.hostname in SOURCE_HOSTS, ident
        assert source.path and source.path != "/"
        extra_sources = item.get("additionalSources", [])
        assert len(extra_sources) == len(set(extra_sources)), ident
        for extra in extra_sources:
            extra_url = urlsplit(extra)
            assert extra_url.scheme == "https" and extra_url.hostname in SOURCE_HOSTS
            assert extra_url.path not in ("", "/")
        year = item["proposedIntroducedYear"]
        if year is None:
            assert item["introducedYearSource"] is None
        else:
            assert 1800 <= year <= 2026
            assert item["introducedYearSource"] in [item["source"], *extra_sources]
        assert item["sourceReviewedOn"] == "2026-11-09"
    assert data["countryCounts"] == {
        code: sum(x["country"] == code for x in data["records"])
        for code in COUNTRIES
    }
    return data


def load_wave02():
    """Enforce new batch provenance and preserve the independent first wave."""
    data = json.loads(WAVE02_SOURCE.read_text(encoding="utf-8"))
    assert data["schemaVersion"] == 1
    assert data["datasetId"] == "world-days-market-wave02-2026-11-09"
    assert data["count"] == len(data["records"]) == 15
    assert set(data["locales"]) == set(LOCALES)
    assert set(data["countryCounts"]) == {"ES", "DE", "PT", "GB"}
    assert data["countryCounts"] == {"ES": 4, "DE": 2, "PT": 5, "GB": 4}
    ids = set()
    titles = set()
    for item in data["records"]:
        rid, name = item["id"], item["canonicalTitleEn"]
        assert rid not in ids and name not in titles
        ids.add(rid)
        titles.add(name)
        assert item["country"] in data["countryCounts"]
        assert set(item["localizedTitles"]) == set(LOCALES)
        assert item["localizedTitles"]["en"] == name
        assert all(item["localizedTitles"][x].strip() for x in LOCALES)
        assert item["humanEditorialStatus"] == "METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert item["sourceReviewedOn"] == data["sourceReviewDate"] == "2026-11-09"
        assert len(item["recurrenceRules"]) == 1
        rule = item["recurrenceRules"][0]
        assert rule["kind"] == "FIXED_DATE"
        from calendar import monthrange
        assert 1 <= rule["month"] <= 12
        assert 1 <= rule["day"] <= monthrange(2028, rule["month"])[1]
        sources = [item["source"], *item.get("additionalSources", [])]
        assert len(sources) == len(set(sources))
        for url in sources:
            parsed = urlsplit(url)
            assert parsed.scheme == "https" and parsed.hostname in SOURCE_HOSTS
            assert parsed.path not in ("", "/")
        year = item["proposedIntroducedYear"]
        if year is None:
            assert item["introducedYearSource"] is None
        else:
            assert 1800 <= year <= 2026
            assert item["introducedYearSource"] in sources
        assert len(item["chronologyNote"]) >= 100
        assert len(item["dateRationale"]) >= 55
    wave01 = load_expansion()
    original_ids = {row["id"] for row in wave01["records"]}
    original_titles = {row["canonicalTitleEn"] for row in wave01["records"]}
    assert ids.isdisjoint(original_ids)
    assert titles.isdisjoint(original_titles)
    return data


def all_expansion_rows():
    return [*load_expansion()["records"], *load_wave02()["records"]]


def expanded_title_map():
    records = all_expansion_rows()
    return {
        locale: {
            item["canonicalTitleEn"]: item["localizedTitles"][locale]
            for item in records
        }
        for locale in LOCALES
    }


def build_expansion_records():
    rows = []
    for item in all_expansion_rows():
        record = {
            "id": item["id"],
            "canonicalTitleEn": item["canonicalTitleEn"],
            "aliases": item["aliases"],
            "periodKind": "DAY",
            "recurrenceRules": item["recurrenceRules"],
            "scope": "NATIONAL",
            "countries": [item["country"]],
            "regions": [],
            "authority": {
                "name": item["authority"],
                "type": "GOVERNMENT",
                "officiality": "OFFICIAL_INSTITUTIONAL",
                "resolution": item["resolution"],
            },
            "categories": [item["subject"], "CIVIC"],
            "sources": [
                {"tier": "A_PRIMARY", "url": url, "verifiedAt": item["sourceReviewedOn"]}
                for url in [item["source"], *item.get("additionalSources", [])]
            ],
            "visualKey": "people",
            "editorialStatus": "STUB",
            "notes": [
                "Source-curated national or civic observance.",
                "Does not imply a public holiday or a complete published history.",
            ],
            "lastVerifiedAt": item["sourceReviewedOn"],
        }
        if item["proposedIntroducedYear"] is not None:
            record["introducedYear"] = item["proposedIntroducedYear"]
            record["introducedYearSource"] = item["introducedYearSource"]
        rows.append(record)
    return rows
