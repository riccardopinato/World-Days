#!/usr/bin/env python3
"""Promote 87 already-written six-locale source dossiers into inspected AI editorial.

Preserves the previously certified 173 and 56 curated rich editorials.
The 87 are AI SOURCE REVIEWED, not falsely represented as human-approved or
fully independent fact-checks. Every original authority URL and source blob
identity remains inspectable. Wave20 EN/IT parity is checked against main.
"""
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit
import json
import re

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/data"
SOURCES=ROOT/"data/editorial/published"
LEDGER=ROOT/"data/editorial/reviews/ph_kr_ca_173_ai_editorial_certification_20261114.json"
MAIN_W20=ROOT/"data/editorial/batches/origin_stories_wave20_20261113.json"
LOCALES=("en","it","es","fr","de","pt")
PROMOTER_LABEL={
 "en":"Originating or supporting institutions",
 "it":"Enti promotori o sostenitori",
 "es":"Instituciones promotoras o participantes",
 "fr":"Institutions à l'origine ou associées",
 "de":"Initiierende oder beteiligte Institutionen",
 "pt":"Instituições promotoras ou participantes",
}
W20_SRC_SHA="6acc4ec387c53faf25aa517a74e8585a88f0eae5"
W20_MAIN_SHA="6fd9814f99fbf59cf5fc4255a5c8dd5ffd30c0cf"
TOP5_SRC_SHA="37bc8b2f03e9123cfbcf04803bb820ad11324d39"

def read(path):
 return json.loads(path.read_text(encoding="utf-8"))

def years(text):
 return set(re.findall(r"\b(?:18|19|20)\d{2}\b",text))

def validate_locales(item,kind):
 oid=item["observanceId"]
 assert set(item["locale"])==set(LOCALES),(oid,"missing locale")
 original_years=None
 for lang in LOCALES:
  txt=item["locale"][lang]
  for key in ("heading","origin","promoter","purpose"):
   assert isinstance(txt.get(key),str) and len(txt[key].strip())>25,(oid,lang,key)
  facts=txt.get("facts",[])
  assert 2<=len(facts)<=5 and all(isinstance(x,str) and len(x.strip())>=20 for x in facts),(oid,lang)
  found=years(txt["origin"]+" "+" ".join(facts))
  if kind=="wave20" and oid=="spain-exile-victims-remembrance-day":
   found-= {"1930","1940"} # decade descriptions, not precise anniversary years
  if kind=="wave20" and oid=="sk-carpathian-dukla-operation-heroes-day":
   found.discard("1994") # speculative unknown inaugural ceremony, not a dated claim
  if original_years is None:original_years=found
  else:assert found==original_years,(oid,lang,sorted(found),sorted(original_years))
  y=item.get("introducedYear")
  assert y is None or (isinstance(y,int) and 1800<=y<=2026),oid
  f=item.get("firstObservedYear")
  assert f is None or (isinstance(f,int) and 1800<=f<=2026),oid
 urls=item.get("sources",[])
 assert urls and len(urls)==len(set(urls)),oid
 assert all(urlsplit(u).scheme=="https" and urlsplit(u).hostname for u in urls),oid

