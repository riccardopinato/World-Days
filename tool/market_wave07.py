#!/usr/bin/env python3
"""Wave07 India: primary-source/country/title/day recurrence gate.

Metadata stage, human editorial review NOT certified.
"""
from datetime import date
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/market/wave07_india_three_20261109.json"
LOCALES={"en","it","es","fr","de","pt"}
EXPECTED={
"india-republic-day":(1,26,"2026-01-26","2027-01-26","2028-01-26"),
"india-independence-day":(8,15,"2026-08-15","2027-08-15","2028-08-15"),
"india-gandhi-jayanti":(10,2,"2026-10-02","2027-10-02","2028-10-02")
}
OFFICIAL="https://www.indiapost.gov.in/holidays-list"
CORROBORATION="https://www.ursc.gov.in/holidays.jsp"
def load_wave07_india():
    d=json.loads(SRC.read_text(encoding="utf-8"))
    assert d["schemaVersion"]==1
    assert d["datasetId"]=="world-days-market-wave07-india-2026-11-09"
    assert d["count"]==len(d["records"])==3
    assert d["countryCounts"]=={"IN":3}
    assert d["sourceReviewDate"]=="2026-11-09"
    assert set(d["locales"])==LOCALES
    assert d["reviewStatus"]=="SOURCE_VERIFIED_METADATA_ONLY_HUMAN_EDITORIAL_NOT_APPROVED"
    byid={r["id"]:r for r in d["records"]}
    assert set(byid)==set(EXPECTED)
    assert len({r["canonicalTitleEn"] for r in d["records"]})==3
    for rid,r in byid.items():
        month,day,*dates=EXPECTED[rid]
        assert r["country"]=="IN"
        assert r["canonicalTitleEn"].endswith(" — India")
        assert r["localizedTitles"]["en"]==r["canonicalTitleEn"]
        assert set(r["localizedTitles"])==LOCALES
        assert all(len(s.strip())>=8 for s in r["localizedTitles"].values())
        assert r["source"]==OFFICIAL
        assert r["additionalSources"]==[CORROBORATION]
        assert r["authority"]=="Government of India, Department of Posts"
        assert r["authorityType"]=="GOVERNMENT"
        assert r["officiality"]=="OFFICIAL_INSTITUTIONAL"
        assert r["sourceTier"]=="A_PRIMARY"
        assert r["designation"]=="NATIONAL_CIVIC_OR_STATUTORY_OBSERVANCE"
        assert r["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert r["proposedIntroducedYear"] is None
        assert r["introducedYearSource"] is None
        assert len(r["chronologyNote"])>=180
        assert len(r["dateRationale"])>=170
        assert len(r["researchSummary"])>=175
        assert r["recurrenceRules"]==[{"kind":"FIXED_DATE","month":month,"day":day}]
        assert [date(year,month,day).isoformat() for year in (2026,2027,2028)]==dates
    return d["records"]
if __name__=="__main__":
    print("WAVE07 INDIA SOURCE GATE PASS:",len(load_wave07_india()),"distinct source-bound fixed dates")
