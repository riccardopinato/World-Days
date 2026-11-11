#!/usr/bin/env python3
"""Exact 611-record Wave09 canonical source/recurrence regression."""
import json
from collections import Counter
from pathlib import Path
from market_wave09 import load_wave09,day
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
by_id={r["id"]:r for r in catalog["records"]}
assert catalog["datasetVersion"]=="2026.11.11.2"
assert len(by_id)==len(catalog["records"])==611
assert Counter(r["scope"] for r in by_id.values())=={"GLOBAL":289,"NATIONAL":322}
old_expected={"SK":6,"CZ":7,"PL":5,"SE":1,"NO":5,"FI":15}
new_counts={"SK":23,"CZ":18,"PL":13,"SE":9,"NO":5,"FI":5}
for country in new_counts:
 assert Counter(r["countries"][0] for r in by_id.values() if r["scope"]=="NATIONAL")[country]==old_expected[country]+new_counts[country]
for source in load_wave09():
 rid=source["id"];r=by_id[rid]
 assert r["scope"]=="NATIONAL"
 assert r["countries"]==[source["country"]]
 assert r["authority"]["officiality"]==source["officiality"]
 assert r["editorialStatus"]=="STUB"
 assert r.get("introducedYear") is None and r.get("introducedYearSource") is None
 assert r["sources"][0]["url"]==source["source"]
 assert r["sources"][0]["tier"]==source["sourceTier"]
 assert r["recurrenceRules"]==source["recurrenceRules"]
 assert r["localizedTitles"]==source["localizedTitles"]
 starts=[o["startDate"] for o in occ["occurrences"] if o["observanceId"]==rid]
 assert starts==[day(source["recurrenceRules"][0],2026).isoformat()],(rid,starts)
# 27 Canadian admissions from Wave08 are preserved: this wave makes the full +100.
assert sum(r["id"].startswith("ca-") for r in by_id.values() if r["scope"]=="NATIONAL")>=27
print("PASS: 611 identities, 73 Wave09 and 27 Wave08 source-level admissions, zero invented rich-editorial approvals")
