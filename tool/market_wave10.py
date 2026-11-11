#!/usr/bin/env python3
"""Wave10 source-index admission gate: 100 distinct KR/PH recurring identity records.

Important: the Philippine National Commission for Culture and the Arts
lists numerous artist birth/death anniversaries as significant dates; these
are catalog cultural anniversaries, NOT statutory public holidays.
"""
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/market/wave10_hundred_kr_ph_20261111.json"
EXPECTED={"KR":50,"PH":50}
URLS={"KR":"https://www.mois.go.kr/chd/sub/a05/feteDay/screen.do",
      "PH":"https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/"}
LOCALES={"en","it","es","fr","de","pt"}
def date_for(rule,year):
 month=rule["month"]
 if rule["kind"]=="FIXED_DATE":
  return date(year,month,rule["day"])
 assert rule["kind"]=="NTH_WEEKDAY"
 first=date(year,month,1)
 return first+timedelta(days=(rule["weekday"]-1-first.weekday())%7+7*(rule["occurrence"]-1))

def load_wave10():
 data=json.loads(SOURCE.read_text(encoding="utf-8"))
 assert data["schemaVersion"]==1
 assert data["datasetId"]=="world-days-wave10-hundred-kr-ph-20261111"
 assert data["sourceReviewDate"]=="2026-11-11"
 assert data["count"]==len(data["records"])==100
 assert data["countryCounts"]==EXPECTED
 assert set(data["locales"])==LOCALES
 assert data["titleReviewStatus"]=="EN_FALLBACK_FIVE_NONEN_NATIVE_REVIEW_REQUIRED"
 assert data["introducedYearPolicy"]=="UNKNOWN_NULL"
 rows=data["records"]
 assert Counter(r["country"] for r in rows)==EXPECTED
 assert len({r["id"] for r in rows})==100
 assert len({r["canonicalTitleEn"] for r in rows})==100
 kinds=Counter(r["recurrenceRules"][0]["kind"] for r in rows)
 assert kinds=={"FIXED_DATE":93,"NTH_WEEKDAY":7},kinds
 for row in rows:
  country=row["country"];rid=row["id"];source=row["source"]
  assert rid.startswith(country.lower()+"-w10-")
  assert row["officiality"]=="OFFICIAL_INSTITUTIONAL"
  assert row["authorityType"]=="GOVERNMENT"
  assert row["sourceTier"]=="A_PRIMARY"
  assert row["sourceReviewedOn"]=="2026-11-11"
  assert source==URLS[country] and urlparse(source).scheme=="https"
  assert len(row["sourceTitleOriginal"].strip())>=2
  assert row["aliases"]==[row["sourceTitleOriginal"]]
  assert row["holidayClassification"].endswith("NOT_STATUTORY_HOLIDAY") if country=="PH" else "NOT_NECESSARILY_HOLIDAY" in row["holidayClassification"]
  assert row["proposedIntroducedYear"] is None and row["introducedYearSource"] is None
  assert row["humanEditorialStatus"]=="SOURCE_INDEX_METADATA_ONLY_STORY_NOT_REVIEWED"
  assert row["titleTranslationStatus"]=="ENGLISH_FALLBACK_NATIVE_REVIEW_PENDING"
  assert set(row["localizedTitles"])==LOCALES
  assert all(value==row["canonicalTitleEn"] for value in row["localizedTitles"].values())
  assert row["subject"]=="CULTURE" and row["periodKind"]=="DAY"
  assert len(row["recurrenceRules"])==1
  rule=row["recurrenceRules"][0]
  assert rule["kind"] in {"FIXED_DATE","NTH_WEEKDAY"}
  for year in (2026,2027,2028,2029):
   d=date_for(rule,year)
   assert d.year==year and d.month==rule["month"]
  assert len(row["chronologyNote"])>=115
  assert len(row["dateRationale"])>=70
 korean=next(r for r in rows if r["id"]=="kr-w10-culture-day-in-korea")
 assert [date_for(korean["recurrenceRules"][0],y).isoformat() for y in (2026,2027,2028)]==["2026-10-17","2027-10-16","2028-10-21"]
 return rows

if __name__=="__main__":
 load_wave10()
 print("PASS: 100 source-index identities, 50 Korean government days and 50 Philippine cultural anniversaries")
