#!/usr/bin/env python3
"""Validate the 16 pre-existing Wave14 individually sourced IT/EN origin narratives.

These are research records, not human fact-certified or six-locale approved rich articles.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
file = ROOT / "data/editorial/batches/origin_stories_wave14_20261112.json"
data = json.loads(file.read_text(encoding="utf-8"))
catalog = json.loads((ROOT / "assets/data/official_core.json").read_text(encoding="utf-8"))
ids = {entry["id"] for entry in catalog["records"]}
assert data["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert data["count"] == len(data["records"]) == 16
records = {r["observanceId"]: r for r in data["records"]}
assert len(records) == 16
assert set(records) <= ids
for oid, r in records.items():
    assert {"en", "it"} <= set(r["locale"]) <= {"en", "it"}
    assert len(r["sources"]) >= 2 and len(r["sources"]) == len(set(r["sources"]))
    assert all(urlsplit(u).scheme == "https" and urlsplit(u).hostname for u in r["sources"])
    assert r["introducedYear"] is None or 1900 <= r["introducedYear"] <= 2026
    assert r["firstObservedYear"] is None or 1900 <= r["firstObservedYear"] <= 2026
    for lang in ("en", "it"):
        t = r["locale"][lang]
        assert len(t["heading"].strip()) >= 18, (oid, lang)
        for key in ("origin", "promoter", "purpose"):
            assert len(t[key].strip()) >= 40, (oid, lang, key)
        assert 2 <= len(t["facts"]) <= 5, (oid, lang)
        assert all(len(f.strip()) >= 25 for f in t["facts"]), (oid, lang)
assert records["world-creativity-and-innovation-day"]["introducedYear"] == 2017
assert records["world-creativity-and-innovation-day"]["firstObservedYear"] == 2002
assert records["international-day-of-plant-health"]["introducedYear"] == 2022
print("PASS Wave14: 16 unique sourced IT/EN drafts, no invented six-language approvals")
