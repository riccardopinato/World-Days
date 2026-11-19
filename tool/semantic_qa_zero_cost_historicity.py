#!/usr/bin/env python3
"""Source-bound World Days historicity triage, offline / read only / no AI costs.

Checks years explicitly stated in the public EN original against every
translation and checks source provenance. This is NOT fact verification:
absence of findings never means that chronology or authority was verified.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
YEARS = re.compile(r"(?<!\\d)(?:1[5-9]\\d{2}|20\\d{2})(?!\\d|s\\b|er\\b|er-)")
DECADE_BEFORE = re.compile(
    r"(?:\\b(?:anni|années|annees|años|anos|década|decada|décennie|decennie|"
    r"jahrzehnt|jahre|decade)\\s+(?:(?:de|del|di|dos|des|of|the)\\s+)?)$",
    re.IGNORECASE,
)

def exact_years(text: str) -> set[str]:
    """Exclude decade ranges (1940s/1940er/anni 1940), not exact calendar years."""
    result = set()
    for match in YEARS.finditer(text):
        preceding = text[max(0, match.start()-45):match.start()]
        if DECADE_BEFORE.search(preceding):
            continue
        result.add(match.group())
    return result

def flattened_strings(value: object) -> str:
    if isinstance(value, dict):
        return " ".join(flattened_strings(x) for x in value.values())
    if isinstance(value, list):
        return " ".join(flattened_strings(x) for x in value)
    return value if isinstance(value, str) else ""

def triage(payload: dict) -> dict:
    if payload.get("adapter") != "world_days_published_editorial":
        raise ValueError("Only normalized World Days published editorial is supported")
    findings = []
    counts = Counter()
    if payload.get("sourceWarnings", {}).get("conflictingDuplicateDossiers"):
        raise ValueError("Cannot silently review conflicting published dossiers")
    if payload.get("sourceWarnings", {}).get("skipped"):
        raise ValueError("Cannot silently omit unsupported published rows")
    for record in payload["records"]:
        rid = record["id"]
        source = flattened_strings(record["source"])
        source_years = exact_years(source)
        refs = record.get("sourceRefs")
        if not isinstance(refs, list) or not refs:
            findings.append({"id": rid, "locale": "*",
                             "code": "MISSING_SOURCE_PROVENANCE",
                             "severity": "REVIEW",
                             "sourceYears": sorted(source_years),
                             "targetYears": [],
                             "evidence": "Published dossier lacks listed source URLs"})
        for locale in payload["targetLocales"]:
            target = record["translations"].get(locale)
            if not isinstance(target, dict):
                findings.append({"id": rid, "locale": locale,
                                 "code": "MISSING_LANGUAGE",
                                 "severity": "HOLD",
                                 "sourceYears": sorted(source_years),
                                 "targetYears": [], "evidence": "No translation record"})
                continue
            target_years = exact_years(flattened_strings(target))
            missing = sorted(source_years-target_years)
            extra = sorted(target_years-source_years)
            if missing:
                findings.append({"id": rid, "locale": locale,
                                 "code": "CANONICAL_YEAR_NOT_PRESERVED",
                                 "severity": "REVIEW", "sourceYears": missing,
                                 "targetYears": sorted(target_years),
                                 "evidence": "Source year absent in translation; verify chronology"})
            if extra:
                findings.append({"id": rid, "locale": locale,
                                 "code": "TARGET_ADDS_YEAR",
                                 "severity": "REVIEW", "sourceYears": sorted(source_years),
                                 "targetYears": extra,
                                 "evidence": "Target includes year not present in canonical content"})
    findings.sort(key=lambda x: (x["id"], x["locale"], x["code"]))
    for f in findings:
        counts[f["code"]] += 1
    return {
        "schemaVersion": 1, "mode": "OFFLINE", "semanticModelActuallyUsed": False,
        "paidAiApiCalls": 0, "certification": "NOT_CERTIFIED",
        "recordCount": len(payload["records"]),
        "comparisonCount": len(payload["records"])*len(payload["targetLocales"]),
        "findingsCount": len(findings), "affectedRecordCount": len({x["id"] for x in findings}),
        "codes": dict(sorted(counts.items())), "findings": findings,
        "note": "Anchor triage only. Dates, true officiality, source reliability and meaning remain unverified.",
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=ROOT/"build/semantic_qa/input.json")
    p.add_argument("--output", type=Path, default=ROOT/"build/semantic_qa/zero_cost_historicity.json")
    args = p.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    result = triage(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k!="findings"}, ensure_ascii=False))
    print(json.dumps({"findingsBrief": [{"id": r["id"], "locale": r["locale"],
              "code": r["code"], "sourceYears": r["sourceYears"],
              "targetYears": r["targetYears"]} for r in result["findings"][:100]]},
              ensure_ascii=False))

if __name__ == "__main__":
    main()
