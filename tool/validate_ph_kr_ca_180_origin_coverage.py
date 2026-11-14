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
assert matrix["counts"]["sixLocaleDrafts"]==168
assert matrix["counts"]["bilingualDrafts"]==0
assert matrix["counts"]["withoutOriginDraft"]==12
assert matrix["counts"]["governmentCategorySpotChecks"]==129
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
"kr_institutions_5_six_locales_20261114.json",
"kr_memory_society_5_six_locales_20261114.json",
"ph_months_heritage_rights_6_six_locales_20261114.json",
"ph_months_language_society_6_six_locales_20261114.json",
"ph_statutory_civic_4_six_locales_20261114.json",
"ph_book_health_protection_4_six_locales_20261114.json",
"ph_books_culture_ecology_5_six_locales_20261114.json",
"ph_civic_holidays_8_six_locales_20261114.json",
"ph_civic_months_6_six_locales_20261114.json",
"ph_seafarer_coconut_republic_balagtas_4_six_locales_20261114.json",
"ph_heroes_awards_5_six_locales_20261114.json",
"ph_local_heritage_honors_4_six_locales_20261114.json",
"ph_institutions_military_legislature_5_six_locales_20261114.json",
"ph_heritage_friendship_archives_5_six_locales_20261114.json",
"ph_language_fisherfolk_magsaysay_independence_4_six_locales_20261114.json",
"ph_civic_environment_movable_4_six_locales_20261114.json",
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

assert set(verified)==set(matrix["originNewDraftIds"]) and len(verified)==125
assert len({r["id"] for r in rows if r["originDraftPR"]==120})==127  # 125 new + 2 prior pilots

# Twenty source-verified Philippine legal/monthly origins, checked against the
# original national NCCA calendar instead of silently freezing movable or ranged dates.
ph_waves=[
"ph_months_heritage_rights_6_six_locales_20261114.json",
"ph_months_language_society_6_six_locales_20261114.json",
"ph_statutory_civic_4_six_locales_20261114.json",
"ph_book_health_protection_4_six_locales_20261114.json",
"ph_books_culture_ecology_5_six_locales_20261114.json",
"ph_civic_holidays_8_six_locales_20261114.json",
"ph_civic_months_6_six_locales_20261114.json",
"ph_seafarer_coconut_republic_balagtas_4_six_locales_20261114.json",
"ph_heroes_awards_5_six_locales_20261114.json",
"ph_local_heritage_honors_4_six_locales_20261114.json",
"ph_institutions_military_legislature_5_six_locales_20261114.json",
"ph_heritage_friendship_archives_5_six_locales_20261114.json",
"ph_language_fisherfolk_magsaysay_independence_4_six_locales_20261114.json",
"ph_civic_environment_movable_4_six_locales_20261114.json",
]
ph_market_files=[
ROOT/"data/market/wave13_ncca_eures_100_20261111.json",
ROOT/"data/market/wave10_hundred_kr_ph_20261111.json",
]
ph_source={}
for source_path in ph_market_files:
    for entry in json.loads(source_path.read_text(encoding="utf-8"))["records"]:
        if entry["country"]=="PH":
            assert entry["id"] not in ph_source,entry["id"]
            ph_source[entry["id"]]=entry
