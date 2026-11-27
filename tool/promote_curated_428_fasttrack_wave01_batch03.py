#!/usr/bin/env python3
"""Fast Track incremental batch03: scoped AI review and six-locale source-pinned import.

Input: 8 newly authored stories from the first canonical 100-ID wave.
Original first 19 are handled separately by the previous wave01 importer.
No source URL presence by itself certifies source contents or human signoff.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from fasttrack_curated_428_qc import audit_row

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/data"
REPORT=ROOT/"reports/editorial_curated_428_origin_research"
LEDGER=ROOT/"data/editorial/reviews/curated_428_fasttrack_wave01_batch03_20261127.json"
OUT=REPORT/"fasttrack_wave01_batch03_runtime_import.json"
LANG=("en","it","es","fr","de","pt")
CONTEXT="AI_CONTEXTUAL_SIX_LOCALE"
REVIEWED="AI_SOURCE_REVIEWED_SIX_LOCALE"
VERSION="2026.11.27.6"
YEARS=re.compile(r"(?<![0-9])(?:1[0-9]{3}|20[0-9]{2})(?![0-9])")

def load(path): return json.loads(path.read_text(encoding="utf-8"))
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def git_blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()

def run():
    approval=load(LEDGER)
    assert approval["mode"]=="APP_FACTORY_CORE_V27_FAST_TRACK_WAVE01_BATCH03"
    assert approval["factoryBaseline"]=="a185c16000608b90c5db639f37903b49b059b10b"
    assert approval["humanCertified"] is False
    assert approval["proposedBatch03"]==len(approval["records"])==8
    official=load(ASSETS/"official_core.json")
    catalog={r["id"]:r for r in official["records"]}
    assert len(catalog)==947 and official["datasetVersion"]=="2026.11.27.5"
    sourcequeue=load(ROOT/"data/editorial/waves/curated_428_unwritten_fasttrack_block_01.json")
    assert len(sourcequeue["canonicalIds"])==100
    allow=set(sourcequeue["canonicalIds"])
    cohorts={}
    for n in (2,3):
        q=load(REPORT/f"cohort_{n:02d}_ordered_ids.json")
        for oid in q["ids"]: cohorts[oid]=n
    packs={loc:load(ASSETS/f"editorial_{loc}.json") for loc in LANG}
    lookup={}
    first=None
    for loc,doc in packs.items():
        ids=[r["observanceId"] for r in doc["entries"]]
        assert len(ids)==len(set(ids))==doc["entryCount"]==947
        if first is None: first=ids
        else: assert ids==first
        assert sum(r["status"]==CONTEXT for r in doc["entries"])==285
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
        assert row["id"]==oid
        assert row["cohort"]==cohorts[oid], ("wrong_source_cohort",oid)
        assert row["schemaVersion"]==1
        assert item["humanSignoff"] is False and item["allSixLocalesAuthored"] is True
        assert item["reviewStatus"]=="AI_SOURCE_SCOPED_PENDING_FINAL_CI_QA"
        assert row["runtimeRichEditorialApproved"] is False
        assert set(row["narratives"])==set(LANG)
        assert all(len(v.strip())>=165 for v in row["narratives"].values())
        if lookup["en"][oid]["status"]!=CONTEXT:
            decisions.append({"id":oid,"outcome":"HOLD_EXISTING_RICH"})
            continue
        qa=audit_row(row,catalog)
        if qa["outcome"]!="OFFLINE_QA_PASS_SOURCE_AND_SEMANTIC_REVIEW_REQUIRED":
            decisions.append({"id":oid,"outcome":"HOLD_STRUCTURAL_OR_PROVENANCE_QA","details":qa})
            continue
        years={loc:sorted(set(YEARS.findall(row["narratives"][loc]))) for loc in LANG}
        if len({tuple(x) for x in years.values()})!=1:
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
    assert len(visited)==len(decisions)==8
    assert len(selected)+sum(d["outcome"].startswith("HOLD") for d in decisions)==8
    assert selected, "zero new stories cleared source and QA gates"
    for loc,doc in packs.items():
        rows=lookup[loc]
        for oid,(research,item) in selected.items():
            dest=rows[oid]
            assert dest["status"]==CONTEXT
            dest["origin"]=research["narratives"][loc].strip()
            dest["status"]=REVIEWED
            dest["lastReviewedAt"]=approval["reviewedAt"]
            dest["sourcePolicy"]="Fast Track IA: checked specific UK, South African, German or Croatian government/institutional documentation for date and origin; AI editorial translations, no professional human sign-off."
            dest["institutionalSourceUrls"]=[s["url"] for s in research["sourceEvidence"]]
            dest["aiEditorialProvenance"]={
                "reviewLevel":"AI_EDITORIAL_REVIEWED",
                "reviewDate":approval["reviewedAt"],
                "sourceResearchFile":item["sourceFile"],
                "sourceResearchBlobSha":item["sourceBlobSha"],
                "humanSignoff":False,
                "everyHistoricalAssertionIndependentlyVerified":False,
            }
        doc["datasetVersion"]=VERSION
    official["datasetVersion"]=VERSION
    write(ASSETS/"official_core.json",official)
    for loc,doc in packs.items():write(ASSETS/f"editorial_{loc}.json",doc)
    op=ASSETS/"origin_review_index.json"
    if op.exists():
        index=load(op);index["datasetVersion"]=VERSION;write(op,index)
    op=REPORT/"index.json"
    if op.exists():
        idx=load(op)
        assert idx["contextualOriginPending"]==285 and idx["nonContextualRich"]==662
        previous=set(idx["fastTrackIntegratedIds"])
        assert len(previous)==143 and not (set(selected)&previous)
        idx["fastTrackIntegratedIds"]=sorted(previous | set(selected))
        idx["contextualOriginPending"]=285-len(selected)
        idx["notYetPersonallyResearched"]=285-len(selected)
        idx["nonContextualRich"]=662+len(selected)
        for oid,(row,_) in selected.items():
            assert idx["countriesPending"][row["country"]]>0
            idx["countriesPending"][row["country"]]-=1
        write(op,idx)
    result={
       "schemaVersion":1,"mode":"APP_FACTORY_CORE_V27_WAVE01_BATCH03_AI",
       "sourceMainCommit":approval["sourceMain"],
       "numberOfNewSixLocaleDossiers":8,
       "integratedNew":len(selected),
       "heldNew":8-len(selected),
       "decisions":decisions,
       "integratedIds":sorted(selected),
       "holdIds":[d["id"] for d in decisions if d["outcome"].startswith("HOLD")],
       "originalTargetTotal":428,"previouslyIntegrated":143,
       "newTotalIntegrated":143+len(selected),
       "richEditorialAfter":662+len(selected),
       "contextualAfter":285-len(selected),
       "notYetAuthoredAfter":244,
       "humanSignoff":False,"physicalRelease":False,
       "contentPackVersion":VERSION,
    }
    write(OUT,result)
    print("FASTTRACK_WAVE01_BATCH03_IMPORT",json.dumps({
       "drafts":8,"integrated":len(selected),"held":result["heldNew"],
       "totalRich":result["richEditorialAfter"],"contextual":result["contextualAfter"],
       "newTotal":result["newTotalIntegrated"]},sort_keys=True))

if __name__=="__main__":run()
