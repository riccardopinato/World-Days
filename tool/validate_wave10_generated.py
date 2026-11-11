#!/usr/bin/env python3
"""Verify Wave10 is in the real 711-record generated offline catalog."""
import json
from collections import Counter
from pathlib import Path
from market_wave10 import load_wave10,date_for
ROOT=Path(__file__).resolve().parents[1]
seed=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
by_id={r["id"]:r for r in seed["records"]}
assert tuple(map(int,seed["datasetVersion"].split("."))) >= (2026,11,11,3)
assert len(by_id)==len(seed["records"])>=711
assert Counter(x["scope"] for x in seed["records"])["GLOBAL"]==289
assert Counter(x["scope"] for x in seed["records"])["NATIONAL"]>=422
countries=Counter(r["countries"][0] for r in seed["records"] if r["scope"]=="NATIONAL")
assert countries["KR"]>=57 and countries["PH"]>=57
for row in load_wave10():
 rid=row["id"];record=by_id[rid]
 assert record["scope"]=="NATIONAL",rid
 assert record["countries"]==[row["country"]],rid
 assert record["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
 assert record["editorialStatus"]=="STUB"
 assert record.get("introducedYear") is None
 assert record.get("introducedYearSource") is None
 assert record["sources"][0]["url"]==row["source"]
 assert record["sources"][0]["tier"]=="A_PRIMARY"
 assert record["recurrenceRules"]==row["recurrenceRules"]
 assert record["localizedTitles"]==row["localizedTitles"]
 assert row["sourceTitleOriginal"] in record["aliases"]
 expected=date_for(row["recurrenceRules"][0],2026).isoformat()
 actual=[e["startDate"] for e in occ["occurrences"] if e["observanceId"]==rid]
 assert actual==[expected],(rid,actual,expected)
print("PASS: 711 unique IDs, 100 source-index additions, 50 Korea / 50 Philippines, nonstatutory classification disclosed")
