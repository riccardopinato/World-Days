#!/usr/bin/env python3
"""Validate 65 EU EURES source rows as quarantined research candidates, never publish."""
import json
from collections import Counter
from datetime import date
from pathlib import Path

root=Path(__file__).resolve().parents[1]
batch=json.loads((root/"data/market/candidates/eures_at_be_bg_hr_cy_2026_20261110.json").read_text(encoding="utf-8"))
assert batch["publicationStatus"]=="NOT_IMPORTED_UNAPPROVED"
assert batch["totalSourceRows"]==65
assert batch["validIndexCandidates"]==len(batch["records"])==64
assert len(batch["invalidSourceRows"])==1
assert batch["invalidSourceRows"][0]["rawDate"]=="25/25"
assert set(batch["sourceCountries"])=={"AT","BE","BG","HR","CY"}
assert Counter(r["country"] for r in batch["records"])=={"AT":13,"BE":11,"BG":12,"HR":13,"CY":15}
keys=set()
for row in batch["records"]:
    assert row["sourceUrl"]=="https://eures.europa.eu/eures-services/chat-eures-advisers/public-holidays-calendar_en"
    assert row["primaryLegalSource"] is None
    assert row["recurrenceRule"] is None
    assert row["introducedYear"] is None
    assert row["scope"]=="RESEARCH_ONLY"
    assert row["editorialStatus"]=="NOT_REVIEWED"
    assert date.fromisoformat(row["observed2026"]).year==2026
    ident=(row["country"],row["observed2026"],row["titleEn"].casefold())
    assert ident not in keys,ident
    keys.add(ident)
print("PASS: 64 EURES index-only rows, 1 invalid date quarantined, no catalog publication")
