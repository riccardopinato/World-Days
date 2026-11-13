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
assert matrix["counts"]["sixLocaleDrafts"]==54
assert matrix["counts"]["bilingualDrafts"]==0
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

# Nine earlier Wave20 EN/IT canonical origins are extended, never replaced or duplicated.
extensions=[
"wave20_ph_kr_kr1_es_fr_de_pt_20261114.json",
"wave20_ph_kr_kr2_es_fr_de_pt_20261114.json",
"wave20_ph_kr_remaining_es_fr_de_pt_20261114.json",
]
extension_ids=set()
for filename in extensions:
    ext_path=ROOT/"data/editorial/locale_extensions"/filename
    batch=json.loads(ext_path.read_text(encoding="utf-8"))
    assert batch["schemaVersion"]==1
    assert "DRAFT" in batch["status"]
    assert batch["baseRef"]=="editorial/wave20-six-locales-20261113@477557ee6a6115e2479c2009c6daecde5a590026"
    assert batch["addedLocales"]==["es","fr","de","pt"]
    assert len(batch["records"])==3
    for record in batch["records"]:
        rid=record["observanceId"]
        assert rid not in extension_ids,rid
        extension_ids.add(rid)
        assert record["humanApproved"] is False
        row=next(row for row in rows if row["id"]==rid)
        assert row["originDraftPR"]==118
        assert row["originDraftPath"]==batch["basePath"]
        assert row["baseLocaleCoverage"]==["en","it"]
        assert row["localeExtensionCoverage"]==batch["addedLocales"]
        assert row["localeExtensionPR"]==120
        assert row["localeExtensionPath"]=="data/editorial/locale_extensions/"+filename
        assert row["originLayeringStatus"]=="ONE_CANONICAL_ORIGIN_WITH_ADDITIONAL_TRANSLATION_LAYER"
        assert row["localeCoverage"]==["en","it","es","fr","de","pt"]
        assert list(record["locale"])==batch["addedLocales"]
        for lang,story in record["locale"].items():
            assert set(story)=={"heading","origin","promoter","purpose","facts"}
            assert len(story["heading"])>=15
            assert len(story["origin"])>=300,(rid,lang,len(story["origin"]))
            assert len(story["promoter"])>=65,(rid,lang)
            assert len(story["purpose"])>=60,(rid,lang)
            assert len(story["facts"])==3,(rid,lang)
            assert all(len(fact)>=30 for fact in story["facts"]),(rid,lang)
assert set(matrix["newTranslationIds"])==extension_ids and len(extension_ids)==9
assert matrix["counts"]["translationExtensions"]==9
assert sum(1 for row in rows if row["originDraftPR"]==118 and row.get("localeExtensionPR")==120)==9
assert all(row["qualifiedEditorialApproval"] is False for row in rows)

errata=json.loads((AUDIT/"ph_kr_wave20_source_errata_20261114.json").read_text(encoding="utf-8"))
assert errata["status"]=="OPEN_CANONICAL_EN_IT_CORRECTION_REQUIRED"
assert errata["qualifiedHumanApproval"] is False
assert {x["id"] for x in errata["items"]}=={"ph-day-of-valor","ph-bonifacio-day"}
for issue in errata["items"]:
    assert len(issue["sources"])>=2
    assert all(urlparse(url).scheme=="https" for url in issue["sources"])
    assert issue["published"] is False
assert next(row for row in rows if row["id"]=="ph-day-of-valor")["factualCorrectionRequired"] is True

print("PASS: 180-ID matrix, 11 new six-locale originals, 9 four-locale extensions (54 effective six-locale AI drafts); source errata gated; 0 qualified human approvals.")

