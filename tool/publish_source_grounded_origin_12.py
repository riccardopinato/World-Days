#!/usr/bin/env python3
"""Promote 12 individually source-grounded origin narratives in all six locales.

Run AFTER contextual 604 generator/validator/audit. This replaces source-
limited contextual paragraphs but never adds an ID or human certification.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"assets/data"
SRC=ROOT/"data/editorial/published"
LOCALES=("en","it","es","fr","de","pt")
FILES=(
 "origin_enrichment_12_de_it.json",
 "origin_enrichment_12_pt_es1.json",
 "origin_enrichment_12_es2_gb_us.json",
)
ORIGIN_STATUS="AI_SOURCE_REVIEWED_SIX_LOCALE"
CONTEXT_STATUS="AI_CONTEXTUAL_SIX_LOCALE"

def load(path):
 return json.loads(path.read_text(encoding="utf-8"))

def main():
 catalog=load(DATA/"official_core.json")
 by_id={row["id"]:row for row in catalog["records"]}
 assert len(by_id)==1111
 sources={}
 rows=[]
 for name in FILES:
  batch=load(SRC/name)
  assert batch["schemaVersion"]==1
  assert batch["status"]=="SOURCE_CHECKED_AI_SIX_LOCALE"
  assert len(batch["records"])==batch["count"]==4
  for row in batch["records"]:
   oid=row["observanceId"]
   assert oid in by_id and oid not in sources
   assert row["introducedYear"]==by_id[oid]["introducedYear"]
   assert row["sources"] and len(set(row["sources"]))==len(row["sources"])
   assert by_id[oid]["introducedYearSource"] in row["sources"]
   assert all(urlsplit(u).scheme=="https" and urlsplit(u).hostname for u in row["sources"])
   assert set(row["locale"])==set(LOCALES)
   for loc in LOCALES:
    t=row["locale"][loc]
    assert all(isinstance(t.get(k),str) and len(t[k].strip())>=45
               for k in ("origin","whyThisDate","fact")),(oid,loc)
    assert len(t["origin"])>=155,(oid,loc)
    assert str(row["introducedYear"]) in t["origin"],(oid,loc,"year missing")
   sources[oid]=row
   rows.append(oid)
 assert len(rows)==len(set(rows))==12

 prior_order=None
 for loc in LOCALES:
  path=DATA/f"editorial_{loc}.json"
  doc=load(path)
  entries=doc["entries"]
  ids=[r["observanceId"] for r in entries]
  assert len(ids)==len(set(ids))==doc["entryCount"]==1111
  if prior_order is None:prior_order=ids
  else:assert prior_order==ids,("locale ordering mismatch",loc)
  lookup={r["observanceId"]:r for r in entries}
  assert all(lookup[oid]["status"]==CONTEXT_STATUS for oid in rows),(loc,"not contextual before")
  for oid,row in sources.items():
   item=lookup[oid]
   t=row["locale"][loc]
   item["status"]=ORIGIN_STATUS
   item["origin"]=t["origin"].strip()
   item["whyThisDate"]=t["whyThisDate"].strip()
   item["quickFacts"]=[t["fact"].strip()]+item["quickFacts"][:2]
   item["sourcePolicy"]="Individual government/legislative/originator chronology source-checked and localized with AI; no independent human editorial certification."
   item["institutionalSourceUrls"]=row["sources"]
   item["lastReviewedAt"]="2026-11-19"
  assert sum(r["status"]==ORIGIN_STATUS for r in entries)==107
  assert sum(r["status"]==CONTEXT_STATUS for r in entries)==592
  path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 report={"catalog":1111,"localeCount":6,"sourceGroundedExisting":507,
         "newIndividualSourceGrounded":12,"sourceGroundedNow":519,
         "contextualStillAwaitingOrigin":592,"noEditorialLocale":0,
         "qualifiedSourceYearBefore":12,"sourceIds":sorted(rows)}
 out=ROOT/"reports/fasttrack_parallel_604/origin_enrichment_12.json"
 out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("ORIGIN_ENRICHMENT_12_SIX_LOCALE_PASS",json.dumps(report,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
 main()
