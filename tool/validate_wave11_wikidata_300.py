#!/usr/bin/env python3
"""Quality gate for 300 Wikidata discovery leads; absolutely no canonical import.

WDQS P837 can have wrong dates, multiple jurisdiction dates and historical feasts.
The 300 rows are source-level research candidates, not 300 published observances.
"""
import json,re
from pathlib import Path
from collections import Counter
from datetime import date
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/"data/editorial/candidates/wave11_wikidata_300_discovery_20261111.json"

def main():
 data=json.loads(FILE.read_text(encoding="utf8"))
 rows=data["records"]
 assert data["schemaVersion"]==1
 assert data["batchId"]=="wave11_300_wikidata_discovery_20261111"
 assert data["count"]==len(rows)==300
 assert data["discoveryOnly"] is True
 assert data["canBeAutoPublished"] is False
 assert data["baselineMain"]==711
 assert data["stagedCanonicalOnBranchAtCreation"]==855
 qids=[]
 for r in rows:
  assert re.fullmatch(r"Q[0-9]+",r["wikidataQid"])
  assert urlparse(r["discoveryUrl"]).netloc=="www.wikidata.org"
  assert r["discoveryUrl"]=="https://www.wikidata.org/wiki/"+r["wikidataQid"]
  assert r["wikidataQueryProperty"]=="P837"
  assert r["sourceType"]=="C_DISCOVERY_UNVERIFIED"
  assert r["primarySource"] is None
  assert r["publishable"] is False
  assert r["authorityVerified"] is False
  assert r["recurrenceVerifiedBeyondWikidata"] is False
  assert r["duplicateSemanticsVerified"] is False
  assert r["editorialStatus"]=="RESEARCH_ONLY"
  assert r["itemLabel"].strip()
  for year in (2026,2027,2028):
   d=date(year,r["month"],r["day"])
   assert d.year==year
  qids.append(r["wikidataQid"])
 assert len(set(qids))==len(qids), "Wikidata concept duplicate within 300 selection"
 assert data["excludedCounts"]["raw"]>=len(rows)
 assert data["excludedCounts"]["semanticLabelDeduped"]>=len(rows)
 print("PASS: 300 unique Wikidata discovery concepts quarantined, no publication permissions")
if __name__=="__main__":main()