ph_new=set()
months=("JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER")
for filename in ph_waves:
    batch=json.loads((RESEARCH/filename).read_text(encoding="utf-8"))
    assert "DRAFT" in batch["status"] and "HUMAN" in batch["status"]
    assert batch["count"] in (4,5,6,8)
    for rec in batch["records"]:
        rid=rec["observanceId"]
        assert rid in ph_source and rid not in ph_new,rid
        ph_new.add(rid)
        src=ph_source[rid]
        assert src["country"]==rec["country"]=="PH"
        assert len(src["recurrenceRules"])==1
        rule=src["recurrenceRules"][0]
        if rule["kind"]=="FIXED_DATE":
            expected=f'{rule["month"]:02d}-{rule["day"]:02d}'
            assert rec["observancePeriodKind"]=="DAY"
        elif rule["kind"]=="NTH_WEEKDAY":
            weekday_names={1:"MONDAY",2:"TUESDAY",3:"WEDNESDAY",4:"THURSDAY",5:"FRIDAY",6:"SATURDAY",7:"SUNDAY"}
            occurrences={1:"FIRST",2:"SECOND",3:"THIRD",4:"FOURTH",5:"FIFTH"}
            assert rule["weekday"] in weekday_names and rule["occurrence"] in occurrences
            expected=f'{occurrences[rule["occurrence"]]}_{weekday_names[rule["weekday"]]}_{months[rule["month"]-1]}'
            assert rec["observancePeriodKind"]=="DAY"
        else:
            assert rule["kind"]=="FIXED_RANGE"
            start=months[rule["startMonth"]-1]
            end=months[rule["endMonth"]-1]
            if rule["startMonth"]==rule["endMonth"] and rule["startDay"]==1 and rule["endDay"] in (28,29,30,31):
                expected=start
                assert rec["observancePeriodKind"]=="MONTH"
            else:
                expected=f'{start[:3]}{rule["startDay"]:02d}_{end[:3]}{rule["endDay"]:02d}'
                assert rec["observancePeriodKind"] in ("WEEK","CAMPAIGN_18_DAYS")
        assert rec["observanceDate"]==expected,(rid,expected,rec["observanceDate"])
        assert isinstance(rec["introducedYear"],int)
        assert rec["firstObservedYear"] is None or rec["firstObservedYear"]<=rec["introducedYear"]
        assert rec["legalStatus"] and len(rec["sources"])>=2
        row=next(item for item in rows if item["id"]==rid)
        assert row["originDraftPath"]=="data/editorial/research_batches/"+filename
        assert row["originDraftPR"]==120 and row["qualifiedEditorialApproval"] is False
assert len(ph_new)==70
assert ph_new.issubset(set(verified))
assert verified["ph-w13-national-children-s-month-philippines"]["observanceDate"]=="NOVEMBER"
assert verified["ph-w13-national-children-s-month-philippines"]["introducedYear"]==2015
assert verified["ph-w13-national-children-s-month-philippines"]["firstObservedYear"]==1993
assert verified["ph-w13-national-indigenous-peoples-month-philippines"]["introducedYear"]==2009
assert verified["ph-w10-philippines-indigenous-peoples-thanksgiving-day"]["introducedYear"]==2003
assert verified["ph-w13-national-indigenous-peoples-month-philippines"]["originClusterId"]==verified["ph-w10-philippines-indigenous-peoples-thanksgiving-day"]["originClusterId"]
assert verified["ph-w10-philippine-national-women-s-day"]["legalStatus"]=="SPECIAL_WORKING_HOLIDAY_NOT_NONWORKING"
assert verified["ph-w13-18-day-campaign-to-end-violence-against-women-philippines"]["observancePeriodKind"]=="CAMPAIGN_18_DAYS"
assert verified["ph-w13-national-book-week-philippines"]["observanceDate"]=="NOV24_NOV30"

assert matrix["counts"]["byCountry"]["PH"]["six"]==79
assert matrix["counts"]["byCountry"]["PH"]["none"]==12
assert verified["ph-w13-philippine-book-development-month"]["introducedYear"]==1999
assert verified["ph-w13-philippine-book-development-month"]["firstObservedYear"]==1997
assert verified["ph-w13-philippine-book-development-month"]["observanceDate"]=="NOVEMBER"
assert verified["ph-w13-conservation-and-protection-of-the-tamaraw-month"]["introducedYear"]==2002
assert verified["ph-w13-national-culture-consciousness-week"]["observanceDate"]=="JUL01_JUL07"

# Enforce the three original PH-only legal-history source batches in this sprint.
sprint_ph_ids=set()
for filename,number in (
    ("ph_civic_holidays_8_six_locales_20261114.json",8),
    ("ph_civic_months_6_six_locales_20261114.json",6),
    ("ph_seafarer_coconut_republic_balagtas_4_six_locales_20261114.json",4),
):
    b=json.loads((RESEARCH/filename).read_text(encoding="utf-8"))
    assert b["count"]==len(b["records"])==number
    for record in b["records"]:
        assert record["observanceId"] not in sprint_ph_ids
        sprint_ph_ids.add(record["observanceId"])
        assert record["country"]=="PH"
        assert len(record["locale"])==6
