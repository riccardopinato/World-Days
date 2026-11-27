#!/usr/bin/env python3
"""Fast Track wave01 cohort03_batch19: source-pinned, ID-scoped, six-locale promotion.
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
LEDGER=ROOT/"data/editorial/reviews/curated_428_fasttrack_cohort03_batch19_20261127.json"
OUT=REPORT/"fasttrack_cohort03_batch19_runtime_import.json"
LANG=("en","it","es","fr","de","pt")
CONTEXT="AI_CONTEXTUAL_SIX_LOCALE"
REVIEWED="AI_SOURCE_REVIEWED_SIX_LOCALE"
VERSION="2026.11.27.21"
YEARS=re.compile(r"(?<![0-9])(?:1[0-9]{3}|20[0-9]{2})(?![0-9])")

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def git_blob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

def run():
    approval=load(LEDGER)
    assert approval["mode"]=="APP_FACTORY_CORE_V27_FAST_TRACK_COHORT03_BATCH19"
    assert approval["factoryBaseline"]=="a68d5ab2a45c30b1f46a91eb79f32685b81df73b"
    assert approval["humanCertified"] is False
    assert approval["proposedBatch19"]==3
    assert approval["cohort"]==3
    assert approval["sourceMain"]=="c6891debd88be327719511154df9a8df872d0d6f"
    assert approval["proposedBatch19"]==len(approval["records"])==3
    official=load(ASSETS/"official_core.json")
    assert len(official["records"])==947 and official["datasetVersion"]=="2026.11.27.20"
    catalog={r["id"]:r for r in official["records"]}
    queue=load(REPORT/"cohort_03_ordered_ids.json")
    assert len(queue["ids"])==100
    allow=set(queue["ids"])
    cohorts={oid:3 for oid in queue["ids"]}
    before=4
    assert before==4
    packs={loc:load(ASSETS/f"editorial_{loc}.json") for loc in LANG}
    lookup={}
    first=None
    for loc,doc in packs.items():
        ids=[r["observanceId"] for r in doc["entries"]]
        assert len(ids)==len(set(ids))==doc["entryCount"]==947
        if first is None: first=ids
        else: assert ids==first
        assert sum(r["status"]==CONTEXT for r in doc["entries"])==212-before
        lookup[loc]={r["observanceId"]:r for r in doc["entries"]}
    selected={}
    decisions=[]
    visited=set()
    for item in approval["records"]:
        oid=item["id"]
        assert oid not in visited and oid in allow and oid in catalog
        visited.add(oid)
        p=ROOT/item["sourceFile"]
        assert p.is_file() and p.parent.name=="curated_428_wave02_sources"
        assert git_blob(p.read_bytes())==item["sourceBlobSha"],("stale_source_blob",oid)
        row=load(p)
        assert row["id"]==oid and row["cohort"]==cohorts[oid]
        if row.get("status")!="AI_DRAFT_SIX_LOCALE_SOURCE_CHECKED_NOT_RUNTIME_PUBLISHED":
            decisions.append({"id":oid,"outcome":"HOLD_NOT_SOURCE_CHECKED"})
            continue
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
            "is-commerce-day":{"kind":"NTH_WEEKDAY","month":8,"weekday":1,"occurrence":1},
            "is-first-day-of-summer":{"kind":"WEEKDAY_ON_OR_AFTER","month":4,"day":19,"weekday":4}
        }
        if oid in movable_expected:
            rule=movable_expected[oid]
            matched=any(all(r.get(k)==v for k,v in rule.items()) for r in catalog[oid]["recurrenceRules"])
            only_calendar_review=not qa["errors"] and not qa["flags"] and set(qa["reviews"]) <= {"DATE_NEEDS_RECURRENCE_CHECK"}
            if not matched or not only_calendar_review or row.get("date") != {"is-commerce-day":"FIRST_MONDAY_AUGUST","is-first-day-of-summer":"FIRST_THURSDAY_AFTER_APRIL_18"}[oid]:
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
    assert len(visited)==len(decisions)==3
    assert len(selected)+sum(z["outcome"].startswith("HOLD") for z in decisions)==3
    for loc,doc in packs.items():
        rows=lookup[loc]
        for oid,(research,item) in selected.items():
            dest=rows[oid]
            assert dest["status"]==CONTEXT
            dest["origin"]=research["narratives"][loc].strip()
            dest["status"]=REVIEWED
            dest["lastReviewedAt"]=approval["reviewedAt"]
            dest["sourcePolicy"]="Fast Track IA: wave02 Iceland six-locale source-reviewed history, source blob pinned, calendar rule verified against official Icelandic sources and canonical recurrence rules, per-ID HOLD, no expert certificate."
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
        assert idx["contextualOriginPending"]==212-before and idx["nonContextualRich"]==735+before
        previous=set(idx["fastTrackIntegratedIds"])
        assert len(previous)==216+before and not (set(selected)&previous)
        idx["fastTrackIntegratedIds"]=sorted(previous|set(selected))
        idx["contextualOriginPending"]=212-before-len(selected)
        idx["notYetPersonallyResearched"]=212-before-len(selected)
        idx["nonContextualRich"]=735+before+len(selected)
        for oid,(row,_) in selected.items():
            assert idx["countriesPending"][row["country"]]>0
            idx["countriesPending"][row["country"]]-=1
        write(index_path,idx)
    result={
       "schemaVersion":1,"mode":"APP_FACTORY_CORE_V27_WAVE01_COHORT03_BATCH19_AI",
       "sourceMainCommit":approval["sourceMain"],
       "numberOfNewSixLocaleDossiers":3,
       "integratedNew":len(selected),"heldNew":3-len(selected),
       "decisions":decisions,
       "integratedIds":sorted(selected),
       "holdIds":[z["id"] for z in decisions if z["outcome"].startswith("HOLD")],
       "originalTargetTotal":428,"previouslyIntegrated":216+before,
       "newTotalIntegrated":216+before+len(selected),
       "richEditorialAfter":735+before+len(selected),
       "contextualAfter":212-before-len(selected),
       "notYetAuthoredAfter":166,
       "humanSignoff":False,"physicalRelease":False,
       "contentPackVersion":VERSION
    }
    write(OUT,result)
    print("FASTTRACK_WAVE01_COHORT03_BATCH19_DECISIONS",json.dumps(decisions,sort_keys=True))
    print("FASTTRACK_WAVE01_COHORT03_BATCH19_IMPORT",json.dumps({
       "drafts":3,"integrated":len(selected),"held":result["heldNew"],
       "totalRich":result["richEditorialAfter"],"contextual":result["contextualAfter"],
       "newTotal":result["newTotalIntegrated"]},sort_keys=True))
if __name__=="__main__":run()
