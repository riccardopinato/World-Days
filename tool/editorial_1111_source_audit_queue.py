#!/usr/bin/env python3
"""Evidence-gated research plan for EVERY canonical World Days identity.

This does not compose unsourced history or certify a foreign country's law.
Existing reviewed copy stays reviewed; country/index entries stay source-level
until their *individual* origin/date/promoter and jurisdiction are checked.
"""
import argparse
import json
from collections import Counter
from pathlib import Path
from editorial_gap_manifest import build as base_manifest

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"assets/data/official_core.json"
EDITORIAL=ROOT/"assets/data/editorial_en.json"
IRISH=ROOT/"data/editorial/candidates/irish_brigid_two_stories_primary_20261111.json"
OUT=ROOT/"reports/editorial_1111_source_audit_queue.json"

def source_quality(record):
    urls=[x.get("url","") for x in record["sources"]]
    tiers={x.get("tier","") for x in record["sources"]}
    if any("eures.europa.eu" in u for u in urls):
        return "EU_INDEX_REQUIRES_COUNTRY_PRIMARY_LAW_OR_ORIGINATOR"
    if any("protocol.dfat.gov.au" in u for u in urls):
        return "AUSTRALIAN_DIPLOMATIC_CALENDAR_NOT_FOREIGN_STATUTORY_HOLIDAY"
    if any("ncca.gov.ph" in u for u in urls):
        return "PHILIPPINE_CULTURAL_INDEX_NOT_STATUTORY_HOLIDAY"
    if "C_DISCOVERY" in tiers and not ({"A_PRIMARY","D_ORIGINATOR"} & tiers):
        return "DISCOVERY_ONLY_NOT_VERIFIED"
    return "CANONICAL_LINK_PRESENT_INDIVIDUAL_STORY_STILL_TO_REVIEW"

def build():
    base=base_manifest()
    catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
    editorial=json.loads(EDITORIAL.read_text(encoding="utf-8"))
    research=json.loads(IRISH.read_text(encoding="utf-8"))
    records={x["id"]:x for x in catalog["records"]}
    reviewed={x["observanceId"]:x for x in editorial["entries"]}
    candidate={x["id"]:x for x in research["records"]}
    assert research["count"]==len(candidate)==2
    assert not (set(candidate)&set(reviewed)), "do not stage already reviewed stories"
    assert set(candidate)<=set(records), "story candidate absent catalog"
    assert len(records)==len(base["items"])==1111
    result=[]
    for row in base["items"]:
        oid=row["id"]; record=records[oid]; rich=reviewed.get(oid)
        draft=candidate.get(oid)
        stage=("SOURCE_RESEARCHED_STORY_DRAFT_PENDING_REVIEW" if draft else row["editorialStage"])
        quality=source_quality(record)
        source_urls=[x["url"] for x in record["sources"] if x.get("url")]
        assert source_urls,oid
        origin=(rich or {}).get("origin","").strip() or None
        why=(rich or {}).get("whyItMatters","").strip() or None
        date_reason=(rich or {}).get("whyThisDate","").strip() or None
        facts=[x.strip() for x in (rich or {}).get("quickFacts",[]) if x.strip()]
        promoter=None # Canonical authority is NOT automatically historical proposer.
        missing=[]
        if origin is None:missing.append("ORIGIN_HISTORY")
        if why is None:missing.append("WHY_OBSERVED")
        if date_reason is None:missing.append("WHY_THIS_DATE")
        if promoter is None:missing.append("FOUNDER_OR_PROPOSER_IF_KNOWN")
        if not facts:missing.append("FACTS_AND_TRADITIONS")
        if record.get("introducedYear") is None:missing.append("FOUNDING_YEAR_IF_PRIMARY_PROVEN")
        if stage!="RUNTIME_REVIEWED":missing.append("INDIVIDUAL_HUMAN_EDITORIAL_QA")
        if quality!="CANONICAL_LINK_PRESENT_INDIVIDUAL_STORY_STILL_TO_REVIEW":
            missing.append("SOURCE_CLASSIFICATION_AND_PRIMARY_VERIFICATION")
        if stage=="RUNTIME_REVIEWED":
            priority="P3_REVIEW_EXISTING_COMPLETENESS"
        elif quality.startswith(("EU_INDEX","AUSTRALIAN_DIPLOMATIC")):
            priority="P0_VERIFY_COUNTRY_LAW_AND_RECURRING_DATE"
        elif quality.startswith("PHILIPPINE_CULTURAL"):
            priority="P1_VERIFY_CULTURAL_SOURCE_IDENTITY_AND_DATE"
        elif draft:
            priority="P1_COMPLETE_SOURCE_REVIEW_AND_NATIVE_TRANSLATIONS"
        else:
            priority="P2_RESEARCH_ORIGINAL_HISTORY_AND_TRANSLATIONS"
        result.append({
            "id":oid,
            "canonicalTitleEn":record["canonicalTitleEn"],
            "scope":record["scope"],
            "countries":record.get("countries",[]),
            "periodKind":record["periodKind"],
            "officiality":record["authority"]["officiality"],
            "recordAuthority":record["authority"]["name"],
            "sourceUrls":source_urls,
            "sourceTiers":[x["tier"] for x in record["sources"]],
            "sourceQualityGate":quality,
            "introducedYear":record.get("introducedYear"),
            "editorialStage":stage,
            "priority":priority,
            "approvedEnglishContent":{
                "origin":origin,"why":why,"whyThisDate":date_reason,
                "historicalProposer":promoter,"facts":facts
            },
            "researchDraft":({
                "origin":draft["origin"],"why":draft["why"],
                "historicalProposer":draft["initiator"],
                "whyThisDate":draft["whyThisDate"],
                "facts":draft["facts"],"sources":draft["sources"],
                "status":"NOT_PUBLISHED_NOT_REVIEWED",
            } if draft else None),
            "missingEditorialEvidence":missing,
            "storyPublished":rich is not None,
            "verifiedTranslationsClaimed":False if not rich else None,
        })
    assert len({r["id"] for r in result})==1111
    priority_counts=dict(sorted(Counter(x["priority"] for x in result).items()))
    stage_counts=dict(sorted(Counter(x["editorialStage"] for x in result).items()))
    assert sum(priority_counts.values())==sum(stage_counts.values())==1111
    assert sum(x["storyPublished"] for x in result)==56
    assert stage_counts.get("SOURCE_RESEARCHED_STORY_DRAFT_PENDING_REVIEW")==2
    ordered=sorted(result,key=lambda x:(x["priority"],x["canonicalTitleEn"].casefold(),x["id"]))
    return {
        "schemaVersion":1,"catalogVersion":catalog["datasetVersion"],
        "catalogTotal":1111,
        "publishedEnglishRichStories":56,
        "irishPrimarySourcedDraftStories":2,
        "priorityCounts":priority_counts,"stageCounts":stage_counts,
        "firstResearchQueue":[x["id"] for x in ordered if not x["storyPublished"]][:50],
        "sourcePolicy":"Never infer years, promoters, annual dates or legal holiday status from titles or diplomatic/EU index alone; preserve unknowns as null.",
        "rows":ordered,
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=OUT)
    args=parser.parse_args()
    result=build()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("1111 RECORD EDITORIAL SOURCE AUDIT",json.dumps({
        "catalogVersion":result["catalogVersion"],
        "count":result["catalogTotal"],"published":result["publishedEnglishRichStories"],
        "irishDrafts":result["irishPrimarySourcedDraftStories"],
        "priority":result["priorityCounts"],"stage":result["stageCounts"]
    },ensure_ascii=False,sort_keys=True))

if __name__=="__main__":main()
