#!/usr/bin/env python3
"""Independent fail-closed regression gate for prepared85 Fast Track import."""
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/data"
REPORT=ROOT/"reports/editorial_curated_428_origin_research/fasttrack_prepared85_runtime_import.json"
LEDGER=ROOT/"data/editorial/reviews/curated_428_fasttrack_prepared85_20261127.json"
LANG=("en","it","es","fr","de","pt")
def load(p): return json.loads(p.read_text(encoding="utf-8"))
r=load(REPORT)
l=load(LEDGER)
assert r["mode"]=="APP_FACTORY_CORE_V27_FAST_TRACK_PREPARED85_AI"
assert r["sourceMainCommit"]==l["targetMainBaseline"]
assert r["sourceResearchFiles"]==147 and r["preparedOpenBefore"]==85
assert r["preparedMainCohort01"]==38 and r["preparedFromBranches"]==47
assert r["approvedCandidateCount"]==l["selectedForIndividualConditionalReview"]==65
assert len(r["integratedIds"])==len(set(r["integratedIds"]))==r["fasttrackNewIntegrated"]>0
assert r["holdCount"]+r["fasttrackNewIntegrated"]==85
assert r["contextualAfter"]==366-r["fasttrackNewIntegrated"]
assert r["totalOriginRichAfter"]==581+r["fasttrackNewIntegrated"]
assert r["preparedButNotIntegratedAfter"]==r["holdCount"]
assert r["stillNotAuthored"]==281
assert r["humanSignoff"] is False and r["physicalReleaseCertified"] is False
decisions=r["decisions"]
assert len(decisions)==85 and len({d["id"] for d in decisions})==85
assert Counter(d["outcome"] for d in decisions)==Counter(r["outcomeCounts"])
assert {d["id"] for d in decisions if d["outcome"]=="AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT"}==set(r["integratedIds"])
assert sum(1 for d in decisions if d["outcome"].startswith("HOLD"))==r["holdCount"]
assert sum(1 for d in decisions if d["id"] in {x["observanceId"] for x in l["records"]})==65
core=load(ASSETS/"official_core.json")
assert core["datasetVersion"]==r["contentPackVersion"]
canonical={i["id"] for i in core["records"]}
assert len(canonical)==947 and set(r["integratedIds"])<=canonical
master=None
for locale in LANG:
    p=load(ASSETS/f"editorial_{locale}.json")
    assert p["datasetVersion"]==r["contentPackVersion"]
    entries=p["entries"]
    ids=[i["observanceId"] for i in entries]
    assert len(ids)==len(set(ids))==p["entryCount"]==947
    if master is None: master=ids
    else: assert ids==master,("locale/order",locale)
    lookup={i["observanceId"]:i for i in entries}
    for id in r["integratedIds"]:
        item=lookup[id]
        assert item["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE",(locale,id)
        assert len(item["origin"].strip())>=180,(locale,id)
        assert item["institutionalSourceUrls"]
        prov=item["aiEditorialProvenance"]
        assert prov["reviewLevel"]=="AI_EDITORIAL_REVIEWED"
        assert prov["sourceResearchBlobSha"] and not prov["humanSignoff"]
        assert prov["everyHistoricalSourceReopened"] is False
    assert sum(i["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for i in entries)==r["contextualAfter"],locale
    assert sum(i["status"]!="AI_CONTEXTUAL_SIX_LOCALE" for i in entries)==r["totalOriginRichAfter"],locale
print("FASTTRACK_PREPARED85_SIX_LOCALE_GATE_PASS", r["fasttrackNewIntegrated"],
      "integrated x", len(LANG), "langs;",r["holdCount"],"HOLD")
