#!/usr/bin/env python3
"""Source and structure gate for the five individually researched UNESCO stories."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"data/editorial/batches/origin_stories_wave01_20261112.json"
batch=json.loads(p.read_text(encoding="utf-8"))
expected={
    "international-day-against-illicit-trafficking-in-cultural-property":2019,
    "international-day-of-islamic-art":2019,
    "international-day-of-mathematics":2019,
    "international-day-of-women-in-multilateralism":2021,
    "world-engineering-day-for-sustainable-development":2019,
}
assert batch["schemaVersion"]==1
assert batch["batchId"]=="ORIGIN-WAVE01-UNESCO-PRIMARY-20261112"
assert batch["status"]=="SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert batch["reviewedOn"]=="2026-11-12"
assert batch["count"]==len(batch["records"])==5
assert {e["observanceId"] for e in batch["records"]}==set(expected)
for r in batch["records"]:
    oid=r["observanceId"]
    assert r["introducedYear"]==expected[oid]
    assert r["firstObservedYear"] is None or 2019 <= r["firstObservedYear"] <= 2026
    assert r["sources"],oid
    for source in r["sources"]:
        parsed=urlsplit(source)
        assert parsed.scheme=="https"
        assert parsed.hostname in {"www.unesco.org","www.mathunion.org","www.idm314.org"}, (oid,source)
    assert set(r["locale"])=={"en","it"}, "other languages need separate review"
    for lang,item in r["locale"].items():
        assert len(item["heading"])>=20,(oid,lang,"heading")
        assert len(item["origin"])>=170,(oid,lang,"origin")
        assert len(item["promoter"])>=60,(oid,lang,"promoter")
        assert len(item["purpose"])>=75,(oid,lang,"purpose")
        assert 2<=len(item["facts"])<=5,(oid,lang,"facts")
        assert all(len(fact)>=45 for fact in item["facts"])
print("PASS: five original IT/EN primary-source stories; six-language claim withheld")
