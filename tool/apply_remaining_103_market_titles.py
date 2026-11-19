#!/usr/bin/env python3
"""Publish source-anchored non-English titles for 62 EU civic + 41 PH national days.

Must run after 153+11 public scope filters and 213+43 prior title localizers.
Bump offline/OTA content version only once after full 103-title change.
"""
from collections import Counter
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/data"
SOURCES=(
 ROOT/"data/editorial/localizations/market_wave09_62_sixlocale_20261119.json",
 ROOT/"data/editorial/localizations/ph_wave10_41_sixlocale_20261119.json",
)
LOCALES=("en","it","es","fr","de","pt")
EXPECTED=103
TOTAL=947
NEW_VERSION="2026.11.19.5"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main():
 batches=[rd(p) for p in SOURCES]
 assert [p["count"] for p in batches]==[62,41]
 items=[r for batch in batches for r in batch["records"]]
 assert len(items)==len({r["observanceId"] for r in items})==EXPECTED
 cat=rd(ASSETS/"official_core.json")
 assert len(cat["records"])==TOTAL and cat["datasetVersion"]=="2026.11.19.4"
 lookup={r["id"]:r for r in cat["records"]}
 assert len(lookup)==TOTAL
 docs={l:rd(ASSETS/f"editorial_{l}.json") for l in LOCALES}
 reference=None
 per_locale={}
 for loc,d in docs.items():
  assert d["entryCount"]==len(d["entries"])==TOTAL
  ids=[r["observanceId"] for r in d["entries"]]
  assert len(set(ids))==TOTAL
  if reference is None:reference=ids
  else:assert reference==ids
  per_locale[loc]={r["observanceId"]:r for r in d["entries"]}
 assert set(lookup)==set(reference)
 for row in items:
  ident=row["observanceId"]
  assert ident in lookup
  record=lookup[ident]
  assert record["countries"]==[row["country"]]
  assert record["canonicalTitleEn"]==row["canonicalTitleEn"]
  assert row["source"] in [s["url"] for s in record["sources"]]
  assert set(row["localizedTitles"])==set(LOCALES)
  assert row["localizedTitles"]["en"]==record["canonicalTitleEn"]
  for loc in LOCALES[1:]:
   before=record["localizedTitles"][loc]
   after=row["localizedTitles"][loc]
   assert before==record["canonicalTitleEn"],(ident,loc,"unexpected prior localized title")
   assert after.strip() and after!=before
   record["localizedTitles"][loc]=after
   article=per_locale[loc][ident]
   if article["status"]=="AI_CONTEXTUAL_SIX_LOCALE":
    for key in ("hook","summary","origin","whyThisDate","whyItMatters"):
     if isinstance(article.get(key),str):article[key]=article[key].replace(before,after)
    for key in ("quickFacts","waysToTakePart"):
     if isinstance(article.get(key),list):
      article[key]=[x.replace(before,after) if isinstance(x,str) else x for x in article[key]]
 cat["datasetVersion"]=NEW_VERSION
 origin_idx=rd(ASSETS/"origin_review_index.json")
 assert origin_idx["recordCount"]==TOTAL
 origin_idx["datasetVersion"]=NEW_VERSION
 wr(ASSETS/"official_core.json",cat)
 wr(ASSETS/"origin_review_index.json",origin_idx)
 for loc in LOCALES[1:]:wr(ASSETS/f"editorial_{loc}.json",docs[loc])
 fallback={loc:sum(r["localizedTitles"]["en"]==r["localizedTitles"][loc] for r in lookup.values())
           for loc in LOCALES[1:]}
 report={
   "publishedCanonicalIDs":TOTAL,"newSourceAnchoredTitles":EXPECTED,
   "newNonEnglishTitleTranslations":EXPECTED*5,
   "priorSourceAnchoredTitles":256,
   "newTotalSourceAnchoredLocalizedTitleIDs":256+EXPECTED,
   "newTotalNonEnglishTitleTranslations":(256+EXPECTED)*5,
   "remainingEnglishEqualTitlesByLocale":fallback,
   "originSpecificNewStories":0,
   "disclosure":"Some proper names remain identical across languages legitimately; 'English-equal' is a heuristic requiring individual checking, not proof of untranslated text.",
 }
 out=ROOT/"reports/remaining_103_market_title_localizations_20261119.json"
 out.parent.mkdir(parents=True,exist_ok=True)
 wr(out,report)
 print("MARKET_WAVE09_WAVE10_103_SIX_LOCALE_PASS",json.dumps(report,ensure_ascii=False,sort_keys=True))
if __name__=="__main__":main()
