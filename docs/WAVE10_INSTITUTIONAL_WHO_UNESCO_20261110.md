# Institutional Wave10 — 7 WHO/UNESCO new global observances

**Factory baseline:** `App-Factory-Core@d4ed1185d36d419228fba6b57a979cde308bd321` (Master 27 / Golden Index 29). World Days main is **456** until content merges. PR #67 proposes **492**, PR #68 proposes **504**, and this dependent branch proposes **511** unique IDs (292 GLOBAL, 219 NATIONAL, 34 countries) before any approvals.

## Primary originator evidence and recurrence

| Institutional identity | Authority | 2026 | Annual rule | Original source |
|---|---|---|---|---|
| World Hearing Day | WHO annual campaign | 3 March | 3 March | https://www.who.int/campaigns/world-hearing-day |
| World Hand Hygiene Day | WHO-led SAVE LIVES campaign | 5 May | 5 May | https://www.who.int/campaigns/world-hand-hygiene-day |
| World Rabies Day | WHO-supported annual campaign | 28 September | 28 September | https://www.who.int/campaigns/world-rabies-day |
| World Polio Day | WHO Europe annual campaign | 24 October | 24 October | https://www.who.int/europe/campaigns/world-polio-day |
| World Leprosy Day | WHO | **25 January** | **last Sunday of January** | https://www.who.int/campaigns/world-leprosy-day |
| International Day of Women in Multilateralism | UNESCO 41 C/57 (2021) | 25 January | 25 January | https://www.unesco.org/en/days/women-multilateralism |
| International Day against Violence and Bullying at School, including Cyberbullying | UNESCO | **5 November** | **first Thursday of November** | https://www.unesco.org/en/days/against-school-violence-and-bullying |

**Date vectors:** Leprosy: 25 Jan 2026 / 31 Jan 2027 / 30 Jan 2028. School bullying: 5 Nov 2026 / 4 Nov 2027 / 2 Nov 2028. WHO's campaign page may show January 30 as a special India day; do not substitute 30 January for the globally observed last Sunday. UNESCO's dated headline for bullying changes each year; the *first Thursday rule* is canonical.

**Officiality nuance:** WHO-led campaigns are *not necessarily* among World Health Assembly-mandated 13 worldwide official WHO health days. Use WHO institutional support and first-party links without falsely claiming WHA designation. UNESCO multilateralism has its own 41 C/57 resolution, not a UN General Assembly A/RES. Originator verification confirms names, scope and recurring date, **not** any invented original legal introduction year. Titles in EN/IT/ES/FR/DE/PT are draft UI display strings, not qualified human-reviewed translations. All seven stories remain `STUB`, and existing 56 reviewed historical articles are untouched.

## Build / review gates

- `tool/build_dataset.py` now appends the seven global source identities with WHO/UNESCO primary source URLs and supported recurrence kind.
- `data/titles/{it,es,fr,de,pt}.json` contains new translations.
- `tool/validate_wave10_institutional.py` asserts exact 2026–2028 dates, authority, source URL, six locale fields, no duplicate IDs and 511 total.
- `.github/workflows/dev-checks.yml` runs the complete earlier Waves05–09 checks plus Wave10, Flutter analyze/test, Europe/Rome timezone tests and Web release build.
- Branch/PR is **stacked behind PR #68 and #67**, and must wait for editorial approval of these prior branches. No merge or public deploy until required gates; no APK, Play, signing or production Web release.

## Source inventory cross-check

The UN's existing official full registry is already heavily represented in `tool/build_dataset.py`; blindly copying it yields duplicates. Our isolated gap review targets genuinely missing WHO annual campaigns and the two UNESCO days. Original research is split into parallel WHO and UNESCO source-review PRs. There is no claim of hundreds of already-vetted new dates just because they are on the UN website.
