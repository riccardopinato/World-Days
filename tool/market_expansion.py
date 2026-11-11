"""Source-pinned national and civic observances, separately from global days.

No substitute public-holiday dates, no inferred founding years, no runtime AI.
The six localized titles live in the same reviewed source payload.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit
from market_wave04 import load_wave04
from market_wave06 import load_wave06
from market_wave07 import load_wave07
from market_wave08 import load_wave08
from market_wave09 import load_wave09
from market_wave10 import load_wave10
from market_wave11 import load_wave11
from market_wave12 import load_wave12

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "market" / "expansion_2026_11_09.json"
WAVE02_SOURCE = ROOT / "data" / "market" / "expansion_wave02_2026_11_09.json"
WAVE03_SOURCE = ROOT / "data" / "market" / "expansion_wave03_2026_11_09.json"
LOCALES = ("en", "it", "es", "fr", "de", "pt")
COUNTRIES = ("IT", "ES", "FR", "DE", "PT", "GB", "US", "CA", "AU", "BR", "MX", "IN", "JP")
SOURCE_HOSTS = {
    "presidenza.governo.it", "www.gazzettaufficiale.it",
    "www.boe.es", "www.cheminsdememoire.gouv.fr",
    "www.legifrance.gouv.fr", "www.bundesregierung.de",
    "diariodarepublica.pt", "portugal.gov.pt", "www.gov.uk",
    "insidemca.blog.gov.uk", "www.opm.gov", "www.archives.gov",
    "www.lamoncloa.gob.es", "boe.es", "www.executiveoffice-ni.gov.uk",
    "www.cps.gov.uk",
    "www.canada.ca", "www.pmc.gov.au", "ministers.pmc.gov.au",
    "planalto.gov.br", "www.planalto.gov.br", "www2.camara.leg.br",
    "sidof.segob.gob.mx", "www.diputados.gob.mx",
    "www.eci.gov.in", "www.pib.gov.in", "www8.cao.go.jp",
}
VALID_RULES = {"FIXED_DATE", "NTH_WEEKDAY", "LAST_WEEKDAY"}


def load_expansion():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert data["schemaVersion"] == 1
    assert data["count"] == len(data["records"]) == 43
    assert set(data["locales"]) == set(LOCALES)
    assert set(data["countryCounts"]) == {"IT", "ES", "FR", "DE", "PT", "GB", "US"}
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
        for code in data["countryCounts"]
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


def load_wave03():
    """New country admission requires source attribution and all six localized titles."""
    data = json.loads(WAVE03_SOURCE.read_text(encoding="utf-8"))
    assert data["schemaVersion"] == 1
    assert data["datasetId"] == "world-days-market-wave03-2026-11-09"
    assert data["count"] == len(data["records"]) == 19
    assert set(data["locales"]) == set(LOCALES)
    expected = {"CA": 5, "AU": 3, "BR": 3, "MX": 3, "IN": 2, "JP": 3}
    assert data["countryCounts"] == expected
    prior = [*load_expansion()["records"], *load_wave02()["records"]]
    ids = {x["id"] for x in prior}
    titles = {x["canonicalTitleEn"] for x in prior}
    from calendar import monthrange
    for item in data["records"]:
        rid, title = item["id"], item["canonicalTitleEn"]
        assert rid not in ids and title not in titles, rid
        ids.add(rid)
        titles.add(title)
        assert item["country"] in expected
        assert item["humanEditorialStatus"] == "METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert item["holidayClassification"] in {"STATUTORY_NATIONAL_HOLIDAY", "NATIONAL_CIVIC_OBSERVANCE_NOT_AUTOMATIC_PUBLIC_HOLIDAY"}
        assert item["holidayClassification"] == ("STATUTORY_NATIONAL_HOLIDAY" if item["country"] == "JP" else "NATIONAL_CIVIC_OBSERVANCE_NOT_AUTOMATIC_PUBLIC_HOLIDAY")
        assert set(item["localizedTitles"]) == set(LOCALES)
        assert item["localizedTitles"]["en"] == title
        assert all(item["localizedTitles"][l].strip() for l in LOCALES)
        assert len(item["recurrenceRules"]) == 1
        rule = item["recurrenceRules"][0]
        assert rule["kind"] == "FIXED_DATE"
        assert 1 <= rule["month"] <= 12 and 1 <= rule["day"] <= monthrange(2028, rule["month"])[1]
        assert item["sourceReviewedOn"] == data["sourceReviewDate"] == "2026-11-09"
        sources = [item["source"], *item.get("additionalSources", [])]
        assert len(sources) == len(set(sources))
        for url in sources:
            parsed = urlsplit(url)
            assert parsed.scheme == "https" and parsed.hostname in SOURCE_HOSTS and parsed.path not in ("", "/")
        year = item["proposedIntroducedYear"]
        if year is None:
            assert item["introducedYearSource"] is None
        else:
            assert 1800 <= year <= 2026 and item["introducedYearSource"] in sources
        assert len(item["chronologyNote"]) >= 115, rid
        assert len(item["dateRationale"]) >= 65, rid
        assert item["subject"] in {"PEOPLE", "CULTURE", "COMMUNITY", "LEARNING", "HISTORY"}
    assert len(ids) == len(prior) + 19
    return data


def all_expansion_rows():
    prior = [*load_expansion()["records"], *load_wave02()["records"], *load_wave03()["records"]]
    next_wave = load_wave04()
    ids = {item["id"] for item in prior}
    titles = {item["canonicalTitleEn"] for item in prior}
    assert all(item["id"] not in ids for item in next_wave), "cross-wave duplicate ID"
    assert all(item["canonicalTitleEn"] not in titles for item in next_wave), "cross-wave title collision"
    wave06 = load_wave06()
    existing_ids = ids | {row['id'] for row in next_wave}
    existing_titles = titles | {row['canonicalTitleEn'] for row in next_wave}
    assert all(item['id'] not in existing_ids for item in wave06), 'Wave06 canonical ID collision'
    assert all(item['canonicalTitleEn'] not in existing_titles for item in wave06), 'Wave06 title collision'
    wave07 = load_wave07()
    previous_ids = existing_ids | {row['id'] for row in wave06}
    previous_titles = existing_titles | {row['canonicalTitleEn'] for row in wave06}
    assert all(item['id'] not in previous_ids for item in wave07), 'Wave07 canonical ID collision'
    assert all(item['canonicalTitleEn'] not in previous_titles for item in wave07), 'Wave07 title collision'
    wave08 = load_wave08()
    known_ids = previous_ids | {item['id'] for item in wave07}
    known_titles = previous_titles | {item['canonicalTitleEn'] for item in wave07}
    assert all(item['id'] not in known_ids for item in wave08), 'Wave08 ID duplicate'
    assert all(item['canonicalTitleEn'] not in known_titles for item in wave08), 'Wave08 title duplicate'
    wave09 = load_wave09()
    known_ids09 = known_ids | {row['id'] for row in wave08}
    known_titles09 = known_titles | {row['canonicalTitleEn'] for row in wave08}
    assert all(item['id'] not in known_ids09 for item in wave09), 'Wave09 ID collision'
    assert all(item['canonicalTitleEn'] not in known_titles09 for item in wave09), 'Wave09 title collision'
    wave10 = load_wave10()
    all_prior = [*prior, *next_wave, *wave06, *wave07, *wave08, *wave09]
    prior_ids = {r["id"] for r in all_prior}
    prior_titles = {r["canonicalTitleEn"] for r in all_prior}
    assert all(r["id"] not in prior_ids for r in wave10), "Wave10 existing-ID collision"
    assert all(r["canonicalTitleEn"] not in prior_titles for r in wave10), "Wave10 existing-title collision"
    wave11 = load_wave11()
    known = [*all_prior, *wave10]
    known_id_set = {r["id"] for r in known}
    known_title_set = {r["canonicalTitleEn"] for r in known}
    assert all(x["id"] not in known_id_set for x in wave11), "Wave11 duplicate IDs"
    assert all(x["canonicalTitleEn"] not in known_title_set for x in wave11), "Wave11 duplicate English titles"
    wave12 = load_wave12()
    previous = [*known, *wave11]
    prior_ids = {x["id"] for x in previous}
    prior_titles = {x["canonicalTitleEn"] for x in previous}
    prior_markets = {x["country"] for x in previous}
    assert all(x["id"] not in prior_ids for x in wave12), "Wave12 duplicate IDs"
    assert all(x["canonicalTitleEn"] not in prior_titles for x in wave12), "Wave12 duplicate titles"
    assert not ({x["country"] for x in wave12} & prior_markets), "Wave12 must add new countries"
    return [*previous, *wave12]


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
            "aliases": item.get("aliases", []),
            "periodKind": "DAY",
            "recurrenceRules": item["recurrenceRules"],
            "scope": "NATIONAL",
            "countries": [item["country"]],
            "regions": [],
            "authority": {
                "name": item["authority"],
                "type": item.get("authorityType", "GOVERNMENT"),
                "officiality": item.get("officiality", "OFFICIAL_INSTITUTIONAL"),
                "resolution": item.get("resolution"),
            },
            "categories": [item.get("subject", item.get("category", "CIVIC_HISTORY")), "CIVIC"],
            "sources": [
                {"tier": item.get("sourceTier", "A_PRIMARY"), "url": url, "verifiedAt": item["sourceReviewedOn"]}
                for url in [item["source"], *item.get("additionalSources", [])]
            ],
            "visualKey": "people",
            "editorialStatus": "STUB",
            "notes": [
                "Source-curated national or civic observance.",
                "Legal holiday treatment is documented per source, not inferred from the observed date.",
                "Does not imply a complete human-reviewed historical narrative.",
            ],
            "lastVerifiedAt": item["sourceReviewedOn"],
        }
        if item["proposedIntroducedYear"] is not None:
            record["introducedYear"] = item["proposedIntroducedYear"]
            record["introducedYearSource"] = item["introducedYearSource"]
        rows.append(record)
    return rows
