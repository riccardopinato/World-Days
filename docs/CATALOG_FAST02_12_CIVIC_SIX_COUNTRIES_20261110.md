# FAST02 Wave09 — six new Asian market choices and 12 fixed civic observances

## Status and provenance

The **content branch** extends the prior Wave05–08 metadata proposal from **492** to **504 unique observances**, with **285 GLOBAL + 219 NATIONAL**, adding six selectable markets **BD, ID, KH, MY, VN, LA** to the earlier 28 (now 34). The main branch remains **456** until reviewed merge of parent PR #67 and this dependent PR #68. The twelve additions have complete draft titles for EN/IT/ES/FR/DE/PT, government-originator URLs, national scope and fixed 2026/2027/2028 civil anniversary dates. Unknown legal introduction year stays **`*`**, and articles remain **STUB**; human multilingual/editorial reviews are NOT claimed.

| Country | National fixed commemorations | Dates |
|---|---|---|
| Bangladesh (BD) | Independence and National Day; Victory Day | 26 March; 16 December |
| Indonesia (ID) | Independence Day; Pancasila Day | 17 August; 1 June |
| Cambodia (KH) | Victory over Genocide Day; Constitution Day; Independence Day | 7 January; 24 September; 9 November |
| Malaysia (MY) | National/Independence Day (Hari Merdeka); Malaysia Day | 31 August; 16 September |
| Vietnam (VN) | Reunification Day; National Day | 30 April; 2 September |
| Laos (LA) | Lao National Day | 2 December |

Primary-source calendars:
- Bangladesh Bank 2026: https://www.bb.org.bd/en/index.php/mediaroom/holiday
- Indonesia State Secretariat three-minister calendar: https://www.setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2026
- National Bank of Cambodia and Law Reform Commission: https://www.nbc.gov.kh/english/news_and_events/official_holiday.php and https://lrc.gov.kh/en/annual-holiday-calendar-2026/
- Malaysian Ministry of Foreign Affairs 2026 calendar: https://www.kln.gov.my/web/gbr_london/holidays
- Government of Vietnam 2026 national holidays: https://en.baochinhphu.vn/ministry-of-home-affairs-announces-2026-holiday-schedule-111251017163421877.htm
- Lao Consular Department 2026 closures: https://laoevisa.gov.la/info

**Date confirmation is not a full historical story or a native-language sign-off.** Public holidays announced for 2026 do not guarantee unchanged legal status in future years; fixed 2027/2028 projections are marked as civil recurrence, and historical/policy changes require later authority review.

## Implementation and tests

- `data/research/FAST02_CIVIC_12_SOURCE_STAGED_20261110.json` preserves the research-stage evidence.
- `data/market/wave09_six_markets_civic_20261110.json` holds only the 12 proposed runtime metadata records.
- `tool/market_wave09.py`, `tool/validate_wave09_content.py` and `tool/validate_fast02_civic_source.py` enforce identity, 2026 date, fixed 2027/2028 vectors, original-source provenance, six locales, and the unchanged old-ID baseline.
- `lib/core/market_options.dart` adds all six choices and localized country names. `lib/l10n/app_{en,it,es,fr,de,pt}.arb` supplies country labels.
- Dataset builders and all prior Wave05–08 content tests now require 504 records, 219 national. Flutter around-the-world selector tests cover 34 markets, including small-screen UI.
- Full GitHub development workflow performs generator checks, Flutter analyze/test, Europe/Rome civil-day tests and Web release build. Independent FAST02 source CI runs on exact branch pushes.
- Existing 56 human-reviewed stories stay untouched; this metadata PR does not certify complete editorial quality.

**Dependencies:** Parent PR #67 (36 source-staged records; 492 total) still requires review. This PR #68 must rebase against `main` **after** #67 merges, run exact-head CI, obtain qualified editor/localization signoff, and only then merge according to protections. No APK signing, Play Console or production Web deployment is requested.
