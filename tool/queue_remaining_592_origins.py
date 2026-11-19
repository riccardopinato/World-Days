#!/usr/bin/env python3
"""Snapshot all 592 still-contextual national histories in 6 independent queues.

Executable queue only: 100-ID packets do not count as published origin stories.
Real source-based drafting/AI translation continues from these work packets.
"""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"assets/data"
OUT=ROOT/"reports/editorial_origin_592"
cat=json.loads((DATA/"official_core.json").read_text(encoding="utf-8"))
en=json.loads((DATA/"editorial_en.json").read_text(encoding="utf-8"))
by_id={x["id"]:x for x in cat["records"]}
pending=[x["observanceId"] for x in en["entries"]
         if x["status"]=="AI_CONTEXTUAL_SIX_LOCALE"]
assert len(pending)==len(set(pending))==592
assert all(by_id[x]["scope"]=="NATIONAL" and len(by_id[x]["countries"])==1
           for x in pending)
counts=Counter(by_id[x]["countries"][0] for x in pending)
ordered=sorted(pending,key=lambda oid:(-counts[by_id[oid]["countries"][0]],
                                      by_id[oid]["countries"][0],oid))
assert len(ordered)==592
groups=[ordered[n:n+100] for n in range(0,592,100)]
assert list(map(len,groups))==[100,100,100,100,100,92]
OUT.mkdir(parents=True,exist_ok=True)
for n,cohort in enumerate(groups,1):
 dossiers=[]
 for oid in cohort:
  r=by_id[oid]
  sources=r["sources"]
  assert sources and all(x["url"].startswith("https://") for x in sources)
  dossiers.append({
    "observanceId":oid,
    "canonicalTitleEn":r["canonicalTitleEn"],
    "country":r["countries"][0],
    "periodKind":r["periodKind"],
    "institutionNamedByCatalog":r["authority"]["name"],
    "institutionNotAutomaticallyOriginalProposer":True,
    "formalReferenceAsCatalogued":r["authority"].get("resolution"),
    "introducedYearVerified":r.get("introducedYear"),
    "catalogSourceUrls":[s["url"] for s in sources],
    "sourceTiers":[s["tier"] for s in sources],
    "sourceVerificationRequired":True,
    "historicalFoundingAct":None,
    "verifiedFirstObservance":None,
    "verifiedWhyChosenDate":None,
    "historySixLocale":None,
    "completionStatus":"RESEARCH_AND_SIX_LOCALE_ORIGIN_WRITING_PENDING"
  })
 (OUT/f"cohort_{n:02d}.json").write_text(
    json.dumps({"schemaVersion":1,"cohort":n,"count":len(cohort),
               "scope":"HISTORICAL_ORIGIN_PENDING_NOT_PUBLISHED",
               "dossiers":dossiers},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
summary={"catalogTotal":1111,"previousRichEditorial":507,
         "newOriginalOriginHistories":12,
         "totalNonContextualEditorial":519,
         "remainingIndividualOrigins":592,
         "cohorts":[len(g) for g in groups],
         "countryPendingDescending":dict(sorted(counts.items(),key=lambda x:(-x[1],x[0])))}
assert sum(counts.values())==592
(OUT/"index.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("ORIGIN_592_PARALLEL_COUNTRY_QUEUE",json.dumps(summary,ensure_ascii=False,sort_keys=True))
