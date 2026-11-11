#!/usr/bin/env python3
import json
from pathlib import Path
from market_expansion import load_expansion, load_wave02, load_wave03
from market_wave04 import load_wave04
from market_wave06 import load_wave06
from market_wave07 import load_wave07
from market_wave08 import load_wave08
from market_wave09 import load_wave09
from market_wave10 import load_wave10
from market_wave11 import load_wave11
from market_wave12 import load_wave12

root = Path(__file__).resolve().parents[1]
seed = json.loads((root / 'assets/data/official_core.json').read_text(encoding='utf-8'))
occ = json.loads((root / 'assets/data/occurrences_2026.json').read_text(encoding='utf-8'))

records = seed.get('records', [])
ids = [r.get('id') for r in records]
visual_keys = {'planet','health','people','learning','culture','food','future','community'}
semantic_categories = {'PLANET','HEALTH','PEOPLE','LEARNING','CULTURE','FOOD','FUTURE','COMMUNITY'}
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
expansion = load_expansion()
expected_market.update({row['id']: row['country'] for row in expansion['records']})
wave02 = load_wave02()
expected_market.update({row['id']: row['country'] for row in wave02['records']})
wave03 = load_wave03()
expected_market.update({row['id']: row['country'] for row in wave03['records']})
wave04 = load_wave04()
expected_market.update({row['id']: row['country'] for row in wave04})
wave06 = load_wave06()
expected_market.update({row['id']: row['country'] for row in wave06})
wave07 = load_wave07()
expected_market.update({row['id']: row['country'] for row in wave07})
wave08 = load_wave08()
expected_market.update({row['id']: row['country'] for row in wave08})
wave09 = load_wave09()
expected_market.update({row['id']: row['country'] for row in wave09})
wave10 = load_wave10()
expected_market.update({row['id']: row['country'] for row in wave10})
wave11 = load_wave11()
expected_market.update({row['id']: row['country'] for row in wave11})
wave12 = load_wave12()
expected_market.update({row['id']: row['country'] for row in wave12})
assert len(ids) == len(records) == 1011, ('catalog growth total', len(records))
assert len(ids) == len(set(ids)), 'duplicate canonical ids'
assert all(ids), 'empty canonical id'
assert len(occ.get('dateIndex', [])) == 365, '2026 date index must cover 365 days'
known = set(ids)
occurrence_keys = set()
for item in occ.get('occurrences', []):
    assert item.get('observanceId') in known, f"unknown occurrence id: {item.get('observanceId')}"
    start = item.get('startDate')
    end = item.get('endDate')
    assert start and end and start <= end, ('invalid occurrence span', item)
    rule_index = item.get('ruleIndex')
    assert isinstance(rule_index, int) and rule_index >= 0, ('invalid ruleIndex', item)
    key = (item.get('observanceId'), start, end, rule_index)
    assert key not in occurrence_keys, ('duplicate occurrence', key)
    occurrence_keys.add(key)
