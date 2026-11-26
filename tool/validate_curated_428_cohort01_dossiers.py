#!/usr/bin/env python3
"""Fail-closed structural QA for curated cohort-01 individual origin dossiers.

This does not certify historical claims, translations, or human review.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "data/editorial/research"
LANGUAGES = ("en", "it", "es", "fr", "de", "pt")
REQUIRED = ("schemaVersion", "cohort", "id", "status", "review", "date",
            "country", "sourceEvidence", "narratives", "runtimeRichEditorialApproved")


def validate(record, path):
    problems = []
    for field in REQUIRED:
        if field not in record:
            problems.append(f"{path.name}: missing {field}")
    if problems:
        return problems
    if not isinstance(record["id"], str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", record["id"]):
        problems.append(f"{path.name}: invalid canonical ID")
    if not isinstance(record["date"], str) or not re.fullmatch(r"(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])", record["date"]):
        problems.append(f"{path.name}: date must be MM-DD")
    if not isinstance(record["country"], str) or not re.fullmatch(r"[A-Z]{2}", record["country"]):
        problems.append(f"{path.name}: country must be ISO alpha-2")
    if record["cohort"] != 1:
        problems.append(f"{path.name}: cohort must be 1")
    if record["runtimeRichEditorialApproved"] is not False:
        problems.append(f"{path.name}: runtime approval must remain false")
    if record["review"] != "PENDING":
        problems.append(f"{path.name}: review must remain PENDING")
    if not str(record["status"]).startswith("AI_DRAFT_"):
        problems.append(f"{path.name}: must remain an AI draft")
    if not isinstance(record["sourceEvidence"], list) or not record["sourceEvidence"]:
        problems.append(f"{path.name}: sourceEvidence missing")
    else:
        for index, source in enumerate(record["sourceEvidence"]):
            if not isinstance(source, dict) or not str(source.get("url", "")).startswith("https://") or not str(source.get("claim", "")).strip():
                problems.append(f"{path.name}: invalid sourceEvidence[{index}]")
    if isinstance(record["sourceEvidence"], list):
        urls = [source.get("url") for source in record["sourceEvidence"] if isinstance(source, dict)]
        if len(urls) != len(set(urls)):
            problems.append(f"{path.name}: duplicate source URLs")
    narratives = record["narratives"]
    if not isinstance(narratives, dict) or set(narratives) != set(LANGUAGES):
        problems.append(f"{path.name}: expected exactly six locale keys")
    else:
        for lang in LANGUAGES:
            if not isinstance(narratives[lang], str) or len(narratives[lang].strip()) < 150:
                problems.append(f"{path.name}: {lang} narrative absent or too short")
    year = record.get("documentedIntroductionYear")
    if year is not None and (not isinstance(year, int) or isinstance(year, bool) or not 1000 <= year <= 2100):
        problems.append(f"{path.name}: invalid documentedIntroductionYear")
    if year is not None and not str(record.get("yearMeaning", "")).strip():
        problems.append(f"{path.name}: yearMeaning required when year is specified")
    return problems


def main():
    files = sorted(DIRECTORY.glob("curated_428_cohort01_*.json"))
    if not files:
        raise SystemExit("FAIL: no cohort-01 dossier files")
    ids, errors = set(), []
    for path in files:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        errors.extend(validate(record, path))
        identity = record.get("id")
        if identity in ids:
            errors.append(f"{path.name}: duplicate canonical id {identity}")
        ids.add(identity)
    if len(ids) > 100:
        errors.append("cohort01: more than 100 distinct IDs")
    try:
        queue_path = ROOT / "reports/editorial_curated_428_origin_research/cohort_01_ordered_ids.json"
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
        allowed = queue["ids"]
        if queue["count"] != 100 or len(allowed) != 100 or len(set(allowed)) != 100:
            errors.append("cohort01 queue: expected 100 unique immutable IDs")
        if not ids.issubset(set(allowed)):
            errors.append(f"cohort01: dossier IDs outside canonical queue: {sorted(ids - set(allowed))}")
        for path in files:
            try:
                entry = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if entry.get("id") not in allowed:
                continue
            prefix = entry["id"].split("-", 1)[0]
            expected_country = {"italian": "IT", "italys": "IT"}.get(prefix, prefix.upper())
            if entry.get("country") != expected_country:
                errors.append(f"{path.name}: country does not match canonical ID")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"cohort01 canonical ordered ID queue invalid: {exc}")
        allowed = []
    manifest_path = DIRECTORY / "curated_428_cohort_artifact_provenance_20261122.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        cohort = manifest["cohort01"]
        recorded_ids = cohort["preparedDossierIds"]
        hold_ids = cohort["relevanceHoldIds"]
        if len(recorded_ids) != len(set(recorded_ids)):
            errors.append("cohort01 manifest: duplicate prepared IDs")
        if set(recorded_ids) != ids:
            errors.append("cohort01 manifest: prepared IDs differ from dossier files")
        if cohort["preparedSixLocaleDossiers"] != len(ids):
            errors.append("cohort01 manifest: prepared count differs from dossier files")
        if not set(hold_ids).issubset(ids):
            errors.append("cohort01 manifest: HOLD references an absent dossier")
        if cohort["integratedInMain"] != 0:
            errors.append("cohort01 manifest: draft validator cannot assert main integration")
        if allowed:
            next_unprepared = next((item for item in allowed if item not in ids), None)
            if cohort.get("nextUnpreparedId") != next_unprepared:
                errors.append("cohort01 manifest: nextUnpreparedId differs from canonical queue")
            if recorded_ids != [item for item in allowed if item in ids]:
                errors.append("cohort01 manifest: preparedDossierIds not in immutable queue order")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"cohort01 manifest unavailable or malformed: {exc}")
    for error in errors:
        print("FAIL:", error)
    print(f"cohort01: {len(ids)} distinct dossier IDs, {len(errors)} structural errors; historical and linguistic review NOT certified")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
