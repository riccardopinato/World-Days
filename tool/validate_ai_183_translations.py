#!/usr/bin/env python3
"""Fail-closed six-language runtime proof after the 183 AI-only review import.

The historical research inventory has 485 unique IDs (some overlap curated
original rich content). There must now be 502 distinct Rich Editorial IDs:
56 legacy + 173 existing AI certified + 90 six-locale source reviewed + 183
new neural-translation review records. 0 source-preview-only histories.
"""
from collections import Counter
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
LANG=("en","it","es","fr","de","pt")
STATUS="AI_CERTIFIED_TRANSLATION_SIX_LOCALE"

def load(path):
 return json.loads(path.read_text(encoding="utf-8"))

pack=load(ROOT/"data/editorial/published/ai_183_sixlocale_reviewed.json")
assert pack["scope"]=="WORLD_DAYS_EXISTING_183_EN_IT_HISTORY_AI_SIX_LOCALE"
assert pack["status"]=="AI_MACHINE_TRANSLATION_SOURCE_CHRONOLOGY_PASSED"
assert pack["recordCount"]==len(pack["records"])==183
assert pack["notHumanFactCertified"] is True
expected={r["observanceId"] for r in pack["records"]}
assert len(expected)==183
catalog=load(ROOT/"assets/data/official_core.json")
all_ids={r["id"] for r in catalog["records"]}
assert len(all_ids)==1111 and expected<=all_ids

research=set()
for path in [ROOT/"data/editorial/batches/origin_stories_primary_20261111.json"]+sorted(
 path for path in (ROOT/"data/editorial/batches").glob("origin_stories_wave*.json") if "wave21" not in path.stem):
 for row in load(path)["records"]:
  oid=row["observanceId"]
  assert oid not in research
  research.add(oid)
assert len(research)==325 and expected<=research

report=load(ROOT/"reports/ai_183_runtime_import.json")
assert report["historicallyPreparedUniqueIDs"]==485
assert report["addedAITranslationCertified"]==183
assert report["totalRich"]==502
assert report["remainingBilingualOnlyResearch"]==0
assert report["notHumanFactCertified"] is True

order=None
for locale in LANG:
 doc=load(ROOT/f"assets/data/editorial_{locale}.json")
 rows=doc["entries"]
 ids=[r["observanceId"] for r in rows]
 assert len(ids)==len(set(ids))==doc["entryCount"]==502,(locale,len(ids))
 assert doc["aiNeuralTranslationReviewedCount"]==183
 counts=Counter(r["status"] for r in rows)
 assert counts["AI_CERTIFIED"]==173
 assert counts["AI_SOURCE_REVIEWED_SIX_LOCALE"]==90
 assert counts[STATUS]==183
 assert sum(counts.values())==502
 assert {r["observanceId"] for r in rows if r["status"]==STATUS}==expected
 assert research<=set(ids),("historical source preview not fully integrated",locale)
 if order is None:order=ids
 else:assert order==ids,("cross-locale drift",locale)
 for row in rows:
  assert row["observanceId"] in all_ids
  assert row["locale"]==locale
  if row["status"]==STATUS:
   assert row["origin"].strip() and row["summary"].strip() and row["hook"].strip()
   assert len(row["quickFacts"])>=2
   assert row["waysToTakePart"]==[] and row["whyItMatters"]==""
   meta=row["aiEditorialProvenance"]
   assert meta["reviewLevel"]=="AI_ONLY_NO_HUMAN_SIGNOFF"
   assert meta["sourceGitBlobSha"] and len(meta["sourceGitBlobSha"])==40
   assert meta["sourceEnglishSha256"] and len(meta["sourceEnglishSha256"])==64
   assert meta["institutionalSourceUrls"]
   if locale not in ("en","it"):
    assert meta["modelEvidence"]["forward"]["modelSha256"]
    assert meta["modelEvidence"]["reverse"]["modelSha256"]
  assert "HUMAN_CERTIFIED" not in row["status"],("no human signoffs",row["observanceId"])
print("AI183_SIX_LOCALE_RUNTIME_PASS",json.dumps({
 "catalog":1111,"uniqueHistoricallyAuthored":485,"richEditorial":502,
 "newAINeuralMachineReviewed":183,
 "remainingSourcePreviewOnly":0,"sixLocales":list(LANG),
 "humanSignoffClaimed":0,
},sort_keys=True))
