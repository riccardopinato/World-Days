#!/usr/bin/env python3
"""Fast Track 428: deterministic 100-ID cohort audit, never a fake factual certification.

A source URL or AI_DRAFT label does not prove that the linked page supports every claim.
Outputs one inspectable decision per canonical ID and preserves individual HOLDs.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("en", "it", "es", "fr", "de", "pt")
COHORT_SIZES = {1: 100, 2: 100, 3: 100, 4: 100, 5: 28}
RESEARCH = ROOT / "data/editorial/research"
QUEUES = ROOT / "reports/editorial_curated_428_origin_research"
OUTPUT = QUEUES
URL_BAD = {"example.com", "localhost"}
DATE = re.compile(r"^(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$")
YEAR = re.compile(r"(?<![0-9])(?:18|19|20)[0-9]{2}(?![0-9])")
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|LOREM IPSUM|TRANSLATE ME|PLACEHOLDER)\b", re.I)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def audit_row(row, canonical):
    errors, review, flags = [], [], []
    oid = row.get("id")
    rec = canonical.get(oid)
    if not rec:
        errors.append("NON_CANONICAL_ID")
    if row.get("schemaVersion") != 1:
        errors.append("BAD_SCHEMA_VERSION")
    if row.get("review") not in ("PENDING", "AI_REVIEWED", "REVIEWED"):
        review.append("UNKNOWN_REVIEW_STATE")
    if row.get("runtimeRichEditorialApproved") is True:
        errors.append("PREMATURE_RUNTIME_APPROVAL")
    src = row.get("sourceEvidence") or []
    if not isinstance(src, list) or not src:
        errors.append("MISSING_SOURCE_EVIDENCE")
    else:
        urls = []
        for source in src:
            u = source.get("url", "") if isinstance(source, dict) else ""
            claim = source.get("claim", "") if isinstance(source, dict) else ""
            x = urlsplit(u)
            if x.scheme != "https" or not x.hostname or x.hostname in URL_BAD:
                errors.append("INVALID_SOURCE_URL")
            else:
                urls.append(u)
                if x.path in ("", "/") or len(x.path) < 9:
                    review.append("SOURCE_TOO_GENERIC")
            if len(str(claim).strip()) < 35:
                review.append("SOURCE_CLAIM_TOO_VAGUE")
        if len(urls) != len(set(urls)):
            review.append("REPEATED_SOURCE_URL")
    if not row.get("authority"):
        errors.append("MISSING_AUTHORITY")
    if rec:
        country = row.get("country")
        countries = rec.get("countries", [])
        if countries and country and country not in countries:
            review.append("COUNTRY_CONFLICT")
        if row.get("documentedIntroductionYear") is not None:
            y = row["documentedIntroductionYear"]
            if not isinstance(y, int) or not (1700 <= y <= 2100):
                errors.append("INVALID_INTRODUCTION_YEAR")
            elif rec.get("introducedYear") is not None and rec["introducedYear"] != y:
                review.append("INTRODUCTION_YEAR_CONFLICT")
        date = row.get("date")
        fixed = [r for r in rec.get("recurrenceRules", []) if r.get("kind") == "FIXED_DATE"]
        if isinstance(date, str) and DATE.fullmatch(date):
            if fixed and not any(date == f'{r["month"]:02d}-{r["day"]:02d}' for r in fixed):
                review.append("CALENDAR_DATE_CONFLICT")
        else:
            review.append("DATE_NEEDS_RECURRENCE_CHECK")
    texts = row.get("narratives")
    if not isinstance(texts, dict) or set(texts) != set(LANGUAGES):
        errors.append("INCOMPLETE_LOCALES")
    else:
        for loc in LANGUAGES:
            value = texts[loc]
            if not isinstance(value, str) or len(value.strip()) < 150:
                errors.append("SHORT_OR_EMPTY_TEXT_" + loc.upper())
            elif PLACEHOLDER.search(value):
                errors.append("PLACEHOLDER_" + loc.upper())
        originals = {loc: str(texts[loc]).strip().lower() for loc in LANGUAGES}
        for loc in LANGUAGES[1:]:
            if originals[loc] == originals["en"]:
                errors.append("ENGLISH_FALLBACK_" + loc.upper())
        english_years = set(YEAR.findall(texts["en"]))
        for loc in LANGUAGES[1:]:
            target_years = set(YEAR.findall(texts[loc]))
            missing_years = english_years - target_years
            added_years = target_years - english_years
            if missing_years or added_years:
                review.append("YEAR_ANCHOR_PARITY_" + loc.upper())
    scope = row.get("scopeDecision")
    scope_str = json.dumps(scope, ensure_ascii=False).upper() if scope is not None else ""
    if "HOLD" in scope_str or "EXCLUDE" in scope_str:
        flags.append("SCOPE_HOLD")
    status = str(row.get("status", ""))
    if "HOLD" in status:
        flags.append("STATUS_HOLD")
    if "SOURCE_CHECKED" not in status:
        review.append("SOURCE_DIRECT_REVIEW_NOT_RECORDED")
    if any(isinstance(s, dict) and s.get("verificationStatus") == "PENDING_DIRECT_SOURCE_REVIEW" for s in src):
        review.append("SOURCE_DIRECT_REVIEW_PENDING")
    # Structural checks cannot determine whether a page supports the historical story.
    if errors or flags:
        outcome = "HOLD"
    elif review:
        outcome = "REVIEW"
    else:
        outcome = "OFFLINE_QA_PASS_SOURCE_AND_SEMANTIC_REVIEW_REQUIRED"
    return dict(id=oid, outcome=outcome, errors=sorted(set(errors)),
                reviews=sorted(set(review)), flags=sorted(set(flags)),
                sourceCount=len(src), sixLocales=bool(isinstance(texts, dict) and set(texts) == set(LANGUAGES)))


def run(cohort):
    queue_path = QUEUES / f"cohort_{cohort:02d}_ordered_ids.json"
    if not queue_path.exists():
        return None
    queue = load(queue_path)
    ids = queue.get("ids", [])
    assert len(ids) == COHORT_SIZES[cohort] and len(set(ids)) == len(ids), "invalid canonical cohort queue"
    core_path = ROOT / "assets/data/official_core.json"
    if not core_path.exists():
        raise SystemExit("Build official_core.json first; fail closed on missing catalog")
    records = load(core_path)["records"]
    canonical = {x["id"]: x for x in records}
    files = sorted(RESEARCH.glob(f"curated_428_cohort{cohort:02d}_*.json"))
    rows = {}
    file_index = {}
    duplicate_ids = []
    for path in files:
        doc = load(path)
        key = doc.get("id")
        if not isinstance(key, str):
            raise SystemExit("missing id: " + str(path))
        if key in rows:
            duplicate_ids.append(key)
        rows[key] = doc
        file_index[key] = path
    decisions = []
    for oid in ids:
        if oid not in rows:
            decisions.append(dict(id=oid, outcome="MISSING", errors=["DOSSIER_ABSENT"],
                                  reviews=[], flags=[], sourceCount=0, sixLocales=False))
            continue
        row = rows[oid]
        result = audit_row(row, canonical)
        if row.get("cohort") != cohort:
            result["errors"].append("COHORT_MISMATCH")
            result["outcome"] = "HOLD"
        result["sha256"] = hashlib.sha256(file_index[oid].read_bytes()).hexdigest()
        result["file"] = str(file_index[oid].relative_to(ROOT))
        decisions.append(result)
    extras = sorted(set(rows) - set(ids))
    counters = Counter(x["outcome"] for x in decisions)
    report = {
        "schemaVersion": 1, "mode": "FASTTRACK_DETERMINISTIC_OFFLINE_ONLY",
        "scope": "NO_AUTOMATIC_FACTUAL_OR_SEMANTIC_CERTIFICATION",
        "cohort": cohort, "expected": len(ids), "filesFound": len(files),
        "processedCanonicalIds": len(decisions), "uniqueFiles": len(rows),
        "counts": dict(sorted(counters.items())),
        "extras": extras, "duplicateIds": sorted(set(duplicate_ids)),
        "sourceRule": "Source URL and claim are leads, not proof of actual source contents",
        "humanSignoffRequiredGlobally": False,
        "promotedToRuntime": 0, "records": decisions,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    file = OUTPUT / f"fasttrack_qa_cohort_{cohort:02d}.json"
    file.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("FASTTRACK_QA_COHORT", json.dumps({k: report[k] for k in (
        "cohort", "expected", "filesFound", "counts", "extras", "duplicateIds",
        "promotedToRuntime")}, sort_keys=True))
    if extras or duplicate_ids:
        raise SystemExit("Cohort identity overlap/extra file detected")
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--cohort", type=int, choices=tuple(COHORT_SIZES))
    a = p.parse_args()
    reports = [run(a.cohort)] if a.cohort else [run(i) for i in COHORT_SIZES]
    if not any(r is not None for r in reports):
        raise SystemExit("No curated research queues in this branch")
