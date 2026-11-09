#!/usr/bin/env python3
"""Wave 04 source/locale consistency gate. Does NOT certify human review."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data" / "editorial" / "candidates"
SOURCE = CANDIDATES / "wave04_sources_20261109.json"
LOCALES = ("en", "it", "es", "fr", "de", "pt")
ALLOW_HOSTS = {
    "www.un.org", "un.org", "www.unesco.org", "www.who.int",
    "mandates.un.org",
}
REVIEW_FLAG = "DRAFT_PENDING_HUMAN_EDITORIAL_REVIEW"

def load(name):
    return json.loads((CANDIDATES / name).read_text(encoding="utf-8"))

def main():
    evidence = json.loads(SOURCE.read_text(encoding="utf-8"))
    assert evidence["batchId"] == "PRIMARY-WAVE04-2026-11-09"
    sources = evidence["records"]
    assert len(sources) == evidence["count"] == 8
    ids = [item["id"] for item in sources]
    assert len(ids) == len(set(ids)), "duplicate candidate"
    for item in sources:
        parsed = urlsplit(item["primarySource"])
        assert parsed.scheme == "https" and parsed.hostname in ALLOW_HOSTS
        assert parsed.path not in ("", "/")
        assert len(item["chronologyNote"]) > 75
        assert 1900 <= item["proposedIntroducedYear"] <= 2026
        assert item["proposedIntroducedYear"] in item["milestones"]
        assert item["humanEditorialReview"] == "PENDING"
        assert item["translationReview"] == "PENDING_HUMAN"
        assert item["runtimePublished"] is False

    by_locale = {}
    for locale in LOCALES:
        pack = load(f"wave04_{locale}.json")
        assert pack["batchId"] == evidence["batchId"]
        assert pack["locale"] == locale
        assert pack["sourceLocale"] == "en"
        assert pack["reviewStatus"] == REVIEW_FLAG
        rows = pack["entries"]
        assert pack["entryCount"] == len(rows) == 8
        assert [x["id"] for x in rows] == ids, (locale, "id/order parity")
        for entry, source in zip(rows, sources):
            assert len(entry["hook"]) >= 25, (locale, entry["id"], "hook")
            assert len(entry["summary"]) >= 100, (locale, entry["id"], "summary")
            assert len(entry["origin"]) >= 190, (locale, entry["id"], "origin")
            assert len(entry["whyItMatters"]) >= 125, (locale, entry["id"], "why")
            assert len(entry["whyThisDate"]) >= 60, (locale, entry["id"], "date")
            actions = entry["waysToTakePart"]
            assert len(actions) == 2
            assert all(len(x) >= 45 for x in actions)
            for milestone in source["milestones"]:
                assert str(milestone) in entry["origin"], (
                    locale, entry["id"], "missing chronological milestone", milestone
                )
            for key in ("summary", "origin", "whyItMatters", "whyThisDate"):
                assert "http://" not in entry[key] and "https://" not in entry[key]
        by_locale[locale] = {x["id"]: x for x in rows}
    for locale in LOCALES[1:]:
        for oid in ids:
            assert by_locale[locale][oid]["origin"] != by_locale["en"][oid]["origin"], (
                locale, oid, "untranslated"
            )

    # Prevent accidental promotion of AI-generated/draft copy to REVIEWED packs.
    generator = (ROOT / "tool" / "build_editorial.py").read_text(encoding="utf-8")
    localizer = (ROOT / "tool" / "build_editorial_locales.py").read_text(encoding="utf-8")
    assert "wave04" not in generator.lower() and "wave04" not in localizer.lower()
    print("wave04 candidates: 8 primary source records x 6 draft locales = 48; "
          "human review PENDING; runtime editorial pack unchanged")


if __name__ == "__main__":
    main()
