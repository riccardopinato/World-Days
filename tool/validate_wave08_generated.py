#!/usr/bin/env python3
"""Canadian Heritage Wave08 27 source-level identities in generated catalog."""
import json
from collections import Counter
from pathlib import Path
from market_wave08 import load_wave08,resolve
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
occ=json.loads((ROOT/"assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
known={r["id"]:r for r in catalog["records"]}
assert tuple(map(int,catalog["datasetVersion"].split("."))) >= (2026,11,11,1)
assert len(known)==len(catalog["records"])>=538
assert Counter(r["scope"] for r in known.values())["GLOBAL"]==289
assert Counter(r["scope"] for r in known.values())["NATIONAL"]>=249
assert Counter(r["countries"][0] for r in known.values() if r["scope"]=="NATIONAL")["CA"]==32
for source in load_wave08():
 rid=source["id"];row=known[rid]
 assert row["scope"]=="NATIONAL" and row["countries"]==["CA"]
 assert row["authority"]["officiality"]=="OFFICIAL_INSTITUTIONAL"
 assert row["editorialStatus"]=="STUB"
 assert row.get("introducedYear") is None and row.get("introducedYearSource") is None
 assert row["sources"][0]["tier"]=="A_PRIMARY"
 assert row["sources"][0]["url"]==source["source"]
 assert row["localizedTitles"]==source["localizedTitles"]
 assert row["recurrenceRules"]==source["recurrenceRules"]
 dates=[r["startDate"] for r in occ["occurrences"] if r["observanceId"]==rid]
 assert dates==[resolve(source["recurrenceRules"][0],2026).isoformat()],rid
print("PASS: 27 Canadian Heritage new IDs, 538 total, country market 32, six title locales")
