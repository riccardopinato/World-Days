# World Days — Wave 04, institutional histories in six locales (candidate)

**Date:** 2026-11-09. **Stage:** ORIGINAL SOURCE-RESEARCHED COPY, **PENDING HUMAN EDITORIAL AND TRANSLATION REVIEW**. No content from this folder is shipped in the app. Preserve the current 56 reviewed stories unchanged.

## Evidence protocol

Eight canonical IDs were selected from the existing 296-record World Days catalog and cross-checked with specific **UN/UNESCO/WHO** source pages or founding resolutions. Each record has:
- a proposed establishment year, separate from historical dates (e.g., 1971 treaty vs 2021 World Wetlands Day);
- a primary institutional URL and explicit timeline notes;
- original, non-copied narrative for EN/IT/ES/FR/DE/PT: hook, summary, origin, date context, importance, two concrete suggestions;
- no claim of first-hand field reporting, new measurements, annual campaign claims or licensed media.

| Canonical record | Proposed year | Historical distinction | Authoritative evidence |
|---|---:|---|---|
| World Wetlands Day | 2021 | 1971 Ramsar Convention vs 2021 UN declaration | [UN historical background](https://www.un.org/en/observances/world-wetlands-day/background) |
| International Day of Light | 2017 | 1960 first laser; 2017 UNESCO decision; 2018 first celebration | [UNESCO founding announcement](https://www.unesco.org/en/articles/unesco-general-conference-proclaims-16-may-international-day-light) |
| World Bicycle Day | 2018 | UN resolution 72/272, not the bicycle's invention | [UN mandate A/RES/72/272](https://mandates.un.org/mandate/A/RES/72/272) |
| International Day of Yoga | 2014 | Ancient Indian practice vs UN resolution 69/131 | [UN observance](https://www.un.org/en/observances/yoga-day) |
| World Food Safety Day | 2018 | 2018 proclamation vs 2019 first observance | [UN background](https://www.un.org/en/observances/food-safety-day/background) |
| World No Tobacco Day | 1987 | Initial WHO decision 1987; 31 May fixed in 1988 | [WHO campaign history](https://www.who.int/campaigns/world-no-tobacco-day) |
| World Population Day | 1989 | 1987 Day of Five Billion, 1989 establishment, 1990 first observance | [UN background](https://www.un.org/en/observances/world-population-day/background) |
| World Teachers' Day | 1994 | ILO/UNESCO Recommendation 1966, annual celebration since 1994 | [UNESCO Teachers Day](https://www.unesco.org/en/days/teachers) |

## What was implemented here

- [Source ledger](../data/editorial/candidates/wave04_sources_20261109.json) with eight source pointers and **proposed** years.
- Separate original draft files: [EN](../data/editorial/candidates/wave04_en.json), [IT](../data/editorial/candidates/wave04_it.json), [ES](../data/editorial/candidates/wave04_es.json), [FR](../data/editorial/candidates/wave04_fr.json), [DE](../data/editorial/candidates/wave04_de.json), [PT](../data/editorial/candidates/wave04_pt.json).
- [Candidate validator](../tool/validate_editorial_wave04_candidates.py): 8 IDs / six locale parity, distinct prose, dates, institutional hosts, 48 full drafts and **no automatic runtime promotion**.
- [Full gap manifest](../tool/editorial_gap_manifest.py) classifies all 296 IDs in CI: RUNTIME_REVIEWED (56), WAVE04_DRAFT_PENDING_HUMAN (8), NOT_RESEARCHED (232).
- [CI workflow](../.github/workflows/editorial-wave04-candidates.yml) checks drafts and archives the manifest, without app changes.

## Mandatory before publication

1. Human editorial review of each primary source, historical statement, copyright/provenance and English prose.
2. Qualified native-language review of IT/ES/FR/DE/PT; numeric parity is NOT linguistic certification.
3. Only after approval, a separate versioned PR may promote selected rows into existing runtime editorial generators, add reviewed dates and introduction years, bump the dataset revision, run all locale validators and exact-head CI.
4. The 232 remaining records retain transparent, factual fallback. No invented historical story or guessed founding year.

## Status accounting

- **Reviewed/published stories:** 56/296 (unchanged).
- **New researched translated candidate stories:** 8/296 (not shipped).
- **Remaining no full researched story:** 232/296.
- **Human reviews outstanding:** 8 English originals + 40 translated editions.
- **User data, privacy, ads and billing:** unchanged.

This is a concrete editorial preparation increment, NOT a claim that all 296 stories are independently reviewed.
