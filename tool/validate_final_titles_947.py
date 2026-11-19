#!/usr/bin/env python3
"""Strict post-publisher test: 947 observances × 6 languages, zero invalid
English title fallbacks, 1 legitimate untranslated proper noun exception.
"""
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/data"
LOCALES=("en","it","es","fr","de","pt")
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
report=rd(ROOT/"reports/final_947_title_translation_completion_20261119.json")
assert report["overallNewNonEnglishStringsAcrossStages"]==2046
assert report["koreanCivicTitlesLocalized"]==50
assert report["distinctImprovedNationalAndCulturalIds"]==409
cat=rd(ASSETS/"official_core.json")
items=cat["records"]
assert len(items)==947 and cat["datasetVersion"]=="2026.11.19.6"
by_id={r["id"]:r for r in items}
assert len(by_id)==947
src=rd(ROOT/"data/editorial/localizations/korean_mois_50_sixlocale_20261119.json")
assert src["count"]==len(src["records"])==50
for row in src["records"]:
 id_=row["observanceId"]
 assert by_id[id_]["localizedTitles"]==row["localizedTitles"]
 assert by_id[id_]["countries"]==["KR"]
 assert row["source"] in [u["url"] for u in by_id[id_]["sources"]]
sid=by_id["safer-internet-day"]["localizedTitles"]
assert sid["de"]=="Tag für mehr Sicherheit im Internet (Safer Internet Day)"
for loc in LOCALES[1:]:
 unchanged={r["id"] for r in items if r["localizedTitles"][loc]==r["localizedTitles"]["en"]}
 expected={"mt-sette-giugno"} if loc!="fr" else set()
 assert unchanged==expected,(loc,unchanged)
origin=rd(ASSETS/"origin_review_index.json")
assert origin["datasetVersion"]==cat["datasetVersion"] and origin["recordCount"]==947
excluded=rd(ROOT/"reports/world_days_excluded_birth_death_20261119.json")
royal=rd(ROOT/"reports/world_days_royal_biographical_11_exclusions_20261119.json")
deleted={r["id"] for r in excluded["records"]}|{r["id"] for r in royal["excluded"]}
assert len(deleted)==164 and not deleted&by_id.keys()
reference=None
for loc in LOCALES:
 doc=rd(ASSETS/f"editorial_{loc}.json")
 entries=doc["entries"]
 ids=[x["observanceId"] for x in entries]
 assert doc["entryCount"]==len(ids)==len(set(ids))==947
 assert set(ids)==by_id.keys()
 if reference is None:reference=ids
 else:assert ids==reference
 assert sum(r["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for r in entries)==428
 assert sum(r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE" for r in entries)==107
 assert all(not deleted.intersection(r.get("relatedObservanceIds",[])) for r in entries)
 assert all(r.get("summary","").strip() for r in entries)
occ=rd(ASSETS/"occurrences_2026.json")
assert len(occ["dateIndex"])==365
assert all(x["observanceId"] in by_id for x in occ["occurrences"])
print("WORLD_DAYS_FINAL_TITLES_SIX_LOCALE_PASS: 947 active, 164 excluded, 2046 new titles, 1 proper-noun exception")
