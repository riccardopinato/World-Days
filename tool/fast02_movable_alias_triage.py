#!/usr/bin/env python3
"""Batch-classify 62 non-fast candidate dates without inventing annual recurrence.

Must run after the existing research certification and semantic triage scripts.
"""
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
import json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"reports/research_semantic_triage.json"
OUT=ROOT/"reports/research_fast02_movable_alias.json"
FLAGS={"SEMANTIC_GROUP:","MULTIYEAR_DATE_REQUIRES_AUTHORITY",
       "REGIONAL_OR_COMMUNITY_ONLY","ASTRONOMICAL_OFFICIAL_ANNUAL_DECLARATION",
       "INTERCALARY_NOT_ANNUAL","POSSIBLY_2026_ONLY_HOLIDAY",
       "LEGAL_DATE_OR_MONARCH_CHANGE","CHECK_SUBSTITUTE_DATE_NOT_EVENT",
       "SAME_CULTURAL_SUBJECT_AS_GLOBAL_OR_OTHER_NATIONAL_DAY"}
def main():
 data=json.loads(SRC.read_text(encoding="utf8"))
 assert data["recordCount"]==153
 rows=[r for r in data["records"] if r["reviewLane"]=="MANUAL_SEMANTIC_AND_DATE_REVIEW"]
 assert len(rows)==62,len(rows)
 out=[]
 for r in rows:
  flags=r["riskFlags"]
  assert len(flags)>=1,(r["country"],r["title"])
  assert any(f.startswith("SEMANTIC_GROUP:") or f in FLAGS for f in flags)
  assert r["semanticUniqueCertified"] is False
  assert r["multiYearRecurrenceCertified"] is False
  assert r["autoAdmit"] is False
  if any(f.startswith("SEMANTIC_GROUP:") or f=="SAME_CULTURAL_SUBJECT_AS_GLOBAL_OR_OTHER_NATIONAL_DAY" for f in flags):
   lane="IDENTITY_AND_ALIAS_REVIEW"
  elif "INTERCALARY_NOT_ANNUAL" in flags or "ASTRONOMICAL_OFFICIAL_ANNUAL_DECLARATION" in flags or "MULTIYEAR_DATE_REQUIRES_AUTHORITY" in flags:
   lane="OFFICIAL_YEARLY_OVERRIDE_REQUIRED"
  elif "REGIONAL_OR_COMMUNITY_ONLY" in flags:
   lane="REGIONAL_SCOPE_PROOF_REQUIRED"
  else:
   lane="LEGAL_CALENDAR_REVIEW"
  out.append({"country":r["country"],"title":r["title"],"date2026":r["occurrence2026"],
   "reviewLane":lane,"riskFlags":flags,"identityCertified":False,
   "multiYearRecurrenceCertified":False,"sixLocaleEditorialCertified":False,
   "admission":"BLOCKED_RESEARCH_ONLY"})
 assert len(out)==len({(r["country"],r["title"]) for r in out})
 report={"schemaVersion":1,"sourceTotal":153,"complexReviewCount":62,
         "laneCounts":dict(Counter(r["reviewLane"] for r in out)),
         "notes":"Date 2026 evidence is not automatic unique/annual approval; all 62 blocked.",
         "records":out}
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 print("FAST02 MOVABLE/ALIAS GATE PASS:",len(out),report["laneCounts"])
if __name__=="__main__":main()
