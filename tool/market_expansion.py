"""Source-pinned national and civic observances, separately from global days.

No substitute public-holiday dates, no inferred founding years, no runtime AI.
The six localized titles live in the same reviewed source payload.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "market" / "expansion_2026_11_09.json"
LOCALES = ("en", "it", "es", "fr", "de", "pt")
COUNTRIES = ("IT", "ES", "FR", "DE", "PT", "GB", "US")
SOURCE_HOSTS = {
    "presidenza.governo.it", "www.gazzettaufficiale.it",
    "www.boe.es", "www.cheminsdememoire.gouv.fr",
    "www.legifrance.gouv.fr", "www.bundesregierung.de",
    "diariodarepublica.pt", "portugal.gov.pt", "www.gov.uk",
    "insidemca.blog.gov.uk", "www.opm.gov", "www.archives.gov",
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


def expanded_title_map():
    data = load_expansion()
    return {
        locale: {
            item["canonicalTitleEn"]: item["localizedTitles"][locale]
            for item in data["records"]
        }
        for locale in LOCALES
    }


def build_expansion_records():
    data = load_expansion()
    rows = []
    for item in data["records"]:
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
