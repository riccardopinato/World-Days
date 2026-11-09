#!/usr/bin/env python3
"""Fail-closed audit of every research candidate and exact provenance level.

Run after build_dataset.py, audit_research_candidates.py and
validate_research_overlap_decisions.py.
This does not certify publication or editorial review.
"""
from collections import Counter
from datetime import date
from pathlib import Path
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "data/research"
OUT = ROOT / "reports/research_certification_coverage.json"
AUDIT = ROOT / "reports/research_semantic_audit.json"
DECISIONS = RESEARCH / "semantic_overlap_decisions_20261109.json"
EVIDENCE = RESEARCH / "primary_2026_calendar_verified_20261109.json"
EXTRA_DUPLICATES = RESEARCH / "semantic_additional_country_date_duplicates_20261109.json"
LOCALES = {"en","it","es","fr","de","pt"}

def key(file, title):
    return (file, title)

def main():
    a = json.loads(AUDIT.read_text(encoding="utf-8"))
    d = json.loads(DECISIONS.read_text(encoding="utf-8"))
    e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    x = json.loads(EXTRA_DUPLICATES.read_text(encoding="utf-8"))
    assert a["catalogCount"] == d["catalogBaseCount"] == 456
    assert a["candidateRecordCount"] == 153, "source inventory drift"
    assert len(a["candidateResults"]) == 153
    assert e["recordCount"] == len(e["records"]) == 121
    assert e["countryCounts"] == {"KH":12,"LK":13,"BD":6,"LA":3,"JP":9,"TH":13,"SG":5,"VN":4,"CA":22,"ZA":6,"ID":3,"PH":5,"IN":13,"KR":4,"MY":3}
    decisions = {key(x["candidateFile"],x["candidateTitle"]):x for x in d["reviewDecisions"]}
    evidence = {key(x["researchFile"],x["title"]):x for x in e["records"]}
    assert len(decisions)==20 and len(evidence)==121
    extra = {key(r["candidateFile"], r["candidateTitle"]):r for r in x["records"]}
    assert x["reviewedCount"] == len(extra) == 7
    assert not (set(extra) & set(decisions))
    assert all(x["decision"] in {"SAME_EXISTING_OBSERVANCE","DIFFERENT_FROM_FLAGGED_MATCH"} for x in decisions.values())
    assert len([x for x in decisions.values() if x["decision"]=="SAME_EXISTING_OBSERVANCE"]) == 17
    assert len([x for x in decisions.values() if x["decision"]=="DIFFERENT_FROM_FLAGGED_MATCH"]) == 3

    pr65 = {
      ("wave05_four_official_candidates_20261109.json","World Day of Romani Language"),
      ("wave05_four_official_candidates_20261109.json","International Day against Illicit Trafficking in Cultural Property"),
      ("wave05_four_official_candidates_20261109.json","International Day of Islamic Art"),
      ("wave06_japan_philippines_india_2026.json","Coming of Age Day"),
      ("wave06_japan_philippines_india_2026.json","Emperor's Birthday"),
      ("wave06_japan_philippines_india_2026.json","Showa Day"),
      ("wave06_japan_philippines_india_2026.json","Greenery Day"),
      ("wave06_japan_philippines_india_2026.json","Children\'s Day (Japan)"),
      ("wave06_japan_philippines_india_2026.json","Marine Day (Japan)"),
      ("wave06_japan_philippines_india_2026.json","Mountain Day (Japan)"),
      ("wave06_japan_philippines_india_2026.json","Respect for the Aged Day"),
      ("wave06_japan_philippines_india_2026.json","Sports Day (Japan)"),
      ("wave06_japan_philippines_india_2026.json","Labor Thanksgiving Day (Japan)"),
      ("wave06_japan_philippines_india_2026.json","Republic Day (India)"),
      ("wave06_japan_philippines_india_2026.json","Independence Day (India)"),
      ("wave06_japan_philippines_india_2026.json","Gandhi Jayanti"),
    }
    assert len(pr65)==16
    duplicate_decisions = {k for k,v in decisions.items() if v["decision"] == "SAME_EXISTING_OBSERVANCE"}
    assert not (pr65 & duplicate_decisions)
    # UNESCO Islamic Art and Japan Children's Day can appear in the 20
    # similarity flags as DISTINCT events, without becoming a duplicate.
    assert not (pr65 & set(evidence))
    assert not (set(evidence) & duplicate_decisions)
    # Date verification may overlap a dismissed similarity alert (e.g.
    # Japanese Children\'s Day versus UN World Children\'s Day).
    source_rows={key(x["researchFile"],x["title"]):x for x in a["candidateResults"]}
    assert len(source_rows)==153
    assert set(decisions)<=set(source_rows)
    assert set(evidence)<=set(source_rows)
    assert pr65<=set(source_rows)
    assert set(extra)<=set(source_rows)
    assert set(extra)<=set(evidence)
    rows=[]
    for idx,r in enumerate(a["candidateResults"]):
        k=key(r["researchFile"],r["title"])
        if (k in decisions and decisions[k]["decision"]=="SAME_EXISTING_OBSERVANCE") or k in extra:
            status="ALREADY_IN_MAIN_456"
            note="Existing source-backed canonical observance; do not admit another ID."
        elif k in pr65:
            status="IN_UNMERGED_CONTENT_PR_67"
            note="Sixteen source-build tested IDs consolidated in PR #67 to main, but unmerged; human editorial approval outstanding."
        elif k in evidence:
            status="PRIMARY_CALENDAR_2026_DATE_CONFIRMED"
            note="2026 occurrence/source certified only; annual recurrence, semantic uniqueness and six-locale editorial blocked."
        else:
            status="PENDING_PRIMARY_SOURCE_IDENTITY_AND_RECURRENCE"
            note="Neither distinct identity nor full annual source chronology has been certified."
        ov=evidence.get(k)
        if ov is not None:
            assert ov["country"]==r["country"],(k,"country mismatch")
            if ov["title"] == "South Africa Family Day":
                assert r["occurrence2026"] is None, ("expected computed Easter holiday", k)
                assert ov["occurrence2026"] == "2026-04-06"
                assert ov["annualRecurrenceCertified"] is True
            else:
                assert ov["occurrence2026"] == r["occurrence2026"],(k,"date mismatch")
                assert ov["annualRecurrenceCertified"] is False
            assert ov["semanticUniquenessCertified"] is False
            assert ov["localizationCertified"] is False
            assert ov["runtimeAdmission"]=="BLOCKED"
            assert urlsplit(ov["officialCalendarUrl"]).scheme=="https"
            date.fromisoformat(ov["occurrence2026"])
        rows.append({
            "index":idx,
            "researchFile":r["researchFile"],
            "title":r["title"],
            "country":r["country"],
            "2026Date":r["occurrence2026"],
            "status":status,
            "existingCanonicalId":(decisions.get(k) or extra.get(k))["existingId"] if status=="ALREADY_IN_MAIN_456" else None,
            "sourceEvidence":ov["officialCalendarUrl"] if ov else None,
            "sourceNote":ov["notes"] if ov else note,
            "annualRecurrenceCert":bool(ov and ov["annualRecurrenceCertified"]),
            "sixLocaleEditorialCert":False,
            "runtimeAdded":False
        })
    counts=Counter(r["status"] for r in rows)
    assert counts=={
      "ALREADY_IN_MAIN_456":24,
      "IN_UNMERGED_CONTENT_PR_67":16,
      "PRIMARY_CALENDAR_2026_DATE_CONFIRMED":104,
      "PENDING_PRIMARY_SOURCE_IDENTITY_AND_RECURRENCE":9,
    },counts
    assert sum(counts.values())==153
    assert sum(r["runtimeAdded"] for r in rows)==0
    report={
      "schemaVersion":1,"auditBaseMainCount":456,"targetCatalog":1000,
      "remainingToTargetBeforePR65":544,
      "catalogAfterPR65IfMerged":462,
      "catalogAfterConsolidatedPR67IfMerged":472,
      "remainingAfterPR65IfMerged":538,
      "remainingAfterConsolidatedPR67IfMerged":528,
      "researchRecords":len(rows),
      "statuses":dict(sorted(counts.items())),
      "notYetVerifiedUnique":len(rows)-counts["ALREADY_IN_MAIN_456"],
      "primaryDateEvidenceTotalIncludingCanonicalDuplicates":len(evidence),
      "publicationGate":"BLOCKED_PENDING_SOURCE_AND_HUMAN_EDITORIAL_APPROVAL",
      "disclaimer":"2026 verified occurrence != multi-year annual identity; PR65 not in main; all other research remains blocked.",
      "records":rows
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("RESEARCH COVERAGE PASS",json.dumps({k:v for k,v in report.items() if k!="records"},ensure_ascii=False))

if __name__=="__main__":
    main()
