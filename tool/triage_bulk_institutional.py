#!/usr/bin/env python3
"""Deterministic triage of official EU index rows; never autonomously publishes."""
import argparse,json,re,unicodedata
from collections import Counter,defaultdict
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INPUTS=(
 "data/market/candidates/eures_at_be_bg_hr_cy_2026_20261110.json",
 "data/market/candidates/eures_19_countries_2026_20261110.json",
)
CIVIC=("independence","liberation","freedom","resistance","statehood","constitution",
       "restoration","republic","national holiday","king mindaugas","anniversary",
       "victory","armistice","jan hus","sete giugno","set te giugno","cultural",
       "settembris","sete giug","culture and literacy","commemoration")
HIGH_RISK=("substitute","bridging","one off","source date","regional","conflicts")
def norm(value):
 value=unicodedata.normalize("NFKD",value.casefold())
 return " ".join(re.sub(r"[^a-z0-9]+"," ",value).split())
def read(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
def triage():
 batches=[read(path) for path in INPUTS]
 rows=[dict(row) for batch in batches for row in batch["records"]]
 assert len(rows)==290,(len(rows),"source batch drift")
 counts=Counter(norm(r["titleEn"]) for r in rows)
 assert len(counts)==90,(len(counts),"source titles drift")
 seen=set()
 for row in rows:
  key=(row["country"],norm(row["titleEn"]),row["observed2026"])
  assert key not in seen,("duplicate source country+name+date",key)
  seen.add(key)
  assert date.fromisoformat(row["observed2026"]).year==2026
  assert row["primaryLegalSource"] is None
  assert row["recurrenceRule"] is None
  row["sourceLabelFrequency"]=counts[norm(row["titleEn"])]
  row["admissionReady"]=False
  name=norm(row["titleEn"])
  if row.get("sourceQualityFlag"):
   row["triage"]="SOURCE_QUALITY_QUARANTINE"
  elif any(word in name for word in CIVIC):
   row["triage"]="CIVIC_IDENTITY_SOURCE_CHECK"
  elif counts[name]>=3:
   row["triage"]="SHARED_HOLIDAY_DEDUP_REVIEW"
  else:
   row["triage"]="OTHER_NATIONAL_SOURCE_CHECK"
  row["requiredChecks"]=[
    "NATIONAL_PRIMARY_AUTHORITY_AND_JURISDICTION",
    "CANONICAL_ENTITY_OR_ALIAS_DEDUP",
    "RECURRENCE_2026_2028_AND_HOLIDAY_SUBSTITUTIONS",
    "SIX_LOCALE_TITLE_AND_RUNTIME_REGRESSION",
  ]
 labels=Counter(r["triage"] for r in rows)
 country_counts=Counter(r["country"] for r in rows)
 assert len(country_counts)==24
 assert labels["SOURCE_QUALITY_QUARANTINE"]==6
 return {"schemaVersion":1,"pipeline":"RESEARCH_TRIAGE_ONLY","sourceBatchCount":2,
  "sourceRows":291,"invalidDateSourceRows":1,"validIndexRows":290,
  "distinctNormalizedLabels":len(counts),"countries":24,"countsByCountry":dict(sorted(country_counts.items())),
  "countsByTriage":dict(sorted(labels.items())),"candidateAdmissionReady":0,
  "knownScope":"EU EURES country holiday index; not a first-party national establishing act",
  "validationNote":"Non-duplicated 290 index rows are NOT 290 distinct canonical observances. Country-specific legal identities may share titles. None is publishable without independent country authority and migration checks.",
  "items":rows}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",type=Path,default=ROOT/"reports/eures_290_triage.json");args=ap.parse_args()
 data=triage();args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("EURES bulk triage:",data["validIndexRows"],"rows",data["countries"],"countries",data["countsByTriage"])
if __name__=="__main__":main()
