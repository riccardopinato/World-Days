#!/usr/bin/env python3
"""Wave06 additive 7-record metadata admission gate (dependent on Wave05 PR #65)."""
import json
from pathlib import Path
from market_wave06 import EXPECTED,load_wave06_japan,date_of
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
r=catalog["records"];by_id={z["id"]:z for z in r}
assert len(by_id)==len(r)==472
assert catalog["datasetVersion"]=="2026.11.09.7"
assert sum(z["scope"]=="GLOBAL" for z in r)==285
assert sum(z["scope"]=="NATIONAL" for z in r)==187
assert sum(z["countries"]==["JP"] for z in r)==13
fresh=load_wave06_japan()
assert {x["id"] for x in fresh}==set(EXPECTED)
for x in fresh:
    rec=by_id[x["id"]]
    assert rec["scope"]=="NATIONAL" and rec["countries"]==["JP"]
    assert rec["editorialStatus"]=="STUB"
    assert rec["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
    assert rec["authority"]["type"]=="GOVERNMENT"
    assert rec.get("introducedYear") is None and rec.get("introducedYearSource") is None
    assert set(rec["localizedTitles"])=={"en","it","es","fr","de","pt"}
    assert rec["localizedTitles"]==x["localizedTitles"]
    assert rec["sources"][0]["tier"]=="A_PRIMARY"
    assert rec["sources"][0]["url"]==x["source"]
    generated=[o["startDate"] for o in occ["occurrences"] if o["observanceId"]==x["id"]]
    assert generated==[EXPECTED[x["id"]][0]],(x["id"],generated)
assert len(occ["dateIndex"])==365
print("WAVE06 JP ADDITIVE PASS: 472 catalog entries, 285 world + 184 national, JP 13; 7 new six-locales source metadata STUB")
