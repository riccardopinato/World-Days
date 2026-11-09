#!/usr/bin/env python3
"""No human-review or publication claims from bilingual draft content."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/editorial/candidates/country_wave01_en_it_20261109.json"
MARKET = ROOT / "data/market/expansion_2026_11_09.json"


def validate():
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    markets = json.loads(MARKET.read_text(encoding="utf-8"))
    by_id = {row["id"]: row for row in markets["records"]}
    assert payload["candidateBatchId"] == "COUNTRY-RICH-WAVE01-2026-11-09"
    assert payload["editorialStatus"] == "DRAFT_PENDING_HUMAN_AND_ALL_SIX_LOCALES"
    assert payload["localeCoverage"] == ["en", "it"]
    assert set(payload["remainingTargetLocales"]) == {"es", "fr", "de", "pt"}
    assert len(payload["entries"]) == payload["entryCount"] == 9
    ids = [row["id"] for row in payload["entries"]]
    assert len(set(ids)) == len(ids)
    assert set(ids) <= set(by_id)
    for row in payload["entries"]:
        assert row["reviewStatus"] == "DRAFT_PENDING_FACT_AND_HUMAN_EDIT"
        assert row["publishedToApp"] is False
        valid_sources = {by_id[row["id"]]["source"], *by_id[row["id"]].get("additionalSources", [])}
        assert row["primarySource"] in valid_sources
        assert set(row["locales"]) == {"en", "it"}
        for locale, article in row["locales"].items():
            assert article["reviewStatus"] == "DRAFT"
            for key, minlen in (("hook", 45), ("summary", 120), ("origin", 210),
                                ("whyThisDate", 60), ("whyItMatters", 150)):
                assert len(article[key].strip()) >= minlen, (row["id"], locale, key)
            assert len(article["quickFacts"]) >= 2
            assert len(article["waysToTakePart"]) == 2
            assert all(len(x) >= 35 for x in article["waysToTakePart"])
        assert row["locales"]["en"]["summary"] != row["locales"]["it"]["summary"]
    builder = (ROOT / "tool/build_editorial.py").read_text(encoding="utf-8")
    localizer = (ROOT / "tool/build_editorial_locales.py").read_text(encoding="utf-8")
    assert "country_wave01_en_it_20261109" not in builder
    assert "country_wave01_en_it_20261109" not in localizer
    print("country editorial: 9 source-linked EN/IT drafts; 4 locales + human approval OPEN")


if __name__ == "__main__":
    validate()
