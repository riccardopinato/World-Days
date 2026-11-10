#!/usr/bin/env python3
"""Source-originator admission audit for WHO/UNESCO Wave10.

All seven sourced observances have verified annual dates. Passing this gate
does NOT assert WHO World Health Assembly official designation or qualify
human editorial/native-language signoff.
"""
import json
from datetime import date, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
core=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
calendar=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
rows=core["records"];by_id={r["id"]:r for r in rows}
expected={
"world-hearing-day":("WHO","https://www.who.int/campaigns/world-hearing-day",("2026-03-03","2027-03-03","2028-03-03"),"FIXED_DATE"),
"world-hand-hygiene-day":("WHO","https://www.who.int/campaigns/world-hand-hygiene-day",("2026-05-05","2027-05-05","2028-05-05"),"FIXED_DATE"),
"world-rabies-day":("WHO","https://www.who.int/campaigns/world-rabies-day",("2026-09-28","2027-09-28","2028-09-28"),"FIXED_DATE"),
"world-polio-day":("WHO","https://www.who.int/europe/campaigns/world-polio-day",("2026-10-24","2027-10-24","2028-10-24"),"FIXED_DATE"),
"world-leprosy-day":("WHO","https://www.who.int/campaigns/world-leprosy-day",("2026-01-25","2027-01-31","2028-01-30"),"LAST_WEEKDAY"),
"international-day-of-women-in-multilateralism":("UNESCO","https://www.unesco.org/en/days/women-multilateralism",("2026-01-25","2027-01-25","2028-01-25"),"FIXED_DATE"),
"international-day-against-violence-and-bullying-at-school-including-cyberbullying":("UNESCO","https://www.unesco.org/en/days/against-school-violence-and-bullying",("2026-11-05","2027-11-04","2028-11-02"),"NTH_WEEKDAY"),
}
assert core["datasetVersion"]=="2026.11.10.10"
assert len(rows)==len(by_id)==511
assert sum(r["scope"]=="GLOBAL" for r in rows)==292
assert sum(r["scope"]=="NATIONAL" for r in rows)==219
assert len(calendar["dateIndex"])==365
assert set(expected).issubset(by_id)
for rid,(agency,source,dates,kind) in expected.items():
    r=by_id[rid];rule=r["recurrenceRules"][0]
    assert r["scope"]=="GLOBAL" and r["countries"]==[]
    assert r["authority"]["type"]==agency
    assert r["authority"]["officiality"]==("OFFICIAL_UNESCO" if agency=="UNESCO" else "OFFICIAL_WHO")
    assert r["editorialStatus"]=="STUB"
    assert r["sources"][0]["tier"]=="A_PRIMARY"
    assert r["sources"][0]["url"]==source
    assert set(r["localizedTitles"])=={"en","it","es","fr","de","pt"}
    assert all(len(str(t).strip())>=7 for t in r["localizedTitles"].values())
    assert rule["kind"]==kind
    if kind=="FIXED_DATE":
        actual=[date(y,rule["month"],rule["day"]).isoformat() for y in (2026,2027,2028)]
    elif kind=="LAST_WEEKDAY":
        actual=[]
        for y in (2026,2027,2028):
            d=date(y,2,1)-timedelta(days=1)
            while d.isoweekday()!=rule["weekday"]:d-=timedelta(days=1)
            actual.append(d.isoformat())
        assert rule["month"]==1 and rule["weekday"]==7
    else:
        actual=[]
        for y in (2026,2027,2028):
            d=date(y,rule["month"],1)
            day=1+(rule["weekday"]-d.isoweekday())%7+7*(rule["occurrence"]-1)
            actual.append(date(y,rule["month"],day).isoformat())
        assert rule["month"]==11 and rule["weekday"]==4 and rule["occurrence"]==1
    assert actual==list(dates),(rid,actual,dates)
    found=[o["startDate"] for o in calendar["occurrences"] if o["observanceId"]==rid]
    assert found==[dates[0]],(rid,found)
print("WAVE10 WHO UNESCO PASS: seven new first-party global observances, 511 canonical / 292 global / 219 national, all 6 title locales, 2026-2028 recurrence vectors")