assert len(sprint_ph_ids)==18
assert sprint_ph_ids.issubset(ph_new)
assert matrix["counts"]["byCountry"]["KR"]["six"]==57
assert matrix["counts"]["byCountry"]["CA"]["six"]==32
assert verified["ph-w10-araw-ng-pagbasa-philippines-national-reading-day"]["introducedYear"]==2013
assert verified["ph-w10-araw-ng-pagbasa-philippines-national-reading-day"]["legalStatus"]=="PH_REGULAR_WORKING_HOLIDAY_WEEKEND_OBSERVED_PRECEDING_FRIDAY"
assert verified["ph-w10-araw-ng-republikang-filipino-first-philippine-republic-anniversary"]["introducedYear"]==2013
assert verified["ph-w10-araw-ng-republikang-filipino-first-philippine-republic-anniversary"]["legalStatus"]=="PH_NATIONAL_SPECIAL_WORKING_HOLIDAY_RA11014_2018"
assert verified["ph-w10-philippine-spanish-friendship-day"]["legalStatus"]=="PH_SPECIAL_WORKING_NATIONWIDE_NONWORKING_AURORA_PROVINCE_RA9187"
assert verified["ph-w10-philippines-national-teachers-day"]["introducedYear"]==2016
assert verified["ph-w10-philippines-national-indigenous-peoples-day"]["introducedYear"]==2015
assert verified["ph-w10-philippine-flag-days-commencement"]["introducedYear"]==1965
assert verified["ph-w10-philippines-national-literacy-day"]["introducedYear"]==1969
assert verified["ph-w10-philippine-republic-day-july-4"]["legalStatus"]=="PH_HISTORICAL_REPUBLIC_DAY_1964_LAW_NOT_IN_1987_REGULAR_HOLIDAY_LIST"
assert verified["ph-w13-national-volunteers-month-philippines"]["introducedYear"]==1998
assert verified["ph-w13-national-volunteers-month-philippines"]["observanceDate"]=="DECEMBER"
assert verified["ph-w13-national-coconut-week-philippines"]["observanceDate"]=="AUG24_AUG30"
assert verified["ph-w13-philippine-tropical-fabrics-month"]["introducedYear"]==2012

# The nine hero/award/animal-care IDs are distinct canonical events, including
# two state honors that share the same decree/date but not the same award criteria.
new_heritage_files={
    "ph_heroes_awards_5_six_locales_20261114.json":5,
    "ph_local_heritage_honors_4_six_locales_20261114.json":4,
}
new_heritage_ids=set()
for name,expected_n in new_heritage_files.items():
    source=json.loads((RESEARCH/name).read_text(encoding="utf-8"))
    assert source["count"]==len(source["records"])==expected_n
    for item in source["records"]:
        ident=item["observanceId"]
        assert ident in ph_new and ident not in new_heritage_ids
        new_heritage_ids.add(ident)
        assert next(x for x in rows if x["id"]==ident)["originDraftPath"]=="data/editorial/research_batches/"+name
assert len(new_heritage_ids)==9

# New institution, heritage and civic-history originals belong to the PH-only
# canonical inventory and preserve individually distinct event origin IDs.
ph_institutional_sprint={
    "ph_institutions_military_legislature_5_six_locales_20261114.json":5,
    "ph_heritage_friendship_archives_5_six_locales_20261114.json":5,
    "ph_language_fisherfolk_magsaysay_independence_4_six_locales_20261114.json":4,
}
sprint_ph_ids=set()
for filename,expected_count in ph_institutional_sprint.items():
    batch=json.loads((RESEARCH/filename).read_text(encoding="utf-8"))
    assert batch["count"]==len(batch["records"])==expected_count
    for item in batch["records"]:
        rid=item["observanceId"]
        assert rid not in sprint_ph_ids and rid in ph_new
        sprint_ph_ids.add(rid)
        assert next(r for r in rows if r["id"]==rid)["originDraftPath"]=="data/editorial/research_batches/"+filename
