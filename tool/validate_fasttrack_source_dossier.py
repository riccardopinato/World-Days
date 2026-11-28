#!/usr/bin/env python3
"""Fail-closed QA for a six-locale Fast Track source dossier.

Usage: python tool/validate_fasttrack_source_dossier.py FILE --source-sha GIT_BLOB_SHA
The expected SHA must be obtained independently from the GitHub blob being promoted.
This validates structure, not the historical truth of cited sources or runtime eligibility.
"""
import argparse
import calendar
import hashlib
import json
import re
from pathlib import Path

LOCALES = ("en", "it", "es", "fr", "de", "pt")
SHA = re.compile(r"[0-9a-f]{40}\Z")
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)+\Z")
DATE = re.compile(r"(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\Z")
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER)\b")
URL = re.compile(r"https://[^\s]+\Z")


def git_blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def validate(raw, expected_sha):
    errors = []
    actual = git_blob_sha(raw)
    if not SHA.fullmatch(expected_sha) or actual != expected_sha:
        errors.append("SOURCE_SHA_MISMATCH")
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        return ["INVALID_JSON: " + str(exc)]
    if not isinstance(data, dict):
        return errors + ["INVALID_ROOT_OBJECT"]
    records = data.get("records")
    if not isinstance(records, list) or not records:
        return errors + ["MISSING_RECORDS"]
    seen = set()
    for i, record in enumerate(records):
        prefix = f"records[{i}]"
        if not isinstance(record, dict):
            errors.append(prefix + ": NOT_OBJECT")
            continue
        key = record.get("id")
        if not isinstance(key, str) or not ID.fullmatch(key):
            errors.append(prefix + ": INVALID_ID")
        elif key in seen:
            errors.append(prefix + ": DUPLICATE_ID")
        seen.add(key)
        if (not isinstance(record.get("date"), str) or not DATE.fullmatch(record["date"]) or
                int(record["date"][3:]) > calendar.monthrange(2024, int(record["date"][:2]))[1]):
            errors.append(prefix + ": INVALID_DATE")
        if not isinstance(record.get("eventYear"), int) or isinstance(record.get("eventYear"), bool):
            errors.append(prefix + ": INVALID_EVENT_YEAR")
        sources = record.get("sources")
        if not isinstance(sources, list) or not sources or any(not isinstance(s, str) or not URL.fullmatch(s) for s in sources):
            errors.append(prefix + ": MISSING_HTTPS_SOURCES")
        texts = record.get("texts")
        if not isinstance(texts, dict) or set(texts) != set(LOCALES):
            errors.append(prefix + ": INCOMPLETE_LOCALES")
            continue
        for locale, prose in texts.items():
            if not isinstance(prose, str) or len(prose.split()) < 35:
                errors.append(prefix + ": SHORT_OR_INVALID_" + locale)
            elif PLACEHOLDER.search(prose):
                errors.append(prefix + ": PLACEHOLDER_" + locale)
        if record.get("humanCertified") is not False or record.get("aiAuthored") is not True:
            errors.append(prefix + ": CERTIFICATION_FLAGS")
        if not str(record.get("editorialState", "")).startswith("HOLD_"):
            errors.append(prefix + ": NOT_IN_HOLD")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()
    errors = validate(args.file.read_bytes(), args.source_sha)
    print(json.dumps({"file": str(args.file), "status": "PASS_STRUCTURE_ONLY" if not errors else "FAIL", "errors": errors}, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
