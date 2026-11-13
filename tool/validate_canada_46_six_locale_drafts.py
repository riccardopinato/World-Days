#!/usr/bin/env python3
"""Canada 46: prove canonical reconciliation and 21 six-locale SOURCE DRAFTS.

A passing machine check is NOT human fact-checking or native review.
The 46 source-index entries do not represent 46 newly created canonical IDs.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/editorial/research_batches/canada_46_candidate_reconciliation_20261113.json"
BATCHES = (
    "origin_stories_wave21_canada_a_20261113.json",
    "origin_stories_wave21_canada_b1_20261113.json",
    "origin_stories_wave21_canada_b2_20261113.json",
    "origin_stories_wave21_canada_c_20261113.json",
)
DIR = ROOT / "data/editorial/batches"
LOCALES = {"en", "it", "es", "fr", "de", "pt"}
YEAR = re.compile(r"\b(?:18|19|20)\d{2}\b")


def validate():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    candidates = a["rows"]
    assert len(candidates) == 46
    ids = [r["candidateId"] for r in candidates]
    assert len(set(ids)) == 46
    national = [r for r in candidates if r.get("canonicalIdVerifiedByWave08")]
    other = [r for r in candidates if r.get("canonicalIdVerifiedByOtherWave")]
    pending = [r for r in candidates if not r.get("canonicalIdVerifiedByWave08")
               and not r.get("canonicalIdVerifiedByOtherWave")]
    assert (len(national), len(other), len(pending)) == (27, 13, 6)
    canonical = json.loads(
        (ROOT / "data/market/wave08_canada_primary_20261111.json").read_text(encoding="utf-8")
    )
    national_ids = {r["id"] for r in canonical["records"]}
    assert len(national_ids) == 27
    assert {r["canonicalIdVerifiedByWave08"] for r in national} == national_ids

    prior = {}
    new = {}
    assert all("CANADA" in b.upper() for b in BATCHES)
    for path in sorted(DIR.glob("origin_stories_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
        assert data["count"] == len(data["records"])
        for row in data["records"]:
            rid = row["observanceId"]
            assert rid not in prior and rid not in new, (rid, path)
            (new if path.name in BATCHES else prior)[rid] = row
    assert len(new) == 23
    assert (national_ids & set(new)) == national_ids - set(prior)
    assert len(national_ids & set(prior)) == 6
    assert {r["canonicalIdVerifiedByOtherWave"] for r in other} <= (set(prior) | set(new))

    for rid, record in new.items():
        assert set(record["locale"]) == LOCALES, rid
        assert record["sources"] and all(
            urlsplit(u).scheme == "https" and urlsplit(u).hostname
            for u in record["sources"]
        )
        assert not record.get("runtimeRichEditorialApproved", False)
        assert "review" in record["sourceReviewNote"].lower()
        year = record["introducedYear"]
        first = record["firstObservedYear"]
        assert year is None or 1800 <= year <= 2026
        assert first is None or 1800 <= first <= 2026
        canonical_years = set(YEAR.findall(record["locale"]["en"]["origin"]))
        for locale, content in record["locale"].items():
            assert all(isinstance(content[k], str) and len(content[k]) > (18 if k == "heading" else 40)
                       for k in ("heading", "origin", "promoter", "purpose")), (rid, locale)
            assert len(content["origin"]) >= 260, (rid, locale, "short origin")
            assert 2 <= len(content["facts"]) <= 5, (rid, locale)
            assert all(isinstance(f, str) and len(f) >= 25 for f in content["facts"])
            assert canonical_years <= set(YEAR.findall(content["origin"])), (
                rid, locale, sorted(canonical_years - set(YEAR.findall(content["origin"])))
            )
    assert not any(row.get("sixLocaleHumanReviewed") for row in candidates)
    print("CANADA_46_RECONCILED", 46, "NATIONAL", 27, "PRIOR_SOURCE", 6,
          "NEW_SOURCE_SIX_LOCALE_DRAFT", len(new), "OTHER_IDENTIFIED_ALIASES", 13,
          "OTHER_IDENTITY_OR_ORIGIN_PENDING", 6, "HUMAN_REVIEW", "PENDING")


if __name__ == "__main__":
    validate()
