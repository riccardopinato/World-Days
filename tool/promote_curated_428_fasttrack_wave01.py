#!/usr/bin/env python3
"""Fast Track v27: independently reviewed wave01 origins, six locales, fail-closed.

Legacy 147-source inventory and its 85-dossier importer remain immutable.
Only the new wave01 source directory is considered for this incremental batch.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from fasttrack_curated_428_qc import audit_row

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data"
R=ROOT/"reports/editorial_curated_428_origin_research"
D=ROOT/"data/editorial/waves/curated_428_wave01_sources"
LEDGER=ROOT/"data/editorial/reviews/curated_428_fasttrack_wave01_20261127.json"
OUT=R/"fasttrack_wave01_runtime_import.json"
LANG=("en","it","es","fr","de","pt")
YEARS=re.compile(r"(?<![0-9])(?:1[0-9]{3}|20[0-9]{2})(?![0-9])")
VERSION="2026.11.27.4"
CONTEXT="AI_CONTEXTUAL_SIX_LOCALE"
REVIEWED="AI_SOURCE_REVIEWED_SIX_LOCALE"

def load(p): return json.loads(p.read_text(encoding="utf-8"))
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def git_sha(p):
    b=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()

def run():
    ledger=load(LEDGER)
    assert ledger["mode"]=="APP_FACTORY_CORE_V27_FAST_TRACK_WAVE01"
    assert ledger["humanSignoffClaim"] is False
    assert ledger["candidateCount"]==len(ledger["records"])==19
    block=load(ROOT/"data/editorial/waves/curated_428_unwritten_fasttrack_block_01.json")
    assert block["count"]==100 and len(block["canonicalIds"])==100
    targeted=set(block["canonicalIds"])
    official=load(A/"official_core.json")
    catalog={r["id"]:r for r in official["records"]}
    assert len(catalog)==947 and official["datasetVersion"]=="2026.11.27.3"
    packs={loc:load(A/f"editorial_{loc}.json") for loc in LANG}
    ids=None
    for loc,pack in packs.items():
        order=[x["observanceId"] for x in pack["entries"]]
        assert len(order)==len(set(order))==pack["entryCount"]==947
        assert order==ids if ids is not None else True
        ids=order
        assert sum(x["status"]==CONTEXT for x in pack["entries"])==313
    originals={x["observanceId"]:x for x in packs["en"]["entries"]}
    files=sorted(D.glob("curated_428_wave01_*.json"))
    assert len(files)==19 and len({load(p)["id"] for p in files})==19
    selected={}
    decisions=[]
    source_blobs={row["sourceFile"]:row for row in ledger["records"]}
    assert len(source_blobs)==19
    for path in files:
        row=load(path)
        oid=row["id"]
        rel=path.relative_to(ROOT).as_posix()
        record=source_blobs.get(rel)
        assert record and record["id"]==oid
        assert git_sha(path)==record["sourceBlobSha"], ("stale_source_sha",oid)
        assert row["cohort"]==2 and oid in targeted and oid in catalog
        assert row["runtimeRichEditorialApproved"] is False
        assert record["review"]=="AI_EDITORIAL_REVIEWED_HISTORY_DATE_TRANSLATIONS"
        assert record["humanSignoff"] is False and record["sixLocaleChecked"] is True
        assert set(row["narratives"])==set(LANG)
        assert row["status"]=="AI_DRAFT_SIX_LOCALE_SOURCE_CHECKED_NOT_RUNTIME_PUBLISHED"
        if originals[oid]["status"]!=CONTEXT:
            decisions.append({"id":oid,"outcome":"HOLD_ALREADY_NON_CONTEXTUAL"})
            continue
        qa=audit_row(row,catalog)
        if qa["outcome"]!="OFFLINE_QA_PASS_SOURCE_AND_SEMANTIC_REVIEW_REQUIRED":
            decisions.append({"id":oid,"outcome":"HOLD_OFFLINE_QA","details":qa})
            continue
        texts=row["narratives"]
        yearsets={loc:set(YEARS.findall(texts[loc])) for loc in LANG}
        if len(set(map(frozenset,yearsets.values())))!=1:
            decisions.append({"id":oid,"outcome":"HOLD_YEAR_PARITY","details":{k:sorted(v) for k,v in yearsets.items()}})
            continue
        if any(len(texts[loc].strip())<165 for loc in LANG):
            decisions.append({"id":oid,"outcome":"HOLD_SHORT_LOCALE"})
            continue
        if len({texts[loc].strip().lower() for loc in LANG})!=6:
            decisions.append({"id":oid,"outcome":"HOLD_TRANSLATION_DUPLICATE"})
            continue
        evidence=row["sourceEvidence"]
        if not evidence or any(urlsplit(x["url"]).scheme!="https" or not urlsplit(x["url"]).hostname
           or x.get("verificationStatus")!="PRIMARY_SOURCE_FOUND_WEB_REVIEW"
           or len(x.get("claim",""))<35 for x in evidence):
            decisions.append({"id":oid,"outcome":"HOLD_SOURCE_EVIDENCE"})
            continue
        selected[oid]=(row,record)
        decisions.append({"id":oid,"outcome":"AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT","gitBlobSha":record["sourceBlobSha"]})
    assert len(decisions)==19 and len(selected)+sum(x["outcome"].startswith("HOLD") for x in decisions)==19
    assert selected, "No approved records after QA"
    for loc,pack in packs.items():
        byid={r["observanceId"]:r for r in pack["entries"]}
        for oid,(research,record) in selected.items():
            dest=byid[oid]
            assert dest["status"]==CONTEXT
            dest["origin"]=research["narratives"][loc].strip()
            dest["status"]=REVIEWED
            dest["lastReviewedAt"]=ledger["reviewedAt"]
            dest["sourcePolicy"]="App Factory Fast Track IA: primary government or legislative references checked for date and specific core origin; AI editorial and translation review, not independent human fact certification."
            dest["institutionalSourceUrls"]=[s["url"] for s in research["sourceEvidence"]]
            dest["aiEditorialProvenance"]={"reviewLevel":"AI_EDITORIAL_REVIEWED","reviewDate":ledger["reviewedAt"],"sourceResearchFile":record["sourceFile"],"sourceResearchBlobSha":record["sourceBlobSha"],"historicSourceScope":"SPECIFIC_LEGAL_OR_STATE_SOURCE_WEB_CHECKED","humanSignoff":False}
        pack["datasetVersion"]=VERSION
    official["datasetVersion"]=VERSION
    write(A/"official_core.json",official)
    for loc,pack in packs.items(): write(A/f"editorial_{loc}.json",pack)
    key=A/"origin_review_index.json"
    if key.exists():
        index=load(key);index["datasetVersion"]=VERSION;write(key,index)
    originindex=R/"index.json"
    if originindex.exists():
        idx=load(originindex)
        assert idx["contextualOriginPending"]==313 and idx["nonContextualRich"]==634
        prior=set(idx["fastTrackIntegratedIds"])
        assert len(prior)==115 and not (prior & selected.keys())
        idx["fastTrackIntegratedIds"]=sorted(prior | set(selected))
        idx["contextualOriginPending"]=313-len(selected)
        idx["notYetPersonallyResearched"]=313-len(selected)
        idx["nonContextualRich"]=634+len(selected)
        for oid,(row,_) in selected.items():
            country=row["country"]
            assert idx["countriesPending"][country]>0
            idx["countriesPending"][country]-=1
        write(originindex,idx)
    result={"schemaVersion":1,"mode":"APP_FACTORY_CORE_V27_WAVE01_FASTTRACK_AI","sourceMain":"0a6922dfb5eace9a4c8ab8f88e6569525caa3a3b","batchNumber":1,"batchSize":100,"sixLocaleDraftsPrepared":19,"aiReviewedIntegrated":len(selected),"holdCount":19-len(selected),"holdIds":sorted(x["id"] for x in decisions if x["outcome"].startswith("HOLD")),"integratedIds":sorted(selected),"decisions":decisions,"newlyUnwrittenRemainingInBlock":100-19,"totalOriginalTarget":428,"totalIntegratedOriginRich":115+len(selected),"catalogRichAfter":634+len(selected),"catalogContextualAfter":313-len(selected),"unwrittenRemainingAcrossThreeBlocks":281-19,"contentPackVersion":VERSION,"humanSignoff":False,"physicalReleaseCertified":False,"mergedMain":False}
    write(OUT,result)
    print("FASTTRACK_WAVE01_IMPORT",json.dumps({"newDrafts":19,"integrated":len(selected),"holds":19-len(selected),"rich":result["catalogRichAfter"],"contextual":result["catalogContextualAfter"],"unwritten":result["unwrittenRemainingAcrossThreeBlocks"]},sort_keys=True))

if __name__=="__main__":
    run()
