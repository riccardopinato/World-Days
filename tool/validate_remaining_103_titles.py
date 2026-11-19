#!/usr/bin/env python3
"""Final 947-record multilingual coverage and 103-title source-identity QA."""
from pathlib import Path
import json
from collections import Counter

R=Path(__file__).resolve().parents[1]
A=R/"assets/data"
LANG=("en","it","es","fr","de","pt")
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
srcfiles=[R/"data/editorial/localizations/market_wave09_62_sixlocale_20261119.json",
          R/"data/editorial/localizations/ph_wave10_41_sixlocale_20261119.json"]
payloads=[rd(p) for p in srcfiles]
assert [p["count"] for p in payloads]==[62,41]
rows=[x for pack in payloads for x in pack["records"]]
assert len(rows)==len({x["observanceId"] for x in rows})==103
manifest=rd(R/"reports/remaining_103_market_title_localizations_20261119.json")
assert manifest["newNonEnglishTitleTranslations"]==515
assert manifest["newTotalNonEnglishTitleTranslations"]==1795
assert manifest["newTotalSourceAnchoredLocalizedTitleIDs"]==359
cat=rd(A/"official_core.json")
assert cat["datasetVersion"]=="2026.11.19.5"
items=cat["records"]
ids={x["id"] for x in items}
assert len(ids)==len(items)==947
assert Counter(x["scope"] for x in items)=={"GLOBAL":289,"NATIONAL":658}
by_id={x["id"]:x for x in items}
exclude=rd(R/"reports/world_days_royal_biographical_11_exclusions_20261119.json")
old_exclude=rd(R/"reports/world_days_excluded_birth_death_20261119.json")
excluded={x["id"] for x in old_exclude["records"]}|{x["id"] for x in exclude["excluded"]}
assert len(excluded)==164 and not ids&excluded
for row in rows:
 ident=row["observanceId"]
 assert ident in by_id
 assert by_id[ident]["localizedTitles"]==row["localizedTitles"]
 assert row["source"] in [s["url"] for s in by_id[ident]["sources"]]
 assert all(row["localizedTitles"][l]!=row["localizedTitles"]["en"] for l in LANG[1:])
origin=rd(A/"origin_review_index.json")
assert origin["datasetVersion"]==cat["datasetVersion"]
assert origin["recordCount"]==origin["sourceCatalogCount"]==947
assert {x["observanceId"] for x in origin["records"]}==ids
ordered=None
for locale in LANG:
 d=rd(A/f"editorial_{locale}.json")
 entries=d["entries"]
 o=[r["observanceId"] for r in entries]
 assert d["entryCount"]==len(o)==len(set(o))==947
 assert set(o)==ids
 if ordered is None:ordered=o
 else:assert o==ordered
 assert sum(r["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for r in entries)==428
 assert sum(r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE" for r in entries)==107
 assert not any(excluded.intersection(r.get("relatedObservanceIds",[])) for r in entries)
 if locale!="en":
  for row in rows:
   x=next(r for r in entries if r["observanceId"]==row["observanceId"])
   if x["status"]=="AI_CONTEXTUAL_SIX_LOCALE":
    assert row["localizedTitles"][locale] in x["origin"],(row["observanceId"],locale)
print("MARKET_TITLE_359_ALL_SIX_LOCALES_PASS: 947 published, 1795 national titles, 428 historical origins pending")
