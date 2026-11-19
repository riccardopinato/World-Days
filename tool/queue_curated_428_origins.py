#!/usr/bin/env python3
"""Create four 100-ID origin research packets plus final 28 from published 947.

Only research assignment. Do not count source-index entries as authored
histories, or infer founding dates from diplomatic holiday calendars.
"""
import concurrent.futures as cf
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data"
OUT=ROOT/"reports/editorial_curated_428_origin_research"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def main():
 cat=rd(A/"official_core.json")
 rows={r["id"]:r for r in cat["records"]}
 assert len(rows)==947
 ed=rd(A/"editorial_en.json")
 context=[x["observanceId"] for x in ed["entries"] if x["status"]=="AI_CONTEXTUAL_SIX_LOCALE"]
 assert len(context)==len(set(context))==428
 country=Counter(rows[oid]["countries"][0] for oid in context)
 ordered=sorted(context,key=lambda oid:(-country[rows[oid]["countries"][0]],rows[oid]["countries"][0],oid))
 batches=[ordered[x:x+100] for x in range(0,428,100)]
 assert list(map(len,batches))==[100,100,100,100,28]
 OUT.mkdir(parents=True,exist_ok=True)
 def make(p):
  n,items=p
  dossiers=[]
  for oid in items:
   r=rows[oid]
   url=[s["url"] for s in r["sources"]]
   assert url and all(s.startswith("https://") for s in url)
   dossiers.append({"id":oid,"country":r["countries"][0],
     "canonicalTitleEn":r["canonicalTitleEn"],
     "localizedTitles":r["localizedTitles"],
     "sourceIndex":url,"sourceTiers":[s["tier"] for s in r["sources"]],
     "institutionNamedByCatalog":r["authority"]["name"],
     "formalReferenceIfKnown":r["authority"].get("resolution"),
     "documentedIntroductionYear":r.get("introducedYear"),
     "historicalFoundingEvidence":None,
     "individualOriginalStoryEN":None,"translationsESFRDEITPT":None,
     "state":"ORIGIN_SOURCE_RESEARCH_NOT_YET_COMPLETE"})
  wr(OUT/f"cohort_{n:02d}.json",{"cohort":n,"count":len(items),
      "status":"RESEARCH_QUEUE_NOT_PUBLISHED_STORIES","dossiers":dossiers})
  return len(items)
 with cf.ThreadPoolExecutor(max_workers=5) as pool:
  counts=list(pool.map(make,enumerate(batches,1)))
 summary={"catalogPublished":947,"nonContextualRich":519,"contextualOriginPending":428,
          "cohorts":counts,"countriesPending":dict(sorted(country.items(),key=lambda p:(-p[1],p[0]))),
          "notYetPersonallyResearched":428}
 wr(OUT/"index.json",summary)
 print("WORLD_DAYS_428_ORIGIN_SOURCE_QUEUES_READY",json.dumps(summary,sort_keys=True))
if __name__=="__main__":main()
