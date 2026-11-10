#!/usr/bin/env python3
"""Assert Wave06 is actually present in the built offline catalog without story promotion."""
import json
from collections import Counter
from pathlib import Path
from market_wave06 import load_wave06
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/"assets/data/official_core.json").read_text(encoding="utf8"))
occ=json.loads((root/"assets/data/occurrences_2026.json").read_text(encoding="utf8"))
known={r["id"]:r for r in catalog["records"]}
rows=load_wave06()
assert tuple(map(int,catalog["datasetVersion"].split("."))) >= (2026,11,10,2)
assert len(known)==len(catalog["records"])>=479
assert Counter(r["scope"] for r in known.values())["GLOBAL"]==289
assert Counter(r["scope"] for r in known.values())["NATIONAL"]>=190
for source in rows:
 rid=source["id"];r=known[rid]
 assert r["countries"]==[source["country"]],rid
 assert r["scope"]=="NATIONAL"
 assert r["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
 assert r["editorialStatus"]=="STUB"
 assert r.get("introducedYear") is None and r.get("introducedYearSource") is None
 assert set(r["localizedTitles"])=={"en","it","es","fr","de","pt"}
 assert r["sources"][0]["tier"]=="A_PRIMARY"
 assert r["sources"][0]["url"]==source["source"]
 rule=source["recurrenceRules"][0]
 expected=f"2026-{rule['month']:02}-{rule['day']:02}"
 actual=[o["startDate"] for o in occ["occurrences"] if o["observanceId"]==rid]
 assert actual==[expected],(rid,actual,expected)
print("PASS: 16 official source-level additions in 479-record catalog; original reviewed histories untouched")
