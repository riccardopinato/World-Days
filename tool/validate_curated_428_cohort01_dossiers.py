#!/usr/bin/env python3
"""Fail-closed structural QA for curated cohort-01 individual origin dossiers.

This does not certify historical claims, translations, or human review.
"""
import json
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
    for error in errors:
        print("FAIL:", error)
    print(f"cohort01: {len(ids)} distinct dossier IDs, {len(errors)} structural errors; historical and linguistic review NOT certified")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
