#!/usr/bin/env python3
"""Validate four same-country/date duplicate source identities missed by fuzzy title matching."""
import json
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/research/semantic_additional_za_duplicates_20261109.json"
EXISTING=ROOT/"data/market/wave04_global_20261109.json"
RESEARCH=ROOT/"data/research/wave05_canada_south_africa_additional_20261109.json"
EVIDENCE=ROOT/"data/research/primary_2026_calendar_verified_20261109.json"
def main():
    payload=json.loads(DATA.read_text(encoding="utf-8"))
    market=json.loads(EXISTING.read_text(encoding="utf-8"))
    wave=json.loads(RESEARCH.read_text(encoding="utf-8"))
    proof=json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert payload["reviewedCount"]==len(payload["records"])==4
    existing={r["id"]:r for r in market["records"]}
    candidates={r["canonicalTitleEn"]:r for r in wave["records"]}
    dates={(r["country"],r["title"]):r for r in proof["records"]}
    seen=set()
    for r in payload["records"]:
        assert r["decision"]=="SAME_EXISTING_OBSERVANCE"
        assert r["country"]=="ZA"
        assert r["candidateTitle"] in candidates
        assert r["existingId"] in existing
        assert r["candidateTitle"] not in seen
        seen.add(r["candidateTitle"])
        candidate=candidates[r["candidateTitle"]]
        target=existing[r["existingId"]]
        assert target["country"]==r["country"]=="ZA"
        assert target["canonicalTitleEn"]==r["canonicalTitle"]
        assert candidate["country"]=="ZA"
        # Prefix and suffix country qualifiers are formatting only, not two events.
        candidate_core=r["candidateTitle"].removeprefix("South Africa ").casefold()
        existing_core=r["canonicalTitle"].removesuffix(" — South Africa").casefold()
        assert candidate_core==existing_core,(candidate_core,existing_core)
        rule=target["recurrenceRules"][0]
        assert rule["kind"]=="FIXED_DATE"
        expected=date(2026,rule["month"],rule["day"]).isoformat()
        assert expected==r["occurrence2026"]
        src=dates[("ZA",r["candidateTitle"])]
        assert src["occurrence2026"]==expected
        assert target["source"]==r["primaryUrl"]==src["officialCalendarUrl"]
    print("ZA CROSS-NAME DUPLICATES PASS: 4 already present, no new admissions")
if __name__=="__main__":
    main()
