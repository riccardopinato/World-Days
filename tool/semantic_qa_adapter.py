#!/usr/bin/env python3
"""World Days published six-locale story dossiers -> Semantic QA v1 adapter.

English is the editorial source. Scope is existing data/editorial/published
bundles (NOT the entire market/discovery catalog), so report coverage honestly.
The adapter is READ-ONLY; duplicate conflicting IDs become review items,
not silently overwritten canonically and never modified in the app.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLISHED = ROOT / "data/editorial/published"
INPUT = ROOT / "build/semantic_qa/world_days_input.json"
LANGS = ("it", "es", "fr", "de", "pt")
FIELDS = ("heading", "origin", "promoter", "purpose", "facts")

def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def text_fields(record: dict) -> dict:
    # Optional fields are included only if present in English; target fields
    # are compared to that authoritative scope, never fallback-copy English.
    out = {}
    for key in FIELDS:
        if key in record:
            value = record[key]
            if key == "facts":
                out[key] = value if isinstance(value, list) else [str(value)]
            else:
                out[key] = value if isinstance(value, str) else str(value)
    return out

def collect(root: Path = ROOT) -> dict:
    bundles = sorted((root / "data/editorial/published").glob("*.json"))
    if not bundles:
        raise ValueError("No published editorial bundles found")
    found = {}
    source_map = {}
    conflicts = []
    skipped = []
    total_rows = 0
    for path in bundles:
        bundle = read(path)
        records = bundle.get("records")
        if not isinstance(records, list):
            skipped.append({"file": path.name, "reason": "NO_RECORDS_ARRAY"})
            continue
        for item in records:
            total_rows += 1
            rid = item.get("observanceId") or item.get("id")
            data = item.get("locale")
            if not isinstance(rid, str) or not rid or not isinstance(data, dict):
                skipped.append({"file": path.name, "reason": "UNSUPPORTED_RECORD",
                                "recordId": str(rid)})
                continue
            if not isinstance(data.get("en"), dict):
                skipped.append({"file": path.name, "reason": "MISSING_EN_MASTER",
                                "recordId": rid})
                continue
            source = text_fields(data["en"])
            if not source:
                skipped.append({"file": path.name, "reason": "EMPTY_EN_MASTER",
                                "recordId": rid})
                continue
            translations = {lang: text_fields(data[lang]) for lang in LANGS
                            if isinstance(data.get(lang), dict)}
            candidate = {
                "id": rid, "source": source, "translations": translations,
                "protectedTerms": [
                    word for word in ("UNESCO", "UNICEF", "WHO", "FAO", "ILO",
                                     "UNHCR", "UNESCO", "PS752")
                    if word.casefold() in json.dumps(source, ensure_ascii=False).casefold()
                ],
                "sourceRefs": item.get("sources", []),
                "context": {
                    "introducedYear": item.get("introducedYear"),
                    "firstObservedYear": item.get("firstObservedYear"),
                    "country": item.get("country"),
                    "observanceDate": item.get("observanceDate"),
                    "originFile": path.name,
                    "status": item.get("reviewStatus", bundle.get("reviewStatus")),
                },
            }
            if rid in found:
                prev = found[rid]
                signature = lambda rec: json.dumps({
                    "source": rec["source"], "translations": rec["translations"]
                }, ensure_ascii=False, sort_keys=True)
                if signature(prev) != signature(candidate):
                    conflicts.append({"id": rid, "firstFile": source_map[rid],
                                      "secondFile": path.name,
                                      "severity": "REVIEW_CONFLICTING_PUBLISHED_DOSSIERS"})
                continue
            found[rid] = candidate
            source_map[rid] = path.name
    if not found:
        raise ValueError("No supported published six-locale dossiers")
    return {
        "schemaVersion": 1,
        "adapter": "world_days_published_editorial",
        "privacy": "PUBLIC_EDITORIAL",
        "sourceLocale": "en",
        "targetLocales": list(LANGS),
        "domainRubric": (
            "World Days. Compare officiality, calendar date or year, founding "
            "authority, source attribution, introduction year versus historical "
            "event year, first observance, location and chronology, uncertainty "
            "markers, named entities and negations. Do not invent official "
            "status from a secondary source or imply a commemoration is an "
            "annual UN day without establishing authority."
        ),
        "records": [found[k] for k in sorted(found)],
        "sourceWarnings": {
            "publishedBundleFiles": len(bundles),
            "rowsSeen": total_rows,
            "uniqueDossiersNormalized": len(found),
            "conflictingDuplicateDossiers": conflicts,
            "skipped": skipped,
            "scopeLimit": ("Published editorial dossiers only; NOT equivalent "
                           "to all 1111 canonical observance IDs or market titles."),
        },
    }

def verify_report(report: dict, count: int) -> dict:
    if report.get("adapter") != "world_days_published_editorial":
        raise ValueError("Wrong audit adapter")
    if report.get("recordCount") != count or report.get("comparisonCount") != count*5:
        raise ValueError("Unexpected World Days report coverage")
    if report.get("certification") != "NOT_CERTIFIED":
        raise ValueError("Unsupported semantic certification")
    states = {}
    for row in report["results"]:
        states[row["state"]] = states.get(row["state"], 0) + 1
    return {"uniquePublishedDossiers": count, "languageComparisons": count*5,
            "states": states}

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, default=INPUT)
    p.add_argument("--verify-report", type=Path)
    p.add_argument("--expected-count", type=int)
    args = p.parse_args()
    if args.verify_report:
        if args.expected_count is None:
            raise ValueError("Expected count required when verifying report")
        print(json.dumps(verify_report(read(args.verify_report), args.expected_count),
                         ensure_ascii=False))
        return 0  # Report inventory may have genuine REVIEW/HOLD; no false PASS.
    payload = collect()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n",
                           encoding="utf-8")
    print(json.dumps(payload["sourceWarnings"], ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
