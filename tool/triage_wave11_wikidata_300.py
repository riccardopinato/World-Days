#!/usr/bin/env python3
"""Research-only screening of 300 P837 Wikidata leads against the actual generated catalog.

Output is diagnostic; Wikidata P837 does not verify a government's public holiday,
legal status, correct contemporary date or first-introduced year.
"""
import json,re,unicodedata
from pathlib import Path
from difflib import SequenceMatcher
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"data/editorial/candidates/wave11_wikidata_300_discovery_20261111.json"
CATALOG=ROOT/"assets/data/official_core.json"
OUTPUT=ROOT/"reports/wave11_300_discovery_triage.json"
def normalized(s):
 s=unicodedata.normalize("NFKD",str(s or "").casefold())
 return re.sub(r"[^a-z0-9]+"," ", "".join(c for c in s if not unicodedata.combining(c))).strip()
def loose(s):
 s=normalized(s)
 s=re.sub(r"\s*(?:—|-|in|of)\s*(?:philippines|south korea|canada|italy|france|germany|united states|uk|japan|sweden|norway|finland|poland)$","",s)
 s=re.sub(r"^(the |international |world |national )","",s)
 return s.strip()
def screen():
 base=json.loads(CATALOG.read_text(encoding="utf-8"))["records"]
 rows=json.loads(INPUT.read_text(encoding="utf-8"))["records"]
 titles={}
 for rec in base:
  for name in [rec["canonicalTitleEn"],*rec.get("aliases",[])]:
   x=loose(name)
   if x and len(x)>3:titles.setdefault(x,set()).add(rec["id"])
 diagnostics=[]
 counts=Counter()
 for row in rows:
  title=row["itemLabel"]
  candidate=loose(title)
  matches=sorted(titles.get(candidate,set()))
  near=[]
  if not matches and len(candidate)>8:
   for key,ids in titles.items():
    if abs(len(candidate)-len(key))>11:continue
    score=SequenceMatcher(None,candidate,key).ratio()
    if score>=.92:near.extend((score, key, list(ids)[:2]))
   near.sort(reverse=True)
  quality=[]
  if matches:quality.append("EXACT_OR_NORMALIZED_EXISTING_TITLE")
  if near:quality.append("SIMILAR_EXISTING_TITLE_REVIEW")
  if not row.get("countryLabel"):quality.append("SCOPE_NOT_ESTABLISHED")
  if re.search(r"feast|christmas|new year|easter|holiday|saint|hike|independence day|national day",title,re.I):
   quality.append("CULTURAL_OR_DATE_CONVENTION_REVIEW")
  quality.append("NO_PRIMARY_OR_ORIGINATOR_EVIDENCE")
  counts[quality[0]]+=1
  diagnostics.append({"wikidataQid":row["wikidataQid"],"label":title,"date":f"{row['month']:02d}-{row['day']:02d}",
   "existingIdMatch":matches[:10],"nearTitleMatch":[{"similarity":round(score,3),"label":key,"ids":ids} for score,key,ids in near[:4]],
   "flags":quality,"publishable":False})
 assert len(diagnostics)==300
 out={"schemaVersion":1,"total":300,"allUnadmitted":True,"mainBaseline":711,"branchCatalogSnapshot":len(base),
  "flagsSummary":dict(counts),"records":diagnostics,
  "status":"TRIAGE_NOT_IN_CANONICAL","instruction":"Primary-source identity, originator, recurrence and country/officiality remain mandatory before admission; do not merge on quota of this report."}
 OUTPUT.parent.mkdir(parents=True,exist_ok=True)
 OUTPUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("Wave11 P837 300 triage",json.dumps({k:v for k,v in out.items() if k!="records"},ensure_ascii=False))
 return out
if __name__=="__main__":screen()
