#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
l10n = root / 'lib' / 'l10n'
paths = sorted(l10n.glob('app_*.arb'))
assert len(paths) == 6, f'expected 6 ARB locales, found {len(paths)}'

key_sets = {}
for path in paths:
    data = json.loads(path.read_text(encoding='utf-8'))
    keys = {key for key in data if not key.startswith('@')}
    assert all(str(data[key]).strip() for key in keys), f'empty translation in {path.name}'
    key_sets[path.name] = keys

reference = key_sets['app_en.arb']
for name, keys in key_sets.items():
    missing = sorted(reference - keys)
    extra = sorted(keys - reference)
    assert not missing, f'{name} missing keys: {missing}'
    assert not extra, f'{name} extra keys: {extra}'

required = {
    'catalogLoadFailed',
    'addFavorite',
    'removeFavorite',
    'offlineFirst',
    'dataPolicy',
    'dataPolicyDescription',
    'verifiedOverview',
    'noSearchResults',
    'clearSearch',
}
assert required <= reference, f'missing QA localization keys: {sorted(required - reference)}'

print(f'localization ok: {len(paths)} locales, {len(reference)} shared keys')
