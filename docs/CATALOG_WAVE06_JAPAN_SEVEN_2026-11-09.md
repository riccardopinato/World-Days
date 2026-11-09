# Wave06 — seven additional Japan holidays (stacked after PR #65)

**DEPENDENCY:** Base branch `content/wave05-unesco-japan-admission-20261109` (PR #65). This is a stacked PR; **do not merge it before #65** and do not count it as main content until both PRs merge with exact-head CI.

## Outcome proposed

- Main remains **456**, PR #65 proposes **462** (285 GLOBAL + 177 NATIONAL).
- Wave06 adds **seven distinct Japanese national holidays** to PR #65: proposed **469** (285 GLOBAL + 184 NATIONAL). Japan's national layer becomes 13, with the existing 28-country selector unchanged.
- Each has original Cabinet Office source, named Article 2 statutory holiday, six EN/IT/ES/FR/DE/PT offline display titles, correct deterministic legal recurrence and an independent 2026–2028 date vector. Long-form editorial remains STUB and qualified language review pending.
- **None of the seven** is Vernal/Autumnal Equinox Day: those need yearly astronomical declarations. Substitute closures (e.g. 6 May 2026) and 2020/2021 Olympics exceptions are not separate observance identities.
- Introduced year unknown `*` for all seven, pending legal date-specific historical evidence; no invented foundation years.

## Dates from original government legislation

| ID | Rule | 2026 | 2027 | 2028 derived |
|---|---|---|---|---|
| japan-greenery-day | May 4 | 2026-05-04 | 2027-05-04 | 2028-05-04 |
| japan-childrens-day | May 5 | 2026-05-05 | 2027-05-05 | 2028-05-05 |
| japan-marine-day | 3rd Monday July | 2026-07-20 | 2027-07-19 | 2028-07-17 |
| japan-mountain-day | August 11 | 2026-08-11 | 2027-08-11 | 2028-08-11 |
| japan-respect-for-the-aged-day | 3rd Monday September | 2026-09-21 | 2027-09-20 | 2028-09-18 |
| japan-sports-day | 2nd Monday October | 2026-10-12 | 2027-10-11 | 2028-10-09 |
| japan-labor-thanksgiving-day | November 23 | 2026-11-23 | 2027-11-23 | 2028-11-23 |

**Originator:** Japan Cabinet Office, National Holidays Act Article 2, 2026/2027 holiday calendar:
- https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html
- https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku.html

The 2028 dates above follow legal formulas, but the Cabinet Office does not publish its actual 2028 public-holiday table until February 2027: 2028 is a *rule-derived* vector, not falsely described as observed official schedule.

## Technical gates

- `data/market/wave06_japan_seven_20261109.json`: canonical metadata and translations.
- `tool/market_wave06.py`: distinct identities, official sources, literal 2026–28 vectors, legal annual rules.
- `tool/market_expansion.py`: stable source catalog append after Wave05, avoids all earlier ID/title collisions.
- `tool/validate_wave05_content.py` and `tool/validate_wave06_content.py`: preservation, source provenance, 462→469 and separation from reviewed narratives.
- `tool/validate_dataset.py`, `tool/market_coverage.py`, Dart market and responsive UI tests and `.github/workflows/dev-checks.yml`: exact-head CI before merge.
- No human/native-language approval, rich editorial histories or mobile release is claimed.

**Owner exclusions unchanged:** no APK, Android signing, physical release certification, Store or production deploy. Do not mark merged until independent checks and source PR sequence are proven.