assert len(sprint_ph_ids)==14
assert verified["ph-w10-philippine-army-founding-anniversary"]["observanceDate"]=="03-22"
assert verified["ph-w10-philippine-army-founding-anniversary"]["introducedYear"]==1897
assert verified["ph-w10-philippine-senate-founding-anniversary"]["originClusterId"]==verified["ph-w10-philippine-house-of-representatives-founding-anniversary"]["originClusterId"]
assert verified["ph-w10-philippine-senate-founding-anniversary"]["locale"]["en"]["origin"]!=verified["ph-w10-philippine-house-of-representatives-founding-anniversary"]["locale"]["en"]["origin"]
assert verified["ph-w10-philippine-film-development-council-founding-anniversary"]["introducedYear"]==2002
assert verified["ph-w10-philippines-national-museum-founding-anniversary"]["introducedYear"]==1901
assert verified["ph-w10-national-library-of-the-philippines-founding-anniversary"]["introducedYear"]==1887
assert verified["ph-w10-philippine-military-academy-establishment-anniversary"]["introducedYear"]==1898
assert verified["ph-w10-philippines-national-archives-day"]["introducedYear"]==1995
assert verified["ph-w10-philippines-national-archives-day"]["firstObservedYear"]==1901
assert verified["ph-w10-philippine-british-friendship-day"]["observanceDate"]=="10-20"
assert verified["ph-w10-puerto-princesa-underground-river-day"]["firstObservedYear"]==2011
assert verified["ph-w10-komisyon-sa-wikang-filipino-founding-anniversary"]["introducedYear"]==1991
assert verified["ph-w10-national-fisherfolks-day-philippines"]["introducedYear"]==2000
assert verified["ph-w10-ramon-magsaysay-memorial-day"]["introducedYear"]==1966
assert verified["ph-w13-linggo-ng-kalayaan"]["observanceDate"]=="JUN06_JUN12"

# Two new national movable weekday observances must follow the legal rule,
# not a hardcoded civil date for a particular year.
assert verified["ph-w13-conflict-resolution-day-philippines"]["observanceDate"]=="THIRD_THURSDAY_OCTOBER"
assert verified["ph-w13-unknown-citizens-day"]["observanceDate"]=="SECOND_SUNDAY_JANUARY"
assert verified["ph-w13-conflict-resolution-day-philippines"]["introducedYear"]==2006
assert verified["ph-w13-unknown-citizens-day"]["introducedYear"]==1936
assert verified["ph-w13-world-clean-and-green-week-philippines"]["observanceDate"]=="SEP17_SEP23"
assert verified["ph-w13-w-a-t-c-h-time-consciousness-and-honesty-month"]["observanceDate"]=="JUNE"
assert verified["ph-w13-w-a-t-c-h-time-consciousness-and-honesty-month"]["legalStatus"].endswith("_REQUIRES_INDEPENDENT_CHECK")


assert verified["ph-w10-julian-felipe-day"]["legalStatus"]=="PH_CAVITE_CITY_SPECIAL_NONWORKING_HOLIDAY_RA7805_1994_NOT_NATIONAL"
assert verified["ph-w10-apolinario-mabini-day"]["legalStatus"]=="PH_TANAUAN_SPECIAL_WORKING_HOLIDAY_RA9430_NOT_NATIONWIDE"
assert verified["ph-w10-graciano-lopez-jaena-day"]["legalStatus"]=="PH_NATIONAL_SPECIAL_WORKING_RA9070_2001_LOCAL_EARLIER_ONLY_BY_YEAR"
assert verified["ph-w10-kindness-to-animal-day-philippines"]["introducedYear"]==1958
assert verified["ph-w10-iglesia-ni-cristo-day"]["introducedYear"]==2009
assert verified["ph-w10-jose-abad-santos-day"]["observanceDate"]=="02-19"
assert verified["ph-w10-order-of-gabriela-silang-founding-anniversary"]["originClusterId"]==verified["ph-w10-order-of-lakandula-founding-anniversary"]["originClusterId"]
assert verified["ph-w10-order-of-gabriela-silang-founding-anniversary"]["legalStatus"]==verified["ph-w10-order-of-lakandula-founding-anniversary"]["legalStatus"]
assert verified["ph-w10-order-of-gabriela-silang-founding-anniversary"]["locale"]["en"]["purpose"]!=verified["ph-w10-order-of-lakandula-founding-anniversary"]["locale"]["en"]["purpose"]



# Do not count legally conflicted or unverified historical origin-years as approved.
ph_issues=json.loads((AUDIT/"ph_open_legal_source_conflicts_20261114.json").read_text(encoding="utf-8"))
assert ph_issues["count"]==len(ph_issues["items"])==13
assert ph_issues["qualifiedEditorialApproval"] is False
assert ph_issues["status"]=="OPEN_SOURCE_DISCREPANCIES_DO_NOT_AUTO_CERTIFY"
assert len({item["observanceId"] for item in ph_issues["items"]})==13
for issue in ph_issues["items"]:
    assert issue["resolved"] is False
    row=next(x for x in rows if x["id"]==issue["observanceId"])
    assert row["qualifiedEditorialApproval"] is False
    assert issue["legalSource"].startswith("https://")
    if issue["observanceId"] in {
        "ph-w13-national-punctuality-and-civility-consciousness-month",
        "ph-w13-week-of-the-philippine-eagle",
        "ph-w10-philippine-department-of-education-founding-anniversary",
        "ph-w13-made-in-the-philippines-product-week",
        "ph-w13-volunteerism-month-philippines",
        "ph-w10-philippine-national-historical-commission-founding-anniversary",
    }:
        assert row["originDraftPath"] is None and row["localeCoverage"]==[]
    else:
        assert row["originDraftPR"]==120 and len(row["localeCoverage"])==6

