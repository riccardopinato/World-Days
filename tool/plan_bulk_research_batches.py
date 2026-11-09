#!/usr/bin/env python3
"""Generate bounded review batches from the 153-record dedup/triage pipeline.

This is a work queue, not an assertion that the 42 low-risk entries are new
unique holidays or that 2027/2028 calendars were verified.
"""
from collections import Counter
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
TRIAGE=ROOT/"reports/research_semantic_triage.json"
COVERAGE=ROOT/"reports/research_certification_coverage.json"
ATTEST=ROOT/"reports/research_date_consensus_2026.json"
OUTPUT=ROOT/"reports/research_fast_batches.json"
BATCH_SIZE=30

def main():
    triage=json.loads(TRIAGE.read_text(encoding="utf-8"))
    coverage=json.loads(COVERAGE.read_text(encoding="utf-8"))
    attest=json.loads(ATTEST.read_text(encoding="utf-8"))
    assert triage["recordCount"]==coverage["researchRecords"]==153
    known={
        (r["researchFile"],r["title"],r["country"]):r
        for r in coverage["records"]
    }
    authoritative={
        (r["researchFile"],r["title"],r["country"]):r
        for r in attest["records"] if r["status"]=="DATE_2026_CONFIRMED_BY_ORIGINATOR"
    }
    fast=[]
    complex_items=[]
    for r in triage["records"]:
        key=(r["researchFile"],r["title"],r["country"])
        assert key in known,key
        state=known[key]
        if r["reviewLane"]=="CANDIDATE_FOR_FIXED_RULE_SOURCE_REVIEW":
            assert state["status"]=="PRIMARY_CALENDAR_2026_DATE_CONFIRMED"
            fast.append({
                "title":r["title"],"country":r["country"],"researchFile":r["researchFile"],
                "date2026":state["2026Date"],"officialCalendarUrl":state["sourceEvidence"],
                "perEventDateExcerptVerified":key in authoritative,
                "requiredChecks":[
                  "Verify country/scope + cultural identity versus canonical 456 and 16 PR67",
                  "Verify fixed/weekday annual date law 2026-2028; not just 2026",
                  "Preserve authority and original document",
                  "Six display titles EN/IT/ES/FR/DE/PT with editorial signoff",
                  "Batch generator and Flutter/Web CI before runtime admission",
                ],
                "admission":"BLOCKED_UNTIL_ALL_GATES_PASS",
            })
        elif r["reviewLane"]=="MANUAL_SEMANTIC_AND_DATE_REVIEW":
            complex_items.append(r)
    # Group by country and then title so one government calendar can be
    # checked in a single pass, instead of 5 website searches per event.
    fast.sort(key=lambda x:(x["country"],x["title"].casefold()))
    assert len(fast)==22,len(fast)
    assert len(complex_items)==62,len(complex_items)
    batches=[]
    for pos in range(0,len(fast),BATCH_SIZE):
        rows=fast[pos:pos+BATCH_SIZE]
        batches.append({
            "batchId":f"FAST-{1+pos//BATCH_SIZE:02d}",
            "targetSize":BATCH_SIZE,"items":rows,
            "count":len(rows),
            "countryCounts":dict(sorted(Counter(x["country"] for x in rows).items())),
            "admission":"RESEARCH_REVIEW_ONLY",
        })
    assert sum(b["count"] for b in batches)==22
    assert [b["count"] for b in batches]==[22]
    output={
        "schemaVersion":1,"catalogMain":456,
        "stagedInConsolidatedPR67":36,
        "confirmedDateResearchButNotAdmitted":84,
        "fastLaneTotal":22,"complexLaneTotal":62,
        "nepalBlock":9,"alreadyCataloguedDuplicates":24,
        "batchSize":BATCH_SIZE,"batches":batches,
        "note":"Queue priority is not certification. Government primary 2026 date can be checked once per official register; 5 mirrors do not add independence, and annual identity/semantic/translation checks remain mandatory.",
    }
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("FAST BULK QUEUE PASS "+json.dumps({
        "batches":[{"id":b["batchId"],"count":b["count"],"countries":b["countryCounts"]} for b in batches],
        "readyForRuntime":0,"pendingSemanticOrDateChecks":22,
    },sort_keys=True))
if __name__=="__main__":main()
