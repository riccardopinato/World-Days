# Wave10 — Sri Lanka, Bangladesh, Laos: 2026 official calendar intake

Source-backed **22 research candidates** in `data/research/wave10_asia_sri_lanka_bangladesh_laos_2026.json`: Sri Lanka 13, Bangladesh 6, Laos 3.

## Official source evidence
- Sri Lanka Central Bank official 2026 register: https://www.cbsl.gov.lk/en/node/19362 — lists 2026 full-moon Poya days and Sinhala/Tamil New Year. Distinct full-moon Poya observances may be legitimate distinct identities, but semantic dedup needed. Adhi Poson is an intercalary occurrence, not necessarily an annual fixed-date festival; recurrence engine needs conditional lunar handling.
- Bangladesh Bank official 2026 calendar: https://www.bb.org.bd/en/index.php/mediaroom/holiday — Language Martyrs Day 21 Feb, Independence 26 Mar, Bengali New Year 14 Apr, July Mass Uprising Day 5 Aug, Victory 16 Dec, Chaitra Sankranti 13 Apr **only for Rangamati, Khagrachari and Bandarban Hill Districts**. International Mother Language Day and national Shaheed Dibosh overlap in date/meaning: editorial identity must not double count without distinct justification. Government embassy corroboration: https://hague.mofa.gov.bd/pages/static-pages/6952667435ce18e1c05a938f .
- Laos official Foreign Ministry eVisa public holidays 2026: https://laoevisa.gov.la/info — Lao New Year 14–16 Apr (ONE multiday festival identity), Lao Women's Union Day 20 Jul, Lao National Day 2 Dec. ASEAN-Japan Centre corroboration: https://www.asean.or.jp/en/learn-about-asean-japan/public-holidays-laopdr/ .

## Quality and uniqueness gates
- Preliminary literal title scan of three Python generator files found **0/22 exact strings**; NOT full semantic dedup (market JSON, aliases, translations and actual 456-record generator output still needed).
- Country-level uniqueness does not justify duplicate global identities.
- 2026 dates are **occurrences only** for lunar/solar calendar events; do not hardcode for subsequent years.
- Year of introduction null until documented.
- No six-locale translations, editorial histories, runtime additions or exact-head CI yet. No APK/Play changes.

## Counts
Wave05 33 + Wave06 38 + Wave07 29 + Wave08 15 + Wave09 16 + Wave10 22 = **153 research candidate records**. Asia Wave06–10 **120**. Main **456**, newly certified and integrated from these waves **0**, remaining to 1000 **544**. User request +300 genuinely new distinct observances is not yet fulfilled.
