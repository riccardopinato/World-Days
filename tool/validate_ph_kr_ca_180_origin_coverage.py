#!/usr/bin/env python3
"""Enforce source and locale coverage for PH/KR/CA 180 retained IDs.

Machine audit only. This validator must NEVER set human editorial approval.
External draft PR #118/#119 sources are pinned references, not files in this checkout.
"""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"data/editorial/audits"
RESEARCH=ROOT/"data/editorial/research_batches"
matrix=json.loads((AUDIT/"ph_kr_ca_180_origin_coverage_matrix_20261114.json").read_text(encoding="utf-8"))
scope=json.loads((AUDIT/"ph_kr_ca_333_editorial_scope_decisions_20261113.json").read_text(encoding="utf-8"))
assert matrix["schemaVersion"]==1
rows=matrix["records"]
assert len(rows)==matrix["counts"]["all"]==180
assert len({r["id"] for r in rows})==180
expected={r["id"] for r in scope["decisions"] if r["decision"]=="RETAIN_AS_UNCERTIFIED_CANDIDATE"}
assert {r["id"] for r in rows}==expected

tally=Counter()
for row in rows:
    assert row["country"] in {"PH","KR","CA"}
    assert row["factReview"]=="REQUIRES_FULL_INDIVIDUAL_CHRONOLOGY_REVIEW"
    assert row["nativeTranslationReview"] is False
    assert row["qualifiedEditorialApproval"] is False
    assert row["richEditorialPublished"] is False
    assert row["inventorySourceUrl"].startswith("https://")
    assert row["localeCoverage"] in [[],["en","it"],["en","it","es","fr","de","pt"]],row["id"]
    assert len(row["localeCoverage"]) in (0,2,6)
    stage={0:"none",2:"two",6:"six"}[len(row["localeCoverage"])]
    tally[row["country"],stage]+=1
    tally[row["country"],"all"]+=1
    if row["governmentCategory"]!="NOT_INDEPENDENTLY_CROSSCHECKED":
        assert row["governmentSources"]
        for url in row["governmentSources"]:
            u=urlparse(url)
            assert u.scheme=="https" and u.hostname
        tally[row["country"],"categoryCrosschecked"]+=1
    if row["originDraftPath"]:
        assert row["originDraftPR"] in {118,119,120}
        assert row["originDraftBranch"]
        assert row["originSourceUrls"]
        assert row["localeCoverage"]
        assert all(urlparse(url).scheme=="https" for url in row["originSourceUrls"])
    else:
        assert not row["localeCoverage"]
        assert row["originDraftBranch"] is None
        assert row["originDraftPR"] is None

for country,stats in matrix["counts"]["byCountry"].items():
    for key,number in stats.items():
        assert tally[country,key]==number,(country,key,tally[country,key],number)
assert matrix["counts"]["sixLocaleDrafts"]==45
assert matrix["counts"]["bilingualDrafts"]==9
assert matrix["counts"]["withoutOriginDraft"]==126
assert matrix["counts"]["governmentCategorySpotChecks"]==15
assert matrix["counts"]["humanCertified"]==0

new_files=[
"ph_national_law_02_six_locales_20261114.json",
"ph_edsa_heritage_six_locales_20261114.json",
"kr_hangeul_constitution_six_locales_20261114.json",
"kr_liberation_foundation_memorial_six_locales_20261114.json",
"ph_rizal_day_and_month_six_locales_20261114.json",
]
verified={}
for filename in new_files:
    batch=json.loads((RESEARCH/filename).read_text(encoding="utf-8"))
    assert batch["schemaVersion"]==1
    assert "DRAFT" in batch["status"]
    assert "HUMAN" in batch["status"] or "QUALIFIED" in batch["status"]
    assert batch["count"]==len(batch["records"])
    assert batch["locales"]==["en","it","es","fr","de","pt"]
    for record in batch["records"]:
        rid=record["observanceId"]
        assert rid not in verified,rid
        verified[rid]=record
        matched=next(r for r in rows if r["id"]==rid)
        assert matched["originDraftPR"]==120
        assert matched["originDraftPath"]=="data/editorial/research_batches/"+filename
        assert matched["country"]==record["country"]
        assert matched["localeCoverage"]==batch["locales"]
        assert matched["originSourceUrls"]==record["sources"]
        assert len(record["sources"])>=2
        assert "human" in record["sourceReviewNote"].lower()
        assert len(record["locale"])==6
        for loc in batch["locales"]:
            story=record["locale"][loc]
            assert set(story)=={"heading","origin","promoter","purpose","facts"}
            assert len(story["heading"])>=15
            assert len(story["origin"])>=300,(rid,loc,len(story["origin"]))
            assert len(story["promoter"])>=50,(rid,loc)
            assert len(story["purpose"])>=50,(rid,loc)
            assert len(story["facts"])==3
            assert all(len(s)>=30 for s in story["facts"])

assert set(verified)==set(matrix["originNewDraftIds"]) and len(verified)==11
assert len({r["id"] for r in rows if r["originDraftPR"]==120})==13  # 11 new + 2 prior pilots
print("PASS: 180-ID source coverage; CA 32 six-locale drafts, KR 6, PH 7; 11 new source-linked six-locale drafts validated; human-approved 0.")
