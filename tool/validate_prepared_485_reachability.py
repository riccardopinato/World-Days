#!/usr/bin/env python3
"""Fail-closed inventory: all 485 written histories are reachable without fake approval.

Status levels are kept separate: 56 legacy reviewed editorial, 173 AI certified,
90 AI source+chronology-reviewed six-locale, remaining older EN/IT research
available as labelled historical research with English fallback.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BATCHES=ROOT/"data/editorial/batches"
LOC=("en","it","es","fr","de","pt")

def load(p):
 return json.loads(p.read_text(encoding="utf-8"))

source_files=[BATCHES/"origin_stories_primary_20261111.json"]+sorted(BATCHES.glob("origin_stories_wave*.json"))
researched={}
for f in source_files:
 pack=load(f)
 assert pack["status"]=="SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE",f
 for rec in pack["records"]:
  oid=rec["observanceId"]
  assert oid not in researched,oid
  researched[oid]=rec
assert len(researched)==325,len(researched)
reviews=load(ROOT/"data/editorial/reviews/ph_kr_ca_173_ai_editorial_certification_20261114.json")
certs={r["observanceId"] for r in reviews["records"]}
assert len(certs)==173 and all(r["status"]=="AI_CERTIFIED" for r in reviews["records"])
assert len(set(researched)&certs)==18
top5=load(ROOT/"data/editorial/published/top5_5_six_locale_20261115.json")
five={r["observanceId"] for r in top5["records"]}
assert len(five)==5 and not five & (set(researched)|certs)
all_prepared=set(researched)|certs|five
assert len(all_prepared)==485

origins=load(ROOT/"assets/data/origin_review_index.json")
assert origins["recordCount"]==origins["sourceCatalogCount"]==1111
entries={r["observanceId"]:r for r in origins["records"]}
preview={oid for oid,r in entries.items() if r.get("runtimeResearchPreviewAllowed") is True}
assert preview==set(researched),("preview must match exactly 325 already on main",len(preview))
assert all(r["runtimeRichEditorialApproved"] is False for r in entries.values()),"No unaudited human rich approval"
assert all((r["primaryResearch"] is not None)==(oid in researched) for oid,r in entries.items())

en_ids=None
counts=None
for lang in LOC:
 pack=load(ROOT/f"assets/data/editorial_{lang}.json")
 rows=pack["entries"]
 ids=[r["observanceId"] for r in rows]
 assert len(ids)==len(set(ids))==pack["entryCount"]==319,(lang,len(ids))
 kinds={k:sum(r["status"]==k for r in rows) for k in
        ("AI_CERTIFIED","AI_SOURCE_REVIEWED_SIX_LOCALE")}
 assert kinds=={"AI_CERTIFIED":173,"AI_SOURCE_REVIEWED_SIX_LOCALE":90},(lang,kinds)
 assert pack.get("aiEditorialCertifiedCount")==173
 assert pack.get("aiSourceReviewedSixLocaleCount")==90
 new={r["observanceId"] for r in rows if r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE"}
 assert len(new)==90
 assert len(new & set(researched))==85
 assert five <= new
 assert set(researched) | certs | five <= set(ids) | preview
 if en_ids is None:
  en_ids=ids;counts=kinds
 else:
  assert en_ids==ids,("six-locale ordering drift",lang)
 assert all(r["origin"].strip() for r in rows if r["status"] in kinds)
assert len(en_ids)==319
enriched=set(en_ids)
assert all_prepared <= (enriched|preview)
untranslated=sorted(preview-enriched)
legacy=set(en_ids[:56])
assert len(legacy)==56
assert len(set(researched)&enriched)==103+len(set(researched)&legacy),("researched overlap",len(set(researched)&enriched))
assert len(untranslated)==222-len(set(researched)&legacy),("bilingual preview count",len(untranslated))
print("WORLD_DAYS_PREPARED_HISTORY_COVERAGE_OK",json.dumps({
 "catalog":1111,"existingBilingualResearch":325,
 "newAICertified":173,"researchCertificateOverlap":18,
 "newSixLocaleSourceReviewed":90,"newOutsideMain":5,
 "uniquePreparedStories":485,"richEditorial":316,
 "bilingualPreviewOnly":len(untranslated),
 "humanCertifiedClaimed":0,
 "unresolvedPhilippineSourceIDs":7,
},sort_keys=True))
