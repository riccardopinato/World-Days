"""NCCA Wave11: source-indexed cultural anniversaries, not government holidays.

Draft branch only. The app's source-tier and officiality must distinguish
government cultural-calendar listing from actual statutory public holidays.
"""
from datetime import date
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit
import json

ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"data/market/wave11_staged_144_ph_20261111.json"
LOCALES={"en","it","es","fr","de","pt"}
def load_wave11():
 data=json.loads(FILE.read_text(encoding="utf8"))
 assert data["schemaVersion"]==1
 assert data["datasetId"]=="world-days-wave11-staged-ncca-144-20261111"
 assert data["sourceReviewDate"]=="2026-11-11"
 assert data["count"]==len(data["records"])==144
 assert data["countryCounts"]=={"PH":144}
 assert data["admissionStatus"]=="STAGED_ON_DRAFT_PR_NOT_MERGED"
 assert set(data["locales"])==LOCALES
 rows=data["records"]
 assert Counter(x["country"] for x in rows)=={"PH":144}
 assert len({x["id"] for x in rows})==144
 assert len({x["canonicalTitleEn"] for x in rows})==144
 for x in rows:
  assert x["country"]=="PH" and x["id"].startswith("ph-w11-")
  assert x["officiality"]=="RECOGNIZED_INSTITUTIONAL"
  assert x["holidayClassification"]=="INSTITUTIONALLY_INDEXED_CULTURAL_HISTORICAL_ANNIVERSARY_NOT_STATUTORY_HOLIDAY"
  assert x["authorityType"]=="GOVERNMENT"
  assert x["sourceTier"]=="A_PRIMARY"
  assert urlsplit(x["source"]).hostname=="ncca.gov.ph"
  assert x["sourceReviewedOn"]=="2026-11-11"
  assert x["proposedIntroducedYear"] is None
  assert x["introducedYearSource"] is None
  assert x["humanEditorialStatus"]=="METADATA_SOURCE_INDEXED_LONG_FORM_NOT_REVIEWED"
  assert x["titleTranslationStatus"]=="EN_FALLBACK_NATIVE_REVIEW_REQUIRED"
  assert set(x["localizedTitles"])==LOCALES
  assert all(x["localizedTitles"][lang]==x["canonicalTitleEn"] for lang in LOCALES)
  assert len(x["recurrenceRules"])==1
  rule=x["recurrenceRules"][0]
  assert rule["kind"]=="FIXED_DATE"
  for year in (2026,2027,2028):
   assert date(year,rule["month"],rule["day"]).year==year
  assert len(x["chronologyNote"])>=115
  assert len(x["dateRationale"])>=80
 return rows
if __name__=="__main__":
 load_wave11()
 print("PASS: 144 culturally sourced historical anniversaries staged; no statutory holidays or rich stories fabricated")
