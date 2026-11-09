#!/usr/bin/env python3
"""Wave08 Canada: strict provenance, distinct 20 federal commemorations and legal date rules.

All 20 are metadata-only government recognized commemorations, not automatically
statutory bank/public holidays; native editorial review remains pending.
"""
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
import json

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/market/wave08_canada_twenty_20261109.json"
LOCALES={"en","it","es","fr","de","pt"}
LEGACY_IDS={
"canada-national-flag-day",
"canada-national-indigenous-peoples-day",
"canada-multiculturalism-day",
"canada-national-acadian-day",
"canada-truth-and-reconciliation-day",
}
EXCLUDED={
"Canadian Multiculturalism Day",
"National Acadian Day",
"National Child Day (Canada)",
"National Day of Observance for COVID-19",
}
EXPECTED_DATES={
"National Day of Remembrance for Victims of Air Disasters":(1,8),
"Sir John A. Macdonald Day":(1,11),
"National Day of Remembrance of the Quebec City Mosque Attack and Action against Islamophobia":(1,29),
"National Indigenous Languages Day":(3,31),
"Anniversary of the Battle of Vimy Ridge":(4,9),
"Armenian Genocide Remembrance Day (Canada)":(4,24),
"British Home Child Day":(9,28),
"Persons Day (Canada)":(10,18),
"Indigenous Veterans Day (Canada)":(11,8),
"National Day of Remembrance and Action on Violence Against Women (Canada)":(12,6),
"National Ribbon Skirt Day":(1,4),
"Raoul Wallenberg Day":(1,17),
"Lincoln Alexander Day":(1,21),
"Red Dress Day":(5,5),
"Dutch Heritage Day":(5,5),
"National Day of Remembrance for Victims of Terrorism":(6,23),
"Day of Commemoration of the Great Upheaval":(7,28),
"Emancipation Day (Canada)":(8,1),
"National Seniors Day (Canada)":(10,1),
"Anniversary of the Statute of Westminster (Canada)":(12,11),
}
CANADA_CALENDAR="https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days.html"
LAW="https://laws-lois.justice.gc.ca/eng/acts/N-16.2/section-2.html"
YEARS={"National Ribbon Skirt Day":2022,"Sir John A. Macdonald Day":2002}

def load_wave08_canada():
    d=json.loads(SRC.read_text(encoding="utf-8"))
    assert d["schemaVersion"]==1
    assert d["datasetId"]=="world-days-market-wave08-canada-2026-11-09"
    assert d["count"]==len(d["records"])==20
    assert d["countryCounts"]=={"CA":20}
    assert d["sourceReviewDate"]=="2026-11-09"
    assert d["reviewStatus"]=="SOURCE_VERIFIED_METADATA_ONLY_HUMAN_EDITORIAL_NOT_APPROVED"
    assert set(d["locales"])==LOCALES and set(d["exclusions"])==EXCLUDED
    bytitle={r["canonicalTitleEn"]:r for r in d["records"]}
    ids={r["id"] for r in d["records"]}
    assert len(bytitle)==len(ids)==20
    assert set(bytitle)==set(EXPECTED_DATES)
    assert not ids.intersection(LEGACY_IDS)
    for title,r in bytitle.items():
        m,day=EXPECTED_DATES[title]
        assert r["id"].startswith("canada-"),title
        assert r["country"]=="CA"
        assert r["localizedTitles"]["en"]==title
        assert set(r["localizedTitles"])==LOCALES
        assert all(isinstance(s,str) and len(s.strip())>=8 for s in r["localizedTitles"].values())
        assert r["recurrenceRules"]==[{"kind":"FIXED_DATE","month":m,"day":day}]
        assert [date(y,m,day).isoformat() for y in (2026,2027,2028)]==[
            f"{y:04d}-{m:02d}-{day:02d}" for y in (2026,2027,2028)]
        assert r["sourceReviewedOn"]==d["sourceReviewDate"]
        assert r["authority"]=="Canadian Heritage, Government of Canada"
        assert r["authorityType"]=="GOVERNMENT"
        assert r["officiality"]=="OFFICIAL_INSTITUTIONAL"
        assert r["sourceTier"]=="A_PRIMARY"
        assert r["designation"]=="NATIONAL_GOVERNMENT_RECOGNIZED_COMMEMORATION"
        assert r["holidayClassification"]=="COMMEMORATIVE_DAY_NOT_AUTOMATIC_PUBLIC_HOLIDAY"
        assert r["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert r["subject"]=="HISTORY" and r["category"]=="CIVIC_HISTORY"
        assert len(r["chronologyNote"])>=160
        assert len(r["dateRationale"])>=125
        assert len(r["researchSummary"])>=150
        urls=[r["source"],*r["additionalSources"]]
        assert len(urls)==len(set(urls))
        assert CANADA_CALENDAR in urls
        for url in urls:
            parts=urlsplit(url)
            assert parts.scheme=="https" and parts.hostname in {
                "www.canada.ca","laws.justice.gc.ca","laws-lois.justice.gc.ca",
                "www.ourcommons.ca","women-gender-equality.canada.ca",
            },(title,url)
        yr=YEARS.get(title)
        assert r["proposedIntroducedYear"]==yr,title
        if yr is None:
            assert r["introducedYearSource"] is None
        else:
            assert r["introducedYearSource"]==r["source"]
        if title=="National Ribbon Skirt Day":
            assert r["source"]==LAW
    return d["records"]

if __name__=="__main__":
    print("WAVE08 CA SOURCE GATE PASS",len(load_wave08_canada()),"government-commemorative metadata only")
