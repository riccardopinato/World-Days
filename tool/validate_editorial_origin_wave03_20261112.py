#!/usr/bin/env python3
"""Source-by-source regression for the 15 pre-researched UN/UNESCO origin stories."""
from pathlib import Path
from urllib.parse import urlsplit
import json

ROOT = Path(__file__).resolve().parents[1]
old = json.loads((ROOT / "data/editorial/batches/un_primary_2026_11_03_03.json").read_text(encoding="utf-8"))
new = json.loads((ROOT / "data/editorial/batches/origin_stories_wave03_20261112.json").read_text(encoding="utf-8"))
catalog = json.loads((ROOT / "assets/data/official_core.json").read_text(encoding="utf-8"))
entries = {x["id"]: x for x in old["entries"]}
canonical = {x["id"]: x for x in catalog["records"]}
assert len(entries) == 15 and len(canonical) >= 1111
assert new["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert new["batchId"] == "ORIGIN-WAVE03-UN-UNESCO-15-20261112"
assert new["count"] == len(new["records"]) == 15
assert len({x["observanceId"] for x in new["records"]}) == 15
assert {x["observanceId"] for x in new["records"]} == set(entries)
assert new["reviewedOn"] == "2026-11-12"
allowed = {"www.un.org", "www.unesco.org", "mandates.un.org",
           "www.irena.org", "www.olympics.com", "www.unesco.org",
           "digitallibrary.un.org"}
for e in new["records"]:
    oid = e["observanceId"]
    base = entries[oid]
    r = canonical[oid]
    assert e["introducedYear"] == base["year"] == r.get("introducedYear"), oid
    assert e["firstObservedYear"] is None or e["firstObservedYear"] >= e["introducedYear"], oid
    assert base["source"] in e["sources"]
    assert len(e["sources"]) == len(set(e["sources"]))
    assert set(e["locale"]) == {"en", "it"}, "no unsupported six-locale certification"
    assert e["sourceReviewNote"] and len(e["sourceReviewNote"]) >= 60
    for u in e["sources"]:
        p = urlsplit(u)
        assert p.scheme == "https" and p.hostname in allowed, (oid,u)
    for lang in ("en","it"):
        item = e["locale"][lang]
        previous = base["translations"][lang]
        assert previous["origin"] in item["origin"], (oid,lang,"preserved prior source research")
        assert previous["whyItMatters"] in item["purpose"], (oid,lang,"preserved prior explanation")
        assert previous["whyThisDate"] == item["facts"][0], (oid,lang,"date context retained")
        for key in ("heading","origin","promoter","purpose"):
            assert len(item[key].strip()) >= (20 if key == "heading" else 60), (oid,lang,key)
        assert len(item["origin"]) >= 170
        assert 2 <= len(item["facts"]) <= 5
        assert all(len(x.strip()) >= 25 for x in item["facts"])
        assert lang != "en" or len(item["facts"][1]) >= 45
print("PASS: 15 source-bound original IT/EN stories, original Wave03 chronology and all founding years preserved")
