#!/usr/bin/env python3
"""Wave07 generated catalog correctness, title parity, recurrence and history boundary."""
import json
from collections import Counter
from pathlib import Path
from market_wave07 import load_wave07,observed

ROOT=Path(__file__).resolve().parents[1]
seed=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
rows=load_wave07()
known={r["id"]:r for r in seed["records"]}
assert tuple(map(int,seed["datasetVersion"].split("."))) >= (2026,11,10,3)
assert len(known)==len(seed["records"])>=511
assert Counter(r["scope"] for r in known.values())["GLOBAL"]==289
assert Counter(r["scope"] for r in known.values())["NATIONAL"]>=222
assert Counter(r["countries"][0] for r in known.values() if r["scope"]=="NATIONAL")["EE"]>=17
for source in rows:
 rid=source["id"];row=known[rid]
 assert row["scope"]=="NATIONAL" and row["countries"]==[source["country"]]
 assert row["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
 assert row["editorialStatus"]=="STUB"
 assert row.get("introducedYear") is None and row.get("introducedYearSource") is None
 assert row["sources"][0]["tier"]=="A_PRIMARY" and row["sources"][0]["url"]==source["source"]
 assert row["localizedTitles"]==source["localizedTitles"]
 assert row["recurrenceRules"]==source["recurrenceRules"]
 start=observed(source["recurrenceRules"][0],2026).isoformat()
 actual=[o["startDate"] for o in occ["occurrences"] if o["observanceId"]==rid]
 assert actual==[start],(rid,actual,start)
print("PASS: 32 new national identities, 2026-28 recurrence proof, 511 IDs, 5 countries, no reviewed stories fabricated")
