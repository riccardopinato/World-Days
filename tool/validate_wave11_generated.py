#!/usr/bin/env python3
"""Wave11 draft generated-catalog proof: 144 NEW entries, 855 total, NOT 1111."""
import json
from collections import Counter
from pathlib import Path
from market_wave11 import load_wave11
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
index={r["id"]:r for r in catalog["records"]}
assert tuple(map(int,catalog["datasetVersion"].split("."))) >= (2026,11,11,4)
assert len(index)==len(catalog["records"])>=855
assert Counter(r["scope"] for r in index.values())["GLOBAL"]==289
assert Counter(r["scope"] for r in index.values())["NATIONAL"]>=566
countries=Counter(r["countries"][0] for r in index.values() if r["scope"]=="NATIONAL")
assert countries["PH"]>=201
for source in load_wave11():
 rid=source["id"]; r=index[rid]
 assert r["scope"]=="NATIONAL" and r["countries"]==["PH"]
 assert r["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
 assert r["editorialStatus"]=="STUB"
 assert r.get("introducedYear") is None and r.get("introducedYearSource") is None
 assert r["sources"][0]["url"]==source["source"]
 assert r["sources"][0]["tier"]=="A_PRIMARY"
 assert r["localizedTitles"]==source["localizedTitles"]
 rule=source["recurrenceRules"][0]
 assert r["recurrenceRules"]==source["recurrenceRules"]
 date=f"2026-{rule['month']:02}-{rule['day']:02}"
 assert [o["startDate"] for o in occ["occurrences"] if o["observanceId"]==rid]==[date],rid
assert len(catalog["records"])>=855,"Do not misstate a partial draft as the requested +400"
print("PASS: Wave11 draft generated source has 855 distinct IDs (+144) with one +400 PR still pending")
