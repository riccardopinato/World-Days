#!/usr/bin/env python3
"""Resolve all reviewable English-fallback titles: 50 Korean civic days + DE SID.

Retain the historically proper name 'Sette Giugno (Malta)' as written.
Run AFTER stage 359 title validator, BEFORE content-pack build.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data"
LOCALES=("en","it","es","fr","de","pt")
SOURCE=ROOT/"data/editorial/localizations/korean_mois_50_sixlocale_20261119.json"
OLD_VERSION="2026.11.19.5"
NEW_VERSION="2026.11.19.6"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def main():
 pack=rd(SOURCE)
 assert pack["schemaVersion"]==1 and pack["count"]==len(pack["records"])==50
 source={r["observanceId"]:r for r in pack["records"]}
 assert len(source)==50
 cat=rd(A/"official_core.json")
 assert cat["datasetVersion"]==OLD_VERSION and len(cat["records"])==947
 recs={r["id"]:r for r in cat["records"]}
 assert len(recs)==947
 docs={l:rd(A/f"editorial_{l}.json") for l in LOCALES}
 maps={l:{x["observanceId"]:x for x in d["entries"]} for l,d in docs.items()}
 assert all(len(maps[l])==docs[l]["entryCount"]==947 for l in LOCALES)
 for id_,row in source.items():
  r=recs[id_]
  assert row["source"] in [s["url"] for s in r["sources"]]
  assert r["countries"]==["KR"] and row["country"]=="KR"
  assert row["canonicalTitleEn"]==r["canonicalTitleEn"]
  assert set(row["localizedTitles"])==set(LOCALES)
  for loc in LOCALES[1:]:
   old=r["localizedTitles"][loc]
   new=row["localizedTitles"][loc]
   assert old==r["canonicalTitleEn"] and new.strip() and old!=new,(id_,loc)
   r["localizedTitles"][loc]=new
   article=maps[loc][id_]
   if article["status"]=="AI_CONTEXTUAL_SIX_LOCALE":
    for key in ("hook","summary","origin","whyThisDate","whyItMatters"):
     if isinstance(article.get(key),str):
      article[key]=article[key].replace(old,new)
    for key in ("quickFacts","waysToTakePart"):
     if isinstance(article.get(key),list):
      article[key]=[v.replace(old,new) if isinstance(v,str) else v for v in article[key]]
 # Internet safety theme: the internationally known English name can remain
 # in parentheses, while the first visible phrase is properly localized.
 sid="safer-internet-day"
 assert sid in recs
 sid_r=recs[sid]
 before=sid_r["localizedTitles"]["de"]
 assert before==sid_r["canonicalTitleEn"]=="Safer Internet Day"
 after="Tag für mehr Sicherheit im Internet (Safer Internet Day)"
 sid_r["localizedTitles"]["de"]=after
 for key in ("hook","summary","origin","whyThisDate","whyItMatters"):
  item=maps["de"][sid]
  if isinstance(item.get(key),str):item[key]=item[key].replace(before,after)
 for key in ("quickFacts","waysToTakePart"):
  item=maps["de"][sid]
  if isinstance(item.get(key),list):
   item[key]=[x.replace(before,after) if isinstance(x,str) else x for x in item[key]]
 cat["datasetVersion"]=NEW_VERSION
 origin=rd(A/"origin_review_index.json")
 assert origin["recordCount"]==947
 origin["datasetVersion"]=NEW_VERSION
 wr(A/"official_core.json",cat)
 wr(A/"origin_review_index.json",origin)
 for loc in LOCALES[1:]:
  wr(A/f"editorial_{loc}.json",docs[loc])
 unchanged={loc:[{"id":r["id"],"title":r["canonicalTitleEn"]}
           for r in cat["records"] if r["localizedTitles"][loc]==r["canonicalTitleEn"]]
           for loc in LOCALES[1:]}
 assert {loc:len(vals) for loc,vals in unchanged.items()}=={
   "it":1,"es":1,"fr":0,"de":1,"pt":1},unchanged
 assert {x["id"] for vals in unchanged.values() for x in vals}=={"mt-sette-giugno"}
 report={"sourceIdsTotal":1111,"published":947,"archived":164,
         "koreanCivicTitlesLocalized":50,"koreanStrings":250,
         "germanSaferInternetDayAdditionalString":1,
         "newLocalizationStringsThisStage":251,
         "overallNewNonEnglishStringsAcrossStages":2046,
         "distinctImprovedNationalAndCulturalIds":409,
         "additionalLocalizedGlobalID":"safer-internet-day",
         "identicalEnglishTitleException":"mt-sette-giugno",
         "stillEnglishEqual":unchanged,
         "humanReviewOrOriginalFoundingHistoryClaim":False}
 path=ROOT/"reports/final_947_title_translation_completion_20261119.json"
 path.parent.mkdir(parents=True,exist_ok=True)
 wr(path,report)
 print("WORLD_DAYS_947_DISPLAY_TITLES_COMPLETE",json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
