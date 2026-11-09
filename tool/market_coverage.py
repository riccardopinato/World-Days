#!/usr/bin/env python3
"""Deterministic source-bound catalog and editorial coverage report.

Never labels a draft as REVIEWED; no provider, device or revenue evidence.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relpath):
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def coverage_report():
    catalog = read("assets/data/official_core.json")
    reviewed = read("assets/data/editorial_en.json")
    wave04 = read("data/editorial/candidates/wave04_sources_20261109.json")
    wave01 = read("data/editorial/candidates/country_wave01_en_it_20261109.json")
    wave02 = read("data/editorial/candidates/country_wave02_en_it_20261109.json")

    ids = [r["id"] for r in catalog["records"]]
    assert len(ids) == len(set(ids)), "canonical record ID conflict"
    strata = {
        "REVIEWED_RUNTIME": {r["observanceId"] for r in reviewed["entries"]},
        "WAVE04_DRAFT_SIX_LOCALES": {r["id"] for r in wave04["records"]},
        "COUNTRY_WAVE01_DRAFT_SIX_LOCALES": {r["id"] for r in wave01["entries"]},
        "COUNTRY_WAVE02_DRAFT_SIX_LOCALES": {r["id"] for r in wave02["entries"]},
    }
    known, seen = set(ids), set()
    for label, entries in strata.items():
        assert entries <= known, (label, "references absent catalog ID")
        assert not seen.intersection(entries), (label, "double-classified review state")
        seen |= entries

    market = Counter()
    counts = Counter()
    without_year = 0
    for r in catalog["records"]:
        scope = r["scope"]
        assert scope in {"GLOBAL", "NATIONAL"}, r["id"]
        assert len(r.get("sources", [])) > 0, r["id"]
        assert set(r["localizedTitles"]) == {"en", "it", "es", "fr", "de", "pt"}
        if r.get("introducedYear") is None:
            without_year += 1
        else:
            year_source = r.get("introducedYearSource")
            assert year_source in {s["url"] for s in r["sources"]}, r["id"]
        if scope == "NATIONAL":
            assert len(r["countries"]) == 1, r["id"]
            market[r["countries"][0]] += 1
        else:
            assert not r["countries"], r["id"]
        counts[scope] += 1

    report = {
        "schemaVersion": 1,
        "sourceCatalogVersion": catalog["datasetVersion"],
        "catalogTotalUnique": len(ids),
        "globalUnique": counts["GLOBAL"],
        "nationalUnique": counts["NATIONAL"],
        "nationalByCountry": {k: market[k] for k in sorted(market)},
        "introducedYearProven": len(ids) - without_year,
        "introducedYearUnknownUsesStar": without_year,
        "editorialStages": {
            **{key: len(val) for key, val in strata.items()},
            "NOT_RESEARCHED_LONG_FORM": len(ids) - len(seen),
        },
        "sourceLevel": "GITHUB_GENERATED_DATASET_AND_EDITORIAL_FILES_ONLY",
        "externalVerification": "NOT_A_PROVIDER_OR_DEVICE_CERTIFICATION",
        "sourcePolicy": "Do not multiply shared global records by country. Drafts are not reviewed.",
    }
    assert report["catalogTotalUnique"] == (
        report["globalUnique"] + report["nationalUnique"]
    )
    assert sum(report["nationalByCountry"].values()) == report["nationalUnique"]
    assert sum(report["editorialStages"].values()) == len(ids)
    assert report["catalogTotalUnique"] == 504
    assert report["globalUnique"] == 285
    assert report["nationalUnique"] == 219
    assert report["introducedYearProven"] == 72
    assert report["editorialStages"]["REVIEWED_RUNTIME"] == 56
    assert report["editorialStages"]["NOT_RESEARCHED_LONG_FORM"] == 423
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "reports/market_coverage.json")
    args = parser.parse_args()
    report = coverage_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("market coverage: " + json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
