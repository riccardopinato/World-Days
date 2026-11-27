#!/usr/bin/env python3
"""Fast Track 85: AI-scoped, SHA-pinned, fail-closed six-locale import.

All 85 already-prepared but not-yet-integrated histories are inspected.
Only explicitly reviewed candidates with clean per-ID QA enter runtime.
Historical source pages were spot-checked, not individually refetched for every
record. Individual source uncertainties must remain HOLD, not be suppressed.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/data"
REPORTS = ROOT / "reports/editorial_curated_428_origin_research"
LEDGER = ROOT / "data/editorial/reviews/curated_428_fasttrack_prepared85_20261127.json"
RESULT = REPORTS / "fasttrack_prepared85_runtime_import.json"
RESEARCH = ROOT / "data/editorial/research"
LANGS = ("en", "it", "es", "fr", "de", "pt")
CONTEXT = "AI_CONTEXTUAL_SIX_LOCALE"
REVIEWED = "AI_SOURCE_REVIEWED_SIX_LOCALE"
VERSION = "2026.11.27.3"
EXPECTED_COUNTS = {1: 100, 2: 14, 3: 15, 4: 9, 5: 9}
SUPPLEMENTS = {
    "ee-local-government-day":
        "https://www.riigikogu.ee/en/pressiteated/riigikogu-supported-appointment-mart-laar-chairman-supervisory-board-eesti-pank/",
    "za-national-womens-day":
        "https://www.gov.za/news/events/commemorative-events/womens-day",
}
YEAR = re.compile(r"(?<![0-9])(?:1[0-9]{3}|20[0-9]{2})(?![0-9])")

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def content_path(cohort, folder=RESEARCH):
    return list(folder.glob(f"curated_428_cohort{cohort:02d}_*.json"))

def normalize_years(text, oid, locale):
    years = set(YEAR.findall(text))
    # A decade such as "1990s"/"1990er"/"anni Novanta" is not a
    # specific historical year. Its written form differs by language.
    if oid == "ee-mother-tongue-day":
        years.discard("1990")
    return years

def reviewed_qa_status(oid, row, audit):
    if row["outcome"] == "OFFLINE_QA_PASS_SOURCE_AND_SEMANTIC_REVIEW_REQUIRED":
        return ("PASS", [])
    if row["outcome"] == "HOLD":
        return ("HOLD", row["errors"] + row["reviews"] + row["flags"])
    warnings = set(row["errors"] + row["reviews"] + row["flags"])
    allowed = set()
    if oid == "ee-mother-tongue-day":
        allowed |= {x for x in warnings if x.startswith("YEAR_ANCHOR_PARITY_")}
    if oid == "za-national-womens-day":
        allowed |= {"SOURCE_DIRECT_REVIEW_NOT_RECORDED", "SOURCE_DIRECT_REVIEW_PENDING"}
    if warnings and warnings <= allowed and oid in audit["reviewedOverrides"]:
        return ("AI_SCOPED_EXCEPTION", sorted(warnings))
    return ("REVIEW", sorted(warnings))

def run():
    approval = load(LEDGER)
    assert approval["mode"] == "APP_FACTORY_CORE_V27_FAST_TRACK_PREPARED_85"
    assert approval["factoryBaseline"] == "f8b9f550c544735237f19cdd723bd2df667ceee6"
    assert approval["reviewAuthority"] == "USER_DELEGATED_AI_EDITORIAL_REVIEW"
    assert approval["humanSignoffClaim"] is False
    assert approval["everySourceURLIndependentlyReopened"] is False
    assert approval["preparedNotIntegratedAtBaseline"] == 85
    assert approval["selectedForIndividualConditionalReview"] == len(approval["records"]) == 65

    official = load(ASSETS / "official_core.json")
    catalog = {r["id"]: r for r in official["records"]}
    assert len(catalog) == 947
    assert official["datasetVersion"] == "2026.11.27.2", "baseline pack moved"
    locale_docs = {loc: load(ASSETS / f"editorial_{loc}.json") for loc in LANGS}
    seq = None
    status_before = {}
    for loc, doc in locale_docs.items():
        ids = [r["observanceId"] for r in doc["entries"]]
        assert len(ids) == len(set(ids)) == doc["entryCount"] == 947
        if seq is None:
            seq = ids
        else:
            assert ids == seq, ("locale order changed", loc)
        status_before[loc] = sum(r["status"] == CONTEXT for r in doc["entries"])
    assert set(status_before.values()) == {366}, status_before
    english = {r["observanceId"]: r for r in locale_docs["en"]["entries"]}

    rows, filenames = {}, {}
    total_by_cohort = Counter()
    for cohort, count in EXPECTED_COUNTS.items():
        files = content_path(cohort)
        assert len(files) == count, ("unexpected cohort inventory", cohort, len(files))
        for file in files:
            raw = file.read_bytes()
            row = json.loads(raw)
            oid = row["id"]
            assert oid in catalog and oid not in rows
            assert row["cohort"] == cohort
            assert all(len(str(v).strip()) >= 180 for v in row["narratives"].values())
            assert set(row["narratives"]) == set(LANGS)
            rows[oid] = row
            filenames[oid] = (file.relative_to(ROOT).as_posix(), git_blob(raw))
            total_by_cohort[cohort] += 1
    assert len(rows) == 147 and dict(total_by_cohort) == EXPECTED_COUNTS

    pending = {oid: row for oid, row in rows.items() if english[oid]["status"] == CONTEXT}
    assert len(pending) == 85, ("prepared queue changed", len(pending))
    assert Counter(row["cohort"] for row in pending.values()) == {1: 38, 2: 14, 3: 15, 4: 9, 5: 9}

    audit = {"reviewedOverrides": SUPPLEMENTS}
    qa = {}
    for cohort in EXPECTED_COUNTS:
        doc = load(REPORTS / f"fasttrack_qa_cohort_{cohort:02d}.json")
        assert doc["mode"] == "FASTTRACK_DETERMINISTIC_OFFLINE_ONLY"
        assert doc["cohort"] == cohort
        assert doc["uniqueFiles"] == EXPECTED_COUNTS[cohort]
        assert doc["duplicateIds"] == [] and doc["extras"] == []
        for record in doc["records"]:
            if record["outcome"] == "MISSING":
                continue
            assert record["id"] not in qa
            qa[record["id"]] = record
    assert set(qa) == set(rows)

    candidates = {}
    for item in approval["records"]:
        oid = item["observanceId"]
        assert oid in pending and oid not in candidates
        assert item["cohort"] == pending[oid]["cohort"]
        assert item["reviewStatus"] == "AI_EDITORIAL_REVIEWED_SCOPED_HISTORICAL_OR_CIVIC_CONTEXT"
        assert item["nonhumanReview"] is True
        assert item["approval"] == "CONDITIONAL_ON_CI_QA_AND_EXISTING_CONTEXTUAL_STATUS"
        assert item["localesReviewed"] == list(LANGS)
        assert item["sourceEvidenceInFileNotIndependentlyRefetchedInFull"] is True
        assert (item["sourceFile"], item["sourceBlobSha"]) == filenames[oid], ("STALE_SOURCE", oid)
        if item["sourceSupplementVerifiedWeb"]:
            assert SUPPLEMENTS.get(oid) == item["sourceSupplementVerifiedWeb"]
        candidates[oid] = item
    assert len(candidates) == 65

    selected = {}
    decisions = []
    for oid in sorted(pending):
        row = pending[oid]
        qa_result = qa[oid]
        base = {
            "id": oid, "cohort": row["cohort"],
            "sha": filenames[oid][1], "sourceFile": filenames[oid][0],
            "qaOutcome": qa_result["outcome"],
            "qaCodes": sorted(set(qa_result["errors"] + qa_result["reviews"] + qa_result["flags"])),
        }
        if oid not in candidates:
            decisions.append({**base, "outcome": "HOLD_NOT_YET_AI_REVIEWED",
                              "reason": "Specific origin/founding/source review or sensitive-content check not completed"})
            continue
        if row.get("runtimeRichEditorialApproved") is True:
            decisions.append({**base, "outcome": "HOLD_PREMATURE_FLAG",
                              "reason": "Research document cannot self-certify runtime"})
            continue
        if "PENDING_DIRECT_SOURCE_REVIEW" in json.dumps(row.get("sourceEvidence", [])) and oid not in SUPPLEMENTS:
            decisions.append({**base, "outcome": "HOLD_SOURCE_PENDING",
                              "reason": "Direct source review has not been completed"})
            continue
        sources = row.get("sourceEvidence") or []
        if not sources or any(not isinstance(s, dict) or not str(s.get("claim", "")).strip()
                              or urlsplit(str(s.get("url", ""))).scheme != "https"
                              or not urlsplit(str(s.get("url", ""))).hostname
                              for s in sources):
            decisions.append({**base, "outcome": "HOLD_SOURCE_INVALID",
                              "reason": "Primary/originator URL or concrete claim missing"})
            continue
        status, details = reviewed_qa_status(oid, qa_result, audit)
        if status not in ("PASS", "AI_SCOPED_EXCEPTION"):
            decisions.append({**base, "outcome": "HOLD_QA_" + status, "reason": details})
            continue
        # Supplementary AI review checks include earlier centuries, ignored by
        # the generic 1800-2099 structural rubric.
        ref_years = normalize_years(row["narratives"]["en"], oid, "en")
        mismatch = {loc: sorted(normalize_years(row["narratives"][loc], oid, loc) ^ ref_years)
                    for loc in LANGS[1:] if normalize_years(row["narratives"][loc], oid, loc) != ref_years}
        if mismatch:
            decisions.append({**base, "outcome": "HOLD_EARLY_CENTURY_YEAR_MISMATCH", "reason": mismatch})
            continue
        if row.get("documentedIntroductionYear") is not None:
            yr = row["documentedIntroductionYear"]
            if type(yr) is not int or yr < 1700 or yr > 2100:
                decisions.append({**base, "outcome": "HOLD_UNSUPPORTED_FOUNDING_YEAR",
                                  "reason": "Unreasonable or invalid establishment-year value"})
                continue
        if row.get("country") not in catalog[oid].get("countries", []):
            decisions.append({**base, "outcome": "HOLD_COUNTRY_SCOPE",
                              "reason": "Country mismatch against canonical catalog"})
            continue
        supplemental = candidates[oid]["sourceSupplementVerifiedWeb"]
        urls = list(dict.fromkeys([s["url"] for s in sources] + ([supplemental] if supplemental else [])))
        selected[oid] = (row, candidates[oid], urls)
        decisions.append({**base, "outcome": "AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT",
                          "reason": "SHA+canonical+six-locale+chronology+source-scoped QA passed"})

    assert len(decisions) == 85
    assert sum(d["outcome"] == "AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT" for d in decisions) == len(selected)
    assert all(english[id_]["status"] == CONTEXT for id_ in selected)
    assert selected, "no candidate cleared the fail-closed review"

    for loc, pack in locale_docs.items():
        by_id = {r["observanceId"]: r for r in pack["entries"]}
        for oid, (origin, approved, urls) in selected.items():
            item = by_id[oid]
            assert item["status"] == CONTEXT
            text = origin["narratives"][loc].strip()
            assert len(text) >= 180
            item["origin"] = text
            item["status"] = REVIEWED
            item["lastReviewedAt"] = approval["reviewedAt"]
            item["sourcePolicy"] = (
                "App Factory Fast Track IA: originator/government sources and localized "
                "narrative reviewed with AI; per-source full independent refetch not "
                "guaranteed, and no professional human sign-off claimed."
            )
            item["institutionalSourceUrls"] = urls
            item["aiEditorialProvenance"] = {
                "reviewLevel": "AI_EDITORIAL_REVIEWED",
                "reviewDate": approval["reviewedAt"],
                "sourceResearchFile": approved["sourceFile"],
                "sourceResearchBlobSha": approved["sourceBlobSha"],
                "sourceSupplementChecked": approved["sourceSupplementVerifiedWeb"],
                "humanSignoff": False,
                "everyHistoricalSourceReopened": False,
            }
        pack["datasetVersion"] = VERSION

    official["datasetVersion"] = VERSION
    write(ASSETS / "official_core.json", official)
    for loc, pack in locale_docs.items():
        write(ASSETS / f"editorial_{loc}.json", pack)
    index_path = ASSETS / "origin_review_index.json"
    if index_path.exists():
        index = load(index_path)
        index["datasetVersion"] = VERSION
        write(index_path, index)
    queue_path = REPORTS / "index.json"
    if queue_path.exists():
        queue = load(queue_path)
        assert queue["contextualOriginPending"] == 366
        prior = set(queue["fastTrackIntegratedIds"])
        assert len(prior) == 62 and not (prior & selected.keys())
        queue["fastTrackIntegratedIds"] = sorted(prior | set(selected))
        queue["contextualOriginPending"] = 366 - len(selected)
        queue["notYetPersonallyResearched"] = 366 - len(selected)
        queue["nonContextualRich"] = 581 + len(selected)
        for oid, (story, _entry, _urls) in selected.items():
            country = story["country"]
            assert queue["countriesPending"][country] > 0
            queue["countriesPending"][country] -= 1
        write(queue_path, queue)

    summary = Counter(d["outcome"] for d in decisions)
    result = {
        "schemaVersion": 1,
        "mode": "APP_FACTORY_CORE_V27_FAST_TRACK_PREPARED85_AI",
        "sourceMainCommit": "c95663d99eadb9258041b94dee0c70c483b5dfc9",
        "inputAlreadyIntegrated": 62,
        "sourceResearchFiles": 147,
        "preparedOpenBefore": 85,
        "preparedMainCohort01": 38,
        "preparedFromBranches": 47,
        "approvedCandidateCount": len(candidates),
        "fasttrackNewIntegrated": len(selected),
        "integratedIds": sorted(selected),
        "holdCount": 85 - len(selected),
        "outcomeCounts": dict(sorted(summary.items())),
        "decisions": decisions,
        "totalOriginRichAfter": 581 + len(selected),
        "contextualAfter": 366 - len(selected),
        "stillNotAuthored": 281,
        "preparedButNotIntegratedAfter": 85 - len(selected),
        "locales": list(LANGS),
        "reviewLevel": "USER_DELEGATED_AI_EDITORIAL_SCOPED_SOURCE_CHECK",
        "notAllIndividualWebSourcesReopened": True,
        "humanSignoff": False,
        "physicalReleaseCertified": False,
        "releasedOnMain": False,
        "contentPackVersion": VERSION,
    }
    write(RESULT, result)
    print("FASTTRACK_PREPARED85_IMPORTED", json.dumps({
        "preparedOpenBefore": 85,
        "candidates": len(candidates), "imported": len(selected),
        "held": result["holdCount"], "afterRich": result["totalOriginRichAfter"],
        "contextual": result["contextualAfter"], "outcomes": dict(summary),
        "version": VERSION}, sort_keys=True))

if __name__ == "__main__":
    run()
