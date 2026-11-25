# Wave08 — Asia: Indonesia, Malaysia, Nepal (2026)

Research pack: `data/research/wave08_asia_indonesia_malaysia_nepal_2026.json`, **15 candidates** (ID 3, MY 3, NP 9). All research-only, not runtime admissions.

## Primary registers
- Indonesia: Presidential State Secretariat official SKB 3 ministers 2026, 17 national holidays and 8 collective leave dates; **collective leave dates are not new observance identities**. https://www.setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2026 ; legal record https://jdih.kemnaker.go.id/peraturan/detail/2723/keputusan-menteri-ketenagakerjaan-nomor-2-tahun-2025
- Malaysia: Cabinet Office register https://www.kabinet.gov.my/hari-kelepasan-am/ and government gazette https://www.kabinet.gov.my/akta-dan-warta/ . The King’s 2026 birthday 1 June is specifically documented by Malaysian Ministry of Human Resources: https://jtksm.mohr.gov.my/sites/default/files/2026-05/Kenyataan%20Media%20Hari%20Wesak%20dan%20Hari%20Keputeraan%20Yang%20di-Pertuan%20Agong%202026.pdf . Merdeka Day and Malaysia Day dates are corroborated by an **official Nepal Embassy** schedule for Kuala Lumpur https://my.nepalembassy.gov.np/pages/public-holidays--2083---2026-27-/ but should be checked against the Malaysian Cabinet gazette before admission.
- Nepal: Ministry of Home Affairs official 2083 (2026/27) register https://moha.gov.np/en/page/government-and-public-holidays-in-2083 . English conversion corroboration: https://www.pradhanlaw.com/publications/list-of-public-holidays-2083-202627 . Nepal uses Bikram Sambat, so Gregorian date conversions and regional applicability must be checked against the original Nepali PDF. Gai Jatra and Indra Jatra are NOT all-Nepal national holidays; Jitiya is community-specific.

## Preliminary dedup and constraints
- Exact literal titles of these 15 records were not found in `tool/build_dataset.py`, `tool/market_catalog.py`, `tool/market_expansion.py`. This is **NOT** full dedup against the generated 456 catalog, market JSON or aliases.
- Cultural celebrations such as Nyepi, Dashain, Tihar and Teej may already be present under synonyms or global scope; do not count twice.
- Dates for lunisolar holidays and Nepal 2083 cannot be extrapolated as fixed annual dates. Royal birthday official date requires annual legal confirmation.
- Founding year remains null until primary evidence; app should show `*` if unknown.
- No 6-locale translation, editorial long-form story or runtime integration yet.

## Current totals
Wave05 33 + Wave06 38 + Wave07 29 + Wave08 15 = **115 candidate records**, **0 certified new additions**, main **456**, missing to 1000 **544**. Asian research records Wave06–08 = **82**. The user's requested +300 distinct days is not yet reached.
