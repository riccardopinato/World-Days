#!/usr/bin/env python3
"""Validate 22 parallel FAST-01 primary-date reviews against the generated queue.

Never equate source-date corroboration with annual recurrence, legal holiday
entitlement or qualified editorial acceptance.
"""
from collections import Counter
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"data/research/FAST01_PARALLEL_22_DATE_AND_SCOPE_20261110.json"
QUEUE=ROOT/"reports/research_fast_batches.json"
COUNTS={"BD":3,"CA":1,"ID":2,"IN":1,"KH":8,"LA":2,"MY":2,"PH":1,"VN":2}
MUST_HAVE={
"National Day of Observance for COVID-19":"RECENT_OR_DISCRETIONARY_DESIGNATION",
"July Mass Uprising Day (Bangladesh)":"RECENT_DESIGNATION_NEEDS_2027_RULE",
"Rabindranath Tagore Jayanti":"RESTRICTED_OR_REGIONAL_EMPLOYEE_HOLIDAY",
"Lao Women's Union Founding Day":"GENDER_SPECIFIC_HOLIDAY_CLASSIFICATION",
"Immaculate Conception Day (Philippines)":"SHARED_RELIGIOUS_DATE_NATIONAL_LEGAL_STATUS",
"King Norodom Sihamoni's Birthday":"MONARCH_DEPENDENT_SCOPE",
"Queen Mother Norodom Monineath Sihanouk's Birthday":"MONARCH_DEPENDENT_SCOPE",
"King Norodom Sihamoni Coronation Day":"MONARCH_DEPENDENT_SCOPE",
"Peace Day in Cambodia":"RECENT_DESIGNATION_NEEDS_HISTORY",
}
def main():
    d=json.loads(SRC.read_text(encoding="utf-8"))
    q=json.loads(QUEUE.read_text(encoding="utf-8"))
    assert d["schemaVersion"]==1
    assert d["candidateCount"]==len(d["records"])==22
    assert d["countryCounts"]==COUNTS
    assert q["fastLaneTotal"]==22
    assert len(q["batches"])==1 and q["batches"][0]["count"]==22
    expected={(r["country"],r["title"],r["date2026"]):r for r in q["batches"][0]["items"]}
    seen=set()
    for r in d["records"]:
        key=r["country"],r["title"],r["occurrence2026"]
        assert key in expected and key not in seen,key
        seen.add(key)
        assert r["batch"]=="FAST-01"
        assert r["source"]==expected[key]["officialCalendarUrl"]
        assert date.fromisoformat(r["occurrence2026"]).year==2026
        assert r["verification"]=="2026_DATE_AND_NAME_CORROBORATED"
        assert r["dateEvidenceClass"]=="PRIMARY_GOVERNMENT"
        for field in ("source","originatorEvidenceUrl"):
            p=urlsplit(r[field])
            assert p.scheme=="https" and p.hostname and not p.username
        assert len(r["originatorPublisher"])>12
        assert len(r["reviewNote"])>60
        assert r["identityCertified"] is False
        assert r["multiYearAnnualCertified"] is False
        assert r["qualifiedLanguageReview"] is False
        assert r["publicationStatus"]=="RESEARCH_ONLY"
        if r["title"] in MUST_HAVE:
            assert r["risk"]==MUST_HAVE[r["title"]],r["title"]
    assert set(expected)==seen
    assert Counter(r["country"] for r in d["records"])==COUNTS
    assert all(r["publicationStatus"]=="RESEARCH_ONLY" for r in d["records"])
    print("FAST01 22-DATE SOURCE-CHECK PASS: 22 official 2026 name/date corroborations across 9 markets, 0 annual/unique/editorial approvals.")
if __name__=="__main__":
    main()
