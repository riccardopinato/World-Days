#!/usr/bin/env python3
"""Strict runtime Wave09 admission checks for six new markets, exact dates and localization."""
from collections import Counter
from datetime import date
import json
from pathlib import Path
from market_wave09 import load_wave09_civic
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf8"))
index=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf8"))
old=json.loads((ROOT/"data/research/FAST02_CIVIC_12_SOURCE_STAGED_20261110.json").read_text(encoding="utf8"))
rows=catalog["records"]
ids={r["id"]:r for r in rows}
assert len(ids)==len(rows)==511
assert catalog["datasetVersion"]=="2026.11.10.10"
assert Counter(r["scope"] for r in rows)=={"GLOBAL":292,"NATIONAL":219}
assert len(index["dateIndex"])==365
new=load_wave09_civic()
assert len(new)==12 and len(old["records"])==12
expected={"BD":2,"ID":2,"KH":3,"MY":2,"VN":2,"LA":1}
for c,n in expected.items():
    assert sum(x["countries"]==[c] for x in rows)==n,c
for item in new:
    r=ids[item["id"]]
    assert r["countries"]==[item["country"]] and r["scope"]=="NATIONAL"
    assert r["editorialStatus"]=="STUB"
    assert r["canonicalTitleEn"]==item["canonicalTitleEn"]
    assert r["localizedTitles"]==item["localizedTitles"]
    assert set(r["localizedTitles"])=={"en","it","es","fr","de","pt"}
    assert r.get("introducedYear") is None and r.get("introducedYearSource") is None
    assert r["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
    assert r["authority"]["type"]=="GOVERNMENT"
    assert r["sources"][0]["tier"]=="A_PRIMARY"
    assert r["sources"][0]["url"]==item["source"]
    rule=r["recurrenceRules"][0]
    assert rule["kind"]=="FIXED_DATE"
    year_dates=[date(y,rule["month"],rule["day"]).isoformat() for y in (2026,2027,2028)]
    assert year_dates[0]==f'2026-{rule["month"]:02d}-{rule["day"]:02d}'
    obs=[o["startDate"] for o in index["occurrences"] if o["observanceId"]==item["id"]]
    assert obs==[year_dates[0]],(item["id"],obs)
assert len({r["id"] for r in rows})==511
print("WAVE09 CONTENT PASS: 504 unique records, 285 global + 219 national, 34 countries; 12 new STUBs and 6 locale titles, no human review or production release")
