#!/usr/bin/env python3
"""Independent exact-inventory six-locale provenance gate for batch09."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data";R=ROOT/"reports/editorial_curated_428_origin_research"
ld=lambda p:json.loads(p.read_text(encoding="utf-8"))
x=ld(R/"fasttrack_wave01_batch09_runtime_import.json")
assert x["mode"]=="APP_FACTORY_CORE_V27_WAVE01_BATCH09_AI"
assert x["numberOfNewSixLocaleDossiers"]==6 and x["integratedNew"]+x["heldNew"]==6
assert x["previouslyIntegrated"]==179 and x["newTotalIntegrated"]==179+x["integratedNew"]
assert x["richEditorialAfter"]==698+x["integratedNew"] and x["contextualAfter"]==249-x["integratedNew"]
assert x["notYetAuthoredAfter"]==207 and x["humanSignoff"] is False and x["physicalRelease"] is False
assert len(x["decisions"])==6 and len({d["id"] for d in x["decisions"]})==6
assert set(x["integratedIds"])=={d["id"] for d in x["decisions"] if d["outcome"]=="AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT"}
core=ld(A/"official_core.json")
assert core["datasetVersion"]==x["contentPackVersion"]=="2026.11.27.12"
assert len({r["id"] for r in core["records"]})==947
previous_ids=None
for locale in ("en","it","es","fr","de","pt"):
    doc=ld(A/f"editorial_{locale}.json")
    assert doc["datasetVersion"]==x["contentPackVersion"]
    entries=doc["entries"];ids=[r["observanceId"] for r in entries]
    assert len(ids)==len(set(ids))==doc["entryCount"]==947
    if previous_ids is None:previous_ids=ids
    else:assert previous_ids==ids
    assert sum(r["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for r in entries)==x["contextualAfter"]
    lookup={r["observanceId"]:r for r in entries}
    for oid in x["integratedIds"]:
        r=lookup[oid]
        assert r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE" and len(r["origin"].strip())>=165 and r["institutionalSourceUrls"]
        p0=r["aiEditorialProvenance"]
        assert p0["reviewLevel"]=="AI_EDITORIAL_REVIEWED" and p0["sourceResearchBlobSha"] and not p0["humanSignoff"]
print("FASTTRACK_WAVE01_BATCH09_SIX_LOCALE_PASS",x["integratedNew"],"integrated;",x["heldNew"],"HOLD")
