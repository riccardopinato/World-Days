# World Days — 40-entry institutional reconciliation, phase 2

**Date:** 2026-11-10  
**Branch:** `research/institutional-40-batch-20261110`  
**Status:** source research / **NOT PUBLISHED** / **NOT HUMAN EDITORIAL REVIEWED**.

## Main findings

- 40 research records across UN (10), UNESCO (11), WHO (15), FAO (4).
- 32 entries match an exact canonical generator title.
- 1 alias is **World TB Day → World Tuberculosis Day**; **do not import a second record**.
- 7 entries are not in the static generator list under canonical titles. They are **admission candidates**, not existing runtime records and not yet published.
- WHO: **World Prematurity Day changes from 17 November to 15 November starting 2026**. The canonical generator already uses 15 November for 2026; historical recurrence modelling needs an explicit product decision and regression tests, not a blind rewrite.
- 4 establishment-year proposals have explicit primary institutional prose: UNESCO Women in Multilateralism (2021), Engineering (2019), Cultural Property Trafficking (2019), Islamic Art (2019). These are not yet applied to the app.

## Seven admission candidates

| Date | Observance | Institution | Per-entry evidence | Introduced year |
|---|---|---|---|---|
| 25 January | International Day of Women in Multilateralism | UNESCO | https://www.unesco.org/en/days/women-multilateralism | 2021 (UNESCO resolution 41 C/57) |
| 4 March | World Engineering Day for Sustainable Development | UNESCO | https://www.unesco.org/en/days/engineering-sustainable-development | 2019 |
| 14 March | International Day of Mathematics | UNESCO | https://www.unesco.org/en/days/mathematics | Unknown in this batch |
| 5 November | World Day of Romani Language | UNESCO | https://www.unesco.org/en/days/list | Unknown; index only |
| 14 November | International Day against Illicit Trafficking in Cultural Property | UNESCO | https://www.unesco.org/en/days/against-illicit-trafficking | 2019 |
| 18 November | International Day of Islamic Art | UNESCO | https://www.unesco.org/en/days/islamic-art | 2019 |
| 3 March | World Hearing Day | WHO | https://www.who.int/campaigns/world-hearing-day | Unknown; history of name differs from earlier Ear and Hearing Care Day |

## Important limitations

The 40 entries have institutional-index provenance, **not 40 independently checked founding acts**. Static matching against `tool/build_dataset.py` does not prove runtime-generated JSON correctness. No translated stories (EN/IT/ES/FR/DE/PT) have been created or reviewed under this PR; preserve the existing 56 approved editorial stories and all user data.

Before publication: resolve all 7 candidate canonical IDs; perform individual source and duplicate checks, establish correct authority and date recurrence, classify officiality; add titles in six languages with review; separately write original long-form editorial copy and pass human/native-language gates; bump monotonic pack version, run full data and Flutter tests and exact-head CI; merge only through protected main.

**WHO exception:** https://www.who.int/campaigns/world-prematurity-day/2026 explicitly describes historical 17 November and a change effective in 2026. Maintain clear separation between first initiative (2008), first celebration (2009), WHO calendar adoption (2025), and the 2026 date shift.

## Useful commands

```bash
python tool/validate_institutional_40_candidates.py
python tool/build_dataset.py
python tool/validate_dataset.py
```

No developer/CI execution is claimed by this report. A passing structural checker is not editorial, release or provider certification.
