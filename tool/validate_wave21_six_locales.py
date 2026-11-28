#!/usr/bin/env python3
"""Validate Wave21's immutable ID cohort and source-linked six-locale draft coverage.

This is a technical gate, never an AI or human editorial certification.
Use --require-complete to block an incomplete cohort from being merged as complete.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COHORT = ROOT / "data/editorial/waves/wave21_cohort.json"
DEFAULT_DRAFTS = ROOT / "data/editorial/batches/origin_stories_wave21_20261116.json"
LANGS = ("en", "it", "es", "fr", "de", "pt")
FIELDS = ("heading", "origin", "promoter", "purpose")


def validate(drafts_path: Path, require_complete: bool) -> int:
    cohort = json.loads(COHORT.read_text(encoding="utf-8"))
    ids = cohort["observanceIds"]
    assert cohort["wave"] == 21 and cohort["schemaVersion"] == 1
    assert len(ids) == cohort["recordCount"] == 100
    assert len(set(ids)) == len(ids) and all(isinstance(x, str) and x.strip() for x in ids)
    digest = hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()
    assert digest == cohort["cohortIdSha256"], "Frozen cohort hash mismatch"
    assert cohort["runtimeRichEditorialApproved"] is False
    assert cohort["humanFactReview"] == cohort["humanSixLocaleReview"] == "PENDING"

    rows = []
    if drafts_path.exists():
        batch = json.loads(drafts_path.read_text(encoding="utf-8"))
        rows = batch["records"]
        assert batch.get("count") == len(rows), "Batch count mismatch"
    seen = set()
    complete = 0
    bilingual = 0
    blocked = 0
    for row in rows:
        rid = row["observanceId"]
        assert rid in ids, ("Out-of-cohort ID", rid)
        assert rid not in seen, ("Duplicate ID", rid)
        seen.add(rid)
        locale = row.get("locale", {})
        assert isinstance(locale, dict)
        assert set(locale).issubset(set(LANGS))
        if row.get("status") in ("BLOCKED", "HOLD_SOURCE_DISPUTE"):
            blocked += 1
            continue
        sources = row.get("sources")
        assert isinstance(sources, list) and sources, ("Missing individual sources", rid)
        assert all(isinstance(url, str) and url.startswith("https://") and len(url) > 8 for url in sources), ("Invalid source URL", rid)
        assert len(set(sources)) == len(sources), ("Duplicate source URL", rid)
        for year_field in ("introducedYear", "firstObservedYear"):
            year = row.get(year_field)
            assert year is None or (type(year) is int and 1800 <= year <= 2100), (rid, year_field, year)
        for lang, story in locale.items():
            assert isinstance(story, dict), (rid, lang)
            for field in FIELDS:
                assert isinstance(story.get(field), str) and story[field].strip(), (rid, lang, field)
            facts = story.get("facts")
            assert isinstance(facts, list) and 2 <= len(facts) <= 5
            assert all(isinstance(fact, str) and fact.strip() for fact in facts)
        if {"en", "it"}.issubset(locale):
            bilingual += 1
        if set(locale) == set(LANGS):
            complete += 1
    pending = len(ids) - complete
    print(f"WAVE21_COHORT_PASS sha256={digest} en_it={bilingual}/100 six_locale={complete}/100 blocked={blocked} pending={pending} human_review=PENDING")
    if require_complete and (complete != 100 or blocked):
        raise SystemExit("Wave21 six-locale source-linked coverage incomplete: fail closed")
    return complete


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--drafts", type=Path, default=DEFAULT_DRAFTS)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    validate(args.drafts, args.require_complete)
