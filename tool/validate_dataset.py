#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
seed = json.loads((root / 'assets/data/official_core.json').read_text(encoding='utf-8'))
occ = json.loads((root / 'assets/data/occurrences_2026.json').read_text(encoding='utf-8'))

records = seed.get('records', [])
ids = [r.get('id') for r in records]
visual_keys = {'planet','health','people','learning','culture','food','future','community'}
title_locales = {'en', 'it', 'es', 'fr', 'de', 'pt'}

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

expected_market = {
    'italys-day-of-remembrance': 'IT',
    'italian-republic-day': 'IT',
    'national-day-of-spain': 'ES',
    'constitution-day-spain': 'ES',
    'national-day-of-the-resistance-france': 'FR',
    'french-national-day': 'FR',
    'german-unity-day': 'DE',
    'portugal-day': 'PT',
    'republic-day-portugal': 'PT',
    'armed-forces-day-uk': 'GB',
    'martin-luther-king-jr-day': 'US',
    'memorial-day-us': 'US',
    'independence-day-us': 'US',
    'veterans-day-us': 'US',
}
assert len(ids) == len(set(ids)), 'duplicate canonical ids'
assert all(ids), 'empty canonical id'
assert len(occ.get('dateIndex', [])) == 365, '2026 date index must cover 365 days'
known = set(ids)
for item in occ.get('occurrences', []):
    assert item.get('observanceId') in known, f"unknown occurrence id: {item.get('observanceId')}"
for record in records:
    assert record.get('visualKey') in visual_keys, (record.get('id'), record.get('visualKey'))
    localized_titles = record.get('localizedTitles') or {}
    assert set(localized_titles) == title_locales, (
        record.get('id'),
        sorted(localized_titles),
    )
    assert localized_titles['en'] == record.get('canonicalTitleEn'), record.get('id')
    assert all(str(value).strip() for value in localized_titles.values()), record.get('id')
    authority = record.get('authority') or {}
    officiality = str(authority.get('officiality', ''))
    sources = record.get('sources', [])
    if officiality.startswith('OFFICIAL_'):
        assert any((s.get('tier') == 'A_PRIMARY') for s in sources), record.get('id')
    if officiality in {'RECOGNIZED_NGO', 'POPULAR'}:
        assert any((s.get('tier') == 'D_ORIGINATOR') for s in sources), record.get('id')
    if record.get('scope') == 'NATIONAL':
        countries = record.get('countries', [])
        assert len(countries) == 1, f"national record must have one country: {record.get('id')}"
        assert countries[0] in {'IT', 'ES', 'FR', 'DE', 'PT', 'GB', 'US'}, record.get('id')
        assert officiality == 'OFFICIAL_INSTITUTIONAL', record.get('id')
        assert any((s.get('tier') == 'A_PRIMARY') for s in sources), record.get('id')

assert expected_consumer.issubset(known), f"missing curated consumer ids: {sorted(expected_consumer - known)}"
assert set(expected_market).issubset(known), f"missing market ids: {sorted(set(expected_market) - known)}"
for market_id, country in expected_market.items():
    record = next(r for r in records if r.get('id') == market_id)
    assert record['scope'] == 'NATIONAL', market_id
    assert record['countries'] == [country], (market_id, record['countries'])

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

market_vectors = {
    'martin-luther-king-jr-day': ['2026-01-19'],
    'memorial-day-us': ['2026-05-25'],
    'armed-forces-day-uk': ['2026-06-27'],
    'italian-republic-day': ['2026-06-02'],
    'national-day-of-spain': ['2026-10-12'],
}
for observance_id, expected_dates in market_vectors.items():
    actual = sorted(
        item['startDate']
        for item in occ.get('occurrences', [])
        if item.get('observanceId') == observance_id
    )
    assert actual == expected_dates, (observance_id, actual, expected_dates)

print(
    f"dataset ok: {len(records)} records, {len(occ.get('occurrences', []))} occurrences, "
    f"{len(expected_consumer)} curated consumer records, {len(expected_market)} market records, "
    f"{len(title_locales)} title locales, 365 days"
)
