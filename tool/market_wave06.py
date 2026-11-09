#!/usr/bin/env python3
"""Seven separate Japanese statutory-day identities (not global day aliases).

Uses Article 2 of Japan's National Holidays Act and the Cabinet Office calendar.
No astronomical equinox, substitute office closure or one-off Olympic exception.
"""
from datetime import date
from calendar import monthrange
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/market/wave06_japan_seven_20261109.json"
LOCALES={"en","it","es","fr","de","pt"}
SOURCES={
    "https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html",
    "https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku.html"
}
EXPECTED={
    "japan-greenery-day":("2026-05-04","2027-05-04","2028-05-04"),
    "japan-childrens-day":("2026-05-05","2027-05-05","2028-05-05"),
    "japan-marine-day":("2026-07-20","2027-07-19","2028-07-17"),
    "japan-mountain-day":("2026-08-11","2027-08-11","2028-08-11"),
    "japan-respect-for-the-aged-day":("2026-09-21","2027-09-20","2028-09-18"),
    "japan-sports-day":("2026-10-12","2027-10-11","2028-10-09"),
    "japan-labor-thanksgiving-day":("2026-11-23","2027-11-23","2028-11-23")
}
def date_of(rule,year):
    if rule["kind"]=="FIXED_DATE":
        return date(year,rule["month"],rule["day"])
    assert rule["kind"]=="NTH_WEEKDAY"
    assert rule["weekday"]==1
    first=date(year,rule["month"],1)
    day=1+(0-first.weekday())%7+7*(rule["occurrence"]-1)
    assert day <= monthrange(year,rule["month"])[1]
    return date(year,rule["month"],day)
def load_wave06_japan():
    d=json.loads(SRC.read_text(encoding="utf-8"))
    assert d["schemaVersion"]==1 and d["count"]==len(d["records"])==7
    assert d["datasetId"]=="world-days-market-wave06-japan-2026-11-09"
    assert d["countryCounts"]=={"JP":7}
    assert set(d["locales"])==LOCALES
    assert d["reviewStatus"]=="SOURCE_VERIFIED_METADATA_ONLY_HUMAN_EDITORIAL_NOT_APPROVED"
    assert d["sourceReviewDate"]=="2026-11-09"
    by_id={r["id"]:r for r in d["records"]}
    assert set(by_id)==set(EXPECTED)
    assert len(set(r["canonicalTitleEn"] for r in d["records"]))==7
    for rid,r in by_id.items():
        assert r["country"]=="JP"
        assert r["canonicalTitleEn"].endswith(" — Japan")
        assert set(r["localizedTitles"])==LOCALES
        assert r["localizedTitles"]["en"]==r["canonicalTitleEn"]
        assert all(len(x.strip()) >= 7 for x in r["localizedTitles"].values())
        assert set([r["source"],*r["additionalSources"]])==SOURCES
        assert len([r["source"],*r["additionalSources"]])==2
        assert r["authority"]=="Cabinet Office, Government of Japan"
        assert r["authorityType"]=="GOVERNMENT"
        assert r["officiality"]=="OFFICIAL_INSTITUTIONAL"
        assert r["sourceTier"]=="A_PRIMARY"
        assert r["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert r["holidayClassification"]=="STATUTORY_NATIONAL_HOLIDAY"
        assert r["sourceReviewedOn"]==d["sourceReviewDate"]
        assert r["proposedIntroducedYear"] is None and r["introducedYearSource"] is None
        assert len(r["chronologyNote"])>=130 and len(r["dateRationale"])>=120
        assert len(r["researchSummary"])>=150
        assert len(r["recurrenceRules"])==1
        rule=r["recurrenceRules"][0]
        assert rule["kind"] in {"FIXED_DATE","NTH_WEEKDAY"}
        if rule["kind"]=="FIXED_DATE":
            assert set(rule)=={"kind","month","day"}
        else:
            assert set(rule)=={"kind","month","weekday","occurrence"}
            assert rule["occurrence"] in {2,3}
        got=tuple(date_of(rule,year).isoformat() for year in (2026,2027,2028))
        assert got==EXPECTED[rid],(rid,got,EXPECTED[rid])
    return d["records"]
if __name__=="__main__":
    print(f"Wave06 JP metadata gate PASS: {len(load_wave06_japan())} distinct legal identities")
