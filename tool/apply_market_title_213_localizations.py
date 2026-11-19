#!/usr/bin/env python3
"""Apply 213 reviewed six-locale country/title localizations to published pack.

Run AFTER 153+11 scope curations, BEFORE content pack build. Only changes
consumer-facing static titles and the same title in existing contextual cards.
No machine translation at runtime, no reclassification as new historical origins.
"""
from collections import Counter
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/data"
LOCAL=ROOT/"data/editorial/localizations/market_title_213_sixlocale_20261119.json"
LANG=("en","it","es","fr","de","pt")
TARGET=213
N=947
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main():
 payload=rd(LOCAL)
 assert payload["schemaVersion"]==1 and payload["count"]==len(payload["entries"])==TARGET
 assert set(payload["locales"])==set(LANG)
 translated={x["observanceId"]:x for x in payload["entries"]}
 assert len(translated)==TARGET
 cat=rd(ASSETS/"official_core.json")
 by_id={x["id"]:x for x in cat["records"]}
 assert len(by_id)==N
 assert set(translated)<=set(by_id)
 docs={loc:rd(ASSETS/f"editorial_{loc}.json") for loc in LANG}
 by_ed={loc:{x["observanceId"]:x for x in docs[loc]["entries"]} for loc in LANG}
 for loc in LANG:
  assert docs[loc]["entryCount"]==len(by_ed[loc])==N
 counts=Counter()
 for rid,row in translated.items():
  rec=by_id[rid]
  assert row["canonicalTitleEn"]==rec["canonicalTitleEn"]
  assert rec["countries"]==[row["country"]]
  assert row["source"] in [x["url"] for x in rec["sources"]]
  assert set(row["localizedTitles"])==set(LANG)
  assert rec["localizedTitles"]["en"]==row["localizedTitles"]["en"]
  for loc in LANG[1:]:
   old=rec["localizedTitles"][loc]
   target=row["localizedTitles"][loc]
   assert target.strip() and old==row["canonicalTitleEn"],(rid,loc,"unexpected prior translation")
   assert target!=row["canonicalTitleEn"],(rid,loc,"English fallback not translated")
   rec["localizedTitles"][loc]=target
   counts[loc]+=1
   ed=by_ed[loc][rid]
   if ed["status"]=="AI_CONTEXTUAL_SIX_LOCALE":
    for key in ("hook","summary","origin","whyThisDate","whyItMatters"):
     if isinstance(ed.get(key),str):
      ed[key]=ed[key].replace(row["canonicalTitleEn"],target)
    for key in ("quickFacts","waysToTakePart"):
     if isinstance(ed.get(key),list):
      ed[key]=[v.replace(row["canonicalTitleEn"],target) if isinstance(v,str) else v for v in ed[key]]
 wr(ASSETS/"official_core.json",cat)
 for loc in LANG[1:]:
  wr(ASSETS/f"editorial_{loc}.json",docs[loc])
 assert counts==Counter({loc:TARGET for loc in LANG[1:]}),counts
 missing={loc:sum(r["localizedTitles"][loc]==r["localizedTitles"]["en"]
                  for r in cat["records"]) for loc in LANG[1:]}
 report={"catalog":N,"localizedTitleRecordsImproved":TARGET,
         "newTitleTranslations":TARGET*5,
         "source":str(LOCAL.relative_to(ROOT)),
         "languageChangedCounts":dict(counts),
         "remainingUntranslatedTitleEqualsEnglish":missing,
         "caution":"Identical proper names can be legitimate; remaining English-exact titles require individual review, not claims of complete native translation."}
 path=ROOT/"reports/market_title_213_localization.json"
 path.parent.mkdir(parents=True,exist_ok=True)
 wr(path,report)
 print("MARKET_TITLE_213_TRANSLATION_PASS",json.dumps(report,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":main()
