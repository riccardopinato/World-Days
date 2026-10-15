#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'assets' / 'data' / 'official_core.json'
EDITORIAL = ROOT / 'assets' / 'data' / 'editorial_en.json'

catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
editorial = json.loads(EDITORIAL.read_text(encoding='utf-8'))

known = {item['id'] for item in catalog.get('records', [])}
entries = editorial.get('entries', [])
ids = [item.get('observanceId') for item in entries]

assert editorial.get('schemaVersion') == 2
assert editorial.get('locale') == 'en'
assert editorial.get('entryCount') == len(entries)
assert len(entries) >= 28, f"editorial coverage unexpectedly low: {len(entries)}"
assert len(ids) == len(set(ids)), 'duplicate editorial ids'
assert set(ids).issubset(known), f"unknown editorial ids: {sorted(set(ids) - known)}"

for item in entries:
    oid = item['observanceId']
    assert item.get('status') == 'REVIEWED', oid
    for key in (
        'hook',
        'summary',
        'whyThisDate',
        'origin',
        'whyItMatters',
        'quickFacts',
        'waysToTakePart',
        'relatedObservanceIds',
    ):
        assert key in item, (oid, key)
    assert len(item.get('summary', '').strip()) >= 80, oid
    assert len(item.get('whyItMatters', '').strip()) >= 80, oid
    actions = item.get('waysToTakePart', [])
    assert 2 <= len(actions) <= 4, oid
    assert all(len(action.strip()) >= 20 for action in actions), oid
    facts = item.get('quickFacts', [])
    assert len(facts) <= 5, oid
    assert all(len(fact.strip()) >= 20 for fact in facts), oid
    related = item.get('relatedObservanceIds', [])
    assert len(related) == len(set(related)), oid
    assert set(related).issubset(known), (oid, sorted(set(related) - known))
    assert oid not in related, oid
    assert item.get('lastReviewedAt') == '2026-10-12', oid
    for key in ('hook', 'summary', 'whyThisDate', 'origin', 'whyItMatters'):
        assert 'http://' not in item.get(key, ''), (oid, key)
        assert 'https://' not in item.get(key, ''), (oid, key)

consumer_required = {
    'world-cancer-day', 'safer-internet-day', 'world-theatre-day',
    'international-dance-day', 'international-nurses-day',
    'international-museum-day', 'world-turtle-day', 'world-ms-day',
    'world-emoji-day', 'world-suicide-prevention-day',
    'world-alzheimer-s-day', 'world-heart-day', 'world-vegan-day',
    'world-kindness-day',
}
assert consumer_required.issubset(set(ids)), sorted(consumer_required - set(ids))

print(f"editorial ok: {len(entries)} reviewed English entries")
