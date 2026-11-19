#!/usr/bin/env python3
"""Apply 43 six-locale NCCA title translations to the 947 published catalog."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data"
SRC=ROOT/"data/editorial/localizations/ph_ncca_title_43_sixlocale_20261119.json"
LANG=("en","it","es","fr","de","pt")
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def main():
 src=rd(SRC)
 assert src["count"]==len(src["entries"])==43
 cat=rd(A/"official_core.json")
 recs={r["id"]:r for r in cat["records"]}
 assert len(recs)==947
 docs={l:rd(A/f"editorial_{l}.json") for l in LANG[1:]}
 ids={r["observanceId"] for r in src["entries"]}
 assert len(ids)==43 and ids<=recs.keys()
 for row in src["entries"]:
  rid=row["observanceId"]
  r=recs[rid]
  assert r["countries"]==["PH"] and r["canonicalTitleEn"]==row["canonicalTitleEn"]
  assert row["source"] in [s["url"] for s in r["sources"]]
  assert r["localizedTitles"]["en"]==row["localizedTitles"]["en"]
  for l in LANG[1:]:
   old=r["localizedTitles"][l];t=row["localizedTitles"][l]
   assert old==row["canonicalTitleEn"] and t!=old,(rid,l)
   assert t.strip()
   r["localizedTitles"][l]=t
   matching=[x for x in docs[l]["entries"] if x["observanceId"]==rid]
   assert len(matching)==1
   entry=matching[0]
   if entry["status"]=="AI_CONTEXTUAL_SIX_LOCALE":
    for key in ("hook","summary","origin","whyThisDate","whyItMatters"):
     if isinstance(entry.get(key),str):entry[key]=entry[key].replace(old,t)
    for key in ("quickFacts","waysToTakePart"):
     if isinstance(entry.get(key),list):
      entry[key]=[x.replace(old,t) if isinstance(x,str) else x for x in entry[key]]
 wr(A/"official_core.json",cat)
 for l in LANG[1:]:wr(A/f"editorial_{l}.json",docs[l])
 report={"catalog":947,"translatedNccaObservanceTitles":43,
         "newLanguageTitleStrings":215,
         "combinedNationalAndNccaTranslatedIDs":256,
         "combinedNonEnglishTitleStrings":1280}
 out=ROOT/"reports/ph_ncca_title_43_localizations.json"
 out.parent.mkdir(parents=True,exist_ok=True)
 wr(out,report)
 print("PH_NCCA_43_TITLE_SIX_LOCALE_PASS",json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
