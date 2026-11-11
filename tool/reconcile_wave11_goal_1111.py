#!/usr/bin/env python3
"""Wave11 reconciliation: candidate identities do not count as canonical admissions."""
import json,re,unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from market_expansion import all_expansion_rows

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"data/editorial/candidates/wave11_ncca_cultural_anniversaries_20261111.json"
OUT=ROOT/"reports/wave11_goal_1111_reconciliation.json"
def norm(v):
 v=unicodedata.normalize("NFKD",v.casefold())
 return re.sub(r"[^a-z0-9]+","", "".join(ch for ch in v if not unicodedata.combining(ch)))
def event_identity(v):
 x=v.lower()
 action="birth" if "birth" in x or "birthday" in x else "death" if "death" in x else "other"
 x=re.sub(r"(?i)(birth|death)(\s+anniversary)?\s+of\s+","",v)
 x=re.sub(r"(?i)national artist|national living treasure|gamaba|president|philippines","",x)
 return action,norm(x)
def main():
 data=json.loads(INPUT.read_text(encoding="utf-8"))
 prior=[r for r in all_expansion_rows() if r["country"]=="PH" and not r["id"].startswith("ph-w11-")]
 pairs=[]
 for row in data["records"]:
  rule=row["recurrenceRules"][0]
  name=row["sourceTitleOriginal"]
  action,subject=event_identity(name)
  possible=[]
  for prev in prior:
   prevname=prev["canonicalTitleEn"]
   prev_action,prev_subject=event_identity(prevname)
   r=prev["recurrenceRules"][0]
   if prev_action != action:continue
   if r["kind"]!="FIXED_DATE":continue
   if (r["month"],r["day"]) != (rule["month"],rule["day"]):continue
   sim=SequenceMatcher(None,subject,prev_subject).ratio()
   if sim>=0.76:possible.append({"id":prev["id"],"label":prevname,"similarity":round(sim,3)})
  if possible:pairs.append({"candidateId":row["id"],"sourceTitle":name,"possibleExisting":possible})
 result={"target":1111,"mainBaseline":711,"requiredNewCanonical":400,"primaryIndexedResearchRows":len(data["records"]),"possibleAliasOrDuplicateReview":pairs,
 "researchRowsNotReady":len(data["records"]),"additionalSourceQualifiedNewIdsNeededAtLeast":400-len(data["records"])+len(pairs),
 "canonicalAdmittedByThisPR":0,
 "remainingCanonicalAdmissionsNeeded":400,
 "potentialResearchCandidatesAfterSimilarityReviewAtMost":len(data["records"])-len(pairs),
 "countingPolicy":"Research-only candidates contribute ZERO to the canonical catalog until individually admitted. The 256+ discovery estimate assumes 144 future admissions and is NOT the current remaining-admissions count.",
 "note":"Source-only NCCA candidates and Wikidata discovery are not yet accepted into the runtime catalog; avoid 1111 claim before 400 distinct canonical identities are source reviewed, tested, merged."
 }
 assert len(prior)==57,("PH market drift",len(prior))
 assert result["primaryIndexedResearchRows"]==144
 assert result["canonicalAdmittedByThisPR"]==0
 assert result["remainingCanonicalAdmissionsNeeded"]==400
 assert result["additionalSourceQualifiedNewIdsNeededAtLeast"]>=256
 OUT.parent.mkdir(parents=True,exist_ok=True)
 OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("WAVE11_RECONCILIATION",json.dumps({k:v for k,v in result.items() if k!="possibleAliasOrDuplicateReview"},sort_keys=True))
 print("WAVE11_SIMILARITY_FLAGS",json.dumps(pairs[:12],ensure_ascii=False))
if __name__=="__main__":main()
