#!/usr/bin/env python3
"""End-to-end Wave12 admission proof: 711 main baseline + 144 NCCA + 156 DFAT = 1011 draft.

This is 300 net new identities ON DRAFT, not 300 committed to main,
and NOT yet the protected 1111 minimum milestone for the single PR.
"""
import json
from collections import Counter
from datetime import date
from pathlib import Path
from market_wave12 import load_wave12
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
records=catalog["records"]
by_id={r["id"]:r for r in records}
assert catalog["datasetVersion"]=="2026.11.11.5"
assert len(records)==len(by_id)==1011
assert Counter(r["scope"] for r in records)=={"GLOBAL":289,"NATIONAL":722}
markets=Counter(r["countries"][0] for r in records if r["scope"]=="NATIONAL")
assert len(markets)==192
assert markets["PH"]==201 and markets["KR"]==57
for row in load_wave12():
 rid=row["id"]; rec=by_id[rid]
 assert rec["scope"]=="NATIONAL"
 assert rec["countries"]==[row["country"]]
 assert rec["authority"]["name"]==row["authority"]
 assert rec["authority"]["type"]=="GOVERNMENT"
 assert rec["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
 assert rec["editorialStatus"]=="STUB"
 assert rec["sources"][0]["tier"]=="A_PRIMARY"
 assert rec["sources"][0]["url"]==row["source"]
 assert rec["localizedTitles"]==row["localizedTitles"]
 assert rec.get("introducedYear") is None and rec.get("introducedYearSource") is None
 assert rec["recurrenceRules"]==row["recurrenceRules"]
 m=row["recurrenceRules"][0]["month"];d=row["recurrenceRules"][0]["day"]
 date_2026=f"2026-{m:02}-{d:02}"
 assert [x["startDate"] for x in occ["occurrences"] if x["observanceId"]==rid]==[date_2026],(rid,date_2026)
 assert markets[row["country"]]==1,row["country"]
assert len([r for r in records if r["id"].startswith("ph-w11-")])==144
assert len([r for r in records if r["id"].endswith("-dfat-national-day")])==156
assert len(records)-711==300
assert len(records)<1111, "PR must stay draft under 1111"
print("PASS: 1011 canonical draft IDs (+300 vs main), 192 markets, 156 DFAT + 144 NCCA, no false 1111 merge claim")
