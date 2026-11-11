#!/usr/bin/env python3
"""Source-index QA for one +400 canonical target; research does not equal admission.

Never autogenerate a publishing-ready record from a dated biography without
checking legal/cultural classification, exact date, semantic aliases and source.
"""
import json, re, unicodedata
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/editorial/candidates/wave11_ncca_cultural_anniversaries_20261111.json"
VALID_LOCALES={"en","it","es","fr","de","pt"}

def clean(value):
    t=unicodedata.normalize("NFKD",value.casefold())
    return re.sub(r"[^a-z0-9]+","", "".join(ch for ch in t if not unicodedata.combining(ch)))

def validate():
    obj=json.loads(PATH.read_text(encoding="utf-8"))
    rows=obj["records"]
    assert obj["schemaVersion"]==1 and obj["goal"]==1111
    assert obj["startingCanonical"]==711
    assert obj["requiredNetNew"]==400
    assert obj["sourceRows"]==145
    assert obj["indexCandidates"]==len(rows)==144
    assert obj["status"]=="RESEARCH_CANDIDATE_NOT_ADMITTED"
    assert len({r["id"] for r in rows})==len(rows)
    assert len({(r["canonicalTitleEn"],r["recurrenceRules"][0]["month"],r["recurrenceRules"][0]["day"]) for r in rows})==len(rows)
    assert "Founding of the National Archives of the Philippines" not in {r["sourceTitleOriginal"] for r in rows}
    for r in rows:
        assert r["country"]=="PH" and r["id"].startswith("ph-w11-")
        assert r["source"]=="https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/"
        assert urlparse(r["source"]).scheme=="https"
        assert r["sourceTier"]=="A_PRIMARY"
        assert r["sourceReviewStatus"]=="INDEX_ONLY_NEEDS_BIOGRAPHY_CORROBORATION"
        assert r["metadataIndexVerified"] is True
        assert r["individualBiographyVerified"] is False
        assert r["richStoryVerified"] is False
        assert r["admissionReady"] is False
        assert r["sourceTitleVerbatim"] is False
        assert r["sourceTitleNormalizedFromIndex"] is True
        assert r["proposedIntroducedYear"] is None
        assert r["introducedYearSource"] is None
        rule=r["recurrenceRules"][0]
        assert rule["kind"]=="FIXED_DATE"
        for year in (2026,2027,2028):
            d=date(year,rule["month"],rule["day"])
            assert d.year==year
        assert set(r["localizedTitles"])==VALID_LOCALES
        assert r["localizedTitles"]["en"]==r["canonicalTitleEn"]
    print(f"PASS: {len(rows)} NCCA index-only culture candidates, none admitted; 256+ other unique source-qualified identities still required for 400.")
    return obj

if __name__=="__main__":
    validate()
