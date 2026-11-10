"""Admission gate for 16 source-backed Malta, Croatia and Cyprus observances."""
import json
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/market/wave06_primary_mt_hr_cy_20261110.json"
EXPECTED={"MT":8,"HR":4,"CY":4}
HOSTS={"MT":"www.gov.mt","HR":"mvep.gov.hr","CY":"www.cysec.gov.cy"}
LOCALES={"en","it","es","fr","de","pt"}
DATES={
 "mt-freedom-day":(3,31),"mt-sette-giugno":(6,7),
 "mt-independence-day":(9,21),"mt-republic-day":(12,13),
 "mt-victory-day":(9,8),"mt-st-pauls-shipwreck-day":(2,10),
 "mt-feast-of-st-joseph":(3,19),"mt-feast-of-st-peter-and-paul":(6,29),
 "hr-statehood-day":(5,30),"hr-antifascist-resistance-day":(6,22),
 "hr-victory-and-homeland-thanksgiving-day":(8,5),
 "hr-homeland-war-remembrance-day":(11,18),
 "cy-national-day":(4,1),"cy-independence-day":(10,1),
 "cy-greek-national-day":(3,25),"cy-ochi-day":(10,28),
}
def load_wave06():
 data=json.loads(SOURCE.read_text(encoding="utf-8"))
 assert data["schemaVersion"]==1
 assert data["datasetId"]=="world-days-market-wave06-primary-2026-11-10"
 assert data["sourceReviewDate"]=="2026-11-10"
 assert data["count"]==len(data["records"])==16
 assert data["countryCounts"]==EXPECTED
 assert set(data["locales"])==LOCALES
 assert {r["id"] for r in data["records"]}==set(DATES)
 assert Counter(r["country"] for r in data["records"])==EXPECTED
 assert len({r["canonicalTitleEn"] for r in data["records"]})==16
 for item in data["records"]:
  rid=item["id"];country=item["country"];rule=item["recurrenceRules"]
  assert rid.startswith(country.lower()+"-")
  assert item["officiality"]=="OFFICIAL_INSTITUTIONAL"
  assert item["authorityType"]=="GOVERNMENT"
  assert item["sourceTier"]=="A_PRIMARY"
  assert urlsplit(item["source"]).hostname==HOSTS[country]
  assert item["sourceReviewedOn"]==data["sourceReviewDate"]
  assert item["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
  assert item["proposedIntroducedYear"] is None
  assert item["introducedYearSource"] is None
  assert item["subject"]=="PEOPLE"
  assert set(item["localizedTitles"])==LOCALES
  assert item["localizedTitles"]["en"]==item["canonicalTitleEn"]
  assert all(item["localizedTitles"][lang].strip() for lang in LOCALES)
  assert len(rule)==1 and rule[0]["kind"]=="FIXED_DATE"
  assert (rule[0]["month"],rule[0]["day"])==DATES[rid]
  for year in (2026,2027,2028):
   date(year,rule[0]["month"],rule[0]["day"])
  assert len(item["chronologyNote"])>=100
  assert len(item["dateRationale"])>=55
 return data["records"]
if __name__=="__main__":
 print("PASS: primary-national Wave06: 16 fixed commemorations, 3 markets")
 load_wave06()
