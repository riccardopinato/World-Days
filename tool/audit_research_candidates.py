#!/usr/bin/env python3
"""Full generated-catalog screening of World Days research candidates.

Research-only. A clean automated screen is NOT officiality, semantic uniqueness,
translation, annual recurrence, legal-source, or runtime-admission certification.
Run after python3 tool/build_dataset.py.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "assets/data/official_core.json"
RESEARCH = ROOT / "data/research"
REPORT = ROOT / "reports/research_semantic_audit.json"
LOCALES = ("en", "it", "es", "fr", "de", "pt")
COUNTRY_SUFFIXES = (
    "canada", "japan", "india", "south africa", "philippines",
    "singapore", "south korea", "bangladesh", "thailand", "vietnam",
    "cambodia", "laos", "nepal", "sri lanka", "indonesia", "malaysia",
)

def normalize(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value.casefold())
    ascii_value = "".join(c for c in ascii_value if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", ascii_value.replace("&", " and "))).strip()

def unqualify(value: str) -> str:
    value = normalize(value)
    for country in COUNTRY_SUFFIXES:
        if value.endswith(" " + country):
            return value[: -len(country) - 1].strip()
    return value

def canonical_name(rec: dict) -> str:
    return rec.get("canonicalTitleEn", "")

def candidate_origin(rec: dict) -> str:
    return rec.get("primarySource") or rec.get("source") or ""

def country_code(rec: dict) -> str:
    country = rec.get("country") or ""
    return str(country).upper()

def catalog_countries(rec: dict) -> set[str]:
    return set(rec.get("countries") or [])

def expected_date_2026(rec: dict) -> str | None:
    if isinstance(rec.get("occurrence2026"), str):
        return rec["occurrence2026"]
    date_obj = rec.get("observedDate2026")
    if isinstance(date_obj, dict) and "month" in date_obj and "day" in date_obj:
        return f"2026-{date_obj['month']:02d}-{date_obj['day']:02d}"
    date_obj = rec.get("date") or rec.get("recurrence")
    if isinstance(date_obj, dict) and "month" in date_obj and "day" in date_obj:
        return f"2026-{date_obj['month']:02d}-{date_obj['day']:02d}"
    return None

def candidate_variants(rec: dict) -> set[str]:
    variants = {normalize(canonical_name(rec))}
    for term in rec.get("aliases") or []:
        if isinstance(term, str):
            variants.add(normalize(term))
    locs = rec.get("localizedTitles") or {}
    for loc in LOCALES:
        if isinstance(locs.get(loc), str):
            variants.add(normalize(locs[loc]))
    return {v for v in variants if v}

def catalog_variants(rec: dict) -> set[str]:
    variants = {normalize(rec["id"]), normalize(canonical_name(rec))}
    for term in rec.get("aliases") or []:
        if isinstance(term, str):
            variants.add(normalize(term))
    for value in (rec.get("localizedTitles") or {}).values():
        if isinstance(value, str):
            variants.add(normalize(value))
    return {v for v in variants if v}

def contextual_match(rec: dict, existing: dict) -> bool:
    country = country_code(rec)
    # An all-world observance is a plausible match to every country-qualified
    # candidate; two different country-specific holidays are NOT identical.
    if existing.get("scope") == "GLOBAL":
        return True
    if country:
        return country in catalog_countries(existing)
    return False

def screen_one(rec: dict, catalog: list[dict], variant_index: dict[str, list[dict]], ids: dict[str, dict]) -> dict:
    title = canonical_name(rec)
    norm = normalize(title)
    country = country_code(rec)
    candidate_id = rec.get("id", "")
    high, possible, homonyms = {}, {}, {}
    if candidate_id in ids:
        high[ids[candidate_id]["id"]] = {"id": candidate_id, "reason": "SAME_CANONICAL_ID"}
    for variant in candidate_variants(rec):
        for existing in variant_index.get(variant, []):
            match = {"id": existing["id"], "reason": "EXACT_TITLE_ALIAS_OR_LOCALE"}
            if contextual_match(rec, existing):
                high[existing["id"]] = match
            else:
                homonyms[existing["id"]] = {"id": existing["id"], "reason": "CROSS_COUNTRY_SAME_LABEL"}
    short = unqualify(title)
    if short != norm:
        for existing in variant_index.get(short, []):
            bucket = possible if contextual_match(rec, existing) else homonyms
            bucket.setdefault(existing["id"], {"id": existing["id"], "reason": "STRIPPED_COUNTRY_QUALIFIER"})
    # Fuzzy matches are review leads only, not automatic duplicate decisions.
    for existing in catalog:
        if existing["id"] in high or existing["id"] in possible:
            continue
        if not contextual_match(rec, existing):
            continue
        ex_norm = normalize(canonical_name(existing))
        sim = SequenceMatcher(None, short, unqualify(ex_norm)).ratio()
        a, b = set(short.split()), set(unqualify(ex_norm).split())
        overlap = len(a & b) / len(a | b) if a and b else 0
        if (sim >= 0.83 or overlap >= 0.72) and len(a & b) >= 2:
            possible[existing["id"]] = {
                "id": existing["id"], "reason": "SIMILAR_TITLE_REQUIRES_SEMANTIC_REVIEW",
                "similarity": round(sim, 3), "tokenJaccard": round(overlap, 3),
            }
    # A date is never sufficient evidence of an identical commemoration.
    when = expected_date_2026(rec)
    if when is not None:
        date.fromisoformat(when)
        if not when.startswith("2026-"):
            raise ValueError("Non-2026 occurrence: " + when)
    source = candidate_origin(rec)
    if not source or urlsplit(source).scheme != "https":
        raise ValueError("Missing HTTPS source: " + title)
    status = "DIRECT_CATALOG_OVERLAP" if high else ("POSSIBLE_CATALOG_OVERLAP" if possible else "NO_AUTOMATED_CATALOG_MATCH")
    return {
        "title": title,
        "id": candidate_id or None,
        "country": country or None,
        "status": status,
        "directMatches": sorted(high.values(), key=lambda x: x["id"]),
        "possibleMatches": sorted(possible.values(), key=lambda x: x["id"]),
        "crossCountryHomonyms": sorted(homonyms.values(), key=lambda x: x["id"]),
        "occurrence2026": when,
        "dateRuleRequiresReview": str(rec.get("recurrenceRuleType") or rec.get("recurrenceRule") or (rec.get("date") or rec.get("recurrence") or {}).get("kind", "")).upper() not in {"FIXED", "FIXED_DATE", ""},
        "source": source,
        "admission": "RESEARCH_ONLY_NOT_CERTIFIED",
    }

def audit(catalog: list[dict], paths: list[Path]) -> dict:
    ids = {r["id"]: r for r in catalog}
    if len(ids) != len(catalog):
        raise ValueError("Catalog contains repeated IDs")
    index: dict[str, list[dict]] = defaultdict(list)
    for r in catalog:
        for variant in catalog_variants(r):
            index[variant].append(r)
    output = []
    seen_candidate_identifiers = defaultdict(list)
    candidates_per_file = {}
    for path in sorted(paths):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("candidateOnly") is not True:
            raise ValueError(f"Non-research source in {path}")
        recs = payload["records"]
        declared = payload.get("recordCount", payload.get("candidateCount"))
        if declared != len(recs):
            raise ValueError(f"Candidate count mismatch in {path}: {declared} vs {len(recs)}")
        candidates_per_file[path.name] = len(recs)
        for i, candidate in enumerate(recs):
            if not isinstance(canonical_name(candidate), str) or not canonical_name(candidate).strip():
                raise ValueError(f"Missing title in {path} position {i}")
            checked = screen_one(candidate, catalog, index, ids)
            checked["researchFile"] = path.name
            checked["index"] = i
            output.append(checked)
            # Cross-wave review is country-scoped; global observances stay global.
            country_scope = country_code(candidate) or "GLOBAL"
            seen_candidate_identifiers[(country_scope, unqualify(canonical_name(candidate)))].append(len(output)-1)
    for indices in seen_candidate_identifiers.values():
        if len(indices) <= 1:
            continue
        for idx in indices:
            output[idx]["crossWaveSameCountryTitle"] = [
                {"researchFile": output[j]["researchFile"], "index": output[j]["index"]}
                for j in indices if j != idx
            ]
    counts = Counter(x["status"] for x in output)
    result = {
        "schemaVersion": 1,
        "disclaimer": "Automated matching against the FULL generated catalog (IDs, English and all six locale titles, aliases). A NO_AUTOMATED_CATALOG_MATCH result is NOT semantically verified unique or ready for admission.",
        "catalogCount": len(catalog),
        "candidateRecordCount": len(output),
        "researchFileCounts": candidates_per_file,
        "classificationCounts": dict(sorted(counts.items())),
        "crossWaveRepeatedCountryTitles": sum("crossWaveSameCountryTitle" in x for x in output),
        "candidateResults": output,
    }
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--research-dir", type=Path, default=RESEARCH)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))["records"]
    paths = sorted(args.research_dir.glob("wave*.json"))
    if not paths:
        raise SystemExit("ERROR: no Wave research sources found")
    report = audit(catalog, paths)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "catalog": report["catalogCount"],
        "researchRecords": report["candidateRecordCount"],
        "classifications": report["classificationCounts"],
        "repeatedCandidateTitles": report["crossWaveRepeatedCountryTitles"],
        "artifact": str(args.output),
        "runtimeNewAdmissions": 0,
        "note": "No automated match does NOT equal certified unique."
    }, indent=2))
    if report["catalogCount"] < 456:
        raise SystemExit("ERROR: canonical catalog unexpectedly shrank below 456")

if __name__ == "__main__":
    main()
