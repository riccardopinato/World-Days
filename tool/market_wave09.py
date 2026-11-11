"""Wave09: 73 country-specific days from 6 competent institutional calendars."""
import json
from collections import Counter
from datetime import date,timedelta
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/market/wave09_primary_sixcountries_20261111.json"
COUNTS={"SK":23,"CZ":18,"PL":13,"SE":9,"NO":5,"FI":5}
HOSTS={"SK":"www.vlada.gov.sk","CZ":"ppropo.mpsv.cz","PL":"www.gov.pl","SE":"www.riksdagen.se","NO":"www.regjeringen.no","FI":"almanakka.helsinki.fi"}
LOCALES={"en","it","es","fr","de","pt"}
def day(rule,year):
 month=rule["month"]
 if rule["kind"]=="FIXED_DATE":return date(year,month,rule["day"])
 if rule["kind"]=="NTH_WEEKDAY":
  first=date(year,month,1)
  return first+timedelta(days=(rule["weekday"]-1-first.weekday())%7+7*(rule["occurrence"]-1))
 if rule["kind"]=="WEEKDAY_ON_OR_AFTER":
  first=date(year,month,rule["day"])
  return first+timedelta(days=(rule["weekday"]-1-first.weekday())%7)
 raise AssertionError(rule)
def load_wave09():
 data=json.loads(SOURCE.read_text(encoding="utf-8"))
 assert data["schemaVersion"]==1
 assert data["datasetId"]=="world-days-national-wave09-73-2026-11-11"
 assert data["sourceReviewDate"]=="2026-11-11"
 assert data["count"]==len(data["records"])==73
 assert data["countryCounts"]==COUNTS
 assert set(data["locales"])==LOCALES
 assert data["titleReviewStatus"]=="EN_SOURCE_FALLBACK_FOR_FIVE_NON_EN_LOCALES_NATIVE_REVIEW_REQUIRED"
 records=data["records"]
 assert Counter(r["country"] for r in records)==COUNTS
 assert len({r["id"] for r in records})==73
 assert len({r["canonicalTitleEn"] for r in records})==73
 kinds=Counter(r["recurrenceRules"][0]["kind"] for r in records)
 assert kinds=={"FIXED_DATE":71,"NTH_WEEKDAY":1,"WEEKDAY_ON_OR_AFTER":1}
 for row in records:
  rid=row["id"];country=row["country"]
  assert rid.startswith(country.lower()+"-")
  assert row["sourceReviewedOn"]=="2026-11-11"
  assert urlparse(row["source"]).hostname==HOSTS[country]
  assert row["proposedIntroducedYear"] is None and row["introducedYearSource"] is None
  assert row["titleTranslationStatus"]=="ENGLISH_FALLBACK_REQUIRES_NATIVE_LOCALE_REVIEW"
  assert row["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
  assert set(row["localizedTitles"])==LOCALES
  assert row["localizedTitles"]["en"]==row["canonicalTitleEn"]
  assert all(row["localizedTitles"][code].strip() for code in LOCALES)
  assert len(row["recurrenceRules"])==1
  rule=row["recurrenceRules"][0]
  for year in (2026,2027,2028,2029):
   assert day(rule,year).year==year
  if country=="FI":
   assert row["authorityType"]=="UNIVERSITY"
   assert row["officiality"]=="RECOGNIZED_INSTITUTIONAL"
   assert row["sourceTier"]=="D_ORIGINATOR"
  else:
   assert row["authorityType"]=="GOVERNMENT"
   assert row["officiality"]=="OFFICIAL_INSTITUTIONAL"
   assert row["sourceTier"]=="A_PRIMARY"
  assert len(row["chronologyNote"])>=100 and len(row["dateRationale"])>=55
 mid=next(r["recurrenceRules"][0] for r in records if r["id"]=="fi-finnish-flag-day-and-midsummer-day")
 assert [day(mid,y).isoformat() for y in (2026,2027,2028,2029)]==["2026-06-20","2027-06-26","2028-06-24","2029-06-23"]
 return records
if __name__=="__main__":
 rows=load_wave09()
 print(f"PASS Wave09: {len(rows)} source-backed national identities; translation fallback is explicit")
