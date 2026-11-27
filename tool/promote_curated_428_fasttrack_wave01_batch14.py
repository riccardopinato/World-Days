#!/usr/bin/env python3
"""Fast Track wave01 batch14: source-pinned, ID-scoped, six-locale promotion.
This runs after the immutable earlier importers, and preserves individual HOLDs.
"""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from fasttrack_curated_428_qc import audit_row

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/data"
REPORT=ROOT/"reports/editorial_curated_428_origin_research"
LEDGER=ROOT/"data/editorial/reviews/curated_428_fasttrack_wave01_batch14_20261127.json"
OUT=REPORT/"fasttrack_wave01_batch14_runtime_import.json"
LANG=("en","it","es","fr","de","pt")
CONTEXT="AI_CONTEXTUAL_SIX_LOCALE"
REVIEWED="AI_SOURCE_REVIEWED_SIX_LOCALE"
VERSION="2026.11.27.16"
YEARS=re.compile(r"(?<![0-9])(?:1[0-9]{3}|20[0-9]{2})(?![0-9])")

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def git_blob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

def run():
    approval=load(LEDGER)
    assert approval["mode"]=="APP_FACTORY_CORE_V27_FAST_TRACK_WAVE01_BATCH14"
    assert approval["factoryBaseline"]=="3e663a1a2a77142ab755e0fa645f14c74991e367"
    assert approval["humanCertified"] is False
    assert approval["proposedBatch14"]==len(approval["records"])==2
    official=load(ASSETS/"official_core.json")
    assert len(official["records"])==947 and official["datasetVersion"]=="2026.11.27.15"
    catalog={r["id"]:r for r in official["records"]}
    queue=load(ROOT/"data/editorial/waves/curated_428_unwritten_fasttrack_block_01.json")
    assert len(queue["canonicalIds"])==100
    allow=set(queue["canonicalIds"])
    cohorts={}
    for n in (2,3):
        q=load(REPORT/f"cohort_{n:02d}_ordered_ids.json")
        for oid in q["ids"]: cohorts[oid]=n
    before=0
    assert before==0
    packs={loc:load(ASSETS/f"editorial_{loc}.json") for loc in LANG}
    lookup={}
    first=None
    for loc,doc in packs.items():
        ids=[r["observanceId"] for r in doc["entries"]]
        assert len(ids)==len(set(ids))==doc["entryCount"]==947
        if first is None: first=ids
        else: assert ids==first
        assert sum(r["status"]==CONTEXT for r in doc["entries"])==227-before
        lookup[loc]={r["observanceId"]:r for r in doc["entries"]}
    selected={}
    decisions=[]
    visited=set()
    for item in approval["records"]:
        oid=item["id"]
        assert oid not in visited and oid in allow and oid in catalog
        visited.add(oid)
        p=ROOT/item["sourceFile"]
        assert p.is_file() and p.parent.name=="curated_428_wave01_sources"
        assert git_blob(p.read_bytes())==item["sourceBlobSha"],("stale_source_blob",oid)
        row=load(p)
        assert row["id"]==oid and row["cohort"]==cohorts[oid]
        assert row["schemaVersion"]==1 and row["runtimeRichEditorialApproved"] is False
        assert item["humanSignoff"] is False and item["allSixLocalesAuthored"] is True
        assert item["reviewStatus"]=="AI_SOURCE_SCOPED_PENDING_FINAL_CI_QA"
        assert set(row["narratives"])==set(LANG)
        assert all(len(v.strip())>=165 for v in row["narratives"].values())
        if any(lookup[loc][oid]["status"]!=CONTEXT for loc in LANG):
            decisions.append({"id":oid,"outcome":"HOLD_EXISTING_RICH"})
            continue
        # Individually fail closed on documented scope or calendar conflict.
        if "HOLD" in row.get("status","") or "HOLD" in json.dumps(row.get("scopeDecision",{})).upper():
            decisions.append({"id":oid,"outcome":"HOLD_DOCUMENTED_SCOPE_OR_CALENDAR_CONFLICT","reason":row.get("scopeDecision",{})})
            continue
        qa=audit_row(row,catalog)
        movable_expected={
            "uk-remembrance-sunday":{"kind":"NTH_WEEKDAY","month":11,"weekday":7,"occurrence":2},
            "us-thanksgiving-day":{"kind":"NTH_WEEKDAY","month":11,"weekday":4,"occurrence":4}
        }
        if oid in movable_expected:
            rule=movable_expected[oid]
            matched=any(all(r.get(k)==v for k,v in rule.items()) for r in catalog[oid]["recurrenceRules"])
            only_calendar_review=not qa["errors"] and not qa["flags"] and set(qa["reviews"]) <= {"DATE_NEEDS_RECURRENCE_CHECK"}
            if not matched or not only_calendar_review or row.get("date") is not None:
                decisions.append({"id":oid,"outcome":"HOLD_RECURRENCE_RULE_OR_SOURCE_QA","expectedRule":rule,"matched":matched,"details":qa})
                continue
        elif qa["outcome"]!="OFFLINE_QA_PASS_SOURCE_AND_SEMANTIC_REVIEW_REQUIRED":
            decisions.append({"id":oid,"outcome":"HOLD_STRUCTURAL_OR_PROVENANCE_QA","details":qa})
            continue
        years={loc:sorted(set(YEARS.findall(row["narratives"][loc]))) for loc in LANG}
        if len({tuple(v) for v in years.values()})!=1:
            decisions.append({"id":oid,"outcome":"HOLD_HISTORICAL_YEAR_PARITY","details":years})
            continue
        if len(set(v.casefold().strip() for v in row["narratives"].values()))!=6:
            decisions.append({"id":oid,"outcome":"HOLD_LANGUAGE_FALLBACK"})
            continue
        sources=row["sourceEvidence"]
        if not sources or any(
            x.get("verificationStatus")!="PRIMARY_SOURCE_FOUND_WEB_REVIEW"
            or urlsplit(x.get("url","")).scheme!="https"
            or len(x.get("claim",""))<35 for x in sources
        ):
            decisions.append({"id":oid,"outcome":"HOLD_SOURCE_EVIDENCE"})
            continue
        selected[oid]=(row,item)
        decisions.append({"id":oid,"outcome":"AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT","gitBlobSha":item["sourceBlobSha"]})
    assert len(visited)==len(decisions)==2
    assert len(selected)+sum(z["outcome"].startswith("HOLD") for z in decisions)==2
    for loc,doc in packs.items():
        rows=lookup[loc]
        for oid,(research,item) in selected.items():
            dest=rows[oid]
            assert dest["status"]==CONTEXT
            dest["origin"]=research["narratives"][loc].strip()
            dest["status"]=REVIEWED
            dest["lastReviewedAt"]=approval["reviewedAt"]
            dest["sourcePolicy"]="Fast Track IA: primary law or government source and canonical recurrence rules checked; translations reviewed with individual per-ID HOLD; no human expert certificate."
            dest["institutionalSourceUrls"]=[s["url"] for s in research["sourceEvidence"]]
            dest["aiEditorialProvenance"]={
                "reviewLevel":"AI_EDITORIAL_REVIEWED",
                "reviewDate":approval["reviewedAt"],
                "sourceResearchFile":item["sourceFile"],
                "sourceResearchBlobSha":item["sourceBlobSha"],
                "humanSignoff":False,
                "everyHistoricalAssertionIndependentlyVerified":False
            }
        doc["datasetVersion"]=VERSION
    official["datasetVersion"]=VERSION
    write(ASSETS/"official_core.json",official)
    for loc,doc in packs.items(): write(ASSETS/f"editorial_{loc}.json",doc)
    index_path=ASSETS/"origin_review_index.json"
    if index_path.exists():
        index=load(index_path);index["datasetVersion"]=VERSION;write(index_path,index)
    index_path=REPORT/"index.json"
    if index_path.exists():
        idx=load(index_path)
        assert idx["contextualOriginPending"]==227-before and idx["nonContextualRich"]==720+before
        previous=set(idx["fastTrackIntegratedIds"])
        assert len(previous)==201+before and not (set(selected)&previous)
        idx["fastTrackIntegratedIds"]=sorted(previous|set(selected))
        idx["contextualOriginPending"]=227-before-len(selected)
        idx["notYetPersonallyResearched"]=227-before-len(selected)
        idx["nonContextualRich"]=720+before+len(selected)
        for oid,(row,_) in selected.items():
            assert idx["countriesPending"][row["country"]]>0
            idx["countriesPending"][row["country"]]-=1
        write(index_path,idx)
    result={
       "schemaVersion":1,"mode":"APP_FACTORY_CORE_V27_WAVE01_BATCH14_AI",
       "sourceMainCommit":approval["sourceMain"],
       "numberOfNewSixLocaleDossiers":2,
       "integratedNew":len(selected),"heldNew":2-len(selected),
       "decisions":decisions,
       "integratedIds":sorted(selected),
       "holdIds":[z["id"] for z in decisions if z["outcome"].startswith("HOLD")],
       "originalTargetTotal":428,"previouslyIntegrated":201+before,
       "newTotalIntegrated":201+before+len(selected),
       "richEditorialAfter":720+before+len(selected),
       "contextualAfter":227-before-len(selected),
       "notYetAuthoredAfter":185,
       "humanSignoff":False,"physicalRelease":False,
       "contentPackVersion":VERSION
    }
    write(OUT,result)
    print("FASTTRACK_WAVE01_BATCH14_IMPORT",json.dumps({
       "drafts":2,"integrated":len(selected),"held":result["heldNew"],
       "totalRich":result["richEditorialAfter"],"contextual":result["contextualAfter"],
       "newTotal":result["newTotalIntegrated"]},sort_keys=True))
if __name__=="__main__":run()
