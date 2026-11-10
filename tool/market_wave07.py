"""Wave07: legal-authority five-market source batch, deterministic 2026-28 vectors."""
from collections import Counter
from datetime import date,timedelta
from pathlib import Path
from urllib.parse import urlsplit
import json
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"data/market/wave07_primary_5markets_20261110.json"
COUNTS={"EE":17,"LV":5,"LT":6,"IS":3,"LU":1}
HOSTS={"EE":"www.eesti.ee","LV":"www.mfa.gov.lv","LT":"e-seimas.lrs.lt","IS":"cb.is","LU":"itm.public.lu"}
LOCALES={"en","it","es","fr","de","pt"}
NTH={"ee-finno-ugric-peoples-day":(10,6,3),"ee-grandparents-day":(9,7,2),"lt-mothers-day":(5,7,1),"lt-fathers-day":(6,7,1),"is-commerce-day":(8,1,1)}
def observed(rule,year):
 m=rule["month"]
 if rule["kind"]=="FIXED_DATE":return date(year,m,rule["day"])
 if rule["kind"]=="WEEKDAY_ON_OR_AFTER":
  first=date(year,m,rule["day"])
  return first+timedelta(days=(rule["weekday"]-1-first.weekday())%7)
 assert rule["kind"]=="NTH_WEEKDAY"
 first=date(year,m,1)
 day=1+(rule["weekday"]-1-first.weekday())%7+7*(rule["occurrence"]-1)
 return date(year,m,day)
def item_sources(row):
 return [row["source"],*row.get("additionalSources",[])]
def load_wave07():
 data=json.loads(FILE.read_text(encoding="utf-8"))
 assert data["schemaVersion"]==1 and data["count"]==32
 assert data["datasetId"]=="world-days-market-wave07-primary-2026-11-10"
 assert data["sourceReviewDate"]=="2026-11-10"
 assert data["countryCounts"]==COUNTS
 assert set(data["locales"])==LOCALES
 rows=data["records"]
 assert len(rows)==32
 assert Counter(x["country"] for x in rows)==COUNTS
 assert len({r["id"] for r in rows})==32
 assert len({r["canonicalTitleEn"] for r in rows})==32
 assert {r["id"] for r in rows if r["recurrenceRules"][0]["kind"]=="NTH_WEEKDAY"}==set(NTH)
 assert {r["id"] for r in rows if r["recurrenceRules"][0]["kind"]=="WEEKDAY_ON_OR_AFTER"}=={"is-first-day-of-summer"}
 for row in rows:
  country=row["country"];rid=row["id"];rule=row["recurrenceRules"]
  assert rid.startswith(country.lower()+"-"),rid
  assert row["officiality"]=="OFFICIAL_INSTITUTIONAL"
  assert row["sourceTier"]=="A_PRIMARY"
  assert row["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
  assert row["proposedIntroducedYear"] is None and row["introducedYearSource"] is None
  assert row["sourceReviewedOn"]=="2026-11-10"
  assert urlsplit(row["source"]).hostname==HOSTS[country]
  assert set(row["localizedTitles"])==LOCALES
  assert row["localizedTitles"]["en"]==row["canonicalTitleEn"]
  assert all(row["localizedTitles"][loc].strip() for loc in LOCALES)
  assert len(rule)==1 and rule[0]["kind"] in {"FIXED_DATE","NTH_WEEKDAY","WEEKDAY_ON_OR_AFTER"}
  if rid in NTH:assert (rule[0]["month"],rule[0]["weekday"],rule[0]["occurrence"])==NTH[rid]
  if rid=="is-first-day-of-summer":
   assert rule[0]=={"kind":"WEEKDAY_ON_OR_AFTER","month":4,"day":19,"weekday":4}
   assert "https://reykjavik.is/en/holidays-and-festive-days" in item_sources(row)
  if rid=="lv-constituent-assembly-day":
   assert "https://www.bank.lv/en/about-us/useful/public-holidays-in-latvia" in item_sources(row)
  for year in (2026,2027,2028):
   d=observed(rule[0],year)
   assert d.year==year and 1<=d.month<=12
  assert len(row["chronologyNote"])>=100 and len(row["dateRationale"])>=55
 summer=next(r["recurrenceRules"][0] for r in rows if r["id"]=="is-first-day-of-summer")
 assert [observed(summer,y).isoformat() for y in (2026,2027,2028)]==["2026-04-23","2027-04-22","2028-04-20"]
 assert observed(next(r["recurrenceRules"][0] for r in rows if r["id"]=="is-commerce-day"),2026).isoformat()=="2026-08-03"
 assert observed(next(r["recurrenceRules"][0] for r in rows if r["id"]=="ee-finno-ugric-peoples-day"),2026).isoformat()=="2026-10-17"
 return rows
if __name__=="__main__":
 print("PASS: 32 source-backed civic records in five new markets",COUNTS)
 load_wave07()
