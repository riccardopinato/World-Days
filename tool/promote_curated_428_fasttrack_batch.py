#!/usr/bin/env python3
"""Fast Track 428: idempotent, source-SHA-pinned batch import of AI-reviewed origin narratives.

The separate reviewed ledger authorizes only its explicitly selected files.
The offline QA is a gate, NOT a factual certificate. Unresolved individual
rows are skipped/HOLD; never overwrite a non-contextual editorial entry.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/data"
REPORTS = ROOT / "reports/editorial_curated_428_origin_research"
LEDGER = ROOT / "data/editorial/reviews/curated_428_fasttrack_c01_bulk_20261127.json"
QA = REPORTS / "fasttrack_qa_cohort_01.json"
RESULT = REPORTS / "fasttrack_bulk_c01_runtime_import.json"
LANGS = ("en", "it", "es", "fr", "de", "pt")
CONTEXT = "AI_CONTEXTUAL_SIX_LOCALE"
REVIEWED = "AI_SOURCE_REVIEWED_SIX_LOCALE"
VERSION = "2026.11.27.2"
GROUPS = {
    "CZECH_STATUTE_HISTORY": ("ppropo.mpsv.cz", "zakon_245_2000"),
    "ESTONIAN_FLAG_ACT": ("www.riigiteataja.ee", "530012023002"),
    "FINNISH_OFFICIAL_FLAG_CALENDAR": ("finland.fi", "the-finnish-flag"),
    "ITALIAN_STATE_CEREMONIAL_CALENDAR": ("presidenza.governo.it", "giornate.html"),
    "SLOVAK_STATUTE_HISTORY": ("www.slov-lex.sk", "1993/241"),
}

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def validate_approval(item):
    assert item["reviewStatus"] == "AI_EDITORIAL_REVIEWED"
    assert item["permission"] == "REVIEWED_EDITORIAL_ACCEPT_IF_DETERMINISTIC_QA_PASS"
    assert item["humanSignoff"] is False
    assert item["historicalPageIndividuallyRefetched"] is False
    group = item["sourceGroup"]
    assert group in GROUPS
    authority = urlsplit(item["calendarSourceReviewed"])
    assert authority.scheme == "https"
    host, path_fragment = GROUPS[group]
    assert authority.hostname == host and path_fragment in authority.path

def run():
    approval = load(LEDGER)
    assert approval["mode"] == "APP_FACTORY_CORE_V27_FAST_TRACK_AI_BATCH"
    assert approval["reviewAuthority"] == "USER_DELEGATED_AI_EDITORIAL_REVIEW"
    assert approval["humanSignoffClaim"] is False
    assert approval["sourceUrlsPerRecordAllRefetched"] is False
    assert approval["candidateCount"] == len(approval["records"]) > 0
    assert approval["originalCohort"] == 100
    audit = load(QA)
    assert audit["mode"] == "FASTTRACK_DETERMINISTIC_OFFLINE_ONLY"
    assert audit["cohort"] == 1 and audit["processedCanonicalIds"] == 100
    assert audit["duplicateIds"] == [] and audit["extras"] == []
    qa_by_id = {r["id"]: r for r in audit["records"]}
    official = load(ASSETS / "official_core.json")
    canonical = {r["id"]: r for r in official["records"]}
    assert len(canonical) == 947
    assert official["datasetVersion"] == "2026.11.27.1", "unexpected source pack version"
    chosen, holds, seen_sources = {}, [], set()
    for entry in approval["records"]:
        validate_approval(entry)
        rel = entry["sourceFile"]
        assert rel.startswith("data/editorial/research/curated_428_cohort01_")
        assert rel.endswith(".json") and ".." not in rel
        assert rel not in seen_sources, "duplicate source file in AI review ledger"
        seen_sources.add(rel)
        path = ROOT / rel
        if not path.is_file():
            raise AssertionError(("source_file_missing", rel))
        assert git_blob(path.read_bytes()) == entry["sourceBlobSha"], ("stale_source_sha", rel)
        record = load(path)
        oid = record["id"]
        assert record["cohort"] == 1 and oid not in chosen and oid in canonical
        assert record["review"] in ("PENDING", "AI_REVIEWED")
        assert record["runtimeRichEditorialApproved"] is False
        assert set(record["narratives"]) == set(LANGS)
        assert all(len(record["narratives"][lang].strip()) >= 180 for lang in LANGS)
        assert record["country"] in canonical[oid]["countries"]
        evidence = record.get("sourceEvidence") or []
        assert evidence and all(
            isinstance(s, dict) and urlsplit(s.get("url", "")).scheme == "https"
            and len(str(s.get("claim", "")).strip()) >= 35 for s in evidence
        ), ("source_evidence_bad", oid)
        qa_row = qa_by_id.get(oid)
        assert qa_row is not None, ("not_in_100_queue", oid)
        if qa_row["outcome"] != "OFFLINE_QA_PASS_SOURCE_AND_SEMANTIC_REVIEW_REQUIRED":
            holds.append({
                "id": oid, "state": "REVIEW_OR_HOLD",
                "reason": qa_row["outcome"],
                "codes": qa_row["errors"] + qa_row["reviews"] + qa_row["flags"],
            })
            continue
        chosen[oid] = (record, entry, [s["url"] for s in evidence])
    assert len(chosen) + len(holds) == len(approval["records"])
    assert chosen, "no source-reviewed records eligible for batch import"

    docs, before, master = {}, None, None
    for lang in LANGS:
        pack = load(ASSETS / f"editorial_{lang}.json")
        entries = pack["entries"]
        order = [r["observanceId"] for r in entries]
        assert len(order) == len(set(order)) == pack["entryCount"] == 947
        if master is None:
            master = order
        else:
            assert master == order, ("locale_order_drift", lang)
        count = sum(r["status"] == CONTEXT for r in entries)
        if before is None:
            before = count
        else:
            assert before == count, ("status_parity", lang)
        by_id = {r["observanceId"]: r for r in entries}
        for oid, (story, entry, urls) in chosen.items():
            dest = by_id[oid]
            assert dest["status"] == CONTEXT, ("overwrite_prevented", lang, oid)
            dest["origin"] = story["narratives"][lang].strip()
            dest["status"] = REVIEWED
            dest["lastReviewedAt"] = approval["reviewedAt"]
            dest["sourcePolicy"] = (
                "App Factory Fast Track: AI editorial chronology/translation review; "
                "official country calendar checked, per-story historical URLs "
                "not all independently reopened; not human-certified."
            )
            dest["institutionalSourceUrls"] = urls
            dest["aiEditorialProvenance"] = {
                "reviewLevel": "AI_EDITORIAL_REVIEWED",
                "reviewDate": approval["reviewedAt"],
                "sourceResearchFile": entry["sourceFile"],
                "sourceResearchBlobSha": entry["sourceBlobSha"],
                "countryCalendarSource": entry["calendarSourceReviewed"],
                "allHistoricPagesIndependentlyReopened": False,
                "humanSignoff": False,
            }
        pack["datasetVersion"] = VERSION
        docs[lang] = pack
    assert before == 426, ("prior_integrations_changed", before)
    official["datasetVersion"] = VERSION
    for name in ("origin_review_index.json",):
        path = ASSETS / name
        if path.exists():
            val = load(path)
            val["datasetVersion"] = VERSION
            write(path, val)
    write(ASSETS / "official_core.json", official)
    for lang, pack in docs.items():
        write(ASSETS / f"editorial_{lang}.json", pack)

    index_path = REPORTS / "index.json"
    if index_path.exists():
        index = load(index_path)
        assert index["contextualOriginPending"] == 426
        previous = set(index.get("fastTrackIntegratedIds", []))
        assert len(previous) == 2 and not (set(chosen) & previous)
        all_ids = sorted(previous | set(chosen))
        index["fastTrackIntegratedIds"] = all_ids
        index["contextualOriginPending"] = before - len(chosen)
        index["notYetPersonallyResearched"] = before - len(chosen)
        index["nonContextualRich"] = 947 - before + len(chosen)
        for oid, (story, _entry, _urls) in chosen.items():
            country = story["country"]
            assert index["countriesPending"][country] > 0
            index["countriesPending"][country] -= 1
        write(index_path, index)
    result = {
        "schemaVersion": 1,
        "mode": "APP_FACTORY_FAST_TRACK_AI_BATCH_NO_HUMAN_SIGNOFF",
        "originalCohort": 100,
        "alreadyIntegratedOnMainBeforeThisBatch": 2,
        "candidateCount": len(approval["records"]),
        "batchAiEditorialReviewedIntegrated": len(chosen),
        "integratedIds": sorted(chosen),
        "individualHolds": holds,
        "holdCount": len(holds),
        "contextualBefore": before,
        "contextualAfter": before - len(chosen),
        "richEditorialAfter": 947 - before + len(chosen),
        "editorialLocalizations": list(LANGS),
        "sourceIntegrityVerified": True,
        "sourceSpecificHistoricalPagesAllIndividuallyReopened": False,
        "humanCertified": False,
        "physicalReleaseCertified": False,
        "contentPackVersion": VERSION,
        "sourceReviewedOnPRNotMainUntilMerge": True,
    }
    write(RESULT, result)
    print("FASTTRACK_428_BULK_REVIEWED_IMPORTED", json.dumps({
        "candidates": len(approval["records"]),
        "imported": len(chosen), "holds": len(holds),
        "richAfter": result["richEditorialAfter"],
        "contextualAfter": result["contextualAfter"],
        "version": VERSION}, sort_keys=True))

if __name__ == "__main__":
    run()
