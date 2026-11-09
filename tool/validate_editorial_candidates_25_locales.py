#!/usr/bin/env python3
"""Validate the exact 25 historical candidates in six locales, WITHOUT human approval.

Evidence: deterministic source/link presence, complete localized sections and the
chronological years mentioned in the canonical English originals.
This is not a native-speaker assessment or proof of historic source interpretation.
"""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data/editorial/candidates"
LOCALES = ("en", "it", "es", "fr", "de", "pt")
TRANSLATIONS = ("es", "fr", "de", "pt")
MAIN_FIELDS = ("hook", "summary", "origin", "whyThisDate", "whyItMatters")
REVIEW_REQUIRED = "AI_DRAFT_PENDING_QUALIFIED_HUMAN_REVIEW"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def english_years(text):
    return set(re.findall(r"\b(?:18|19|20)\d{2}\b", text))


def validate():
    original = []
    for suffix, expected in (("01", 9), ("02", 8)):
        batch = read(CANDIDATES / f"country_wave{suffix}_en_it_20261109.json")
        assert len(batch["entries"]) == batch["entryCount"] == expected
        assert batch["editorialStatus"] == "DRAFT_PENDING_HUMAN_AND_ALL_SIX_LOCALES"
        assert batch["localeCoverage"] == ["en", "it"]
        original.extend(batch["entries"])
    expected_ids = [x["id"] for x in original]
    assert len(set(expected_ids)) == len(expected_ids) == 17

    sources = {}
    for f in ("expansion_2026_11_09.json", "expansion_wave02_2026_11_09.json"):
        pack = read(ROOT / "data" / "market" / f)
        sources.update({x["id"]: x for x in pack["records"]})
    for item in original:
        assert item["id"] in sources
        assert item["primarySource"] in [
            sources[item["id"]]["source"],
            *sources[item["id"]].get("additionalSources", []),
        ]
        assert item["publishedToApp"] is False
        assert item["reviewStatus"] == "DRAFT_PENDING_FACT_AND_HUMAN_EDIT"
        assert set(item["locales"]) == {"en", "it"}

    translations = {}
    for locale in TRANSLATIONS:
        pack = read(CANDIDATES / f"country_translations_{locale}_20261109.json")
        assert pack["schemaVersion"] == 1
        assert pack["batchId"] == "COUNTRY_TRANSLATIONS_2026-11-09"
        assert pack["locale"] == locale and pack["sourceLocale"] == "en"
        assert pack["translationStatus"] == REVIEW_REQUIRED
        assert pack["entryCount"] == len(pack["entries"]) == 17
        assert [x["id"] for x in pack["entries"]] == expected_ids
        translations[locale] = {r["id"]: r for r in pack["entries"]}

    problems = []
    for source in original:
        oid = source["id"]
        by_locale = dict(source["locales"])
        by_locale.update({loc: translations[loc][oid] for loc in TRANSLATIONS})
        assert set(by_locale) == set(LOCALES)
        original_en = source["locales"]["en"]
        needed_years = english_years(original_en["origin"])
        for locale, entry in by_locale.items():
            if entry.get("reviewStatus") != "DRAFT":
                problems.append(f"{oid} {locale}: reviewed status improperly set")
            for field, minimum in (
                ("hook", 35), ("summary", 100), ("origin", 180),
                ("whyThisDate", 55), ("whyItMatters", 105),
            ):
                if len(entry[field].strip()) < minimum:
                    problems.append(f"{oid} {locale}: insufficient {field}")
            if len(entry["quickFacts"]) < 2 or len(entry["waysToTakePart"]) != 2:
                problems.append(f"{oid} {locale}: missing facts or actions")
            if any(len(z.strip()) < 30 for z in entry["waysToTakePart"]):
                problems.append(f"{oid} {locale}: too-short action")
            if any(len(z.strip()) < 25 for z in entry["quickFacts"]):
                problems.append(f"{oid} {locale}: truncated fact")
            if "http://" in entry["origin"] or "https://" in entry["origin"]:
                problems.append(f"{oid} {locale}: inline URL copied into editorial text")
            years = english_years(entry["origin"] + " " + entry["whyThisDate"])
            if not needed_years <= years:
                problems.append(f"{oid} {locale}: missing source chronology {sorted(needed_years - years)}")
        if by_locale["en"]["origin"] == by_locale["fr"]["origin"]:
            problems.append(f"{oid}: French text not translated")

    wave04 = read(CANDIDATES / "wave04_sources_20261109.json")
    assert wave04["count"] == len(wave04["records"]) == 8
    global_ids = [r["id"] for r in wave04["records"]]
    assert set(global_ids).isdisjoint(expected_ids)
    global_packs = {}
    for locale in LOCALES:
        pack = read(CANDIDATES / f"wave04_{locale}.json")
        assert pack["entryCount"] == len(pack["entries"]) == 8
        assert pack["locale"] == locale
        assert pack["reviewStatus"] == "DRAFT_PENDING_HUMAN_EDITORIAL_REVIEW"
        assert [x["id"] for x in pack["entries"]] == global_ids
        global_packs[locale] = pack
    for i, item in enumerate(wave04["records"]):
        assert urlsplit(item["primarySource"]).scheme == "https"
        assert item["humanEditorialReview"] == "PENDING"
        assert item["translationReview"] == "PENDING_HUMAN"
        for locale in LOCALES:
            row = global_packs[locale]["entries"][i]
            for field in MAIN_FIELDS:
                assert len(row[field].strip()) >= 45, (item["id"], locale, field)
            for year in item["milestones"]:
                if str(year) not in row["origin"]:
                    problems.append(f"{item['id']} {locale}: missing milestone {year}")
    assert not problems, "\n" + "\n".join(problems)

    # Both 17 country stories and 8 global stories must stay outside runtime generators.
    builder = (ROOT / "tool/build_editorial.py").read_text(encoding="utf-8")
    localizer = (ROOT / "tool/build_editorial_locales.py").read_text(encoding="utf-8")
    for script in (builder, localizer):
        assert "country_translations_" not in script
        assert "country_wave01_en_it_20261109" not in script
        assert "country_wave02_en_it_20261109" not in script
        assert "wave04_sources_20261109" not in script

    return {
        "schemaVersion": 1,
        "reviewType": "AUTOMATED_CANDIDATE_PARITY_AND_CHRONOLOGY_ONLY",
        "status": "STRUCTURAL_PARITY_PASSED_HUMAN_APPROVAL_PENDING",
        "totalCandidateStories": 25,
        "globalCandidateStories": 8,
        "countryCandidateStories": 17,
        "candidateLocaleEditions": 25 * 6,
        "translatedNationalStoriesPerLocale": {loc: 17 for loc in TRANSLATIONS},
        "humanSourceReviewApproved": 0,
        "qualifiedNativeLanguageReviewApproved": 0,
        "runtimePromotedByThisWorkflow": 0,
        "remainingManualGates": [
            "Confirm official primary sources, historical interpretation and cultural context",
            "Independent qualified linguistic review for all five target languages",
            "Approve only selected edited originals in a separate versioned runtime PR",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "reports/editorial_candidates_25_parity.json")
    args = parser.parse_args()
    report = validate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("25 candidate stories: six-locale source and chronological parity PASS; human review PENDING")


if __name__ == "__main__":
    main()
