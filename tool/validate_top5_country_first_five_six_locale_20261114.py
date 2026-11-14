#!/usr/bin/env python3
"""Fail-closed checks for five sourced, unapproved six-locale national drafts."""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from editorial_research_handoff import load_handoff
from editorial_1111_source_audit_queue import build as build_audit
from editorial_origin_completion_waves import _read_origin
from report_country_authoring_backlog import build as build_rank

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/editorial/research_batches/top5_country_first_five_six_locale_20261114.json"
d = json.loads(SRC.read_text(encoding="utf-8"))
audit = build_audit()
by_id = {r["id"]:r for r in audit["rows"]}
rank = build_rank()
top = rank["ranking"][:5]
assert [(r["country"],r["pendingNewResearch"]) for r in top] == [
    ("CZ",28), ("SK",27), ("IT",24), ("FI",22), ("EE",20)]
assert rank["catalogTotal"] == 1111
assert rank["globalNoCountryCount"] == 289
assert sum(r["pendingNewResearch"] for r in rank["ranking"]) == 461
assert d["schemaVersion"] == 1
assert d["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_HUMAN_CERTIFIED"
assert d["count"] == len(d["records"]) == 5
assert d["locales"] == ["en","it","es","fr","de","pt"]
assert set(r["country"] for r in d["records"]) == {"CZ","SK","IT","FI","EE"}
assert len({r["observanceId"] for r in d["records"]}) == 5
handoff = load_handoff(set(by_id))
main = set(_read_origin())
untouched = main | handoff["six_locale_draft_ids"] | handoff["out_of_scope_ids"]
for r in d["records"]:
    oid = r["observanceId"]
    assert oid in by_id and oid not in untouched, ("duplicate or out-of-scope ID",oid)
    row = by_id[oid]
    assert row["countries"] == [r["country"]] and row["scope"] == "NATIONAL"
    assert r["country"] in {c["country"] for c in top}
    assert oid in {x["id"] for c in top for x in c["pendingIds"]}
    assert len(r["sources"]) >= 2 and len(r["sources"]) == len(set(r["sources"]))
    assert all(urlsplit(url).scheme == "https" and urlsplit(url).hostname for url in r["sources"])
    assert r["firstObservedYear"] is None, "do not invent earliest celebration"
    if r["introducedYear"] is not None:
        assert r["introducedYear"] in (1949,2000)
    assert len(r["sourceReviewNote"]) >= 65
    assert set(r["locale"]) == set(d["locales"])
    years_en = set(re.findall(r"\b(?:18|19|20)\d\d\b", r["locale"]["en"]["origin"]))
    assert years_en
    origins = []
    for lang in d["locales"]:
        x = r["locale"][lang]
        assert set(x) == {"heading","origin","promoter","purpose","facts"}
        assert len(x["heading"]) >= 20
        assert len(x["origin"]) >= 400
        assert len(x["promoter"]) >= 50
        assert len(x["purpose"]) >= 45
        assert len(x["facts"]) == 3
        assert all(len(f) >= 20 for f in x["facts"])
        assert set(re.findall(r"\b(?:18|19|20)\d\d\b", x["origin"])) == years_en, (oid,lang,"year drift")
        origins.append(x["origin"])
    assert len(set(origins)) == 6, "translations must not be English copies"
print("PASS: top-five accurate ranking; 5 distinct canonical source histories x 6 substantive locales = 30 draft locale records; human certification 0")
