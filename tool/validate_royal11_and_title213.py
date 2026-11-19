#!/usr/bin/env python3
"""Test all public-layer curation and multilingual title translations."""
import json
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
A=R/"assets/data"
LANG=("en","it","es","fr","de","pt")
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
audit=rd(R/"reports/world_days_royal_biographical_11_exclusions_20261119.json")
tr=rd(R/"reports/market_title_213_localization.json")
base=rd(R/"reports/world_days_excluded_birth_death_20261119.json")
d=rd(R/"data/editorial/localizations/market_title_213_sixlocale_20261119.json")
cat=rd(A/"official_core.json")
records={r["id"]:r for r in cat["records"]}
assert len(records)==audit["publishedIds"]==tr["catalog"]==947
assert cat["datasetVersion"]=="2026.11.19.4"
excluded={r["id"] for r in base["records"]}|{r["id"] for r in audit["excluded"]}
assert len(excluded)==164 and not excluded&records.keys()
assert len([r for r in records.values() if r["scope"]=="GLOBAL"])==289
assert len([r for r in records.values() if r["scope"]=="NATIONAL"])==658
cc=Counter(r["countries"][0] for r in records.values() if r["scope"]=="NATIONAL")
assert cc["PH"]==91 and cc["SE"]==3 and cc["NO"]==6
assert tr["newTitleTranslations"]==1065 and tr["localizedTitleRecordsImproved"]==213
assert len(d["entries"])==d["count"]==213
for row in d["entries"]:
 rid=row["observanceId"]
 assert rid in records
 assert records[rid]["localizedTitles"]==row["localizedTitles"]
 assert all(row["localizedTitles"][loc]!=row["canonicalTitleEn"] for loc in LANG[1:]),rid
dates=rd(A/"occurrences_2026.json")
assert dates["occurrenceCount"]==len(dates["occurrences"])
assert len(dates["dateIndex"])==365
assert all(x["observanceId"] in records for x in dates["occurrences"])
assert all(set(x["observanceIds"])<=records.keys() for x in dates["dateIndex"])
origin=rd(A/"origin_review_index.json")
assert origin["recordCount"]==origin["sourceCatalogCount"]==947
assert {x["observanceId"] for x in origin["records"]}==records.keys()
parity=None
for loc in LANG:
 doc=rd(A/f"editorial_{loc}.json")
 rows=doc["entries"]
 ids=[x["observanceId"] for x in rows]
 assert doc["entryCount"]==len(ids)==len(set(ids))==947
 assert set(ids)==records.keys()
 if parity is None:parity=ids
 else:assert ids==parity
 assert sum(x["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for x in rows)==428
 assert sum(x["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE" for x in rows)==107
 assert not any(excluded.intersection(x.get("relatedObservanceIds",[])) for x in rows)
print("WORLD_DAYS_947_CURATED_6_LOCALES_213_TITLES_PASS: 164 archived / 519 rich / 428 contextual")
