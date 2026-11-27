#!/usr/bin/env python3
"""Independent QA contract for the first new 100-ID historical origin wave."""
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data"
R=ROOT/"reports/editorial_curated_428_origin_research"
LANG=("en","it","es","fr","de","pt")
rd=lambda p: json.loads(p.read_text(encoding="utf-8"))
report=rd(R/"fasttrack_wave01_runtime_import.json")
ledger=rd(ROOT/"data/editorial/reviews/curated_428_fasttrack_wave01_20261127.json")
assert report["mode"]=="APP_FACTORY_CORE_V27_WAVE01_FASTTRACK_AI"
assert report["sourceMain"]==ledger["mainBaseline"]
assert report["batchSize"]==100 and report["sixLocaleDraftsPrepared"]==ledger["candidateCount"]==19
assert report["aiReviewedIntegrated"]+report["holdCount"]==19
assert report["aiReviewedIntegrated"]==len(set(report["integratedIds"]))>0
assert report["catalogRichAfter"]==634+report["aiReviewedIntegrated"]
assert report["catalogContextualAfter"]==313-report["aiReviewedIntegrated"]
assert report["totalIntegratedOriginRich"]==115+report["aiReviewedIntegrated"]
assert report["unwrittenRemainingAcrossThreeBlocks"]==262
assert report["humanSignoff"] is False and report["physicalReleaseCertified"] is False
decisions=report["decisions"]
assert len(decisions)==19 and len({d["id"] for d in decisions})==19
assert {d["id"] for d in decisions if d["outcome"]=="AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT"}==set(report["integratedIds"])
assert sum(d["outcome"].startswith("HOLD") for d in decisions)==report["holdCount"]
queue=rd(ROOT/"data/editorial/waves/curated_428_unwritten_fasttrack_block_01.json")
assert set(d["id"] for d in decisions)<=set(queue["canonicalIds"])
core=rd(A/"official_core.json")
assert core["datasetVersion"]==report["contentPackVersion"]
assert len({r["id"] for r in core["records"]})==947
first_order=None
for locale in LANG:
    doc=rd(A/f"editorial_{locale}.json")
    assert doc["datasetVersion"]==report["contentPackVersion"]
    entries=doc["entries"]
    ids=[x["observanceId"] for x in entries]
    assert len(ids)==len(set(ids))==doc["entryCount"]==947
    if first_order is None: first_order=ids
    else: assert ids==first_order
    assert sum(x["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for x in entries)==report["catalogContextualAfter"]
    byid={x["observanceId"]:x for x in entries}
    for oid in report["integratedIds"]:
        x=byid[oid];prov=x["aiEditorialProvenance"]
        assert x["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE"
        assert len(x["origin"].strip())>=165
        assert prov["reviewLevel"]=="AI_EDITORIAL_REVIEWED"
        assert prov["sourceResearchBlobSha"] and not prov["humanSignoff"]
        assert x["institutionalSourceUrls"]
print("FASTTRACK_WAVE01_SIX_LOCALE_PASS",report["aiReviewedIntegrated"],"integrated x",len(LANG),"HOLD",report["holdCount"])
