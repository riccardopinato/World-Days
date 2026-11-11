#!/usr/bin/env python3
"""Deterministic 100-item original-history research batch; never invent prose.

Links from the canonical catalog are *starting evidence*, not proof that each
individual history/year/promoter has been independently verified. The output
is a durable, inspectable research worklist, NOT 100 published stories.
"""
import json
from pathlib import Path
from editorial_1111_source_audit_queue import build as build_audit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/editorial_origin_wave100.json"
LOCALES = ("it", "en", "es", "fr", "de", "pt")
BLOCKED_QUALITY = {
    "EU_INDEX_REQUIRES_COUNTRY_PRIMARY_LAW_OR_ORIGINATOR",
    "AUSTRALIAN_DIPLOMATIC_CALENDAR_NOT_FOREIGN_STATUTORY_HOLIDAY",
    "PHILIPPINE_CULTURAL_INDEX_NOT_STATUTORY_HOLIDAY",
    "DISCOVERY_ONLY_NOT_VERIFIED",
}
FIRST_FOUR = {
    "world-braille-day", "international-day-of-education",
    "world-environment-day", "ie-w13-eures-st-brigid-s-day",
}

def build():
    audit = build_audit()
    # Future-proof: read the actual source-researched batch when integrated.
    origin_batch = ROOT / "data/editorial/batches/origin_stories_primary_20261111.json"
    excluded = set(FIRST_FOUR)
    if origin_batch.exists():
        origin = json.loads(origin_batch.read_text(encoding="utf-8"))
        excluded.update(r["observanceId"] for r in origin["records"])

    eligible = []
    for r in audit["rows"]:
        if (r["id"] in excluded or r["storyPublished"] or r["researchDraft"]
                or r["editorialStage"] != "NOT_RESEARCHED"):
            continue
        if r["sourceQualityGate"] in BLOCKED_QUALITY:
            continue
        if not ({"A_PRIMARY", "D_ORIGINATOR"} & set(r["sourceTiers"])):
            continue
        if not r["sourceUrls"] or any(not u.startswith("https://") for u in r["sourceUrls"]):
            continue
        eligible.append(r)

    # Give source-addressable international days a slight preference while
    # retaining national institutional observances in the 100-item batch.
    def order(r):
        return (r["introducedYear"] is None, r["canonicalTitleEn"].casefold(), r["id"])
    global_rows = sorted((r for r in eligible if r["scope"] == "GLOBAL"), key=order)
    national_rows = sorted((r for r in eligible if r["scope"] == "NATIONAL"), key=order)
    target = min(100, len(eligible))
    chosen = (global_rows[:60] + national_rows[:40])[:target]
    chosen_ids = {r["id"] for r in chosen}
    if len(chosen) < 100:
        chosen += [r for r in sorted(eligible, key=order) if r["id"] not in chosen_ids][:target-len(chosen)]
    assert len(chosen) == target and len({r["id"] for r in chosen}) == target, "selection must remain complete and unique"

    dossiers = []
    for i, r in enumerate(chosen, start=1):
        dossiers.append({
            "sequence": i,
            "observanceId": r["id"],
            "titleEn": r["canonicalTitleEn"],
            "scope": r["scope"],
            "countries": r["countries"],
            "periodKind": r["periodKind"],
            "listedAuthorityNotAssumedFounder": r["recordAuthority"],
            "catalogIntroducedYear": r["introducedYear"],
            "catalogSourceUrls": r["sourceUrls"],
            "catalogSourceTiers": r["sourceTiers"],
            "sourceQualityGate": r["sourceQualityGate"],
            "priorEditorialStage": r["editorialStage"],
            "historicalEvidenceStatus": "SOURCE_LINK_PRESENT_INDIVIDUAL_HISTORY_UNVERIFIED",
            "storyStatus": "RESEARCH_NOT_PUBLISHED",
            "storyDraft": {
                "origin": None,
                "formalIntroductionYearConfirmed": None,
                "reasonForCalendarDate": None,
                "individualPromoterOrIssuingAuthority": None,
                "purpose": None,
                "contextualFacts": []
            },
            "localeStatus": {locale: "AWAITING_SOURCE_RESEARCH" for locale in LOCALES},
            "reviewChecklist": [
                "Verify original issuing act or first-party individual page",
                "Distinguish founding, event and first observance dates",
                "Verify actual proposer rather than infer from listed authority",
                "Research motive, date rationale and 2-5 specific facts",
                "Write original six-locale prose and obtain editorial review",
            ]
        })
    return {
        "schemaVersion": 1,
        "batchId": "WORLD-DAYS-ORIGIN-WAVE100-20261111",
        "canonicalDatasetVersion": audit["catalogVersion"],
        "catalogTotalAtGeneration": audit["catalogTotal"],
        "targetCount": target,
        "recordCount": len(dossiers),
        "historicallyVerifiedCompletedStories": 0,
        "reviewStatus": ("100_PRIMARY_LINKED_RESEARCH_DOSSIERS_NOT_100_APPROVED_STORIES"
                         if target == 100 else f"{target}_PRIMARY_LINKED_RESEARCH_DOSSIERS_NOT_APPROVED_STORIES"),
        "exclusions": "Existing 56 published histories, original four-source stories, individually researched pending drafts, and potentially misleading institutional index records",
        "sourcePolicy": "A catalog link does not prove individual history, founder, formal introduction year or legal status. Unknown fields remain null. No automatic publication.",
        "dossiers": dossiers,
    }

def main():
    result = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ORIGIN_WAVE100", json.dumps({
        "batch": result["batchId"],
        "records": result["recordCount"],
        "individually_verified_stories": result["historicallyVerifiedCompletedStories"],
        "status": result["reviewStatus"],
    }, sort_keys=True))

if __name__ == "__main__":
    main()
