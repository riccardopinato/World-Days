# World Days — single Wave11 +400 target, 711 → 1111

## Rule of admission

This is ONE protected branch and ONE draft PR for **400 truly new canonical observance identities**. A count of 400 indexed source rows, 400 historical news articles, 400 country repetitions, or 400 duplicates does **not** pass. Maintain the existing 711 stable IDs and their favorites/local content. No merges of partial quotas into the main catalog under this target.

The source repository baseline is **711** catalog IDs on `main`, composed of 289 global and 422 national source-level observances. Target is **1111**, exactly **400 net new**.

## Real evidence materialized on branch

- 145 initially transcribed entries from the Philippines National Commission for Culture and the Arts annual cultural dates index; one already catalogued National Archives anniversary quarantined; **144 research-only candidates** now in `data/editorial/candidates/wave11_ncca_cultural_anniversaries_20261111.json`.
- NCCA source https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/ ; records cover cultural birth/death anniversaries and historical dates, not newly legislated national holidays.
- Titles are editorially normalized English references (not verbatim copied titles); an independently verified biography and introduction year remain outstanding. Candidate flags `admissionReady=false`, `individualBiographyVerified=false`, `richStoryVerified=false`.
- `tool/validate_wave11_bulk_research.py` gates all 144 source rows and publication status. `tool/reconcile_wave11_goal_1111.py` compares them with the existing Philippine national market and reports potential same-person/date duplicates.
- `tool/probe_wikidata_recurring_days.py` is a read-only exploration of Wikidata P837 recurring dates under CC0. Its output is **not** evidence of officiality or grounds for automatic publication.

## Remaining checks before one 400-identity merge

1. Complete primary-source or documented originator evidence for **256+** additional distinct identities, **more** if a candidate is found to be a duplicate.
2. Validate semantic identity and aliases, country or global scope, correct fixed/movable recurrence with 2026–2028 independent vectors, A/B/C/D source tier and officiality without upgrading discovery sources to government status.
3. Add all source-admitted records as ONE canonical new dataset with idempotent stable IDs and six locale title keys; EN fallback must be explicitly disclosed if native translation remains incomplete.
4. Keep all newly added records as editorial `STUB` unless rich history, verified founding year, and localized article checks have separate evidence.
5. Update generator, exact 1111-ID validations, country counts, all Flutter tests, Web build and protected PR review. Confirm exact-head CI and merged `main` commit.
6. Do not build APK, sign, run physical-device certification or publish Play releases while suspended.

**Status now: NOT 1111. The draft PR is a research and reconciliation checkpoint; main remains 711 until a real protected merge.** Do not merge this draft as a partial substitute for the user's requested one-block +400.
