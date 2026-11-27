#!/usr/bin/env python3
"""Validate exact batch04 integration and six locale parity after source-pinned promotion."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data"
R=ROOT/"reports/editorial_curated_428_origin_research"
load=lambda p: json.loads(p.read_text(encoding="utf-8"))
x=load(R/"fasttrack_wave01_batch04_runtime_import.json")
ledger=load(ROOT/"data/editorial/reviews/curated_428_fasttrack_wave01_batch04_20261127.json")
assert x["mode"]=="APP_FACTORY_CORE_V27_WAVE01_BATCH04_AI"
assert len(ledger["records"])==4==x["numberOfNewSixLocaleDossiers"]
assert x["integratedNew"]+x["heldNew"]==4
assert x["newTotalIntegrated"]==150+x["integratedNew"]
assert x["richEditorialAfter"]==669+x["integratedNew"]
assert x["contextualAfter"]==278-x["integratedNew"]
assert x["notYetAuthoredAfter"]==240
assert x["physicalRelease"] is False and x["humanSignoff"] is False
assert len(x["decisions"])==4 and len({d["id"] for d in x["decisions"]})==4
assert len(x["integratedIds"])==len(set(x["integratedIds"]))==x["integratedNew"]
assert set(x["integratedIds"])=={d["id"] for d in x["decisions"] if d["outcome"]=="AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT"}
core=load(A/"official_core.json")
assert core["datasetVersion"]==x["contentPackVersion"]=="2026.11.27.7"
assert len({r["id"] for r in core["records"]})==947
ordering=None
for locale in ("en","it","es","fr","de","pt"):
    doc=load(A/f"editorial_{locale}.json")
    assert doc["datasetVersion"]==x["contentPackVersion"]
    entries=doc["entries"]
    ids=[r["observanceId"] for r in entries]
    assert len(ids)==len(set(ids))==doc["entryCount"]==947
    if ordering is None:ordering=ids
    else:assert ordering==ids
    assert sum(r["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for r in entries)==x["contextualAfter"]
    lookup={r["observanceId"]:r for r in entries}
    for oid in x["integratedIds"]:
        r=lookup[oid]
        assert r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE" and len(r["origin"].strip())>=165
        assert r["institutionalSourceUrls"]
        p=r["aiEditorialProvenance"]
        assert p["reviewLevel"]=="AI_EDITORIAL_REVIEWED" and p["sourceResearchBlobSha"] and not p["humanSignoff"]
print("FASTTRACK_WAVE01_BATCH04_SIX_LOCALE_PASS",x["integratedNew"],"integrated;",x["heldNew"],"HOLD")
