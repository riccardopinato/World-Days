#!/usr/bin/env python3
"""Check 12 truly individual source stories, six-language parity, 592 remaining."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LANG=("en","it","es","fr","de","pt")
report=json.loads((ROOT/"reports/fasttrack_parallel_604/origin_enrichment_12.json").read_text(encoding="utf-8"))
assert report["newIndividualSourceGrounded"]==12
assert report["sourceGroundedNow"]==519
assert report["contextualStillAwaitingOrigin"]==592
ids=report["sourceIds"]
assert len(ids)==len(set(ids))==12
catalog={x["id"]:x for x in json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))["records"]}
assert len(catalog)==1111
reference=None
for locale in LANG:
 doc=json.loads((ROOT/f"assets/data/editorial_{locale}.json").read_text(encoding="utf-8"))
 rows=doc["entries"]
 ids_all=[r["observanceId"] for r in rows]
 assert doc["entryCount"]==len(ids_all)==len(set(ids_all))==1111,locale
 if reference is None:reference=ids_all
 else:assert ids_all==reference,("locale drift",locale)
 mapped={r["observanceId"]:r for r in rows}
 assert set(ids)<=set(mapped)
 assert sum(r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE" for r in rows)==107
 assert sum(r["status"]=="AI_CONTEXTUAL_SIX_LOCALE" for r in rows)==592
 for id_ in ids:
  r=mapped[id_]
  assert r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE"
  assert len(r["origin"])>=155 and len(r["whyThisDate"])>=45
  assert len(r["quickFacts"])>=3
  assert r["institutionalSourceUrls"]
  assert catalog[id_]["introducedYearSource"] in r["institutionalSourceUrls"]
  assert str(catalog[id_]["introducedYear"]) in r["origin"]
  assert "no independent human" in r["sourcePolicy"]
print("ORIGIN12_ALL_SIX_LOCALES_VALID: 519 sourced-rich, 592 contextual")
