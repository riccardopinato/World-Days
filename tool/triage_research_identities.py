#!/usr/bin/env python3
"""Plan research-only identity/recurrence adjudication; never auto-certify.

Input: full 153-row fail-closed ledger plus wave-specific research metadata.
Output: inspectable triage for human/editorial + additional primary-source research.
No runtime imports or writes; no promotion to 462/1000.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports/research_certification_coverage.json"
OUT = ROOT / "reports/research_semantic_triage.json"
RESEARCH = ROOT / "data/research"

SHARED_CULTURE_CLUSTERS = {
    "LUNAR_NEW_YEAR": {
        "Seollal", "Vietnamese Lunar New Year (Tet)", "Chinese New Year (Singapore)"
    },
    "SOUTH_ASIAN_SOLAR_NEW_YEAR": {
        "Songkran Festival", "Khmer New Year", "Lao New Year (Pi Mai)",
        "Sinhala and Tamil New Year Day", "Nepali New Year (Bikram Sambat)",
        "Pahela Baishakh (Bangladesh Bengali New Year)",
    },
    "BUDDHIST_VESAK_BIRTH": {
        "Buddha Purnima", "Buddha's Birthday (South Korea)",
        "Vesak Day (Singapore)", "Visakha Bucha Day",
    },
    "DIWALI_DEEPAVALI_TIHAR": {
        "Diwali", "Deepavali (Singapore)", "Tihar"
    },
    "ISLAMIC_HOLIDAYS_SHARED": {
        "Hari Raya Puasa (Singapore)", "Hari Raya Haji (Singapore)"
    },
    "FULL_MOON_BUDDHIST": {
        "Duruthu Full Moon Poya Day", "Navam Full Moon Poya Day",
        "Medin Full Moon Poya Day", "Bak Full Moon Poya Day",
        "Adhi Poson Full Moon Poya Day", "Poson Full Moon Poya Day",
        "Esala Full Moon Poya Day", "Nikini Full Moon Poya Day",
        "Binara Full Moon Poya Day", "Vap Full Moon Poya Day",
        "Ill Full Moon Poya Day", "Unduvap Full Moon Poya Day",
    }
}
ASTRONOMICAL = {"Vernal Equinox Day", "Autumnal Equinox Day"}
ONE_OFF_LEAVE_RISK = {
    "All Souls Day (Philippines)", "Black Saturday (Philippines)"
}
REGIONAL_SCOPE = {
    "Chaitra Sankranti (Bangladesh Hill Districts)",
    "Gai Jatra", "Indra Jatra", "Jitiya Parwa",
}
LEGAL_CHANGES = {
    "Yang di-Pertuan Agong's Official Birthday",
    "Emperor's Birthday", "Queen Suthida's Birthday",
    "King Vajiralongkorn's Birthday",
}
NATIONAL_NAME_GLOBAL_IDENTITY = {
    "Language Martyrs' Day (Shaheed Dibosh)",
    "National Child Day (Canada)",
    "Children's Day (Japan)",
    "Children's Day (South Korea)",
}
DATE_RISK_KEYWORDS = (
    "LUNAR", "LUNISOLAR", "NEPALI_CALENDAR", "BENGALI_SOLAR",
    "OFFICIAL_ANNUAL_DATE_CHECK", "ROYAL_CALENDAR",
    "EASTER", "ASTRONOMICAL", "EQUINOX"
)

def risks(title, recurrence_type, note):
    result = []
    for group, names in SHARED_CULTURE_CLUSTERS.items():
        if title in names:
            result.append("SEMANTIC_GROUP:" + group)
    if title in ASTRONOMICAL:
        result.append("ASTRONOMICAL_OFFICIAL_ANNUAL_DECLARATION")
    if title in ONE_OFF_LEAVE_RISK:
        result.append("POSSIBLY_2026_ONLY_HOLIDAY")
    if title in REGIONAL_SCOPE:
        result.append("REGIONAL_OR_COMMUNITY_ONLY")
    if title in LEGAL_CHANGES:
        result.append("LEGAL_DATE_OR_MONARCH_CHANGE")
    if title in NATIONAL_NAME_GLOBAL_IDENTITY:
        result.append("SAME_CULTURAL_SUBJECT_AS_GLOBAL_OR_OTHER_NATIONAL_DAY")
    if "Adhi Poson" in title:
        result.append("INTERCALARY_NOT_ANNUAL")
    if any(x in str(recurrence_type).upper() for x in DATE_RISK_KEYWORDS):
        result.append("MULTIYEAR_DATE_REQUIRES_AUTHORITY")
    if "substitute" in str(note).lower():
        result.append("CHECK_SUBSTITUTE_DATE_NOT_EVENT")
    return sorted(set(result))

def main():
    coverage = json.loads(REPORT.read_text(encoding="utf-8"))
    assert coverage["researchRecords"] == 153
    source_map = {}
    for path in RESEARCH.glob("wave*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data.get("records", []):
            title = row["canonicalTitleEn"]
            source_map[(path.name, title)] = row
    rows = []
    for item in coverage["records"]:
        k = (item["researchFile"], item["title"])
        assert k in source_map, k
        source = source_map[k]
        rule = source.get("recurrenceRule") or source.get("recurrenceRuleType")
        if not rule:
            rule_obj = source.get("date") or source.get("recurrence") or {}
            rule = rule_obj.get("kind", "") if isinstance(rule_obj, dict) else str(rule_obj)
        flags = risks(item["title"],rule,item.get("sourceNote", ""))
        phase = item["status"]
        if phase == "ALREADY_IN_MAIN_456":
            lane = "EXCLUDE_ALREADY_CANONICAL"
        elif phase == "IN_UNMERGED_CONTENT_PR_67":
            lane = "PR67_CONSOLIDATED_EDITORIAL_GATE"
        elif phase == "PENDING_PRIMARY_SOURCE_IDENTITY_AND_RECURRENCE":
            lane = "PRIMARY_SOURCE_PDF_AND_SCOPE_FIRST"
        elif flags:
            lane = "MANUAL_SEMANTIC_AND_DATE_REVIEW"
        else:
            lane = "CANDIDATE_FOR_FIXED_RULE_SOURCE_REVIEW"
        rows.append({
            "researchFile": k[0],
            "title": k[1],
            "country": item["country"],
            "occurrence2026": item["2026Date"],
            "currentEvidenceStatus": phase,
            "reviewLane": lane,
            "riskFlags": flags,
            "semanticUniqueCertified": False,
            "multiYearRecurrenceCertified": False,
            "humanTranslationsCertified": False,
            "autoAdmit": False
        })
    counts = Counter(row["reviewLane"] for row in rows)
    assert len(rows) == 153
    assert counts["EXCLUDE_ALREADY_CANONICAL"] == 24
    assert counts["PR67_CONSOLIDATED_EDITORIAL_GATE"] == 36
    assert counts["PRIMARY_SOURCE_PDF_AND_SCOPE_FIRST"] == 9
    assert counts["MANUAL_SEMANTIC_AND_DATE_REVIEW"] + counts["CANDIDATE_FOR_FIXED_RULE_SOURCE_REVIEW"] == 84
    assert all(x["autoAdmit"] is False for x in rows)
    report = {
        "schemaVersion": 1,
        "meaning": "Research prioritization, NOT official or editorial certification.",
        "catalogMain": 456,
        "recordCount": len(rows),
        "laneCounts": dict(sorted(counts.items())),
        "blockedHumanOrSourceReview": 153 - counts["EXCLUDE_ALREADY_CANONICAL"],
        "semanticClusters": {label: sorted(names) for label,names in SHARED_CULTURE_CLUSTERS.items()},
        "records": rows,
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("SEMANTIC TRIAGE PASS "+json.dumps(report["laneCounts"],sort_keys=True))

if __name__ == "__main__":
    main()