assert {issue["observanceId"] for issue in ph_issues["items"] if issue["observanceId"].startswith("ph-w10-") and issue["problem"] in (
    "NCCA_LEGISLATIVE_YEAR_2012_VS_APPROVED_RA10556_2013",
    "REPUBLIC_DAY_HISTORIC_HOLIDAY_NOT_LISTED_AS_MODERN_REGULAR_HOLIDAY",
)}=={
    "ph-w10-araw-ng-pagbasa-philippines-national-reading-day",
    "ph-w10-philippine-republic-day-july-4",
}




# Verify the last ten KR six-locale dossiers and ensure all 57 retained Korean
# candidates have an actual source-linked origin coverage entry, no hidden misses.
final_kr_batches=[
"kr_institutions_5_six_locales_20261114.json",
"kr_memory_society_5_six_locales_20261114.json",
]
canon_market=json.loads((ROOT/"data/market/wave10_hundred_kr_ph_20261111.json").read_text(encoding="utf-8"))
canon_by_id={entry["id"]:entry for entry in canon_market["records"]}
final_kr_ids=set()
for filename in final_kr_batches:
    batch=json.loads((RESEARCH/filename).read_text(encoding="utf-8"))
    assert len(batch["records"])==5 and batch["count"]==5
    for record in batch["records"]:
        rid=record["observanceId"]
        assert rid not in final_kr_ids
        final_kr_ids.add(rid)
        row=next(x for x in rows if x["id"]==rid)
        assert row["originDraftPR"]==120 and row["originDraftPath"]=="data/editorial/research_batches/"+filename
        assert row["country"]=="KR" and record["country"]=="KR"
        assert row["originClusterId"]==record["originClusterId"]
        assert row["proposedIntroducedYear"]==record["introducedYear"]
        assert row["proposedFirstObservedYear"]==record["firstObservedYear"]
        assert rid in canon_by_id
        rules=canon_by_id[rid]["recurrenceRules"]
        assert len(rules)==1
        rule=rules[0]
        if rule["kind"]=="FIXED_DATE":
            expected=f'{rule["month"]:02d}-{rule["day"]:02d}'
        else:
            assert rule["kind"]=="NTH_WEEKDAY"
            names={1:"MONDAY",2:"TUESDAY",3:"WEDNESDAY",4:"THURSDAY",5:"FRIDAY",6:"SATURDAY",7:"SUNDAY"}
            ranks={1:"FIRST",2:"SECOND",3:"THIRD",4:"FOURTH",5:"FIFTH"}
            months=["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]
            expected=f'{ranks[rule["occurrence"]]}_{names[rule["weekday"]]}_{months[rule["month"]-1]}'
        assert record["observanceDate"]==expected,(rid,record["observanceDate"],expected)
        if record["firstObservedYear"] is not None:
            assert record["firstObservedYear"]<=record["introducedYear"]
assert len(final_kr_ids)==10
assert matrix["counts"]["byCountry"]["KR"]["all"]==57
assert matrix["counts"]["byCountry"]["KR"]["six"]==57
assert matrix["counts"]["byCountry"]["KR"]["none"]==0
assert set(r["id"] for r in rows if r["country"]=="KR" and len(r["localeCoverage"])==6)==set(r["id"] for r in rows if r["country"]=="KR")
assert verified["kr-w10-west-sea-defense-day"]["introducedYear"]==2016
assert verified["kr-w10-west-sea-defense-day"]["firstObservedYear"]==2016
assert verified["kr-w10-sports-day-in-korea"]["introducedYear"]==1969
assert verified["kr-w10-righteous-armies-remembrance-day"]["introducedYear"]==2010


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

print("PASS: 180-ID matrix, 125 new six-locale originals, 9 four-locale extensions (168 effective six-locale AI drafts); KR 57/57, CA 32/32, PH 79/91; 12 pending, 13 source discrepancies gated; 0 qualified human approvals.")

