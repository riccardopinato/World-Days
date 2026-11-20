# Wave09 — Cambodia and Vietnam 2026 official observances

New research-only file: `data/research/wave09_asia_cambodia_vietnam_2026.json`: **16 candidate identities** (Cambodia 12, Vietnam 4), not admitted into app.

## Evidence
Cambodia National Bank official 2026 public holidays: https://www.nbc.gov.kh/english/news_and_events/official_holiday.php ; Cambodia Law Reform Commission independent government listing: https://lrc.gov.kh/en/annual-holiday-calendar-2026/ . Both support 2026 dates for 12 selected culturally distinctive events. Some sources differ on royal ploughing and lunar festival dates; the two government sources agree for the selected dates here. Do not count 3 days of Pchum Ben or Water Festival as 3 unique observances.

Vietnam government Ministry of Home Affairs 2026 schedule: https://en.baochinhphu.vn/ministry-of-home-affairs-announces-2026-holiday-schedule-111251017163421877.htm ; corroborating ASEAN-Japan Centre 2026: https://www.asean.or.jp/en/learn-about-asean-japan/public-holidays-vietnam/ . Hung Kings commemoration **actual festival Sunday 26 April**, **Monday 27 April substitute holiday**. Vietnam National Day is **2 September**; additional closure days are not additional identities.

## Admission gates
- Literal English-title scan of `tool/build_dataset.py`, `tool/market_catalog.py`, `tool/market_expansion.py`: 0 of 16 matched. **Not** proof of unique identities against all 456 generated records, aliases, market JSON, or translations.
- Festivals shared across Asia (Tet vs Lunar New Year, Cambodian Khmer New Year vs other regional solar new years) require semantic review, not automatic duplication.
- Lunisolar and royal-calendar dates are 2026 occurrences only, never hardcoded for other years.
- Founding year is null, app display `*` unless documentary primary evidence.
- No runtime integration, six-locale translations or editorial long-form histories yet. No APK/Play.

## Cumulative research-only inventory
Wave05 33 + Wave06 38 + Wave07 29 + Wave08 15 + Wave09 16 = **131 research records**. Asia Wave06–09 = **98 records**. Main remains **456**. Certified newly integrated in these waves = **0**. User goal of +300 new distinct days still requires full dedup, admission, and more primary-source research.
