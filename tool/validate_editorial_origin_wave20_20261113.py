#!/usr/bin/env python3
"""Fail-closed structural and cohort-consistency gate for Wave20 source research.

This validates provenance fields and bookkeeping, NOT the truth of linked
historical claims or qualified six-locale editorial approval.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/editorial/research_batches/wave20_first100_20261113.json"
STORIES = ROOT / "data/editorial/batches/origin_stories_wave20_20261113.json"

def check():
    cohort = json.loads(MANIFEST.read_text(encoding="utf-8"))
    wave = json.loads(STORIES.read_text(encoding="utf-8"))
    items = cohort["items"]
    stories = wave["records"]
    assert cohort["recordCount"] == cohort["batchSizeLimit"] == len(items) == 100
    assert len({r["id"] for r in items}) == 100
    assert wave["count"] == len(stories)
    story_ids = [r["observanceId"] for r in stories]
    assert len(set(story_ids)) == len(story_ids)
    assert set(story_ids) <= {r["id"] for r in items}
    assert cohort["progress"]["individuallyResearchedInThisBlock"] == len(stories)
    assert cohort["progress"]["awaitingIndependentResearch"] + len(stories) + cohort["progress"]["blockedForMissingOriginalSource"] == 100
    assert cohort["progress"]["qualifiedSixLocaleHumanReviewed"] == 0
    assert cohort["progress"]["publishedAsRichEditorial"] == 0
    by_id = {r["id"]: r for r in items}
    for story in stories:
        oid = story["observanceId"]
        item = by_id[oid]
        assert item["storyFile"] == "data/editorial/batches/origin_stories_wave20_20261113.json", oid
        assert item["originResearchStage"] == "SOURCE_LINKED_IT_EN_ORIGIN_DRAFT_PENDING_QUALIFIED_EDITORIAL_REVIEW", oid
        assert item["formalIntroductionYearVerified"] == story["introducedYear"], oid
        assert item["firstObservedYearVerified"] == story["firstObservedYear"], oid
        # An earlier unofficial observance may precede formal UN/institutional
        # designation; preserve that distinction instead of rejecting history.
        for year_field in ("introducedYear", "firstObservedYear"):
            year = story[year_field]
            assert year is None or (isinstance(year, int) and 1800 <= year <= 2100), (oid, year_field)
        sources = story["sources"]
        assert len(sources) >= 1 and len(sources) == len(set(sources)), oid
        assert all(url.startswith("https://") for url in sources), oid
        assert set(sources) == set(item["verifiedSourceUrls"]), oid
        for locale in ("en", "it"):
            article = story["locale"][locale]
            for field in ("heading", "origin", "promoter", "purpose"):
                assert isinstance(article[field], str) and len(article[field].strip()) > 15, (oid, locale, field)
            assert 2 <= len(article["facts"]) <= 5, (oid, locale)
            assert all(isinstance(f, str) and len(f.strip()) >= 15 for f in article["facts"]), (oid, locale)
        assert "review" in story["sourceReviewNote"].lower(), oid
    for item in items:
        if item["id"] not in story_ids:
            assert item["storyFile"] is None, item["id"]
    print(f"WAVE20_COHORT_STRUCTURAL_PASS researched={len(stories)} pending={cohort['progress']['awaitingIndependentResearch']} blocked={cohort['progress']['blockedForMissingOriginalSource']} /100; factual/native editorial review NOT certified")

if __name__ == "__main__":
    check()
