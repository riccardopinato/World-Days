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
assert matrix["counts"]["sixLocaleDrafts"]==88
assert matrix["counts"]["bilingualDrafts"]==0
assert matrix["counts"]["withoutOriginDraft"]==92
assert matrix["counts"]["governmentCategorySpotChecks"]==49
assert matrix["counts"]["humanCertified"]==0

new_files=[
"ph_national_law_02_six_locales_20261114.json",
"ph_edsa_heritage_six_locales_20261114.json",
"kr_hangeul_constitution_six_locales_20261114.json",
"kr_liberation_foundation_memorial_six_locales_20261114.json",
"ph_rizal_day_and_month_six_locales_20261114.json",
"kr_1960_movements_three_six_locales_20261114.json",
"kr_gwangju_donghak_two_six_locales_20261114.json",
"kr_june10_two_histories_six_locales_20261114.json",
"kr_provisional_jeju_two_six_locales_20261114.json",
"kr_war_martyrs_two_six_locales_20261114.json",
"kr_rail_cyber_two_six_locales_20261114.json",
"kr_reserve_disability_two_six_locales_20261114.json",
"kr_students_law_two_six_locales_20261114.json",
"kr_contemporary_5_six_locales_20261114.json",
"kr_economy_6_six_locales_20261114.json",
"kr_social_6_six_locales_20261114.json",
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

assert set(verified)==set(matrix["originNewDraftIds"]) and len(verified)==45
assert len({r["id"] for r in rows if r["originDraftPR"]==120})==47  # 45 new + 2 prior pilots

# Explicit source-to-record correspondence for the seventeen newly authored Korean days.
new_sprint_names=[
"kr_contemporary_5_six_locales_20261114.json",
"kr_economy_6_six_locales_20261114.json",
"kr_social_6_six_locales_20261114.json",
]
new_sprint_ids=set()
for name in new_sprint_names:
    b=json.loads((RESEARCH/name).read_text(encoding="utf-8"))
    assert b["status"].endswith("PENDING_QUALIFIED_HUMAN_REVIEW")
    for rec in b["records"]:
        rid=rec["observanceId"]
        assert rid not in new_sprint_ids
        new_sprint_ids.add(rid)
        row=next(x for x in rows if x["id"]==rid)
        assert row["country"]=="KR" and row["originDraftPR"]==120
        assert row["governmentCategory"]=="KR_STATUTORY_COMMEMORATIVE_DAY_"+str(rec["introducedYear"])
        raw=market_by_id[rid] if "market_by_id" in globals() else None
        if raw is None:
            source=json.loads((ROOT/"data/market/wave10_hundred_kr_ph_20261111.json").read_text(encoding="utf-8"))
            raw=next(v for v in source["records"] if v["id"]==rid)
        rules=raw["recurrenceRules"]
        assert len(rules)==1
        rule=rules[0]
        if rule["kind"]=="FIXED_DATE":
            expected=f'{rule["month"]:02d}-{rule["day"]:02d}'
        else:
            assert rule["kind"]=="NTH_WEEKDAY"
            weekdays={1:"MONDAY",2:"TUESDAY",3:"WEDNESDAY",4:"THURSDAY",5:"FRIDAY",6:"SATURDAY",7:"SUNDAY"}
            ordinals={1:"FIRST",2:"SECOND",3:"THIRD",4:"FOURTH",5:"FIFTH"}
            months=["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]
            expected=f'{ordinals[rule["occurrence"]]}_{weekdays[rule["weekday"]]}_{months[rule["month"]-1]}'
        assert rec["observanceDate"]==expected,(rid,expected,rec["observanceDate"])
        if rec["firstObservedYear"] is not None:
            assert rec["firstObservedYear"]<=rec["introducedYear"]
assert len(new_sprint_ids)==17
assert new_sprint_ids.issubset(set(verified))
assert verified["kr-w10-king-sejong-birthday-commemoration"]["introducedYear"]==2024
assert verified["kr-w10-teachers-day-in-korea"]["introducedYear"]==1982
assert verified["kr-w10-king-sejong-birthday-commemoration"]["originClusterId"]==verified["kr-w10-teachers-day-in-korea"]["originClusterId"]
assert verified["kr-w10-culture-day-in-korea"]["observanceDate"]=="THIRD_SATURDAY_OCTOBER"
assert verified["kr-w10-commerce-and-industry-day"]["observanceDate"]=="THIRD_WEDNESDAY_MARCH"
assert verified["kr-w10-fallen-military-service-members-remembrance-day"]["observanceDate"]=="FOURTH_FRIDAY_APRIL"


# Protect the cross-origin non-duplication decisions and recurrence patterns for 12 new KR records.
assert verified["kr-w10-june-10-democracy-movement-remembrance"]["introducedYear"]==2007
assert verified["kr-w10-june-10-independence-movement-remembrance"]["introducedYear"]==2020
assert verified["kr-w10-june-10-democracy-movement-remembrance"]["originClusterId"]==verified["kr-w10-june-10-independence-movement-remembrance"]["originClusterId"]
assert verified["kr-w10-june-10-democracy-movement-remembrance"]["observanceDate"]=="06-10"
assert verified["kr-w10-june-10-independence-movement-remembrance"]["observanceDate"]=="06-10"
assert verified["kr-w10-provisional-government-establishment-day"]["observanceDate"]=="04-11"
assert verified["kr-w10-provisional-government-establishment-day"]["introducedYear"]==1989
assert verified["kr-w10-railway-day-in-korea"]["observanceDate"]=="06-28"
assert verified["kr-w10-railway-day-in-korea"]["introducedYear"]==1964
assert verified["kr-w10-information-security-day-in-korea"]["observanceDate"]=="SECOND_WEDNESDAY_JULY"
assert verified["kr-w10-reserve-forces-day"]["observanceDate"]=="FIRST_FRIDAY_APRIL"
assert verified["kr-w10-day-of-persons-with-disabilities-in-korea"]["observanceDate"]=="04-20"
assert verified["kr-w10-student-independence-movement-remembrance-day"]["observanceDate"]=="11-03"
assert verified["kr-w10-law-day-in-korea"]["observanceDate"]=="04-25"
assert verified["kr-w10-jeju-april-3-victims-remembrance-day"]["introducedYear"]==2014

# The 12 new official Korean commemorations must agree with the original market source
# on both the specific canonical ID and its fixed or relative yearly recurrence.
origin_market=json.loads((ROOT/"data/market/wave10_hundred_kr_ph_20261111.json").read_text(encoding="utf-8"))
market_by_id={record["id"]:record for record in origin_market["records"]}
new_kr_names=[
"kr_june10_two_histories_six_locales_20261114.json",
"kr_provisional_jeju_two_six_locales_20261114.json",
"kr_war_martyrs_two_six_locales_20261114.json",
"kr_rail_cyber_two_six_locales_20261114.json",
"kr_reserve_disability_two_six_locales_20261114.json",
"kr_students_law_two_six_locales_20261114.json",
]
new_kr_ids=set()
for filename in new_kr_names:
    b=json.loads((RESEARCH/filename).read_text(encoding="utf-8"))
    for rec in b["records"]:
        ident=rec["observanceId"]
        assert ident not in new_kr_ids,ident
        new_kr_ids.add(ident)
        assert ident in market_by_id
        raw=market_by_id[ident]
        assert raw["country"]=="KR" and len(raw["recurrenceRules"])==1
        rule=raw["recurrenceRules"][0]
        if rule["kind"]=="FIXED_DATE":
            expected_date=f'{rule["month"]:02d}-{rule["day"]:02d}'
        elif rule["kind"]=="NTH_WEEKDAY":
            assert rule["month"] in (4,7) and rule["weekday"] in (3,5) and rule["occurrence"] in (1,2)
            wd={3:"WEDNESDAY",5:"FRIDAY"}[rule["weekday"]]
            occ={1:"FIRST",2:"SECOND"}[rule["occurrence"]]
            expected_date=f'{occ}_{wd}_{["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"][rule["month"]-1]}'
        else:
            raise AssertionError(f"Unexpected recurrence for {ident}: {rule}")
        assert rec["observanceDate"]==expected_date,(ident,expected_date,rec["observanceDate"])
        assert rec["firstObservedYear"] is None
assert len(new_kr_ids)==12
assert new_kr_ids.issubset(set(verified))

assert all(verified[ident]["country"]=="KR" and verified[ident]["firstObservedYear"] is None for ident in (
    "kr-w10-june-10-democracy-movement-remembrance",
    "kr-w10-june-10-independence-movement-remembrance",
    "kr-w10-provisional-government-establishment-day",
    "kr-w10-jeju-april-3-victims-remembrance-day",
    "kr-w10-korean-war-remembrance-day",
    "kr-w10-patriotic-martyrs-remembrance-day",
    "kr-w10-railway-day-in-korea",
    "kr-w10-information-security-day-in-korea",
    "kr-w10-reserve-forces-day",
    "kr-w10-day-of-persons-with-disabilities-in-korea",
    "kr-w10-student-independence-movement-remembrance-day",
    "kr-w10-law-day-in-korea",
))


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

print("PASS: 180-ID matrix, 45 new six-locale originals, 9 four-locale extensions (88 effective six-locale AI drafts); source errata gated; 0 qualified human approvals.")

