#!/usr/bin/env python3
"""Proof that seven country/date/title research records alias existing canonical IDs.

No automated merge: explicit mapping is checked against 2026 original source,
the country and the canonical public title.
"""
from datetime import date
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/research/semantic_additional_country_date_duplicates_20261109.json"
EXISTING=ROOT/"data/market/wave04_global_20261109.json"
EVIDENCE=ROOT/"data/research/primary_2026_calendar_verified_20261109.json"
RESEARCH=ROOT/"data/research"
EXPECTED={
    ("ZA","South Africa Freedom Day"):"za-freedom-day",
    ("ZA","South Africa Youth Day"):"za-youth-day",
    ("ZA","South Africa National Women's Day"):"za-national-womens-day",
    ("ZA","South Africa Heritage Day"):"za-heritage-day",
    ("PH","Araw ng Kagitingan"):"ph-day-of-valor",
    ("PH","Philippine Independence Day"):"ph-independence-day",
    ("KR","Memorial Day (South Korea)"):"kr-memorial-day",
}
def main():
    payload=json.loads(DATA.read_text(encoding="utf-8"))
    market=json.loads(EXISTING.read_text(encoding="utf-8"))
    proof=json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert payload["reviewedCount"]==len(payload["records"])==len(EXPECTED)==7
    existing={r["id"]:r for r in market["records"]}
    dates={(r["country"],r["title"]):r for r in proof["records"]}
    candidates={}
    for filename in {item["candidateFile"] for item in payload["records"]}:
        wave=json.loads((RESEARCH/filename).read_text(encoding="utf-8"))
        for r in wave["records"]:
            candidates[(filename,r["canonicalTitleEn"])]=r
    seen=set()
    for r in payload["records"]:
        k=(r["country"],r["candidateTitle"])
        assert k in EXPECTED and k not in seen,k
        seen.add(k)
        assert EXPECTED[k]==r["existingId"]
        assert r["decision"]=="SAME_EXISTING_OBSERVANCE"
        assert len(r["reason"]) >= 90
        candidate=candidates[(r["candidateFile"],r["candidateTitle"])]
        target=existing[r["existingId"]]
        assert target["country"]==candidate["country"]==r["country"]
        assert target["canonicalTitleEn"]==r["canonicalTitle"]
        rule=target["recurrenceRules"][0]
        assert rule["kind"]=="FIXED_DATE"
        expected=date(2026,rule["month"],rule["day"]).isoformat()
        assert expected==r["occurrence2026"]
        evidence=dates[k]
        assert evidence["occurrence2026"]==expected
        assert target["source"]==r["primaryUrl"]
        assert evidence["runtimeAdmission"]=="BLOCKED"
    assert seen==set(EXPECTED)
    print("COUNTRY-DATE IDENTITY PASS: seven canonical duplicates (4 ZA, 2 PH, 1 KR)")
if __name__=="__main__":
    main()
