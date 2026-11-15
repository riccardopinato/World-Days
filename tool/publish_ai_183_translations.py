#!/usr/bin/env python3
"""World Days: publish only fully AI-reviewed translations of 183 prewritten histories.

Run strictly AFTER the existing 319 six-language editorial imports.
AI certification describes neural translation, a separate reverse-neural
check, source-preserving prose/years and per-locale QA. It is NOT independent
human native-language verification nor a fresh official-site fact audit.
"""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/editorial/published/ai_183_sixlocale_reviewed.json"
DATA=ROOT/"assets/data"
REPORT=ROOT/"reports/ai_183_runtime_import.json"
LANG=("en","it","es","fr","de","pt")
YEARS=re.compile(r"\b(?:18|19|20)\d{2}\b")
LABELS={
 "en":"Originating or supporting institutions",
 "it":"Enti promotori o sostenitori",
 "es":"Instituciones promotoras o participantes",
 "fr":"Institutions à l'origine ou associées",
 "de":"Initiierende oder beteiligte Institutionen",
 "pt":"Instituições promotoras ou participantes",
}
STATUS="AI_CERTIFIED_TRANSLATION_SIX_LOCALE"

def read(path):
 return json.loads(path.read_text(encoding="utf-8"))

def fingerprint(obj):
 return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True).encode()).hexdigest()

