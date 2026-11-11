#!/usr/bin/env python3
"""Fail-closed checks for the first 100 source-linked story research dossiers."""
import json
from pathlib import Path
from editorial_origin_wave100 import build, LOCALES

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/"reports/editorial_origin_wave100.json"
published=json.loads(path.read_text(encoding="utf-8"))
expected=build()
assert published==expected, "wave100 artifact must be generated from current canonical audit"
assert published["schemaVersion"]==1
assert published["targetCount"]==published["recordCount"]==len(published["dossiers"])==100
assert published["historicallyVerifiedCompletedStories"]==0
assert published["reviewStatus"]=="100_PRIMARY_LINKED_RESEARCH_DOSSIERS_NOT_100_APPROVED_STORIES"
rows=published["dossiers"]
assert len({r["observanceId"] for r in rows})==100
assert [r["sequence"] for r in rows]==list(range(1,101))
for r in rows:
    assert r["storyStatus"]=="RESEARCH_NOT_PUBLISHED"
    assert r["priorEditorialStage"]=="NOT_RESEARCHED", "duplicate existing editorial draft"
    assert r["historicalEvidenceStatus"]=="SOURCE_LINK_PRESENT_INDIVIDUAL_HISTORY_UNVERIFIED"
    assert {"A_PRIMARY","D_ORIGINATOR"} & set(r["catalogSourceTiers"])
    assert r["catalogSourceUrls"] and all(x.startswith("https://") for x in r["catalogSourceUrls"])
    assert set(r["localeStatus"])==set(LOCALES)
    assert all(status=="AWAITING_SOURCE_RESEARCH" for status in r["localeStatus"].values())
    story=r["storyDraft"]
    assert story=={
        "origin":None,
        "formalIntroductionYearConfirmed":None,
        "reasonForCalendarDate":None,
        "individualPromoterOrIssuingAuthority":None,
        "purpose":None,
        "contextualFacts":[]
    }, "never fabricate facts or publish unfinished history"
# Independent regression: pre-existing Wave04 and country Wave01/Wave02
# draft IDs are not allowed to re-enter the new-research worklist.
preexisting=set()
for name in ("wave04_sources_20261109.json", "country_wave01_en_it_20261109.json",
             "country_wave02_en_it_20261109.json"):
    path=ROOT/"data/editorial/candidates"/name
    doc=json.loads(path.read_text(encoding="utf-8"))
    for item in doc.get("records",doc.get("entries",[])):
        preexisting.add(item["id"])
assert preexisting.isdisjoint({r["observanceId"] for r in rows}), "old drafts duplicated in new 100 batch"
print("PASS: 100 unique primary-linked research dossiers, zero falsely approved histories")
