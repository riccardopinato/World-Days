#!/usr/bin/env python3
"""Validate one exactly-100 research intake without promoting any candidate into runtime."""
import json,re
from collections import Counter
from pathlib import Path
from datetime import date
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/"data/editorial/candidates/institutional_100_ca_gb_20261111.json"
batch=json.loads(path.read_text(encoding="utf-8"))
assert batch["schemaVersion"]==1
assert batch["batchId"]=="WD-CANDIDATES-100-CA-GB-20261111"
assert batch["stage"]=="INSTITUTIONAL_INDEX_RESEARCH_NOT_RUNTIME"
rows=batch["rows"]
assert batch["count"]==len(rows)==100
assert batch["sourceCounts"]=={"CA":46,"GB":54}
assert Counter(r["market"] for r in rows)=={"CA":46,"GB":54}
assert len({(r["market"],r["candidateId"]) for r in rows})==100
hosts={"CA":"www.canada.ca","GB":"www.camden.gov.uk"}
date_count=0
for row in rows:
 assert row["publicationStatus"]=="CANDIDATE_NOT_IN_CANONICAL"
 assert not row["authorityVerifiedForIdentity"]
 assert not row["recurrenceVerifiedBeyond2026"]
 assert not row["dedupVerified"]
 assert row["introducedYear"] is None
 assert row["richEditorialStatus"]=="NOT_REVIEWED"
 assert urlparse(row["sourceUrl"]).hostname==hosts[row["market"]]
 raw=row["sourceDateNotation"]
 if re.fullmatch(r"\d{2}-\d{2}",raw):
  month,day=map(int,raw.split("-"))
  date(2026,month,day)
  date_count+=1
 else:
  assert re.fullmatch(r"\d{2}-(?:NTH-[A-Z]{3}-\d|MON-BEFORE-25)",raw),raw
assert date_count>=95
print("PASS: exactly 100 source-index candidates, no authority claim, no runtime publication")
