#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
seed = json.loads((root / 'assets/data/official_core.json').read_text(encoding='utf-8'))
occ = json.loads((root / 'assets/data/occurrences_2026.json').read_text(encoding='utf-8'))

records = seed.get('records', [])
ids = [r.get('id') for r in records]
assert len(ids) == len(set(ids)), 'duplicate canonical ids'
assert all(ids), 'empty canonical id'
assert len(occ.get('dateIndex', [])) == 365, '2026 date index must cover 365 days'
known = set(ids)
for item in occ.get('occurrences', []):
    assert item.get('observanceId') in known, f"unknown occurrence id: {item.get('observanceId')}"
for record in records:
    authority = record.get('authority') or {}
    if str(authority.get('officiality', '')).startswith('OFFICIAL_'):
        assert any((s.get('tier') == 'A_PRIMARY') for s in record.get('sources', [])), record.get('id')

print(f"dataset ok: {len(records)} records, {len(occ.get('occurrences', []))} occurrences, 365 days")
