#!/usr/bin/env python3
"""Validate 12 source-stage civic commemorations WITHOUT adding unsupported markets to runtime."""
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
import json
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data/research/FAST02_CIVIC_12_SOURCE_STAGED_20261110.json"
EXPECTED={"BD":2,"ID":2,"KH":3,"MY":2,"VN":2,"LA":1}
LOCALES={"en","it","es","fr","de","pt"}
def main():
    d=json.loads(P.read_text(encoding="utf8"))
    assert d["schemaVersion"]==1 and d["count"]==len(d["records"])==12
    assert d["countryCounts"]==EXPECTED and set(d["locales"])==LOCALES
    assert d["admission"]=="SOURCE_STAGED_MARKET_EXPANSION_REQUIRED"
    assert d["baseCatalog"]==492 and d["proposedCatalogIfAllQualifiedAndIntegrated"]==504
    ids=set();titles=set()
    for row in d["records"]:
        rid=row["id"];title=row["canonicalTitleEn"]
        assert rid not in ids and (row["country"],title) not in titles
        ids.add(rid);titles.add((row["country"],title))
        assert row["country"] in EXPECTED
        assert row["countryExpansionRequired"] is True
        assert row["admission"]=="SOURCE_STAGED_NOT_RUNTIME"
        assert row["humanEditorialStatus"]=="METADATA_PRIMARY_VERIFIED_STORY_NOT_REVIEWED"
        assert row["proposedIntroducedYear"] is None and row["introducedYearSource"] is None
        assert set(row["localizedTitles"])==LOCALES
        assert row["localizedTitles"]["en"]==title
        assert all(len(t.strip())>=6 for t in row["localizedTitles"].values())
        assert row["sourceTier"]=="A_PRIMARY" and row["authorityType"]=="GOVERNMENT"
        u=urlsplit(row["source"])
        assert u.scheme=="https" and u.hostname and not u.username
        assert row["recurrenceRules"][0]["kind"]=="FIXED_DATE"
        rule=row["recurrenceRules"][0]
        assert [date(y,rule["month"],rule["day"]).year for y in (2026,2027,2028)]==[2026,2027,2028]
        assert len(row["chronologyNote"])>=80 and len(row["dateRationale"])>=80
    assert Counter(r["country"] for r in d["records"])==EXPECTED
    print("FAST02 CIVIC SOURCE GATE PASS: 12 source-stage records, six locales, six unsupported markets; runtime unchanged")
if __name__=="__main__":main()
