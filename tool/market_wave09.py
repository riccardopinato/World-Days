#!/usr/bin/env python3
"""Wave09: 12 national fixed civic days across BD ID KH MY VN LA.

Technical metadata only: primary 2026 registers and fixed civil anniversaries.
Native-language human editorial and formal release gates remain pending.
"""
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/market/wave09_six_markets_civic_20261110.json"
STAGED=ROOT/"data/research/FAST02_CIVIC_12_SOURCE_STAGED_20261110.json"
EXPECTED={"BD":2,"ID":2,"KH":3,"MY":2,"VN":2,"LA":1}
LOCALES={"en","it","es","fr","de","pt"}
HOSTS={"www.bb.org.bd","www.setneg.go.id","www.nbc.gov.kh","www.kln.gov.my","en.baochinhphu.vn","laoevisa.gov.la"}
def load_wave09_civic():
    data=json.loads(SRC.read_text(encoding="utf8"))
    old=json.loads(STAGED.read_text(encoding="utf8"))
    assert data["schemaVersion"]==old["schemaVersion"]==1
    assert data["count"]==len(data["records"])==old["count"]==12
    assert data["countryCounts"]==EXPECTED
    assert data["reviewStatus"]=="SOURCE_METADATA_PROPOSED_HUMAN_EDITORIAL_PENDING"
    assert data["admission"]=="PROPOSED_METADATA_IN_UNMERGED_PR68"
    assert data["countryExpansionImplementedInBranch"] is True
    assert set(data["locales"])==LOCALES
    assert data["sourceReviewDate"]=="2026-11-10"
    staged={r["id"]:r for r in old["records"]}
    assert len(staged)==12
    seen=set();names=set();bycountry={}
    for r in data["records"]:
        rid=r["id"];country=r["country"];title=r["canonicalTitleEn"]
        assert rid not in seen and (country,title) not in names
        seen.add(rid);names.add((country,title))
        assert country in EXPECTED
        bycountry[country]=bycountry.get(country,0)+1
        assert r["source"]==staged[rid]["source"]
        assert r["recurrenceRules"]==staged[rid]["recurrenceRules"]
        assert r["localizedTitles"]==staged[rid]["localizedTitles"]
        assert r["countryExpansionRequired"] is False
        assert r["admission"]=="PROPOSED_METADATA_IN_UNMERGED_PR68"
        assert r["scope"]=="NATIONAL"
        assert r["sourceTier"]=="A_PRIMARY"
        assert r["authorityType"]=="GOVERNMENT"
        assert r["officiality"]=="OFFICIAL_INSTITUTIONAL"
        assert r["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert r["proposedIntroducedYear"] is None and r["introducedYearSource"] is None
        assert set(r["localizedTitles"])==LOCALES
        assert r["localizedTitles"]["en"]==title
        assert all(len(t.strip())>=6 for t in r["localizedTitles"].values())
        url=urlsplit(r["source"])
        assert url.scheme=="https" and url.hostname in HOSTS,(rid,url.hostname)
        rule=r["recurrenceRules"][0]
        assert rule["kind"]=="FIXED_DATE"
        assert set(rule)=={"kind","month","day"}
        assert 1<=rule["month"]<=12
        assert [date(y,rule["month"],rule["day"]).isoformat() for y in (2026,2027,2028)]
        assert len(r["researchSummary"])>=90 and len(r["chronologyNote"])>=100
    assert bycountry==EXPECTED
    return data["records"]
if __name__=="__main__":
    print("WAVE09 SIX-MARKET SOURCE PASS:",len(load_wave09_civic()),"metadata drafts")
