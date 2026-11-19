#!/usr/bin/env python3
"""Strict post-curation six-locale/runtime/archival invariant checks."""
from pathlib import Path
from collections import Counter
import json
root=Path(__file__).resolve().parents[1]
assets=root/"assets/data"
report=json.loads((root/"reports/world_days_catalog_relevance_audit_20261119.json").read_text())
excluded=json.loads((root/"reports/world_days_excluded_birth_death_20261119.json").read_text())
assert report["catalogSourceCandidatesAudited"]==1111
assert report["excludedPersonalBirthDeathAnniversaries"]==excluded["count"]==153
assert report["publishedObservances"]==958
removed={r["id"] for r in excluded["records"]}
assert len(removed)==153 and all(r["country"]=="PH" for r in excluded["records"])
cat=json.loads((assets/"official_core.json").read_text())
records=cat["records"]
assert len(records)==958 and len({x["id"] for x in records})==958
assert cat["datasetVersion"]=="2026.11.19.3"
by_id={r["id"]:r for r in records}
assert not removed&set(by_id)
assert len([r for r in records if r["scope"]=="GLOBAL"])==289
assert len([r for r in records if r["scope"]=="NATIONAL"])==669
assert len([r for r in records if r["countries"]==["PH"]])==91
assert report["philippinesPublished"]==91
occ=json.loads((assets/"occurrences_2026.json").read_text())
assert len(occ["dateIndex"])==365
assert occ["occurrenceCount"]==len(occ["occurrences"])
assert all(x["observanceId"] in by_id for x in occ["occurrences"])
assert all(set(x["observanceIds"])<=set(by_id) for x in occ["dateIndex"])
assert all(x["observanceId"] not in removed for x in occ["occurrences"])
origin=json.loads((assets/"origin_review_index.json").read_text())
assert origin["recordCount"]==origin["sourceCatalogCount"]==len(origin["records"])==958
assert {x["observanceId"] for x in origin["records"]}==set(by_id)
assert sum(origin["originStatusCounts"].values())==958
assert origin["datasetVersion"]==cat["datasetVersion"]
reference=None
for locale in ("en","it","es","fr","de","pt"):
 doc=json.loads((assets/f"editorial_{locale}.json").read_text())
 rows=doc["entries"]
 ids=[r["observanceId"] for r in rows]
 assert doc["entryCount"]==len(ids)==len(set(ids))==958,locale
 assert set(ids)==set(by_id),locale
 if reference is None:reference=ids
 else:assert ids==reference,locale
 assert sum(r["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for r in rows)==439
 assert sum(r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE" for r in rows)==107
 assert all(r.get("summary","").strip() for r in rows)
 assert all(r.get("origin","").strip() for r in rows if r["status"]=="AI_CONTEXTUAL_SIX_LOCALE")
 assert all(not (removed & set(r.get("relatedObservanceIds",[]))) for r in rows)
assert len(report["outsidePolicyBiographicalCandidates"])==0,report["outsidePolicyBiographicalCandidates"]
assert len(report["retainedStatutoryCivicCommemorationExceptions"])==2
print("WORLD_DAYS_SCOPE_958_SIX_LOCALES_PASS: 153 archived, 439 contextual, 519 richer")
