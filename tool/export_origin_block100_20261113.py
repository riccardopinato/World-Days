#!/usr/bin/env python3
"""Print the next EXACT 100 pending canonical origin IDs and their source leads.

This is a planning export. Individual historical origin verification and authored
narratives are separate and no worklist item is counted as an approved story.
"""
import json
from editorial_origin_completion_waves import build

index, batches = build()
assert index["catalogTotal"] >= 1111
assert index["individuallyOriginResearched"] >= 225
assert index["outstandingOriginResearch"] == index["catalogTotal"] - index["individuallyOriginResearched"]
first = batches["batch_001.json"]
assert first["recordCount"] == first["batchLimit"] == 100
ids = [d["observanceId"] for d in first["dossiers"]]
assert len(ids) == len(set(ids)) == 100
print("WAVE20_CANONICAL_FIRST100_COUNTS", json.dumps({
    "mainResearched": index["individuallyOriginResearched"],
    "catalog": index["catalogTotal"], "pending": index["outstandingOriginResearch"],
    "batches": index["batchCount"], "firstBatchCount": len(ids)
}, sort_keys=True))
for d in first["dossiers"]:
    print("WAVE20_FIRST100_ID", json.dumps({
        "sequence": d["sequence"],
        "id": d["observanceId"],
        "titleEn": d["titleEn"],
        "scope": d["scope"],
        "countries": d["countries"],
        "periodKind": d["periodKind"],
        "introducedYearLead": d["catalogIntroducedYearUnrecertified"],
        "sourceLeads": d["catalogSourceUrlsAreStartingLeads"],
        "sourceGate": d["sourceQualityGate"],
        "workType": d["workType"],
        "existingEditorialStage": d["existingEditorialStage"]
    }, ensure_ascii=False, sort_keys=True))
print("WAVE20_FIRST100_READY_NOT_CERTIFIED", len(ids))
