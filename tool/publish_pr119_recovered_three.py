#!/usr/bin/env python3
"""Recover three already-drafted six-locale originals from frozen PR #119.

Runs after publish_prepared_sixlocale_87.py; retains all pre-existing 316
articles and the primary-source EN/IT previews. This is source/chronology
AI review, *never* independent human editorial certification.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
LANG=("en","it","es","fr","de","pt")
SOURCE=ROOT/"data/editorial/published/legacy_pr119_three_sixlocale_20261115.json"
ASSETS=ROOT/"assets/data"
PREVIEW=ROOT/"assets/data/origin_review_index.json"
REPORT=ROOT/"reports/legacy_pr119_three_publication.json"
RECORDS={
 "world-day-for-african-and-afrodescendant-culture":("origin_stories_wave05_20261112.json","165103bb3a5dd69ef035fe03fd3248b82b98d36c","eeff0f1e0cb34e54249a6fcdeae75a80122e56a1"),
 "international-day-to-combat-islamophobia":("origin_stories_wave09_20261112.json","2f54ca7845806059bd967cfd5a2df4a63f2c3a44","c43bd79df75af9cf0c9d27fbd65c6f19e455ebfa"),
 "international-day-of-the-girl-child":("origin_stories_wave17_20261112.json","6cccfc2c817bc349c0fd10dffd0bacb2f69564e7","8b8e68b3813f8950c5e7c8cd4a456eb61d7a175e")
}

PROMOTER={
 "en":"Originating or supporting institutions",
 "it":"Enti promotori o sostenitori",
 "es":"Instituciones promotoras o participantes",
 "fr":"Institutions à l'origine ou associées",
 "de":"Initiierende oder beteiligte Institutionen",
 "pt":"Instituições promotoras ou participantes"
}
def read(path):
 return json.loads(path.read_text(encoding="utf-8"))
def years(text):
 return set(re.findall(r"\b(?:18|19|20)\d{2}\b",text))
def main():
 pack=read(SOURCE)
 assert pack["schemaVersion"]==1 and pack["count"]==len(pack["records"])==3
 assert pack["scope"]=="PR119_SIX_LOCALE_RECOVERY_3"
 assert pack["reviewedAt"]=="2026-11-15"
 preview={x["observanceId"]:x for x in read(PREVIEW)["records"]}
 records={}
 for row in pack["records"]:
  oid=row["observanceId"]
  assert oid in RECORDS and oid not in records
  fname,sha,main_sha=RECORDS[oid]
  assert row["sourcePR"]==119 and row["sourceHead"]=="3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"
  assert row["sourceFile"]=="data/editorial/batches/"+fname
  assert row["sourceBlobSha"]==sha and row["mainBlobSha"]==main_sha
  prior=read(ROOT/row["sourceFile"])
  base=next((r for r in prior["records"] if r["observanceId"]==oid),None)
  assert base and row["introducedYear"]==base["introducedYear"]
  assert row["firstObservedYear"]==base["firstObservedYear"] and row["sources"]==base["sources"]
  for lang in ("en","it"):
   assert row["locale"][lang]==base["locale"][lang],(oid,lang)
  assert set(row["locale"])==set(LANG)
  assert preview[oid]["primaryResearch"] is not None and preview[oid]["runtimeResearchPreviewAllowed"] is True
  assert row["sources"] and all(urlsplit(url).scheme=="https" and urlsplit(url).netloc for url in row["sources"])
  refyears=None
  for lang in LANG:
   data=row["locale"][lang]
   for field in ("heading","origin","promoter","purpose"):
    assert isinstance(data.get(field),str) and len(data[field].strip())>25,(oid,lang,field)
   assert 2<=len(data["facts"])<=5 and all(len(f.strip())>=20 for f in data["facts"])
   current=years(data["origin"]+" "+" ".join(data["facts"]))
   if refyears is None:refyears=current
   else:assert current==refyears,(oid,lang,current,refyears)
  records[oid]=row
 assert set(records)==set(RECORDS)
 original_order=None
 for lang in LANG:
  file=ASSETS/f"editorial_{lang}.json"
  doc=read(file);existing=doc["entries"]
  assert len(existing)==doc["entryCount"]==316,(lang,len(existing))
  assert doc["aiSourceReviewedSixLocaleCount"]==87
  ids=[x["observanceId"] for x in existing]
  assert len(ids)==len(set(ids)) and not (set(ids)&set(records))
  if original_order is None:original_order=ids
  else:assert original_order==ids,(lang,"existing order drift")
  extra=[]
  for oid,row in sorted(records.items()):
   t=row["locale"][lang]
   extra.append({
    "observanceId":oid,"locale":lang,"translationOf":"en" if lang!="en" else None,
    "status":"AI_SOURCE_REVIEWED_SIX_LOCALE",
    "hook":t["heading"].strip(),
    "summary":t["purpose"].strip(),
    "whyThisDate":"",
    "origin":t["origin"].strip()+"\n\n"+PROMOTER[lang]+": "+t["promoter"].strip(),
    "whyItMatters":"",
    "quickFacts":[f.strip() for f in t["facts"]],
    "waysToTakePart":[],"relatedObservanceIds":[],
    "lastReviewedAt":"2026-11-15",
    "sourcePolicy":"UN/UNESCO original-source chronology and six-locale AI review; no independent human signoff.",
    "aiEditorialProvenance":{
      "sourcePR":119,"sourceHead":row["sourceHead"],"sourceFile":row["sourceFile"],
      "sourceBlobSha":row["sourceBlobSha"],"evidenceUrls":row["sources"],
      "aiCertLevel":"SOURCE_AND_CHRONOLOGY_REVIEWED_NO_HUMAN_SIGNOFF"
    }
   })
  doc["entries"]=existing+extra
  doc["entryCount"]=len(doc["entries"])
  doc["aiSourceReviewedSixLocaleCount"]=90
  assert doc["entryCount"]==319
  file.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 REPORT.parent.mkdir(parents=True,exist_ok=True)
 report={"previousRichEditorialCount":316,"recovered":3,"newRichEditorialCount":319,
         "totalPreparedHistoricalIDs":485,"sourcePR":119,
         "previousResearchOnlyBilingualPreviews":186,"remainingResearchOnlyBilingualPreviews":183,
         "independentHumanApprovals":0,"sourceCheckedLocales":list(LANG),
         "sourceProofs":{k:{"sourceBlobSha":v[1],"mainBlobSha":v[2]} for k,v in RECORDS.items()}}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("PR119_RECOVERED_THREE_OK",json.dumps(report,sort_keys=True))
if __name__=="__main__":
 main()
