#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "editorial" / "translations"
ASSET_DIR = ROOT / "assets" / "data"
MASTER_PATH = ASSET_DIR / "editorial_en.json"
LOCALES = ("it", "es", "fr", "de", "pt")
REVIEWED = "2026-10-12"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_entries(locale: str):
    merged = []
    for suffix in ("a", "b"):
        path = SOURCE_DIR / f"{locale}_{suffix}.json"
        payload = load_json(path)
        assert payload.get("locale") == locale, path
        merged.extend(payload.get("entries", []))
    return merged


def main():
    master = load_json(MASTER_PATH)
    master_ids = [item["observanceId"] for item in master.get("entries", [])]
    assert master_ids, "English editorial master is empty"

    for locale in LOCALES:
        raw = source_entries(locale)
        by_id = {item["observanceId"]: item for item in raw}
        missing = sorted(set(master_ids) - set(by_id))
        extra = sorted(set(by_id) - set(master_ids))
        assert not missing, f"{locale} missing ids: {missing}"
        assert not extra, f"{locale} extra ids: {extra}"
        assert len(raw) == len(by_id), f"{locale} duplicate ids"

        entries = []
        for observance_id in master_ids:
            item = by_id[observance_id]
            entries.append({
                "observanceId": observance_id,
                "locale": locale,
                "translationOf": "en",
                "status": "REVIEWED_TRANSLATION",
                "hook": item.get("hook", "").strip(),
                "summary": item["summary"].strip(),
                "whyThisDate": item.get("whyThisDate", "").strip(),
                "origin": item.get("origin", "").strip(),
                "whyItMatters": item["whyItMatters"].strip(),
                "quickFacts": [
                    value.strip() for value in item.get("quickFacts", [])
                    if value.strip()
                ],
                "waysToTakePart": [value.strip() for value in item["waysToTakePart"]],
                "relatedObservanceIds": [
                    value.strip() for value in item.get("relatedObservanceIds", [])
                    if value.strip()
                ],
                "lastReviewedAt": REVIEWED,
                "sourcePolicy": "Translation of the reviewed English editorial master; factual claims remain governed by the canonical observance sources.",
            })

        payload = {
            "schemaVersion": 2,
            "datasetId": f"world-days-editorial-{locale}",
            "datasetVersion": "2026.10.15.2",
            "locale": locale,
            "sourceLocale": "en",
            "entryCount": len(entries),
            "entries": entries,
        }
        path = ASSET_DIR / f"editorial_{locale}.json"
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"editorial {locale}: {len(entries)} reviewed translations")


if __name__ == "__main__":
    main()
