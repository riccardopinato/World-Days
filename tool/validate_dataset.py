#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
seed = json.loads((root / 'assets/data/official_core.json').read_text(encoding='utf-8'))
occ = json.loads((root / 'assets/data/occurrences_2026.json').read_text(encoding='utf-8'))

records = seed.get('records', [])
ids = [r.get('id') for r in records]

expected_consumer = {
    'world-cancer-day',
    'safer-internet-day',
    'world-theatre-day',
    'international-dance-day',
    'international-nurses-day',
    'international-museum-day',
    'world-turtle-day',
    'world-ms-day',
    'world-emoji-day',
    'world-suicide-prevention-day',
    'world-alzheimer-s-day',
    'world-heart-day',
    'world-vegan-day',
    'world-kindness-day',
}
assert len(ids) == len(set(ids)), 'duplicate canonical ids'
assert all(ids), 'empty canonical id'
assert len(occ.get('dateIndex', [])) == 365, '2026 date index must cover 365 days'
known = set(ids)
for item in occ.get('occurrences', []):
    assert item.get('observanceId') in known, f"unknown occurrence id: {item.get('observanceId')}"
for record in records:
    authority = record.get('authority') or {}
    officiality = str(authority.get('officiality', ''))
    sources = record.get('sources', [])
    if officiality.startswith('OFFICIAL_'):
        assert any((s.get('tier') == 'A_PRIMARY') for s in sources), record.get('id')
    if officiality in {'RECOGNIZED_NGO', 'POPULAR'}:
        assert any((s.get('tier') == 'D_ORIGINATOR') for s in sources), record.get('id')

assert expected_consumer.issubset(known), f"missing curated consumer ids: {sorted(expected_consumer - known)}"

emoji = next(r for r in records if r.get('id') == 'world-emoji-day')
assert emoji['authority']['officiality'] == 'POPULAR'
cancer = next(r for r in records if r.get('id') == 'world-cancer-day')
assert cancer['authority']['officiality'] == 'RECOGNIZED_NGO'
safer = next(r for r in records if r.get('id') == 'safer-internet-day')
assert safer['authority']['officiality'] == 'OFFICIAL_INSTITUTIONAL'

safer_dates = sorted(
    item['startDate']
    for item in occ.get('occurrences', [])
    if item.get('observanceId') == 'safer-internet-day'
)
assert safer_dates == ['2026-02-10'], safer_dates

print(
    f"dataset ok: {len(records)} records, {len(occ.get('occurrences', []))} occurrences, "
    f"{len(expected_consumer)} curated consumer records, 365 days"
)
