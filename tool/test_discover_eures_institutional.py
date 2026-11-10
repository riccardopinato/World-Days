#!/usr/bin/env python3
"""Offline regression: duplicate rows, malformed dates, country isolation and year boundary."""
import discover_eures_institutional as mod
html = """<h2>2026 public holidays</h2>
<h3>Austria</h3><table><tr><th>Date</th><th>Holiday</th></tr>
<tr><td>26/10</td><td>National Holiday</td></tr>
<tr><td>26/10</td><td>National Holiday</td></tr>
<tr><td>25/25</td><td>Invalid Holiday</td></tr></table>
<h3>Belgium</h3><table><tr><td>11/11</td><td>Armistice Day</td></tr></table>
<h2>2027 public holidays</h2><h3>Austria</h3>
<table><tr><td>01/01</td><td>Future Record</td></tr></table>"""
records, rejected = mod.parse(html)
assert len(records) == 2, records
assert len(rejected) == 1, rejected
assert {r["country"] for r in records} == {"AT", "BE"}
assert all(r["status"] == "DISCOVERY_ONLY" and r["primaryLegalSource"] is None for r in records)
assert all(r["introducedYear"] is None and r["recurrenceRule"] is None for r in records)
assert not any(r["titleEn"] == "Future Record" for r in records)
print("PASS: bulk importer source isolation, duplicate prevention, invalid dates, no publication")
