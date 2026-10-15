#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "data"
LOCALES = ("it", "es", "fr", "de", "pt")

def load(locale):
    path = ASSET_DIR / f"editorial_{locale}.json"
    return json.loads(path.read_text(encoding="utf-8"))

master = load("en")
assert master.get("schemaVersion") == 2
master_entries = master.get("entries", [])
master_ids = [item["observanceId"] for item in master_entries]
master_actions = {
    item["observanceId"]: len(item.get("waysToTakePart", []))
    for item in master_entries
}

for locale in LOCALES:
    pack = load(locale)
    entries = pack.get("entries", [])
    ids = [item.get("observanceId") for item in entries]

    assert pack.get("schemaVersion") == 2
    assert pack.get("locale") == locale
    assert pack.get("sourceLocale") == "en"
    assert pack.get("entryCount") == len(entries) == len(master_entries)
    assert ids == master_ids, f"{locale} editorial ids/order diverge from English master"
    assert len(ids) == len(set(ids)), f"{locale} duplicate editorial ids"

    for item in entries:
        oid = item["observanceId"]
        assert item.get("translationOf") == "en", (locale, oid)
        assert item.get("status") == "REVIEWED_TRANSLATION", (locale, oid)
        for key in (
            "hook",
            "summary",
            "whyThisDate",
            "origin",
            "whyItMatters",
            "quickFacts",
            "waysToTakePart",
            "relatedObservanceIds",
        ):
            assert key in item, (locale, oid, key)
        assert len(item.get("summary", "").strip()) >= 55, (locale, oid, "summary")
        assert len(item.get("whyItMatters", "").strip()) >= 65, (locale, oid, "why")
        actions = item.get("waysToTakePart", [])
        assert len(actions) == master_actions[oid], (locale, oid, "actions")
        assert all(len(action.strip()) >= 15 for action in actions), (locale, oid)
        assert item.get("relatedObservanceIds", []) == next(
            master_item.get("relatedObservanceIds", [])
            for master_item in master_entries
            if master_item["observanceId"] == oid
        ), (locale, oid, "related")
        assert item.get("lastReviewedAt") == "2026-10-12", (locale, oid)
        assert item.get("locale") == locale, (locale, oid)

print(
    f"editorial locales ok: {len(master_entries)} entries x "
    f"{1 + len(LOCALES)} locales"
)