def main():
 cert={r["observanceId"] for r in read(LEDGER)["records"]}
 assert len(cert)==173
 main=read(MAIN_W20)
 assert main["count"]==len(main["records"])==100
 orig={r["observanceId"]:r for r in main["records"]}
 six=read(SOURCES/"wave20_82_six_locale_20261115.json")
 assert six["sourceType"]=="EXACT_MAIN_WAVE20_PLUS_SIX_LOCALE_PR118"
 assert six["sourceHead"]=="47cff4c5b22e55156e9444a3240511530a6f01f9"
 assert six["sourceBlobSha"]==W20_SRC_SHA and six["mainBlobSha"]==W20_MAIN_SHA
 assert six["count"]==len(six["records"])==82 and six["excludedExistingAiCertified"]==18
 assert len(cert & set(orig))==18
 assert {r["observanceId"] for r in six["records"]}==set(orig)-cert
 for r in six["records"]:
  oid=r["observanceId"]
  base=orig[oid]
  for fld in ("introducedYear","firstObservedYear","sources"):
   assert r[fld]==base[fld],(oid,fld)
  for lang in ("en","it"):
   assert r["locale"][lang]==base["locale"][lang],(oid,lang)
  if oid=="sk-carpathian-dukla-operation-heroes-day":
   assert r["publicationCorrection"]=="REMOVED_SPECULATIVE_1994_FIRST_CEREMONY_REFERENCE_FROM_ES_FR_DE_PT"
  else:assert r.get("publicationCorrection") is None,oid
  validate_locales(r,"wave20")
 top=read(SOURCES/"top5_5_six_locale_20261115.json")
 assert top["sourceBlobSha"]==TOP5_SRC_SHA and top["sourcePR"]==122
 assert top["sourceHead"]=="00801cae31957e48166ccd2c760883fd0f96171f"
 assert top["count"]==len(top["records"])==5
 assert {x["country"] for x in top["records"]}=={"CZ","SK","IT","FI","EE"}
 for x in top["records"]:
  validate_locales(x,"top5")
  assert x.get("firstObservedYear") is None
 all_rows=[(r,"wave20",six) for r in six["records"]]+[(r,"top5",top) for r in top["records"]]
 known=set(cert)
 catalog={r["id"]:r for r in read(ASSETS/"official_core.json")["records"]}
 assert len(catalog)==1111
 for row,kind,pack in all_rows:
  oid=row["observanceId"]
  assert oid in catalog and oid not in known,oid
  known.add(oid)
  if row.get("introducedYear") is not None and catalog[oid].get("introducedYear") is not None:
   assert row["introducedYear"]==catalog[oid]["introducedYear"],oid
 assert len(known)==260

 expectedIds={r["observanceId"] for r,_,_ in all_rows}
 en_baseline=None
 for lang in LOCALES:
  path=ASSETS/f"editorial_{lang}.json"
  document=read(path)
  prev=document["entries"]
  assert len(prev)==229 and document["entryCount"]==229,(lang,len(prev))
  ids={x["observanceId"] for x in prev}
  assert not ids & expectedIds,(lang,"overwrite")
  if en_baseline is None:en_baseline=[x["observanceId"] for x in prev]
  else:assert [x["observanceId"] for x in prev]==en_baseline,lang
  extra=[]
  for row,kind,pack in sorted(all_rows,key=lambda z:z[0]["observanceId"]):
   t=row["locale"][lang]
   extra.append({
    "observanceId":row["observanceId"],
    "locale":lang,
    "translationOf":"en" if lang!="en" else None,
    "status":"AI_SOURCE_REVIEWED_SIX_LOCALE",
    "hook":t["heading"].strip(),
    "summary":t["purpose"].strip(),
    "whyThisDate":"",
    "origin":t["origin"].strip()+"\n\n"+PROMOTER_LABEL[lang]+": "+t["promoter"].strip(),
    "whyItMatters":"",
    "quickFacts":[x.strip() for x in t["facts"]],
    "waysToTakePart":[],
    "relatedObservanceIds":[],
    "lastReviewedAt":"2026-11-15",
    "sourcePolicy":"Source-linked AI review; original prose and locale chronology checked, not qualified independent human signoff.",
    "aiEditorialProvenance":{
     "sourcePR":pack["sourcePR"],
     "sourceHead":pack["sourceHead"],
     "sourceFile":pack["sourceFile"],
     "sourceBlobSha":pack["sourceBlobSha"],
     "evidenceUrls":row["sources"],
     "publicationCorrection":row.get("publicationCorrection"),
     "aiCertLevel":"SOURCE_AND_CHRONOLOGY_REVIEWED_NO_HUMAN_SIGNOFF",
    }
   })
  document["entries"]=prev+extra
  document["entryCount"]=len(document["entries"])
  document["aiSourceReviewedSixLocaleCount"]=87
  assert document["entryCount"]==316
  path.write_text(json.dumps(document,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 report={"schemaVersion":1,"originalRichEntries":229,"newSixLocaleSourceReviewed":87,"sixLocaleRichTotal":316,
         "wave20FromPr118":82,"top5FromPr122":5,"existingAiCertified":173,
         "allSixLocalizationsComplete":True,
         "noQualifiedHumanSignoffsClaimed":True,
         "sourceSha":{"wave20":W20_SRC_SHA,"top5":TOP5_SRC_SHA},
         "specialCorrection":"sk-carpathian-dukla-operation-heroes-day"}
 dest=ROOT/"reports/prepared_history_integration_20261115.json"
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("PREPARED_87_RICH_IMPORT_OK",json.dumps(report,sort_keys=True))

if __name__=="__main__": main()
