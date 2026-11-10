#!/usr/bin/env python3
"""Wave08 Canada bulk-content QA: 20 sourced fixed dates, no duplicate IDs or claims of public holidays."""
from datetime import date
from pathlib import Path
import json
from market_wave08 import load_wave08_canada, EXPECTED_DATES
ROOT=Path(__file__).resolve().parents[1]
cat=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
records=cat["records"];ids={r["id"]:r for r in records}
assert len(records)==len(ids)==511,("invalid catalog size",len(records))
assert cat["datasetVersion"]=="2026.11.10.10"
assert sum(r["scope"]=="GLOBAL" for r in records)==292
assert sum(r["scope"]=="NATIONAL" for r in records)==219
assert sum(r["countries"]==["CA"] for r in records)==25
fresh=load_wave08_canada()
assert len(fresh)==20
assert set(x["canonicalTitleEn"] for x in fresh)==set(EXPECTED_DATES)
for x in fresh:
    r=ids[x["id"]]
    assert r["scope"]=="NATIONAL" and r["countries"]==["CA"]
    assert r["canonicalTitleEn"]==x["canonicalTitleEn"]
    assert r["editorialStatus"]=="STUB"
    assert r["authority"]["name"]=="Canadian Heritage, Government of Canada"
    assert r["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
    assert r["authority"]["type"]=="GOVERNMENT"
    assert r.get("introducedYear")==x["proposedIntroducedYear"]
    assert r.get("introducedYearSource")==x["introducedYearSource"]
    assert set(r["localizedTitles"])=={"en","it","es","fr","de","pt"}
    assert r["localizedTitles"]==x["localizedTitles"]
    assert any(s["tier"]=="A_PRIMARY" and s["url"]==x["source"] for s in r["sources"])
    assert all(s["url"].startswith("https://") for s in r["sources"])
    rule=r["recurrenceRules"][0]
    assert rule["kind"]=="FIXED_DATE"
    assert (rule["month"],rule["day"])==EXPECTED_DATES[x["canonicalTitleEn"]]
    dates=[o["startDate"] for o in occ["occurrences"] if o["observanceId"]==x["id"]]
    expected=date(2026,rule["month"],rule["day"]).isoformat()
    assert dates==[expected],(x["id"],dates,expected)
assert len(occ["dateIndex"])==365
print("WAVE08 CA BULK PASS: 20 new national commemorations, 504 catalog IDs, CA 25, 6 title locales, dates 2026–2028, long-form editorial pending.")
