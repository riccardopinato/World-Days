# World Days — Wave11 minimum +400, 711 → at least 1111

## Rule of admission

This is ONE protected branch and ONE draft PR for **at least 400 truly new canonical observance identities**. A count of 400 indexed source rows, 400 historical news articles, 400 country repetitions, or 400 duplicates does **not** pass. Maintain the existing 711 stable IDs and their favorites/local content. No merges of partial quotas into the main catalog under this target.

The source repository baseline is **711** catalog IDs on `main`, composed of 289 global and 422 national source-level observances. The first merge threshold is **at least 1111**, requiring **at least 400 net new**. There is no maximum: admit every additional independently sourced and distinct identity that passes validation, even if the first PR exceeds 1111. After the first qualifying merge, continue with incremental reviewed PRs indefinitely.

## Real evidence materialized on branch

- 145 initially transcribed entries from the Philippines National Commission for Culture and the Arts annual cultural dates index; one already catalogued National Archives anniversary quarantined; **144 research-only candidates** now in `data/editorial/candidates/wave11_ncca_cultural_anniversaries_20261111.json`.
- NCCA source https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/ ; records cover cultural birth/death anniversaries and historical dates, not newly legislated national holidays.
- Titles are editorially normalized English references (not verbatim copied titles); an independently verified biography and introduction year remain outstanding. Candidate flags `admissionReady=false`, `individualBiographyVerified=false`, `richStoryVerified=false`.
- `tool/validate_wave11_bulk_research.py` gates all 144 source rows and publication status. `tool/reconcile_wave11_goal_1111.py` compares them with the existing Philippine national market and reports potential same-person/date duplicates.
- `tool/probe_wikidata_recurring_days.py` is a read-only exploration of Wikidata P837 recurring dates under CC0. Its output is **not** evidence of officiality or grounds for automatic publication.

## Remaining checks before the first ≥400-identity merge

1. Complete primary-source or documented originator evidence for **256+** additional distinct identities, **more** if a candidate is found to be a duplicate.
2. Validate semantic identity and aliases, country or global scope, correct fixed/movable recurrence with 2026–2028 independent vectors, A/B/C/D source tier and officiality without upgrading discovery sources to government status.
3. Add all source-admitted records as ONE canonical new dataset with idempotent stable IDs and six locale title keys; EN fallback must be explicitly disclosed if native translation remains incomplete.
4. Keep all newly added records as editorial `STUB` unless rich history, verified founding year, and localized article checks have separate evidence.
5. Update generator, lower-bound ≥1111-ID validations (not equality-to-1111 assertions), exact actual country counts, all Flutter tests, Web build and protected PR review. Validate uniqueness and provenance independently of the total count. Confirm exact-head CI and merged `main` commit.
6. Do not build APK, sign, run physical-device certification or publish Play releases while suspended.

**Status now: NOT 1111. The draft PR is a research and reconciliation checkpoint; main remains 711 until a real protected merge.** Do not merge this draft as a partial substitute for the user's requested one-block +400.

## Continuous growth policy (approved 2026-11-11)

- **1111 is a minimum milestone, never a ceiling or a stopping condition.** Do not discard eligible records to force the total to exactly 1111.
- Keep this first draft PR as the single protected intake block until its distinct, source-reviewed additions reach at least 400; the PR may contain more than 400. Do not merge merely because a count passes while identity, evidence, reviews or CI remain incomplete.
- Once the first qualifying merge is confirmed on `main`, use `main` as the new baseline and continue reviewing, committing and merging additional nonduplicate source-verified batches in subsequent PRs. Avoid unnecessary empty PRs and avoid reprocessing previously rejected candidates without new evidence.
- Report the actual main total, staged total, eligible new distinct identities, rejected candidates and missing count toward the **minimum**. After reaching 1111, report further net growth rather than a zero remaining quota.
- Preserve the exact 711/855 counts in historical checkpoint tests as historical snapshots only; future production dataset checks must derive the actual totals and enforce minimum thresholds and invariants, not hard-coded equality to 1111.


## 11 November: additional 300-lead discovery block (research, NOT 300 published days)

A separate intake in `data/editorial/candidates/wave11_wikidata_300_discovery_20261111.json` contains exactly **300 unique Wikidata P837 QIDs** with a one-date indexed label, discovery URL, and optional country label. Built from a completed GitHub CI research run with 930 date-labelled search hits. The source contains common public holidays, non-holiday traditions, historical feasts, popular awareness dates, and country-specific date conventions: **the existence of 300 rows must NEVER be used as proof of 300 new genuine observances**.

`tool/validate_wave11_wikidata_300.py` enforces the exact 300/QID/date and research-only flags; `tool/triage_wave11_wikidata_300.py` compares labels against the actual generated canonical catalogue (including all 144 NCCA staged records) and writes `reports/wave11_300_discovery_triage.json`, including suspicious duplicates and source/recurrence/authority gaps.

All 300 have `publishable=false`, `primarySource=null`, `authorityVerified=false`, `duplicateSemanticsVerified=false` and `recurrenceVerifiedBeyondWikidata=false`. They do **not** change the actual app's generated count of **855 on branch** or **711 on main**.

For one protected import of at least 400 valid net-new canonicals (at least 1111 on main), require per-item first-party or originator references and year-independent recurrence rules. The staged 144 NCCA are still institutional-index source-level entries, not 144 completely researched historical narratives; all existing + new publisher quality caveats continue to apply.
