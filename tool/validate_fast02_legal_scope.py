#!/usr/bin/env python3
"""Fail-closed 10-case legal scope and continuity ledger; no automatic yearly admission."""
from pathlib import Path
from datetime import date
from urllib.parse import urlsplit
import json
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data/research/FAST02_LEGAL_SCOPE_DECISIONS_20261110.json"
EXPECTED={"BD":1,"CA":1,"IN":1,"LA":1,"PH":1,"KH":4,"VN":1}
def main():
 d=json.loads(P.read_text(encoding="utf8"))
 assert d["schemaVersion"]==1 and d["recordCount"]==len(d["records"])==10
 assert d["status"]=="HUMAN_OR_AUTHORITY_REVIEW_REQUIRED"
 seen=set();country={}
 for r in d["records"]:
  key=r["country"],r["title"]
  assert key not in seen
  seen.add(key)
  country[r["country"]]=country.get(r["country"],0)+1
  assert date.fromisoformat(r["date2026"]).year==2026
  url=urlsplit(r["source"])
  assert url.scheme=="https" and url.hostname
  assert len(r["required"])>=55
  assert r["risk"] not in {"APPROVED","ANNUAL_CERTIFIED"}
 assert country==EXPECTED,(country,EXPECTED)
 print("FAST02 LEGAL GATE PASS: 10 source-identified scope/year risks, zero automatic admissions")
if __name__=="__main__":main()
