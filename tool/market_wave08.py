"""Wave08: Canadian Heritage 27 national civic and remembrance observances."""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from datetime import date,timedelta
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/market/wave08_canada_primary_20261111.json"
LOCALES={"en","it","es","fr","de","pt"}
MOVABLE={"ca-armed-forces-day":(6,7,1),"ca-holodomor-memorial-day":(11,6,4)}
def resolve(rule,year):
 m=rule["month"]
 if rule["kind"]=="FIXED_DATE":return date(year,m,rule["day"])
 assert rule["kind"]=="NTH_WEEKDAY"
 first=date(year,m,1);offset=(rule["weekday"]-1-first.weekday())%7
 return first+timedelta(days=offset+7*(rule["occurrence"]-1))
def load_wave08():
 data=json.loads(SOURCE.read_text(encoding="utf-8"))
 assert data["schemaVersion"]==1 and data["datasetId"]=="world-days-market-wave08-canada-primary-2026-11-11"
 assert data["sourceReviewDate"]=="2026-11-11"
 assert data["count"]==len(data["records"])==27
 assert data["countryCounts"]=={"CA":27}
 assert set(data["locales"])==LOCALES
 ids=set();titles=set()
 for row in data["records"]:
  rid=row["id"];name=row["canonicalTitleEn"]
  assert rid.startswith("ca-") and rid not in ids
  assert name not in titles;ids.add(rid);titles.add(name)
  assert row["country"]=="CA"
  assert row["authorityType"]=="GOVERNMENT"
  assert row["officiality"]=="OFFICIAL_INSTITUTIONAL"
  assert row["sourceTier"]=="A_PRIMARY"
  assert urlsplit(row["source"]).hostname=="www.canada.ca"
  assert row["sourceReviewedOn"]=="2026-11-11"
  assert row["proposedIntroducedYear"] is None and row["introducedYearSource"] is None
  assert row["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
  assert set(row["localizedTitles"])==LOCALES
  assert row["localizedTitles"]["en"]==name
  assert all(str(value).strip() for value in row["localizedTitles"].values())
  assert len(row["recurrenceRules"])==1
  rule=row["recurrenceRules"][0]
  assert rule["kind"] in {"FIXED_DATE","NTH_WEEKDAY"}
  if rid in MOVABLE:assert (rule["month"],rule["weekday"],rule["occurrence"])==MOVABLE[rid]
  else:assert rule["kind"]=="FIXED_DATE"
  for year in (2026,2027,2028):assert resolve(rule,year).year==year
  assert len(row["chronologyNote"])>=100 and len(row["dateRationale"])>=55
 assert {r["id"] for r in data["records"] if r["recurrenceRules"][0]["kind"]=="NTH_WEEKDAY"}==set(MOVABLE)
 return data["records"]
if __name__=="__main__":
 load_wave08();print("PASS: 27 Canadian Heritage source observations with five translated display-title locales")