def main():
 if not SOURCE.is_file():
  raise SystemExit("AI183 review snapshot absent; never auto-certify from English fallback")
 pack=read(SOURCE)
 assert pack["schemaVersion"]==1 and pack["scope"]=="WORLD_DAYS_EXISTING_183_EN_IT_HISTORY_AI_SIX_LOCALE"
 assert pack["status"]=="AI_MACHINE_TRANSLATION_SOURCE_CHRONOLOGY_PASSED"
 assert pack["expectedCount"]==pack["recordCount"]==183
 assert pack["originalRichEditorialCount"]==319 and pack["catalogTotal"]==1111
 assert pack["notHumanFactCertified"] is True
 assert pack["originalSourceUrlsNotIndependentlyRefetched"] is True
 assert set(pack["models"])==set(LANG)-{"en","it"}
 assert all(model["forward"]["modelSha256"] and model["reverse"]["modelSha256"] for model in pack["models"].values())
 observed=set()
 data={}
 for original in pack["records"]:
  oid=original["observanceId"]
  assert oid not in observed
  observed.add(oid)
  assert original["reviewStatus"]=="AI_MACHINE_TRANSLATION_SOURCE_CHRONOLOGY_PASSED"
  assert set(original["locale"])==set(LANG)
  assert set(original["reviewEvidence"])=={"es","fr","de","pt"}
  assert original["sourceUrls"] and all(urlsplit(u).scheme=="https" and urlsplit(u).netloc for u in original["sourceUrls"])
  path=ROOT/original["sourceFile"]
  assert path.is_file() and path.suffix==".json" and "origin_stories_" in path.name
  primary=next((r for r in read(path)["records"] if r["observanceId"]==oid),None)
  assert primary is not None
  for field in ("introducedYear","firstObservedYear"):
   assert original[field]==primary[field], (oid,field)
  assert original["sourceUrls"]==primary["sources"]
  assert original["sourceEnglishSha256"]==fingerprint(primary["locale"]["en"])
  for locale in ("en","it"):
   assert original["locale"][locale]==primary["locale"][locale]
  for locale in LANG:
   t=original["locale"][locale]
   assert all(isinstance(t.get(k),str) and len(t[k].strip())>24
              for k in ("heading","origin","promoter","purpose")), (oid,locale)
   assert len(t["origin"])>=75 and 2<=len(t["facts"])<=5
   assert all(isinstance(f,str) and len(f.strip())>=20 for f in t["facts"])
   if locale not in ("en","it"):
    proof=original["reviewEvidence"][locale]
    assert proof["issues"]==[]
    assert proof["languageClassified"]==locale and proof["languageConfidence"]>=0.70
    assert proof["roundtripMinRecall"]>=0.20
    actualYears=set(YEARS.findall(" ".join([t["origin"],t["purpose"],*t["facts"]])))
    originalYears=set(YEARS.findall(" ".join([
      original["locale"]["en"]["origin"],original["locale"]["en"]["purpose"],
      *original["locale"]["en"]["facts"]])))
    assert actualYears==originalYears,(oid,locale,"year drift")
  data[oid]=original
 assert len(data)==183

 # Origin stories are already available and must retain their authorial
 # identity, source notes, source URLs and unknown initial celebration years.
 original=None
 for locale in LANG:
  file=DATA/f"editorial_{locale}.json"
  doc=read(file)
  old=doc["entries"]
  ids=[r["observanceId"] for r in old]
  assert doc["entryCount"]==len(old)==len(set(ids))==319
  assert set(ids).isdisjoint(data)
  if original is None:original=ids
  else:assert original==ids,("locale order drift",locale)
  extra=[]
  for oid,row in sorted(data.items()):
   t=row["locale"][locale]
   # The Irish St Brigid statutory holiday already has six source-written
   # translations. Preserve those originals, using the second AI-model
   # translation as a corroborating check instead of replacing prior prose.
   preserved=False
   if oid=="ie-w13-eures-st-brigid-s-day" and locale in ("es","fr","de","pt"):
    source_record=next(x for x in read(ROOT/row["sourceFile"])["records"] if x["observanceId"]==oid)
    t=source_record["locale"][locale]
    assert set(YEARS.findall(" ".join([t["origin"],t["purpose"],*t["facts"]])))==set(
      YEARS.findall(" ".join([row["locale"]["en"]["origin"],row["locale"]["en"]["purpose"],*row["locale"]["en"]["facts"]]))
    )
    preserved=True
   origin=t["origin"].strip()+"\n\n"+LABELS[locale]+": "+t["promoter"].strip()
   extra.append({
    "observanceId":oid,
    "locale":locale,
    "translationOf":"en" if locale!="en" else None,
    "status":STATUS,
    "hook":t["heading"].strip(),
    "summary":t["purpose"].strip(),
    "whyThisDate":"",
    "origin":origin,
    "whyItMatters":"",
    "quickFacts":[f.strip() for f in t["facts"]],
    "waysToTakePart":[],
    "relatedObservanceIds":[],
    "lastReviewedAt":"2026-11-15",
    "sourcePolicy":"AI-only neural-translation + independently backtranslated source and chronology QA; not human fact/language certification.",
    "aiEditorialProvenance":{
       "originFile":row["sourceFile"],
       "sourceGitBlobSha":row["sourceGitBlobSha"],
       "sourceEnglishSha256":row["sourceEnglishSha256"],
       "institutionalSourceUrls":row["sourceUrls"],
       "reviewAuthority":pack["reviewAuthority"],
       "reviewLevel":"AI_ONLY_NO_HUMAN_SIGNOFF",
       "modelEvidence":pack["models"].get(locale),
       "previouslySourceLocalizedPreserved":preserved,
    }
   })
  doc["entries"]=old+extra
  doc["entryCount"]=len(doc["entries"])
  doc["aiNeuralTranslationReviewedCount"]=183
  assert doc["entryCount"]==502
  file.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 REPORT.parent.mkdir(parents=True,exist_ok=True)
 report={
  "catalogTotal":1111,
  "historicallyPreparedUniqueIDs":485,
  "richBefore":319,
  "addedAITranslationCertified":183,
  "totalRich":502,
  "remainingBilingualOnlyResearch":0,
  "modelCertificationScope":"AI_NEURAL_TRANSLATION_BACKTRANSLATION_SOURCE_AND_YEAR_GATES",
  "notHumanFactCertified":True,
  "locales":list(LANG),
  "reviewSnapshot":SOURCE.relative_to(ROOT).as_posix(),
 }
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("AI183_RUNTIME_IMPORT_OK",json.dumps(report,sort_keys=True))

if __name__=="__main__":main()