for record in records:
    introduced_year = record.get('introducedYear')
    introduced_source = record.get('introducedYearSource')
    if introduced_year is not None:
        assert type(introduced_year) is int and 1800 <= introduced_year <= 2026, (
            'invalid introduction year', record.get('id'),
        )
        assert isinstance(introduced_source, str) and introduced_source.startswith('https://'), (
            'introduction year missing primary evidence', record.get('id'),
        )
        assert introduced_source in [item.get('url') for item in record.get('sources', [])], (
            'introduction evidence not in canonical sources', record.get('id'),
        )
    else:
        assert introduced_source is None, (
            'unsourced introduction year URL', record.get('id'),
        )
    assert record.get('sources'), f"missing sources: {record.get('id')}"
    assert str(record.get('lastVerifiedAt') or '').strip(), (
        'missing lastVerifiedAt',
        record.get('id'),
    )
    assert all(
        str(source.get('verifiedAt') or '').strip()
        for source in record.get('sources', [])
    ), ('missing source verifiedAt', record.get('id'))
    assert record.get('visualKey') in visual_keys, (record.get('id'), record.get('visualKey'))
    categories = record.get('categories') or []
    assert categories, f"missing semantic categories: {record.get('id')}"
    assert set(categories).issubset(semantic_categories), (record.get('id'), categories)
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
        assert countries[0] in {'IT', 'ES', 'FR', 'DE', 'PT', 'GB', 'US', 'CA', 'AU', 'BR', 'MX', 'IN', 'JP', 'CZ', 'SK', 'NO', 'FI', 'SE', 'PL', 'IE', 'NL', 'ZA', 'PH', 'NZ', 'SG', 'KR', 'AR', 'PE', 'MT', 'HR', 'CY', 'EE', 'LV', 'LT', 'IS', 'LU', 'CU', 'HT', 'SD', 'MM', 'NR', 'LK', 'GD', 'IR', 'RS', 'GM', 'LC', 'BN', 'GY', 'KW', 'DO', 'BG', 'GH', 'MU', 'TN', 'NA', 'PK', 'GR', 'BD', 'SN', 'ZW', 'TZ', 'SL', 'TG', 'MH', 'PY', 'CM', 'TL', 'YE', 'EC', 'ER', 'JO', 'GE', 'AZ', 'ET', 'WS', 'RU', 'SC', 'MZ', 'SI', 'MG', 'DJ', 'CD', 'BI', 'SO', 'BY', 'CV', 'RW', 'VE', 'KM', 'MW', 'SB', 'SS', 'BS', 'MN', 'KI', 'ST', 'ME', 'CO', 'BE', 'EG', 'LR', 'MV', 'MA', 'VU', 'BJ', 'CH', 'CK', 'BO', 'JM', 'CI', 'TD', 'CG', 'LI', 'GA', 'ID', 'AF', 'HU', 'UA', 'UY', 'MD', 'KG', 'MY', 'TT', 'UZ', 'VN', 'SM', 'SZ', 'AD', 'MK', 'KP', 'TJ', 'CR', 'SV', 'GT', 'HN', 'NI', 'PG', 'CL', 'KN', 'NP', 'AM', 'BZ', 'ML', 'SA', 'GW', 'TM', 'BW', 'CN', 'GN', 'NG', 'PW', 'TV', 'IQ', 'LS', 'UG', 'FJ', 'GQ', 'NU', 'ZM', 'KZ', 'AT', 'VC', 'TR', 'DZ', 'AG', 'DM', 'FM', 'PA', 'TO', 'KH', 'AO', 'OM', 'MC', 'LB', 'BA', 'SR', 'AL', 'MR', 'BB', 'CF', 'RO', 'LA', 'AE', 'TH', 'BF', 'KE', 'BH', 'BT', 'NE', 'QA', 'LY'}, record.get('id')
        assert officiality in {'OFFICIAL_INSTITUTIONAL', 'RECOGNIZED_INSTITUTIONAL'}, record.get('id')
        if officiality == 'OFFICIAL_INSTITUTIONAL':
            assert any((s.get('tier') == 'A_PRIMARY') for s in sources), record.get('id')
        else:
            assert record['authority']['type'] == 'UNIVERSITY', record.get('id')
            assert any((s.get('tier') == 'D_ORIGINATOR') for s in sources), record.get('id')

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
    'italian-national-flag-day': ['2026-01-07'],
    'italian-mafia-victims-remembrance-day': ['2026-03-21'],
    'italian-national-innovation-day': ['2026-06-09'],
    'italian-national-sports-day': ['2026-06-07'],
    'france-deportation-victims-remembrance-day': ['2026-04-26'],
    'uk-remembrance-sunday': ['2026-11-08'],
    'us-thanksgiving-day': ['2026-11-26'],
    'us-labor-day': ['2026-09-07'],
    'portugal-freedom-day': ['2026-04-25'],
    'spain-roma-people-recognition-day': ['2026-04-08'],
    'spain-national-sign-languages-day': ['2026-06-14'],
    'spain-victims-of-terrorism-tribute-day': ['2026-06-27'],
    'germany-nazi-persecution-victims-remembrance-day': ['2026-01-27'],
    'germany-flight-and-expulsion-victims-day': ['2026-06-20'],
    'portugal-national-students-day': ['2026-03-24'],
    'portugal-national-blood-donors-day': ['2026-03-27'],
    'portugal-national-grandparents-day': ['2026-07-26'],
    'portugal-national-sea-day': ['2026-11-16'],
    'uk-holocaust-memorial-day': ['2026-01-27'],
    'uk-stephen-lawrence-day': ['2026-04-22'],
    'uk-victory-in-europe-commemoration': ['2026-05-08'],
    'uk-victory-over-japan-commemoration': ['2026-08-15'],
    'canada-national-flag-day': ['2026-02-15'],
    'canada-national-indigenous-peoples-day': ['2026-06-21'],
    'australia-national-sorry-day': ['2026-05-26'],
    'australia-anzac-day': ['2026-04-25'],
    'brazil-indigenous-peoples-day': ['2026-04-19'],
    'brazil-black-consciousness-day': ['2026-11-20'],
    'mexico-national-flag-day': ['2026-02-24'],
    'mexico-constitution-day': ['2026-02-05'],
    'india-national-voters-day': ['2026-01-25'],
    'india-national-science-day': ['2026-02-28'],
    'japan-national-foundation-day': ['2026-02-11'],
    'japan-constitution-memorial-day': ['2026-05-03'],
    'japan-culture-day': ['2026-11-03'],
    'cz-independent-state-restoration': ['2026-01-01'],
    'cz-czechoslovak-independence-day': ['2026-10-28'],
    'sk-national-uprising-day': ['2026-08-29'],
    'no-constitution-day': ['2026-05-17'],
    'fi-kalevala-day': ['2026-02-28'],
    'fi-finnish-nature-day': ['2026-08-29'],
    'se-national-day': ['2026-06-06'],
    'pl-flag-day': ['2026-05-02'],
    'ie-st-brigids-day': ['2026-02-01'],
    'nl-kings-day': ['2026-04-27'],
    'za-human-rights-day': ['2026-03-21'],
    'za-reconciliation-day': ['2026-12-16'],
    'ph-edsa-people-power-anniversary': ['2026-02-25'],
    'ph-national-heroes-day': ['2026-08-31'],
    'nz-waitangi-day': ['2026-02-06'],
    'nz-labour-day': ['2026-10-26'],
    'sg-total-defence-day': ['2026-02-15'],
    'sg-national-day': ['2026-08-09'],
    'kr-hangeul-day': ['2026-10-09'],
    'kr-constitution-day': ['2026-07-17'],
    'ar-memory-truth-justice-day': ['2026-03-24'],
    'ar-national-sovereignty-day': ['2026-11-20'],
    'pe-battle-of-arica-flag-day': ['2026-06-07'],
    'pe-battle-of-ayacucho-day': ['2026-12-09'],
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
