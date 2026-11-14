#!/usr/bin/env python3
"""Wave20 six-locale parity: real drafts are not qualified editorial approval.

Normal mode checks all existing localized records and prints honest progress.
--require-complete enforces 100/100 across EN/IT/ES/FR/DE/PT before merge.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORIES = ROOT / "data/editorial/batches/origin_stories_wave20_20261113.json"
MANIFEST = ROOT / "data/editorial/research_batches/wave20_first100_20261113.json"
LOCALES = {"en", "it", "es", "fr", "de", "pt"}
ORIGINAL = {"en", "it"}
YEARS = re.compile(r"\b(?:18|19|20)\d{2}\b")


def validate(require_complete=False):
    batch = json.loads(STORIES.read_text(encoding="utf-8"))
    cohort = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = batch["records"]
    ids = [item["observanceId"] for item in rows]
    fixed = {item["id"] for item in cohort["items"]}
    assert batch["count"] == len(rows) == len(fixed) == 100
    assert len(set(ids)) == 100 and set(ids) == fixed
    complete = []
    remaining = []
    for row in rows:
        rid = row["observanceId"]
        localized = row["locale"]
        present = set(localized)
        assert present in (ORIGINAL, LOCALES), (rid, "partial locale set", sorted(present))
        assert row["sources"] and row["sourceReviewNote"]
        assert "review" in row["sourceReviewNote"].lower()
        english_years = set(YEARS.findall(localized["en"]["origin"]))
        for lang, story in localized.items():
            for key in ("heading", "origin", "promoter", "purpose"):
                assert isinstance(story[key], str) and len(story[key].strip()) > (18 if key == "heading" else 40), (rid,lang,key)
            assert 2 <= len(story["facts"]) <= 5
            assert all(isinstance(f, str) and len(f.strip()) >= 25 for f in story["facts"]), (rid,lang)
            if lang not in ORIGINAL:
                years = set(YEARS.findall(story["origin"]))
                assert english_years <= years, (rid, lang, "years missing", sorted(english_years-years))
                assert story["origin"] != localized["en"]["origin"], (rid,lang,"not translated")
        (complete if present == LOCALES else remaining).append(rid)
    assert len(complete) + len(remaining) == 100
    if require_complete:
        assert not remaining, ("Wave20 remains incomplete",len(complete),len(remaining),remaining[:10])
    print("WAVE20_SIX_LOCALE_DRAFT_COVERAGE",f"{len(complete)}/100","pending",len(remaining),"qualified_human_review=NOT_CLAIMED")
    return len(complete)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    validate(args.require_complete)
