#!/usr/bin/env python3
"""Verify exactly five new complete six-language articles after the 502 baseline."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LANG = ("en", "it", "es", "fr", "de", "pt")
cohort = json.loads((ROOT / "data/editorial/waves/wave21_fasttrack_first5_ids.json").read_text(encoding="utf-8"))
ids = cohort["observanceIds"]
assert len(ids) == len(set(ids)) == 5
observed = None
for locale in LANG:
    document = json.loads((ROOT / f"assets/data/editorial_{locale}.json").read_text(encoding="utf-8"))
    records = document["entries"]
    sequence = [r["observanceId"] for r in records]
    assert len(sequence) == len(set(sequence)) == document["entryCount"] == 507
    assert sequence[-5:] == ids
    if observed is None: observed = sequence
    else: assert observed == sequence, ("translation order mismatch", locale)
    for row in records[-5:]:
        assert row["locale"] == locale
        assert row["status"] == "AI_SOURCE_REVIEWED_SIX_LOCALE"
        assert row["hook"] and row["summary"] and len(row["origin"]) >= 140
        assert len(row["quickFacts"]) == 3
        assert row["institutionalSourceUrls"]
print("FASTTRACK_SIX_LOCALE_507_PASS: 507 complete / 0 IT-EN only / 604 pending")
