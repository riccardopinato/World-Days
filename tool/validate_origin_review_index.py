#!/usr/bin/env python3
"""Independently validate origin-review coverage against generated canonical data.

PASS only certifies IDs, provenance structure and the explicitly researched
stories. Do not present 1107 unresearched origin narratives as certified.
"""
from collections import Counter
from pathlib import Path
import json
from datetime import datetime
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
ledger=json.loads((ROOT/"assets/data/origin_review_index.json").read_text(encoding="utf-8"))
report=json.loads((ROOT/"reports/origin_review_coverage.json").read_text(encoding="utf-8"))
by_id={r["id"]:r for r in catalog["records"]}
items=ledger["records"]
assert len(by_id)==len(catalog["records"])>=1111
assert ledger["recordCount"]==ledger["sourceCatalogCount"]==len(items)==len(by_id)
assert ledger["datasetVersion"]==catalog["datasetVersion"]
assert ledger["coverage"]=="ALL_CANONICAL_ACCOUNTED_FOR_NOT_ALL_HISTORIES_CERTIFIED"
assert ledger["reviewedRichOriginCount"]>=4
assert ledger["legacyReviewedEditorialCount"]>=56
assert report["originPendingCount"]==len(by_id)-ledger["reviewedRichOriginCount"]
assert report["allIdSourceProvenanceChecked"]==len(by_id)
assert len({e["observanceId"] for e in items})==len(by_id)
assert {e["observanceId"] for e in items}==set(by_id)
states=Counter(e["originResearchStatus"] for e in items)
assert states["PRIMARY_RESEARCHED_ORIGIN_IT_EN"]==ledger["reviewedRichOriginCount"]
assert states["SOURCE_INDEX_ONLY_ORIGIN_NOT_RESEARCHED"]+states["LEGACY_EDITORIAL_EXISTS_ORIGIN_NOT_RECERTIFIED"]==len(by_id)-ledger["reviewedRichOriginCount"]
assert sum(states.values())==len(by_id)
for e in items:
 r=by_id[e["observanceId"]]
 assert e["scope"]==r["scope"]
 assert e["countries"]==r["countries"]
 assert e["introducedYear"]==r.get("introducedYear")
 assert e["canonicalSourceUrls"]==[x["url"] for x in r["sources"]]
 assert e["sourceTiers"]==[x["tier"] for x in r["sources"]]
 assert e["authority"]==r["authority"]["name"]
 p=e["primaryResearch"]
 if p is None:
  assert e["originResearchStatus"]!="PRIMARY_RESEARCHED_ORIGIN_IT_EN"
 else:
  assert e["originResearchStatus"]=="PRIMARY_RESEARCHED_ORIGIN_IT_EN"
  assert p["sourceUrls"] and {"it","en"} <= set(p["locale"]) <= {"it","en","es","fr","de","pt"}
  assert p["reviewedAt"]=="2026-11-11"
  if r.get("introducedYear") is not None:
   assert p["introducedYear"]==r["introducedYear"]
  for url in p["sourceUrls"]:
   assert urlsplit(url).scheme=="https"
  for locale in p["locale"]:
   x=p["locale"][locale]
   for key in ("heading","origin","promoter","purpose"):
    assert len(x[key].strip())>=(18 if key=="heading" else 40)
   assert 2<=len(x["facts"])<=5
print("PASS: canonical source provenance and researched-origin ledger covers every current ID")
