#!/usr/bin/env python3
"""Generate consecutive, non-overlapping 100-ID historical-story work batches.

This is a source-linked RESEARCH AND PRODUCTION QUEUE, not a mass certification.
Never infer an original proposer, establishment year, legal status or story from
a calendar index. Missing story details remain explicitly unverified.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from editorial_1111_source_audit_queue import build as build_audit
from editorial_origin_wave100 import build as build_first_100

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = ROOT / "data/editorial/batches/origin_stories_primary_20261111.json"
OUTPUT = ROOT / "reports/editorial_origin_completion"
LANGUAGES = ("en", "it", "es", "fr", "de", "pt")
BATCH_SIZE = 100
SOURCE_GATES = {
    "EU_INDEX_REQUIRES_COUNTRY_PRIMARY_LAW_OR_ORIGINATOR",
    "AUSTRALIAN_DIPLOMATIC_CALENDAR_NOT_FOREIGN_STATUTORY_HOLIDAY",
    "PHILIPPINE_CULTURAL_INDEX_NOT_STATUTORY_HOLIDAY",
    "DISCOVERY_ONLY_NOT_VERIFIED",
}

def _read_origin():
    doc = json.loads(ORIGIN.read_text(encoding="utf-8"))
    entries = doc["records"]
    ids = [r["observanceId"] for r in entries]
    assert len(ids) == len(set(ids)) == doc["count"] >= 4
    assert set(doc["records"][0]["locale"]) >= {"en", "it"}
    return ids

def _ordering(row):
    """Prioritize existing useful research and primary-linked histories."""
    quality = row["sourceQualityGate"]
    has_primary = bool({"A_PRIMARY", "D_ORIGINATOR"} & set(row["sourceTiers"]))
    if row["editorialStage"] == "RUNTIME_REVIEWED":
        priority = 2    # Existing article: certify specific origin, not republish
    elif row["editorialStage"] != "NOT_RESEARCHED":
        priority = 0    # Existing draft: finish evidence/review
    elif quality in SOURCE_GATES:
        priority = 4    # Resolve national/legal/source identity first
    elif has_primary:
        priority = 1    # Stronger original-source research lead
    else:
        priority = 3
    return (priority, row["introducedYear"] is None,
            row["canonicalTitleEn"].casefold(), row["id"])

def _dossier(row, sequence):
    stage = row["editorialStage"]
    quality = row["sourceQualityGate"]
    has_previous = stage != "NOT_RESEARCHED"
    individual_evidence_missing = "SOURCE_CLASSIFICATION_AND_PRIMARY_VERIFICATION" in row["missingEditorialEvidence"]
    if stage == "RUNTIME_REVIEWED":
        work = "RECERTIFY_ORIGIN_OF_EXISTING_EDITORIAL_STORY"
    elif has_previous:
        work = "VERIFY_AND_COMPLETE_EXISTING_UNPUBLISHED_DRAFT"
    elif quality in SOURCE_GATES:
        work = "VALIDATE_INDIVIDUAL_PRIMARY_SOURCE_AND_LEGAL_STATUS_FIRST"
    else:
        work = "RESEARCH_AND_DRAFT_NEW_ORIGIN_STORY"
    return {
        "sequence": sequence,
        "observanceId": row["id"],
        "titleEn": row["canonicalTitleEn"],
        "scope": row["scope"],
        "countries": row["countries"],
        "periodKind": row["periodKind"],
        "catalogIntroducedYearUnrecertified": row["introducedYear"],
        "listedAuthorityNotNecessarilyOriginalProposer": row["recordAuthority"],
        "catalogSourceUrlsAreStartingLeads": row["sourceUrls"],
        "sourceTiers": row["sourceTiers"],
        "sourceQualityGate": quality,
        "individualSourceVerificationRequired": True,
        "explicitSourceRisk": individual_evidence_missing,
        "existingEditorialStage": stage,
        "existingEditorialContentInSeparatePack": bool(row["storyPublished"]),
        "existingIndividualResearchDraftInSeparateFile": bool(row["researchDraft"]) or (
            stage not in ("NOT_RESEARCHED", "RUNTIME_REVIEWED")),
        "workType": work,
        "historyStatus": "NOT_INDEPENDENTLY_ORIGIN_CERTIFIED",
        "storyPublicationAction": "NONE_UNTIL_FACT_AND_TRANSLATION_GATES_PASS",
        "missingEvidence": row["missingEditorialEvidence"],
        "researchFields": {
            "originalEstablishingActOrFirstPartySource": None,
            "formalIntroductionYear": None,
            "firstObservanceYear": None,
            "whyCalendarDateWasChosen": None,
            "historicalOriginAndMilestones": None,
            "verifiedProposerIfKnown": None,
            "currentOrganizingAuthorityIfKnown": None,
            "purposeAndSignificance": None,
            "specificContextualFacts": [],
        },
        "localeReview": {locale: "PENDING_ORIGIN_SPECIFIC_FACT_AND_TRANSLATION_REVIEW"
                         for locale in LANGUAGES},
    }

def build():
    audit = build_audit()
    by_id = {r["id"]: r for r in audit["rows"]}
    assert len(by_id) == audit["catalogTotal"] >= 1111
    certified_origin_ids = set(_read_origin())
    assert certified_origin_ids <= set(by_id)

    pending = set(by_id) - certified_origin_ids
    first = build_first_100()
    first_ids = [d["observanceId"] for d in first["dossiers"]]
    # Preserve the original first 100 as wave 001; never reassign any of them
    # within this catalog snapshot. Future catalog expansion is re-audited.
    assert len(first_ids) == 100 and len(set(first_ids)) == 100
    assert set(first_ids) <= pending

    remaining = sorted((by_id[oid] for oid in pending - set(first_ids)),
                       key=_ordering)
    ordered = first_ids + [r["id"] for r in remaining]
    assert len(ordered) == len(pending)
    assert len(set(ordered)) == len(ordered)
    assert set(ordered).isdisjoint(certified_origin_ids)

    files = {}
    work_types = Counter()
    for start in range(0, len(ordered), BATCH_SIZE):
        number = start // BATCH_SIZE + 1
        ids = ordered[start:start + BATCH_SIZE]
        dossiers = [_dossier(by_id[oid], start + n + 1)
                    for n, oid in enumerate(ids)]
        work_types.update(d["workType"] for d in dossiers)
        filename = f"batch_{number:03d}.json"
        files[filename] = {
            "schemaVersion": 1,
            "batchNumber": number,
            "rangeStart": start + 1,
            "rangeEnd": start + len(ids),
            "recordCount": len(ids),
            "batchLimit": BATCH_SIZE,
            "reviewState": "RESEARCH_WORKLIST_NOT_100_PUBLISHED_HISTORIES",
            "catalogVersion": audit["catalogVersion"],
            "dossiers": dossiers,
        }

    digest = hashlib.sha256("\n".join(ordered).encode("utf-8")).hexdigest()
    index = {
        "schemaVersion": 1,
        "datasetVersion": audit["catalogVersion"],
        "catalogTotal": audit["catalogTotal"],
        "individuallyOriginResearched": len(certified_origin_ids),
        "outstandingOriginResearch": len(pending),
        "legacyReviewedEditorialCount": audit["publishedEnglishRichStories"],
        "batchLimit": BATCH_SIZE,
        "batchCount": len(files),
        "batchSizes": [d["recordCount"] for d in files.values()],
        "orderedIdSha256": digest,
        "workTypeCounts": dict(sorted(work_types.items())),
        "progress": {
            "dossiersScheduled": len(ordered),
            "newHistoricalArticlesCertifiedByThisQueue": 0,
            "newSixLocaleTranslationsCertifiedByThisQueue": 0,
            "remainingToIndividuallyResearch": len(pending),
        },
        "guardrails": [
            "Never treat listed source links as independent historical certification.",
            "Do not fabricate a proposer, introduced year, date rationale or customs.",
            "Existing reviewed articles remain separate from independently researched origin history.",
            "If new origin stories are approved, regenerate queue from main to remove their IDs.",
            "If catalog grows, regenerate; 1111 is a minimum, never a fixed maximum.",
            "Do not publish draft narratives or bypass human editorial/factual review.",
        ],
        "batches": [
            {"file": name, "number": payload["batchNumber"],
             "size": payload["recordCount"],
             "rangeStart": payload["rangeStart"],
             "rangeEnd": payload["rangeEnd"]}
            for name, payload in files.items()
        ],
    }
    return index, files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUTPUT)
    args = parser.parse_args()
    index, files = build()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for old in args.output_dir.glob("batch_*.json"):
        old.unlink()
    for name, payload in files.items():
        (args.output_dir / name).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ORIGIN_COMPLETION_WAVES", json.dumps({
        "catalog": index["catalogTotal"],
        "originResearched": index["individuallyOriginResearched"],
        "pending": index["outstandingOriginResearch"],
        "waves": index["batchCount"],
        "batchSizes": index["batchSizes"],
        "certifiedNewStories": index["progress"]["newHistoricalArticlesCertifiedByThisQueue"],
    }, sort_keys=True))

if __name__ == "__main__":
    main()
