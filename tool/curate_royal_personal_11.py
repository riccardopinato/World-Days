#!/usr/bin/env python3
"""Secondary audited scope pass: exclude 11 low-value royal birthday/name-day
flag dates, not public national holidays. Original government flag-day records
are preserved in source-controlled wave09 as reversible source history.
"""
from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"assets/data"
REPORT=ROOT/"reports"
LOCALES=("en","it","es","fr","de","pt")
SRC=ROOT/"data/market/wave09_primary_sixcountries_20261111.json"
BEFORE=958
AFTER=947
def rd(path):return json.loads(path.read_text(encoding="utf-8"))
def wr(path,v):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def main():
 raw=rd(SRC)
 selected=[r for r in raw["records"] if r["country"] in ("SE","NO")
           and r["canonicalTitleEn"].split(" — ")[0].endswith((" Name Day"," Birthday"))]
 assert len(selected)==11 and Counter(r["country"] for r in selected)=={"SE":6,"NO":5}
 excluded={r["id"]:r for r in selected}
 cat=rd(DATA/"official_core.json")
 assert len(cat["records"])==BEFORE
 existing={r["id"]:r for r in cat["records"]}
 assert set(excluded)<=set(existing)
 assert all(existing[id_]["countries"]==[row["country"]] and
            existing[id_]["sources"][0]["url"]==row["source"]
            for id_,row in excluded.items())
 locales={}
 for loc in LOCALES:
  doc=rd(DATA/f"editorial_{loc}.json")
  assert doc["entryCount"]==len(doc["entries"])==BEFORE
  lookup={r["observanceId"]:r for r in doc["entries"]}
  assert all(lookup[x]["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for x in excluded)
  locales[loc]=doc
 cat["records"]=[r for r in cat["records"] if r["id"] not in excluded]
 cat["datasetVersion"]="2026.11.19.4"
 assert len(cat["records"])==AFTER
 cat["coverage"]=cat.get("coverage","")+" 11 individual Scandinavian royal birthday/name-day flag dates excluded."
 cat["yearOverrides"]=[r for r in cat.get("yearOverrides",[]) if r.get("observanceId") not in excluded]
 wr(DATA/"official_core.json",cat)
 occ=rd(DATA/"occurrences_2026.json")
 before_occ=len(occ["occurrences"])
 occ["occurrences"]=[r for r in occ["occurrences"] if r["observanceId"] not in excluded]
 occ["occurrenceCount"]=len(occ["occurrences"])
 for row in occ["dateIndex"]:
  row["observanceIds"]=[x for x in row["observanceIds"] if x not in excluded]
 wr(DATA/"occurrences_2026.json",occ)
 for loc,doc in locales.items():
  doc["entries"]=[r for r in doc["entries"] if r["observanceId"] not in excluded]
  for row in doc["entries"]:
   if "relatedObservanceIds" in row:
    row["relatedObservanceIds"]=[x for x in row["relatedObservanceIds"] if x not in excluded]
  doc["entryCount"]=len(doc["entries"])
  assert doc["entryCount"]==AFTER
  assert sum(r["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for r in doc["entries"])==428
  wr(DATA/f"editorial_{loc}.json",doc)
 idx=rd(DATA/"origin_review_index.json")
 assert len(idx["records"])==BEFORE
 idx["records"]=[r for r in idx["records"] if r["observanceId"] not in excluded]
 idx["datasetVersion"]=cat["datasetVersion"]
 idx["recordCount"]=idx["sourceCatalogCount"]=AFTER
 states=Counter(r["originResearchStatus"] for r in idx["records"])
 idx["originStatusCounts"]=dict(states)
 idx["sourceTiersCount"]=dict(Counter(x for r in idx["records"] for x in r["sourceTiers"]))
 idx["reviewedRichOriginCount"]=states["PRIMARY_RESEARCHED_ORIGIN_IT_EN"]
 wr(DATA/"origin_review_index.json",idx)
 audit={
  "sourceCandidates":1111,"initialBiographicalExclusions":153,
  "additionalRoyalBirthdayAndNameDayExclusions":11,
  "totalArchivedNotPublished":164,"publishedIds":AFTER,
  "remainingGenericContextual":428,"existingNonContextualRichEditorial":519,
  "totalLocales":len(LOCALES),
  "removedRoyalDateOccurrences2026":before_occ-len(occ["occurrences"]),
  "sourceOfRoyalDateFlags":"SOURCE_ONLY_FLAG_DAY_INDEX_NOT_INDEPENDENT_NATIONAL_HOLIDAY",
  "sourceFilesRemainArchived":True,
  "excluded":[{"id":id_,"country":r["country"],"title":r["canonicalTitleEn"],"source":r["source"],"reason":"SINGLE_ROYAL_PERSON_BIRTHDAY_OR_NAME_DAY_FLAG_DATE"}
              for id_,r in sorted(excluded.items())]
 }
 wr(REPORT/"world_days_royal_biographical_11_exclusions_20261119.json",audit)
 print("ROYAL_PERSONAL_11_EXCLUDED",json.dumps({k:v for k,v in audit.items() if k!="excluded"}))
if __name__=="__main__":main()
