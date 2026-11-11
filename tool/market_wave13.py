#!/usr/bin/env python3
"""Wave13: 43 Philippine NCCA cultural periods/days + 57 EURES member-state holidays.

Source-status distinction: an EU institutional index of member states' public
holidays does not replace a national legislative text, and a Philippine NCCA
cultural period is not necessarily a statutory non-working holiday.
"""
import json, calendar
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"data/market/wave13_ncca_eures_100_20261111.json"
SOURCES={
"PH":"https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/",
"EU":"https://eures.europa.eu/eures-services/chat-eures-advisers/public-holidays-calendar_en"
}
LOCALES={"en","it","es","fr","de","pt"}
def dates(rule,year):
 k=rule["kind"]
 if k=="FIXED_DATE":
  d=date(year,rule["month"],rule["day"])
  return d,d
 if k=="FIRST_MONDAY_EXCEPT_FEB1_FRIDAY":
  assert rule["month"]==2
  first=date(year,2,1)
  d=first if first.weekday()==4 else first+timedelta(days=(0-first.weekday())%7)
  return d,d
 if k=="NTH_WEEKDAY":
  first=date(year,rule["month"],1)
  days=(rule["weekday"]-1-first.weekday())%7+7*(rule["occurrence"]-1)
  day=first+timedelta(days=days)
  assert day.month==rule["month"]
  return day,day
 assert k=="FIXED_RANGE"
 start=date(year,rule["startMonth"],rule["startDay"])
 endyear=year+int(rule["endMonth"]<rule["startMonth"])
 end=date(endyear,rule["endMonth"],rule["endDay"])
 assert start<=end
 return start,end
def load_wave13():
 d=json.loads(FILE.read_text(encoding="utf-8"))
 assert d["schemaVersion"]==1 and d["count"]==100
 assert d["datasetId"]=="world-days-wave13-ncca-eures-100-20261111"
 assert d["groupCounts"]=={"PH":43,"EURES_EU":57}
 assert d["previousDraft"]==1011 and d["expectedDraft"]==1111
 assert len(d["records"])==100
 assert len({r["id"] for r in d["records"]})==100
 assert len({r["canonicalTitleEn"] for r in d["records"]})==100
 assert set(d["locales"])==LOCALES
 assert Counter(r["country"]=="PH" for r in d["records"])=={True:43,False:57}
 assert Counter(r.get("periodKind","DAY") for r in d["records"])=={"MONTH":28,"WEEK":11,"DAY":61}
 assert len({r["country"] for r in d["records"] if r["country"]!="PH"})==24
 for row in d["records"]:
  country=row["country"];ph=country=="PH";r=row["recurrenceRules"]
  assert country.isupper() and len(country)==2
  assert row["scope"]=="NATIONAL"
  is_bridgid=row["id"]=="ie-w13-eures-st-brigid-s-day"
  assert row["officiality"]==("OFFICIAL_INSTITUTIONAL" if (ph or is_bridgid) else "RECOGNIZED_INSTITUTIONAL")
  assert row["authorityType"]==("GOVERNMENT" if (ph or is_bridgid) else "EU_INSTITUTION")
  assert row["source"]==("https://www.workplacerelations.ie/en/what_you_should_know/public-holidays/" if is_bridgid else SOURCES["PH" if ph else "EU"])
  assert row["sourceTier"]==("A_PRIMARY" if (ph or is_bridgid) else "B_INSTITUTIONAL")
  assert row["sourceReviewedOn"]=="2026-11-11"
  assert row["humanEditorialStatus"]==("SOURCE_PRIMARY_DATE_ESTABLISHMENT_VERIFIED_LONG_FORM_STUB" if is_bridgid else "INDEXED_STUB_NO_LONG_FORM")
  if is_bridgid:
   assert row["proposedIntroducedYear"]==2023
   assert row["introducedYearSource"]==row["source"]
  else:
   assert row["proposedIntroducedYear"] is None and row["introducedYearSource"] is None
  assert set(row["localizedTitles"])==LOCALES
  assert all(row["localizedTitles"][l]==row["canonicalTitleEn"] for l in LOCALES)
  assert row["titleTranslationStatus"]=="ENGLISH_FALLBACK_NATIVE_REVIEW_PENDING"
  assert len(r)==1
  for year in (2026,2027,2028,2029):
   start,end=dates(r[0],year)
   assert start.year==year
   assert start<=end
   if row["periodKind"]=="MONTH":
    assert start.day==1 and end.day==calendar.monthrange(year,start.month)[1]
    assert start.month==end.month
   if row["periodKind"]=="WEEK":
    assert 3<= (end-start).days <=17
   if row["periodKind"]=="DAY":
    assert start==end
  assert len(row["chronologyNote"])>=120 and len(row["dateRationale"])>=120
 return d["records"]
if __name__=="__main__":
 load_wave13()
 print("PASS: 43 NCCA periods/days and 57 EURES country-calendar entries, exactly 100 distinct scoped IDs")
