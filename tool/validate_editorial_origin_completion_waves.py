#!/usr/bin/env python3
"""Fail-closed coverage check for every 100-record origin-history work batch."""
import json
from pathlib import Path
from editorial_origin_completion_waves import build, OUTPUT, BATCH_SIZE, LANGUAGES
from editorial_1111_source_audit_queue import build as build_audit

index, files = build()
stored_index = json.loads((OUTPUT / "index.json").read_text(encoding="utf-8"))
assert stored_index == index, "stale batch index"
assert index["schemaVersion"] == 1
assert index["batchLimit"] == BATCH_SIZE == 100
assert index["catalogTotal"] >= 1111
assert index["individuallyOriginResearched"] >= 4
assert index["outstandingOriginResearch"] == index["catalogTotal"] - index["individuallyOriginResearched"]
assert index["batchCount"] == (index["outstandingOriginResearch"] + 99) // 100
assert len(files) == index["batchCount"]
assert index["progress"]["newHistoricalArticlesCertifiedByThisQueue"] == 0
assert index["progress"]["newSixLocaleTranslationsCertifiedByThisQueue"] == 0
assert len(list(OUTPUT.glob("batch_*.json"))) == len(files), "stale or missing wave outputs"

ids = []
for i, (name, expected) in enumerate(files.items(), start=1):
    saved = json.loads((OUTPUT / name).read_text(encoding="utf-8"))
    assert saved == expected, ("stale batch", name)
    assert saved["batchNumber"] == i
    assert saved["rangeStart"] == len(ids) + 1
    assert saved["rangeEnd"] == len(ids) + saved["recordCount"]
    assert saved["recordCount"] == 100 or i == index["batchCount"], "partial nonfinal batch"
    assert saved["reviewState"] == "RESEARCH_WORKLIST_NOT_100_PUBLISHED_HISTORIES"
    for d in saved["dossiers"]:
        assert d["catalogSourceUrlsAreStartingLeads"]
        assert all(u.startswith("https://") for u in d["catalogSourceUrlsAreStartingLeads"])
        assert d["individualSourceVerificationRequired"] is True
        assert d["historyStatus"] == "NOT_INDEPENDENTLY_ORIGIN_CERTIFIED"
        assert d["storyPublicationAction"] == "NONE_UNTIL_FACT_AND_TRANSLATION_GATES_PASS"
        assert set(d["localeReview"]) == set(LANGUAGES)
        assert all(s == "PENDING_ORIGIN_SPECIFIC_FACT_AND_TRANSLATION_REVIEW" for s in d["localeReview"].values())
        assert d["researchFields"] == {
            "originalEstablishingActOrFirstPartySource": None,
            "formalIntroductionYear": None,
            "firstObservanceYear": None,
            "whyCalendarDateWasChosen": None,
            "historicalOriginAndMilestones": None,
            "verifiedProposerIfKnown": None,
            "currentOrganizingAuthorityIfKnown": None,
            "purposeAndSignificance": None,
            "specificContextualFacts": [],
        }, "fabricated or prematurely certified history"
        ids.append(d["observanceId"])

assert len(ids) == len(set(ids)) == index["outstandingOriginResearch"]
audit_ids = {r["id"] for r in build_audit()["rows"]}
assert set(ids) <= audit_ids
assert index["individuallyOriginResearched"] == len(audit_ids - set(ids))
assert index["batchSizes"] == [len(f["dossiers"]) for f in files.values()]
assert sum(index["batchSizes"]) == len(ids)
print(f"PASS: {len(ids)} outstanding identities, {len(files)} non-overlapping "
      f"research batches of at most 100, zero invented histories.")
