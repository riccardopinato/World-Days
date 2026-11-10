#!/usr/bin/env python3
"""Wave07 India content admission gate, stacked after PR #65 + PR #66."""
import json
from pathlib import Path
from market_wave07 import EXPECTED, load_wave07_india
ROOT=Path(__file__).resolve().parents[1]
cat=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
records=cat["records"];byid={r["id"]:r for r in records}
assert len(records)==len(byid)==511
assert cat["datasetVersion"]=="2026.11.10.10"
assert sum(r["scope"]=="GLOBAL" for r in records)==285
assert sum(r["scope"]=="NATIONAL" for r in records)==219
assert sum(r["countries"]==["IN"] for r in records)==5
fresh=load_wave07_india()
assert len(fresh)==3 and {x["id"] for x in fresh}==set(EXPECTED)
for x in fresh:
    r=byid[x["id"]]
    assert r["scope"]=="NATIONAL" and r["countries"]==["IN"]
    assert r["canonicalTitleEn"]==x["canonicalTitleEn"]
    assert r["editorialStatus"]=="STUB"
    assert r["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
    assert r["authority"]["type"]=="GOVERNMENT"
    assert r.get("introducedYear") is None
    assert r.get("introducedYearSource") is None
    assert set(r["localizedTitles"])=={"en","it","es","fr","de","pt"}
    assert r["localizedTitles"]==x["localizedTitles"]
    assert r["sources"][0]["url"]==x["source"] and r["sources"][0]["tier"]=="A_PRIMARY"
    dates=[o["startDate"] for o in occ["occurrences"] if o["observanceId"]==x["id"]]
    assert dates==[EXPECTED[x["id"]][2]],(x["id"],dates)
assert len(occ["dateIndex"])==365
print("WAVE07 IN CONTENT PASS: 511 unique; 285 global, 207 national, India five; three 6-locales original source STUBs; no release or human content approval.")
