#!/usr/bin/env python3
"""Build per-observance origin-research ledger without inventing histories.

Each canonical ID is accounted for. Exactly source-researched stories get rich
origin, promoter, purpose and fact fields. Legacy editorial remains independently
labelled rather than retroactively claiming a new historical source audit.
"""
from collections import Counter,defaultdict
from pathlib import Path
from urllib.parse import urlsplit
import json

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"assets/data/official_core.json"
LEGACY=ROOT/"assets/data/editorial_en.json"
BATCH=ROOT/"data/editorial/batches/origin_stories_primary_20261111.json"
OUT=ROOT/"assets/data/origin_review_index.json"
REPORT=ROOT/"reports/origin_review_coverage.json"

def run():
 catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
 legacy=json.loads(LEGACY.read_text(encoding="utf-8"))
 records=catalog["records"]
 ids={r["id"] for r in records}
 assert len(ids)==len(records)>=1111
 old_ids={e["observanceId"] for e in legacy["entries"]}
 assert len(old_ids)==len(legacy["entries"])==56
 assert old_ids<=ids
 # The initial four-stories file is immutable in meaning; later source-backed
 # waves are separate append-only batches, discovered deterministically.
 batch_files=[BATCH]+sorted((ROOT/"data/editorial/batches").glob("origin_stories_wave*.json"))
 stories={}
 story_reviewed_at={}
 for batch_file in batch_files:
  batch=json.loads(batch_file.read_text(encoding="utf-8"))
  assert batch["status"]=="SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE",batch_file
  assert batch["count"]==len(batch["records"]),batch_file
  assert batch["reviewedOn"] and len(batch["reviewedOn"])==10,batch_file
  for item in batch["records"]:
   oid=item["observanceId"]
   assert oid not in stories,("duplicate source-researched origin",oid,batch_file)
   assert oid in ids,("origin absent canonical catalog",oid,batch_file)
   stories[oid]=item
   story_reviewed_at[oid]=batch["reviewedOn"]
 assert len(stories)>=4
 result=[]
 source_tiers=Counter()
 by_status=Counter()
 by_scope=Counter()
 unknown_years=0
 by_country=Counter()
 no_source=[]
 for record in records:
  rid=record["id"]
  source_urls=[x["url"] for x in record.get("sources",[])]
  tiers=[x["tier"] for x in record.get("sources",[])]
  assert len(source_urls)>0,("no source",rid)
  for url in source_urls:
   parsed=urlsplit(url)
   assert parsed.scheme=="https" and parsed.hostname,("invalid source",rid,url)
  for t in tiers:
   assert t in {"A_PRIMARY","B_INSTITUTIONAL","C_DISCOVERY","D_ORIGINATOR"},(rid,t)
   source_tiers[t]+=1
  by_scope[record["scope"]]+=1
  if record["scope"]=="NATIONAL":
   assert len(record["countries"])==1
   by_country[record["countries"][0]]+=1
  else:
   assert record["scope"]=="GLOBAL" and not record["countries"]
  year=record.get("introducedYear")
  if year is None:unknown_years+=1
  else:
   assert isinstance(year,int) and 1800<=year<=2026
   assert record.get("introducedYearSource") in source_urls
  story=stories.get(rid)
  status="SOURCE_INDEX_ONLY_ORIGIN_NOT_RESEARCHED"
  if rid in old_ids:status="LEGACY_EDITORIAL_EXISTS_ORIGIN_NOT_RECERTIFIED"
  if story is not None:status="PRIMARY_RESEARCHED_ORIGIN_IT_EN"
  by_status[status]+=1
  entry={
   "observanceId":rid,
   "scope":record["scope"],
   "countries":record["countries"],
   "periodKind":record["periodKind"],
   "authority":record["authority"]["name"],
   "officiality":record["authority"]["officiality"],
   "sourceTiers":tiers,
   "canonicalSourceUrls":source_urls,
   "introducedYear":year,
   "originResearchStatus":status,
   "editorialTranslationStatus":"IT_EN_RESEARCHED_OTHERS_FALLBACK_EN" if story else "NO_NEW_ORIGIN_TEXT",
   "additionalTranslationDrafts":sorted(set(story["locale"])-{"it","en"}) if story else [],
   "primaryResearch":None,
  }
  if story:
   assert story["sources"] and all(urlsplit(u).scheme=="https" for u in story["sources"])
   assert {"it","en"} <= set(story["locale"]) <= {"it","en","es","fr","de","pt"}
   for locale in story["locale"]:
    content=story["locale"][locale]
    for field in ("heading","origin","promoter","purpose"):
     assert isinstance(content[field],str) and len(content[field])>(18 if field=="heading" else 40),(rid,locale,field)
    assert 2<=len(content["facts"])<=5
    assert all(len(fact)>=25 for fact in content["facts"])
   if year is not None:
    assert story["introducedYear"]==year,(rid,year,story["introducedYear"])
   entry["primaryResearch"]={
    "reviewedAt":story_reviewed_at[rid],
    "sourceUrls":story["sources"],
    "introducedYear":story["introducedYear"],
    "firstObservedYear":story["firstObservedYear"],
    "locale":story["locale"],
   }
  result.append(entry)
 assert len(result)==len(ids)>=1111, "canonical provenance ledger must be complete"
 assert len({x["observanceId"] for x in result})==len(ids)
 assert sum(by_status.values())==len(ids)
 assert sum(by_scope.values())==len(ids)
 assert by_scope["GLOBAL"]>=289 and by_scope["NATIONAL"]>=822,by_scope
 assert len(by_country)>=193,len(by_country)
 payload={
  "schemaVersion":1,
  "datasetVersion":catalog["datasetVersion"],
  "sourceCatalogCount":len(records),
  "recordCount":len(result),
  "coverage":"ALL_CANONICAL_ACCOUNTED_FOR_NOT_ALL_HISTORIES_CERTIFIED",
  "reviewedRichOriginCount":len(stories),
  "legacyReviewedEditorialCount":len(old_ids),
  "sourceTiersCount":dict(source_tiers),
  "originStatusCounts":dict(by_status),
  "records":sorted(result,key=lambda x:x["observanceId"]),
 }
 REPORT.parent.mkdir(parents=True,exist_ok=True)
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 report={
  "schemaVersion":1,
  "datasetVersion":catalog["datasetVersion"],
  "allIdSourceProvenanceChecked":len(records),
  "richOriginNewPrimaryResearch":len(stories),
  "legacyReviewedEditorialEntries":len(old_ids),
  "originPendingCount":len(records)-len(stories),
  "originStatusCounts":dict(by_status),
  "scope":dict(by_scope),
  "countryMarkets":len(by_country),
  "introducedYearKnown":len(records)-unknown_years,
  "introducedYearUnknown":unknown_years,
  "sourceTierOccurrences":dict(source_tiers),
  "limitation":"Identifier/source/schema/recurrence validation is not human historical certification of individual entries; the outstanding history count is recorded separately.",
 }
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("ORIGIN_REVIEW_COVERAGE",json.dumps(report,ensure_ascii=False,sort_keys=True))
 return payload

if __name__=="__main__":
 run()
