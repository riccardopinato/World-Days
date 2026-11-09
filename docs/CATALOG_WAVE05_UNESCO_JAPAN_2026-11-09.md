# Wave05 — UNESCO + Japan, metadata-only catalog admission (9 November 2026)

## Scope and immutable baselines
- Factory baseline pinned once: `riccardopinato/App-Factory-Core@d4ed1185d36d419228fba6b57a979cde308bd321`, Master v27, Golden Index v29, Localization Golden v1.
- World Days main baseline: `9e312432b7fb46be1fc66437587d4cbe49033ad9` with **456 unique** identities.
- This branch proposes **6 new identities**: **3 international UNESCO + 3 Japan**, keeping prior 456 IDs. Expected build **462 = 285 GLOBAL + 177 NATIONAL** across the **existing 28 markets**; Japan increases from 3 to 6 national entries.
- Dataset revision `2026.11.09.5`; rich-editorial payloads remain **56 reviewed** stories, and no new candidate story is falsely marked REVIEWED.
- All dates use commemorative occurrence, **not substitute workplace holidays**. 2026–2028 recurrence vectors are test-gated. Six offline titles EN/IT/ES/FR/DE/PT are structurally complete, but qualified human/native-language editorial approval is NOT claimed.
- APK signing, Android physical QA, Play Console and native mobile release stay **SUSPENDED**.

## UNESCO global entries (originator primary sources)

| Canonical ID | Date | Formal proclamation | UNESCO evidence |
| --- | --- | --- | --- |
| `world-day-of-romani-language` | 5 November | 2015 | https://www.unesco.org/es/days/romani-language ; https://www.unesco.org/en/days/list |
| `international-day-against-illicit-trafficking-in-cultural-property` | 14 November | 2019 | https://www.unesco.org/en/days/against-illicit-trafficking |
| `international-day-of-islamic-art` | 18 November | 2019 | https://www.unesco.org/en/days/islamic-art |

UNESCO's own pages specify annual dates and 2015/2019 proclamation decisions. The year field records **formal introduction by UNESCO**, not a guessed first-ever celebration. Two 40th-General-Conference items have no claimed resolution number because the precise resolution has not been independently confirmed. Metadata is classified `OFFICIAL_UNESCO` under `GLOBAL`; the source URL is specific to each observance.

## Japanese entries (Cabinet Office / statutory)

| Canonical ID | 2026 | Annual rule | Documented introduction |
| --- | --- | --- | --- |
| `japan-coming-of-age-day` | 12 January | Second Monday of January | 1948, creation of holiday; date rule later changed |
| `japan-emperors-birthday` | 23 February | 23 February under present reign/law | `*`; holiday category predates current date |
| `japan-showa-day` | 29 April | 29 April | 2007; 2005 amendment created holiday name |

Japanese original government calendar and National Holidays Act:
- https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html
- https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku.html

No substitute Sunday/Monday closure is treated as a separate observance. The Emperor's Birthday date is subject to future legal change after a succession. `japan-coming-of-age-day` resolves to 2026-01-12, 2027-01-11, 2028-01-10. Existing 3 Japanese canonical IDs remain unchanged.

## Implementation and QA
- `tool/build_dataset.py` adds 3 Unicode-safe UNESCO canonical titles, their primary sources, fixed recurrence and introduction-year evidence.
- `data/titles/{it,es,fr,de,pt}.json` adds 3 translated display titles per locale; English remains the source identity.
- `data/market/wave05_japan_20261109.json` adds 3 nationally scoped, separately sourced and translated Japanese holiday records.
- `tool/market_wave05.py` validates source domains/URLs, date rules, six title locales, evidence for founding year, and independent 2026–2028 vectors. `tool/market_expansion.py` appends only the validated new records.
- `tool/validate_dataset.py`, `tool/validate_wave05_content.py` and `tool/market_coverage.py` validate unique count, year-date index, country segregation, source quality, localization, year evidence, fixed-day and second-Monday recurrence.
- Flutter around-the-world and market-layer tests update their **deliberate total assertions** from 456 to 462 without altering existing design. `tool/build_editorial.py` and `tool/build_editorial_locales.py` align dataset revision to `2026.11.09.5`.
- Content/admission test runs in the existing Development CI; CI PASS must be verified on the exact final commit before merge.
- Expected content-only coverage: **70 sourced introduced years**, **392 unknown years** displayed `*`; **56 reviewed stories**, **25 six-locale drafts awaiting review**, **381 lacking long-form research**. These are expected generator outputs, not assertions of human editorial review.

## Publication gates
- This is a distinct **metadata-only integration PR** from the original research Draft PR #64. It does not merge or overwrite PR #64.
- 6×6 display-title parity is structurally tested; translation nuance and rich editorial articles require subsequent human/native-language review. Source metadata is source-pinned. If review policies require approval before merge, keep Draft.
- No claim that main or a deployed Web Preview contains 462 until merge and live confirmation. No APK/Play work.
