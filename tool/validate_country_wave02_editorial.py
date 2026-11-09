#!/usr/bin/env python3
"""Validate country Wave02 bilingual drafts; never equate drafting with human approval."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data/editorial/candidates"
LEDGER = ROOT / "data/market/expansion_wave02_2026_11_09.json"


def validate():
    source = json.loads(LEDGER.read_text(encoding="utf-8"))
    draft = json.loads(
        (CANDIDATES / "country_wave02_en_it_20261109.json").read_text(encoding="utf-8")
    )
    by_id = {r["id"]: r for r in source["records"]}
    assert draft["candidateBatchId"] == "COUNTRY-RICH-WAVE02-2026-11-09"
    assert draft["editorialStatus"] == "DRAFT_PENDING_HUMAN_AND_ALL_SIX_LOCALES"
    assert draft["localeCoverage"] == ["en", "it"]
    assert set(draft["remainingTargetLocales"]) == {"es", "fr", "de", "pt"}
    assert len(draft["entries"]) == draft["entryCount"] == 8
    assert len({item["id"] for item in draft["entries"]}) == 8
    for item in draft["entries"]:
        assert item["id"] in by_id
        assert item["reviewStatus"] == "DRAFT_PENDING_FACT_AND_HUMAN_EDIT"
        assert item["publishedToApp"] is False
        assert item["primarySource"] == by_id[item["id"]]["source"]
        assert set(item["locales"]) == {"en", "it"}
        for locale, article in item["locales"].items():
            assert article["reviewStatus"] == "DRAFT"
            for field, minimum in (
                ("hook", 42), ("summary", 110), ("origin", 180),
                ("whyThisDate", 42), ("whyItMatters", 110),
            ):
                assert isinstance(article[field], str)
                assert len(article[field].strip()) >= minimum, (item["id"], locale, field)
            assert len(article["quickFacts"]) >= 2
            assert len(article["waysToTakePart"]) == 2
            assert all(len(a) >= 32 for a in article["waysToTakePart"])
        assert item["locales"]["en"]["origin"] != item["locales"]["it"]["origin"]
    generator = (ROOT / "tool/build_editorial.py").read_text(encoding="utf-8")
    localizer = (ROOT / "tool/build_editorial_locales.py").read_text(encoding="utf-8")
    for text in (generator, localizer):
        assert "country_wave02_en_it_20261109" not in text
    print("country wave02: 8 bilingual drafts with provenance; human review + 4 locales PENDING")


if __name__ == "__main__":
    validate()
