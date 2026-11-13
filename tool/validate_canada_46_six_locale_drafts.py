#!/usr/bin/env python3
"""Canada 46: source provenance, canonical alias reconciliation and six draft locales.

'46/46 researched drafts' does NOT mean 46 new canonical records or human review.
Nine candidate rows depend on the separate Wave20 localization PR #118.
Six candidates have full research-only dossiers but NO canonical identity.
"""
from pathlib import Path
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "data/editorial/batches"
AUDIT = ROOT / "data/editorial/research_batches/canada_46_candidate_reconciliation_20261113.json"
RESEARCH = ROOT / "data/editorial/research_batches"
BATCHES = {
    "origin_stories_wave21_canada_a_20261113.json",
    "origin_stories_wave21_canada_b1_20261113.json",
    "origin_stories_wave21_canada_b2_20261113.json",
    "origin_stories_wave21_canada_c_20261113.json",
}
RESEARCH_ONLY = {
    "canada_46_unmapped_origins_a_20261113.json",
    "canada_46_unmapped_origins_b_20261113.json",
}
LOCALES = {"en", "it", "es", "fr", "de", "pt"}
YEAR = re.compile(r"\b(?:18|19|20)\d{2}\b")
PR118 = "editorial/wave20-six-locales-20261113"

def validate_locales(rid, story, *, research_only=False):
    assert set(story["locale"]) == LOCALES, (rid, "missing six drafts")
    assert story["sources"], (rid, "missing individual sources")
    assert all(urlsplit(u).scheme == "https" and urlsplit(u).hostname
               for u in story["sources"]), (rid, "invalid sources")
    assert not story.get("runtimeRichEditorialApproved", False)
    if research_only:
        assert not story.get("humanFactualEditorialApproved", False)
        assert not story.get("allSixLocaleNativeReviewed", False)
    year = story["introducedYear"]
    first = story["firstObservedYear"]
    assert year is None or isinstance(year, int) and 1800 <= year <= 2026
    assert first is None or isinstance(first, int) and 1800 <= first <= 2026
    english_years = set(YEAR.findall(story["locale"]["en"]["origin"]))
    for lang, item in story["locale"].items():
        assert all(isinstance(item.get(k), str) and len(item[k]) > (18 if k == "heading" else 40)
                   for k in ("heading", "origin", "promoter", "purpose")), (rid,lang)
        assert len(item["origin"]) >= 260, (rid,lang,"short narrative")
        assert 2 <= len(item["facts"]) <= 5 and all(
            isinstance(f, str) and len(f) >= 25 for f in item["facts"]
        ), (rid,lang,"facts")
        missing_years = english_years - set(YEAR.findall(item["origin"]))
        assert not missing_years, (rid,lang,"missing chronology", sorted(missing_years))

