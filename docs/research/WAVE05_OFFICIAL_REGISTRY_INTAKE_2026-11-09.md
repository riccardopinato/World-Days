# World Days — Wave05 research intake (9 November 2026)

**Status: RESEARCH_ONLY / NOT CATALOG-ADMITTED.** Base `main@9e312432b7fb46be1fc66437587d4cbe49033ad9`: 456 unique observances (282 global, 174 national), 28 markets. Target >=1000 means >=544 additional *independent* identities. This file adds **zero** approved catalog IDs until deterministic existing-282/global + national duplicate reconciliation, source/date/officiality review, six-language titles, recurrence tests and Flutter CI.

## Official registries consulted

- United Nations master register: https://www.un.org/observances/list-days-weeks
- UNESCO international days: https://www.unesco.org/en/days/list
- WHO global health days and campaigns: https://www.who.int/campaigns

These are source registers, **not** proof that each listed item is absent from the current World Days catalog. Preserve source-defined officiality (UN/UNESCO/WHO), distinguish agency campaigns from UN General Assembly proclamations. Weeks must not be flattened into single dates; moving weekday dates must be computed from the relevant year. An institution-year must not be inferred from a resolution number or anniversary.

## Candidate research queue — explicit non-admission

| # | Canonical English candidate | Date or recurrence | Source | Classification | Dedupe state |
|---:|---|---|---|---|---|
| 1 | International Day of Safe, Secure and Trustworthy Artificial Intelligence | 31 August | UN register | UN observance | NOT CHECKED |
| 2 | International Day of the World's Indigenous Women and Girls | 5 September | UN register | UN observance | NOT CHECKED |
| 3 | International Day of Science, Technology and Innovation for the South | 16 September | UN register | UN observance | NOT CHECKED |
| 4 | International Coffee Day | 1 October | UN register | UN observance | NOT CHECKED |
| 5 | International Day of the Mediterranean Diet | 16 November | UN register | UN observance | NOT CHECKED |
| 6 | International Day for the Prevention of and Fight against All Forms of Transnational Organized Crime | 15 November | UN register | UN observance | NOT CHECKED |
| 7 | World Conjoined Twins Day | 24 November | UN register | UN observance | NOT CHECKED |
| 8 | International Day for the Elimination of Child, Early and Forced Marriage | 27 November | UN register | UN observance | NOT CHECKED |
| 9 | International Day for Caves and Karst | 13 September | UNESCO register | UNESCO observance | NOT CHECKED |
| 10 | International Day of the Intangible Cultural Heritage | 17 October | UNESCO register | UNESCO observance | NOT CHECKED |
| 11 | World Coding Day | 29 October | UNESCO register | UNESCO observance | NOT CHECKED |
| 12 | International Day for Biosphere Reserves | 3 November | UNESCO register | UNESCO observance | NOT CHECKED |
| 13 | World Day of Romani Language | 5 November | UNESCO register | UNESCO observance | NOT CHECKED |
| 14 | International Day against Illicit Trafficking in Cultural Property | 14 November | UNESCO register | UNESCO observance | NOT CHECKED |
| 15 | International Day of Islamic Art | 18 November | UNESCO register | UNESCO observance | NOT CHECKED |
| 16 | World Olive Tree Day | 26 November | UNESCO register | UNESCO observance | NOT CHECKED |
| 17 | International Day of Engagement in Science for Sustainable Development | 27 November | UNESCO register | UNESCO observance | NOT CHECKED |
| 18 | World Futures Day | 2 December | UNESCO register | UNESCO observance | NOT CHECKED |
| 19 | World Cervical Cancer Elimination Day | 17 November | WHO campaigns | WHO official health day | NOT CHECKED |
| 20 | World Prematurity Day | 15 November | WHO campaigns | WHO official health day | NOT CHECKED |
| 21 | World Immunization Week | 24–30 April | WHO campaigns | WHO official health week | NOT CHECKED |
| 22 | World AMR Awareness Week | 18–24 November | WHO campaigns | WHO official health week | NOT CHECKED |

**Date QA:** UN calendar pages may present annual date changes or inconsistent display for particular observances; check each canonical event page and legal instrument before admission. UNESCO's anti-bullying school day has a movable recurrence; do not turn a year-specific calendar display into a fixed 6 November. UNESCO World Philosophy Day is movable; do not assume 20 November is fixed. The candidate list is **not** a set of 22 unique additions.

## Admission checklist

1. Compare against all 456 current canonical IDs, synonyms, semantic identity and date; preserve shared global identities rather than cloning for countries.
2. Open the individual official event/resolution page; record institution, exact annual recurrence, geographic scope, source URL, officiality tier and any verified founding year (otherwise `*`).
3. Record six localized titles (en/it/es/fr/de/pt) and non-misleading overview text; maintain historical/editorial human-review status separately.
4. Validate fixed/moving recurrence across 2026–2028, locale parity, source URLs, stable IDs and user-data preservation.
5. Admit only source-backed nonduplicates through the existing dataset generator and PR exact-head Flutter CI. Do not change APK, signing, Play or native release workflows.

## Expansion funnel

- 456 → 600: first +144 verified unique records from national government civic registers and global agencies, with at least 200 raw candidates to account for duplicates.
- 600 → 800: +200 verified, diversify undercovered countries and sectoral institution calendars.
- 800 → 1000+: +200 verified, final cross-country semantic deduplication and source-tier audit.

**No claim of completed research or admission beyond this initial source-register screening.** APK/Google Play remain suspended.
