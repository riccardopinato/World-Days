#!/usr/bin/env python3
import json
from datetime import date,timedelta
from urllib.parse import urlsplit
from pathlib import Path
from collections import Counter
p=Path(__file__).resolve().parents[1]/"data/research/UNESCO_PRIMARY_SOURCE_AUDIT_20261110.json"
d=json.loads(p.read_text(encoding="utf-8"))
assert d["schemaVersion"]==1 and d["count"]==len(d["records"])==2
assert d["institution"]=="UNESCO"
assert d["certification"]=="PRIMARY_SOURCE_DATE_AND_AUTHORITY_ONLY"
assert Counter(r["rule"] for r in d["records"])=={'FIXED_DATE':1,'NTH_WEEKDAY':1}
assert len({r["name"] for r in d["records"]})==2
for r in d["records"]:
  assert r["status"]=="SOURCE_DATE_AUTHENTICATED_NOT_MERGED"
  h=urlsplit(r["source"])
  assert h.scheme=="https" and h.hostname.endswith("unesco.org")
  assert len(r["note"])>35
  kind=r["rule"]
  assert kind in ("FIXED_DATE","NTH_WEEKDAY","LAST_WEEKDAY")
  for year in (2026,2027,2028):
    if kind=="FIXED_DATE":
      date(year,r["month"],r["day"])
    elif kind=="LAST_WEEKDAY":
      assert r["month"]==1 and r["day"]==7
      day=date(year,2,1)-timedelta(days=1)
      while day.isoweekday()!=7:day-=timedelta(days=1)
    else:
      assert r["month"]==11 and r["day"]==4
      day=date(year,11,1)
      while day.isoweekday()!=4:day+=timedelta(days=1)
print("INSTITUTION SOURCE PASS: UNESCO 2 verified names and documented recurring dates; no release/editorial signoff")