def validate():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    rows = audit["rows"]
    assert len(rows) == 46
    assert len({r["candidateId"] for r in rows}) == 46
    assert all(r["sixLocaleDraftCoverage"] and not r["sixLocaleHumanReviewed"]
               for r in rows)
    groups = {
        "on_pr119": [r for r in rows if r["sourceResearchBranch"] == "editorial/canada-46-origin-audit-20261113"],
        "on_pr118": [r for r in rows if r["sourceResearchBranch"] == PR118],
    }
    assert len(groups["on_pr119"]) == 37
    assert len(groups["on_pr118"]) == 9
    national_rows = [r for r in rows if r.get("canonicalIdVerifiedByWave08")]
    other_rows = [r for r in rows if r.get("canonicalIdVerifiedByOtherWave")]
    research_rows = [r for r in rows if not r.get("canonicalIdVerifiedByWave08")
                     and not r.get("canonicalIdVerifiedByOtherWave")]
    assert (len(national_rows),len(other_rows),len(research_rows)) == (27,13,6)

    canonical = json.loads(
        (ROOT/"data/market/wave08_canada_primary_20261111.json").read_text(encoding="utf-8")
    )["records"]
    national_ids = {r["id"] for r in canonical}
    assert len(national_ids) == 27
    assert {r["canonicalIdVerifiedByWave08"] for r in national_rows} == national_ids

    prior, fresh = {}, {}
    for path in sorted(DIR.glob("origin_stories_*.json")):
        batch = json.loads(path.read_text(encoding="utf-8"))
        assert batch["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
        assert batch["count"] == len(batch["records"])
        for entry in batch["records"]:
            id_ = entry["observanceId"]
            assert id_ not in prior and id_ not in fresh, ("duplicate",id_,path)
            (fresh if path.name in BATCHES else prior)[id_] = entry
    assert len(fresh) == 23
    assert (national_ids & set(fresh)) == (national_ids - set(prior))
    assert len(national_ids & set(prior)) == 6
    for rid, entry in fresh.items():
        validate_locales(rid,entry)
        assert "review" in entry["sourceReviewNote"].lower()

    research={}
    for filename in sorted(RESEARCH_ONLY):
        batch=json.loads((RESEARCH/filename).read_text(encoding="utf-8"))
        assert batch["status"] == "RESEARCH_ONLY_NOT_CANONICAL_SIX_LOCALE_DRAFT"
        assert batch["count"] == len(batch["records"]) == 3
        for entry in batch["records"]:
            rid=entry["candidateId"]
            assert rid not in research and rid not in fresh and rid not in prior
            assert entry["scope"] in {"GLOBAL_SHARED_RESEARCH_ONLY",
                                     "GLOBAL_SHARED_CANADIAN_ORIGIN_RESEARCH_ONLY",
                                     "CANADA_NATIONAL_RESEARCH_ONLY"}
            validate_locales(rid,entry,research_only=True)
            research[rid]=entry
    assert {r["candidateId"] for r in research_rows} == set(research)
    assert len(research) == 6

    externally_verified = set()
    for r in rows:
        id_ = r.get("canonicalIdVerifiedByWave08") or r.get("canonicalIdVerifiedByOtherWave")
        assert r["sourceSpecificUrls"]
        assert r["sourceResearchSourceFile"].startswith("data/editorial/")
        if not id_:
            e=research[r["candidateId"]]
            assert r["sourceResearchSourceFile"].endswith(
                "canada_46_unmapped_origins_"+("a" if r["candidateId"] in
                 {"ca-international-women-s-day","ca-commonwealth-day",
                  "ca-international-transgender-day-of-visibility"} else "b")+"_20261113.json"
            )
            assert r["sourceSpecificUrls"] == e["sources"]
            assert r["yearEstablishedVerified"] == e["introducedYear"]
            assert r["firstObservedYearVerified"] == e["firstObservedYear"]
            assert r["primarySourceStatus"] == "INDIVIDUAL_ORIGIN_RESEARCH_COMPLETED_RESEARCH_ONLY"
        elif r["sourceResearchBranch"] == PR118:
            assert id_ in prior and r["sourceResearchSourceFile"].endswith(
                "origin_stories_wave20_20261113.json"
            )
            assert set(prior[id_]["locale"]) >= {"en","it"}
            # PR #118 is an external branch: 6/6 was checked at audit creation,
            # and MUST be rechecked at its exact head before either merge.
            externally_verified.add(id_)
            assert r["primarySourceStatus"] == "SOURCE_BACKED_SIX_LOCALE_DRAFT_EXISTS_IN_PR118_NOT_MAIN"
        else:
            assert id_ in prior or id_ in fresh, id_
            entry=prior.get(id_) or fresh[id_]
            validate_locales(id_,entry)
            assert r["sourceSpecificUrls"] == entry["sources"]
            assert r["sourceResearchSourceFile"].endswith(".json")
            assert r["sourceResearchBranch"] == "editorial/canada-46-origin-audit-20261113"
    assert len(externally_verified) == 6  # nine candidate aliases map to six Wave20 IDs
    assert audit["stats"]["sourceResearchedSixLocaleDraftCandidateCoverage"] == 46
    assert audit["stats"]["qualifiedHumanSixLocaleReviews"] == 0
    assert audit["stats"]["existingCanonicalDraftsOnPR119"] == 31
    assert audit["stats"]["existingCanonicalDraftsOnPR118"] == 9
    assert audit["stats"]["fullResearchOnlyNotCanonical"] == 6
    print("CANADA46_DRAFT_COVERAGE",46,"PR119_CANDIDATES",31,
          "PR118_DEPENDENT_CANDIDATES",9,"RESEARCH_ONLY",6,
          "NEW_CANONICAL_HISTORY_IDS",23,
          "HUMAN_EDITORIAL_APPROVAL","PENDING")

if __name__=="__main__":
    validate()
