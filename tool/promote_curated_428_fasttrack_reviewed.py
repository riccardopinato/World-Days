#!/usr/bin/env python3
"""Fast Track: promote only exact-source, explicitly AI-reviewed origins into app packs.

Run after 947-catalog curation, before build_content_pack.py. No blanket
promotion from AI_DRAFT, no overwrite of canonical facts or user-owned data.
"""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/data"
LEDGER_PATH = ROOT / "data/editorial/reviews/curated_428_fasttrack_czech_civic_ai_review_20261127.json"
QA_PATH = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_qa_cohort_01.json"
REPORT_PATH = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_runtime_import.json"
LANGS = ("en", "it", "es", "fr", "de", "pt")
STATUS = "AI_SOURCE_REVIEWED_SIX_LOCALE"
CONTEXT = "AI_CONTEXTUAL_SIX_LOCALE"
VERSION = "2026.11.27.1"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def blob_sha(payload):
    return hashlib.sha1(b"blob " + str(len(payload)).encode("ascii") + b"\0" + payload).hexdigest()


def run():
    approval = read(LEDGER_PATH)
    assert approval["mode"] == "APP_FACTORY_CORE_V27_FAST_TRACK_AI"
    assert approval["reviewAuthority"] == "USER_DELEGATED_AI_EDITORIAL_REVIEW"
    assert approval["humanSignoffClaim"] is False
    certs = approval["records"]
    ids = [row["observanceId"] for row in certs]
    assert len(ids) == len(set(ids)) and len(ids) > 0
    qa = read(QA_PATH)
    assert qa["mode"] == "FASTTRACK_DETERMINISTIC_OFFLINE_ONLY"
    assert qa["cohort"] == 1 and qa["processedCanonicalIds"] == 100
    audit = {row["id"]: row for row in qa["records"]}
    official = read(ASSETS / "official_core.json")
    catalog = {row["id"]: row for row in official["records"]}
    assert len(catalog) == 947
    row_by_id = {}
    for approved in certs:
        oid = approved["observanceId"]
        source_path = ROOT / approved["sourceFile"]
        assert source_path.is_file(), oid
        assert blob_sha(source_path.read_bytes()) == approved["sourceBlobSha"], (oid, "source SHA changed")
        row = read(source_path)
        assert row["id"] == oid and row["cohort"] == 1 and oid in catalog
        assert row["review"] == "AI_REVIEWED" and "SOURCE_CHECKED" in row["status"], oid
        assert row["scopeDecision"] == approved["scope"]
        assert row["reviewEvidence"]["sourceChecked"] == approved["officialCivicDesignationSource"], oid
        assert row["runtimeRichEditorialApproved"] is False, "research staging must not self-publish"
        assert set(row["narratives"]) == set(LANGS)
        assert all(len(row["narratives"][x].strip()) >= 180 for x in LANGS)
        assert audit[oid]["outcome"] == "OFFLINE_QA_PASS_SOURCE_AND_SEMANTIC_REVIEW_REQUIRED", (oid, audit[oid])
        assert approved["reviewStatus"] == "AI_EDITORIAL_REVIEWED" and approved["runtimeImportAllowed"] is True
        source_urls = [x["url"] for x in row["sourceEvidence"]]
        assert approved["officialCivicDesignationSource"] in source_urls
        assert approved["historicalSource"] in source_urls
        assert all(urlsplit(s).scheme == "https" and urlsplit(s).hostname for s in source_urls)
        assert row["country"] in catalog[oid]["countries"]
        if row.get("documentedIntroductionYear") is not None:
            assert isinstance(row["documentedIntroductionYear"], int)
        row_by_id[oid] = (row, approved, source_urls)
    master_order = None
    old_status_counts = None
    locale_docs = {}
    for lang in LANGS:
        path = ASSETS / f"editorial_{lang}.json"
        pack = read(path)
        entries = pack["entries"]
        sequence = [r["observanceId"] for r in entries]
        assert len(sequence) == len(set(sequence)) == pack["entryCount"] == 947
        if master_order is None:
            master_order = sequence
        else:
            assert sequence == master_order, ("locale order changed", lang)
        by_id = {r["observanceId"]: r for r in entries}
        assert set(ids) <= set(by_id)
        if old_status_counts is None:
            old_status_counts = sum(r["status"] == CONTEXT for r in entries)
        else:
            assert sum(r["status"] == CONTEXT for r in entries) == old_status_counts, lang
        for oid in ids:
            row, approved, urls = row_by_id[oid]
            entry = by_id[oid]
            assert entry["status"] == CONTEXT, (oid, lang, "cannot overwrite non-contextual editorial")
            entry["origin"] = row["narratives"][lang].strip()
            entry["status"] = STATUS
            entry["lastReviewedAt"] = approved["reviewedAt"]
            entry["sourcePolicy"] = (
                "App Factory Fast Track AI historical and six-locale review; "
                "Czech statutory significant-day designation and historical accession "
                "sources verified, without claim of professional human certification."
            )
            entry["aiEditorialProvenance"] = {
                "reviewLevel": "AI_EDITORIAL_REVIEWED",
                "reviewDate": approved["reviewedAt"],
                "sourceResearchFile": approved["sourceFile"],
                "sourceResearchBlobSha": approved["sourceBlobSha"],
                "legalRecognitionSource": approved["officialCivicDesignationSource"],
                "historicalEvidenceSource": approved["historicalSource"],
                "humanSignoff": False,
            }
        pack["datasetVersion"] = VERSION
        locale_docs[lang] = pack
    assert old_status_counts == 428, ("unexpected pre-import backlog", old_status_counts)
    assert len(ids) <= old_status_counts
    official["datasetVersion"] = VERSION
    for extra_name in ("origin_review_index.json",):
        path = ASSETS / extra_name
        if path.exists():
            extra = read(path)
            extra["datasetVersion"] = VERSION
            write(path, extra)
    write(ASSETS / "official_core.json", official)
    for lang, pack in locale_docs.items():
        write(ASSETS / f"editorial_{lang}.json", pack)
    report = {
        "schemaVersion": 1, "reviewAuthority": approval["reviewAuthority"],
        "promotion": "AI_EDITORIAL_REVIEWED_TO_APP_BUILD", "humanCertified": False,
        "sourceCohort": 1, "originalCohortSize": 100,
        "aiReviewedAndAppBuildIntegrated": len(ids),
        "integratedIds": ids, "preexistingOriginRich": 519,
        "originRichInAppBuild": 947 - old_status_counts + len(ids),
        "contextualOriginsRemainingInAppBuild": old_status_counts - len(ids),
        "contentPackVersion": VERSION,
        "sourceIntegrityVerified": True, "sixLocaleParityVerified": True,
        "releasedOnMain": False, "physicalReleaseCertified": False,
        "sourceReviewPendingOtherIds": 428 - len(ids),
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    write(REPORT_PATH, report)
    print("FASTTRACK_CURATED_428_IMPORTED", json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    run()
