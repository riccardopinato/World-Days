#!/usr/bin/env python3
"""Independent exact-inventory, locale and provenance gate for Fast Track batch03."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data"
R=ROOT/"reports/editorial_curated_428_origin_research"
rd=lambda p: json.loads(p.read_text(encoding="utf-8"))
x=rd(R/"fasttrack_wave01_batch03_runtime_import.json")
ledger=rd(ROOT/"data/editorial/reviews/curated_428_fasttrack_wave01_batch03_20261127.json")
assert x["mode"]=="APP_FACTORY_CORE_V27_WAVE01_BATCH03_AI"
assert x["numberOfNewSixLocaleDossiers"]==len(ledger["records"])==8
assert x["integratedNew"]+x["heldNew"]==8
assert len(x["integratedIds"])==len(set(x["integratedIds"]))==x["integratedNew"]>0
assert x["previouslyIntegrated"]==143 and x["newTotalIntegrated"]==143+x["integratedNew"]
assert x["richEditorialAfter"]==662+x["integratedNew"]
assert x["contextualAfter"]==285-x["integratedNew"]
assert x["notYetAuthoredAfter"]==244
assert x["physicalRelease"] is False and x["humanSignoff"] is False
assert len(x["decisions"])==8 and len({z["id"] for z in x["decisions"]})==8
assert {z["id"] for z in x["decisions"] if z["outcome"]=="AI_EDITORIAL_REVIEWED_READY_FOR_APP_IMPORT"}==set(x["integratedIds"])
assert sum(z["outcome"].startswith("HOLD") for z in x["decisions"])==x["heldNew"]
core=rd(A/"official_core.json")
assert len({r["id"] for r in core["records"]})==947
assert core["datasetVersion"]==x["contentPackVersion"]
ordering=None
for locale in ("en","it","es","fr","de","pt"):
    doc=rd(A/f"editorial_{locale}.json")
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
print("FASTTRACK_WAVE01_BATCH03_SIX_LOCALE_PASS", x["integratedNew"],"integrated;",x["heldNew"],"HOLD")
