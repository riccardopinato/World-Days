#!/usr/bin/env python3
"""Wave12: 156 national dates from the Australian DFAT diplomatic-protocol index.

This is first-party evidence of Australia's diplomatic national-day listing,
NOT independent legal proof that the listed day is a statutory paid holiday.
Syria's evolving national-day position and Danish monarch's birthday are
quarantined from this annual fixed-date dataset until separately verified.
"""
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
import json
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/market/wave12_diplomatic_158_countries_20261111.json"
DFAT="https://protocol.dfat.gov.au/Public/NationalDays"
LOCALES={"en","it","es","fr","de","pt"}
def load_wave12():
 d=json.loads(SOURCE.read_text(encoding="utf-8"))
 assert d["schemaVersion"]==1
 assert d["datasetId"]=="world-days-wave12-dfat-156-countries-20261111"
 assert d["count"]==d["countryCount"]==len(d["records"])==len(d["countries"])==156
 assert d["source"]==DFAT and d["sourceReviewedOn"]=="2026-11-11"
 assert d["sourceRole"]=="GOVERNMENT_RECOGNIZED_DIPLOMATIC_PROTOCOL_NATIONAL_DAYS_NOT_NATIONAL_STATUTORY_LAW"
 assert {x["country"] for x in d["records"]}=={c["code"] for c in d["countries"]}
 assert len({r["id"] for r in d["records"]})==156
 assert len({r["canonicalTitleEn"] for r in d["records"]})==156
 assert {x["country"] for x in d["excludedForDateOrContemporaryStatusReview"]}=={"DK","SY"}
 for r in d["records"]:
  code=r["country"];rid=r["id"]
  assert len(code)==2 and code.isupper()
  assert rid==code.lower()+"-dfat-national-day"
  assert r["source"]==DFAT and r["sourceTier"]=="A_PRIMARY"
  assert r["authorityType"]=="GOVERNMENT"
  assert r["officiality"]=="RECOGNIZED_INSTITUTIONAL"
  assert r["holidayClassification"]=="AUSTRALIAN_DIPLOMATIC_PROTOCOL_NATIONAL_DAY_NOT_INDEPENDENTLY_VERIFIED_STATUTORY_HOLIDAY"
  assert r["sourceReviewedOn"]=="2026-11-11"
  assert r["proposedIntroducedYear"] is None and r["introducedYearSource"] is None
  assert r["humanEditorialStatus"]=="SOURCE_INDEX_ONLY_LONG_FORM_NOT_REVIEWED"
  assert r["titleTranslationStatus"]=="EN_FALLBACK_NOT_NATIVE_TRANSLATION"
  assert len(r["recurrenceRules"])==1
  rule=r["recurrenceRules"][0]
  assert rule["kind"]=="FIXED_DATE"
  for year in (2026,2027,2028,2029):
   assert date(year,rule["month"],rule["day"]).year==year
  assert set(r["localizedTitles"])==LOCALES
  assert all(r["localizedTitles"][locale]==r["canonicalTitleEn"] for locale in LOCALES)
  assert len(r["chronologyNote"])>=100 and len(r["dateRationale"])>=90
 return d["records"]
if __name__=="__main__":
 load_wave12()
 print("PASS: 156 country-specific DFAT diplomatic-protocol dates, fixed annual rules, nonstatutory distinction; DK/SY excluded")
