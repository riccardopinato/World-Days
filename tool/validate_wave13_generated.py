#!/usr/bin/env python3
"""Exactly 1111 source-index records in the generated World Days catalog."""
import json
from collections import Counter
from pathlib import Path
from market_wave13 import load_wave13, dates

ROOT=Path(__file__).resolve().parents[1]
cat=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
by_id={r["id"]:r for r in cat["records"]}
assert cat["datasetVersion"]=="2026.11.11.6"
assert len(cat["records"])==len(by_id)==1111
assert Counter(r["scope"] for r in by_id.values())=={"GLOBAL":289,"NATIONAL":822}
markets=Counter(r["countries"][0] for r in by_id.values() if r["scope"]=="NATIONAL")
assert len(markets)==193
assert markets['DK']==3
assert markets["PH"]==244
new=load_wave13()
assert len(new)==100
for row in new:
 rid=row["id"];r=by_id[rid]
 assert r["canonicalTitleEn"]==row["canonicalTitleEn"]
 assert r["periodKind"]==row["periodKind"]
 assert r["scope"]=="NATIONAL"
 assert r["countries"]==[row["country"]]
 assert r["authority"]["officiality"]==row["officiality"]
 assert r["authority"]["type"]==row["authorityType"]
 assert r["sources"][0]["tier"]==row["sourceTier"]
 assert r["sources"][0]["url"]==row["source"]
 assert r["localizedTitles"]==row["localizedTitles"]
 assert r["editorialStatus"]=="STUB"
 if rid=="ie-w13-eures-st-brigid-s-day":
  assert r.get("introducedYear")==2023
  assert r.get("introducedYearSource")==row["source"]
 else:
  assert r.get("introducedYear") is None and r.get("introducedYearSource") is None
 assert r["recurrenceRules"]==row["recurrenceRules"]
 start,end=dates(row["recurrenceRules"][0],2026)
 hits=[x for x in occ["occurrences"] if x["observanceId"]==rid]
 assert len(hits)==1,(rid,hits)
 assert hits[0]["startDate"]==start.isoformat(),rid
 assert hits[0]["endDate"]==end.isoformat(),rid
assert len([r for r in cat["records"] if r["id"].startswith("ph-w13-")])==43
print("PASS: 1111 canonical IDs, +100 Wave13, 193 country markets, Irish WRC movable February exception verified")
