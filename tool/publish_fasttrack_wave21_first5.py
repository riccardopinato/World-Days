#!/usr/bin/env python3
"""Append source-backed six-locale Wave21 stories after the existing 502.
No human-editorial signoff required for ordinary entertainment content.
Fail closed on ID, locale, source, chronology, duplication and stale counts.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/editorial/published/wave21_fasttrack_first5_six_locale_20261119.json"
DATA = ROOT / "assets/data"
LANG = ("en", "it", "es", "fr", "de", "pt")
STATUS = "AI_SOURCE_REVIEWED_SIX_LOCALE"
YEARS = re.compile(r"\b(?:18|19|20)\d{2}\b")
LABELS = {
    "en": "Originating or supporting institutions",
    "it": "Enti promotori o sostenitori",
    "es": "Instituciones promotoras o participantes",
    "fr": "Institutions à l'origine ou associées",
    "de": "Initiierende oder beteiligte Institutionen",
    "pt": "Instituições promotoras ou participantes",
}

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    pack = read(SRC)
    assert pack["schemaVersion"] == 1
    assert pack["status"] == "AI_REVIEWED_READY_FOR_APP_IMPORT"
    assert pack["count"] == len(pack["records"]) == 5
    assert pack["locales"] == list(LANG)
    catalog = {r["id"]: r for r in read(DATA / "official_core.json")["records"]}
    assert len(catalog) == 1111
    cohorts = read(ROOT / "data/editorial/waves/wave21_fasttrack_first5_ids.json")
    expected = cohorts["observanceIds"]
    ids = [r["observanceId"] for r in pack["records"]]
    assert ids == expected and len(set(ids)) == len(ids)
    for row in pack["records"]:
        oid = row["observanceId"]
        assert oid in catalog, ("not canonical", oid)
        assert set(row["locale"]) == set(LANG)
        assert row["sources"] and len(row["sources"]) == len(set(row["sources"]))
        assert all(urlsplit(u).scheme == "https" and urlsplit(u).hostname for u in row["sources"])
        year = row.get("introducedYear")
        catalog_year = catalog[oid].get("introducedYear")
        # The catalog can use a later date for holiday legislation than for the
        # constitutional event. Keep facts distinct; do not overwrite metadata.
        assert year is None or isinstance(year, int), oid
        assert catalog_year is None or isinstance(catalog_year, int), oid
        base_years = None
        for locale in LANG:
            item = row["locale"][locale]
            assert all(isinstance(item.get(k), str) and len(item[k].strip()) >= 24
                       for k in ("heading", "origin", "promoter", "purpose")), (oid, locale)
            assert len(item["origin"]) >= 130, (oid, locale)
            assert len(item["facts"]) == 3 and all(len(x) >= 20 for x in item["facts"])
            found = set(YEARS.findall(item["origin"] + " " + " ".join(item["facts"])))
            if base_years is None:
                base_years = found
            else:
                assert found == base_years, ("chronology mismatch", oid, locale, found, base_years)

    baseline = None
    for locale in LANG:
        path = DATA / f"editorial_{locale}.json"
        document = read(path)
        existing = document["entries"]
        old_ids = [r["observanceId"] for r in existing]
        assert document["entryCount"] == len(existing) == len(set(old_ids)) == 502
        assert not (set(ids) & set(old_ids)), ("already published", locale)
        if baseline is None:
            baseline = old_ids
        else:
            assert old_ids == baseline, ("existing parity", locale)
        additions = []
        for row in pack["records"]:
            story = row["locale"][locale]
            additions.append({
                "observanceId": row["observanceId"],
                "locale": locale,
                "translationOf": "en" if locale != "en" else None,
                "status": STATUS,
                "hook": story["heading"].strip(),
                "summary": story["purpose"].strip(),
                "whyThisDate": "",
                "origin": story["origin"].strip() + "\n\n" + LABELS[locale] + ": " + story["promoter"].strip(),
                "whyItMatters": "",
                "quickFacts": story["facts"],
                "waysToTakePart": [],
                "relatedObservanceIds": [],
                "lastReviewedAt": pack["checkedOn"],
                "sourcePolicy": "AI editorial drafting and translation, checked against source-linked institution pages; no mandatory human external certification.",
                "institutionalSourceUrls": row["sources"],
            })
        document["entries"] = existing + additions
        document["entryCount"] = len(document["entries"])
        assert document["entryCount"] == 507
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("FASTTRACK_WAVE21_FIRST5_IMPORTED", json.dumps({
        "catalog": 1111, "sixLocaleComplete": 507, "onlyEnglishItalian": 0,
        "pending": 604, "newStories": 5, "locales": list(LANG)
    }, sort_keys=True))

if __name__ == "__main__":
    main()
