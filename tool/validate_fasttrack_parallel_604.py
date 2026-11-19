#!/usr/bin/env python3
"""Prove 604 metadata-only contextual articles are complete in six locales.
Does not certify individually researched historical origins.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LANG=("en","it","es","fr","de","pt")
OUT=ROOT/"reports"/"fasttrack_parallel_604"
REPORT=json.loads((OUT/"manifest.json").read_text(encoding="utf-8"))
assert REPORT["catalog"]==REPORT["sixLocaleEditorialArticles"]==1111
assert REPORT["newContextualArticles"]==REPORT["contextualNotOriginResearched"]==604
assert REPORT["originSpecificArticlesBefore"]==507
assert REPORT["cohortSizes"]==[100]*6+[4]
assert REPORT["missingAnyEditorialLocale"]==0
catalog=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
all_ids={r["id"] for r in catalog["records"]}
assert len(all_ids)==1111
manifest_ids=[]
for n,expected in enumerate([100]*6+[4],1):
    c=json.loads((OUT/f"cohort_{n:02d}.json").read_text(encoding="utf-8"))
    assert c["cohort"]==n and c["count"]==len(c["ids"])==expected
    manifest_ids.extend(c["ids"])
assert len(manifest_ids)==len(set(manifest_ids))==604 and set(manifest_ids)<=all_ids
first=None
for loc in LANG:
    data=json.loads((ROOT/f"assets/data/editorial_{loc}.json").read_text(encoding="utf-8"))
    entries=data["entries"]
    ids=[r["observanceId"] for r in entries]
    assert len(ids)==len(set(ids))==data["entryCount"]==1111,loc
    assert ids[-604:]==manifest_ids,loc
    assert set(ids)==all_ids,loc
    assert sum(r["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for r in entries)==604,loc
    if first is None:first=ids
    else:assert ids==first,("cross-locale identity drift",loc)
    for row in entries[-604:]:
        assert row["locale"]==loc and row["status"]=="AI_CONTEXTUAL_SIX_LOCALE"
        assert row["hook"].strip() and len(row["origin"])>=140
        assert len(row["quickFacts"])==3 and all(x.strip() for x in row["quickFacts"])
        assert row["summary"] and row["whyItMatters"] and len(row["waysToTakePart"])==2
        assert "not individually researched" in row["sourcePolicy"]
print("FASTTRACK_PARALLEL_604_LOCALE_PARITY_PASS",REPORT)
