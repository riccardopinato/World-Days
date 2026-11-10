# Wave06 bulk institutional intake — first 291 source rows (10 Nov 2026)

## Evidence / status

**Scope: source-index research ONLY.** EURES (European Employment Services / European Commission) lists holidays from many countries for 2026–27:
https://eures.europa.eu/eures-services/chat-eures-advisers/public-holidays-calendar_en

The data files contain **291 listed source rows** across **24 countries**: **290 calendar-date records** plus **1 impossible source date** (Belgium, `25/25`, Whit/Pentecost Monday), explicitly quarantined.

Two committed provenance batches:
- `data/market/candidates/eures_at_be_bg_hr_cy_2026_20261110.json` — 5 countries / 65 source rows / 64 valid date syntax;
- `data/market/candidates/eures_19_countries_2026_20261110.json` — 19 more countries / 226 source rows / six additional warning flags.

Reconciliation yields **90 normalized distinct name strings** out of 290 rows; this is NOT the number of genuinely distinct national observances or of usable new canonical IDs. For example, "New Year's Day" and "Christmas Day" each appear in 24 countries. The normalized label "Independence Day" appearing in several countries can describe *different* legal anniversaries — titles cannot be collapsed blindly. Conversely, the same common international holiday must not be multiplied into 24 separate GLOBAL days.

The original source itself contains potential mistakes. EU EURES lists German "Good Friday" as `06/04` (contradicts European Central Bank `03/04`), while Danish Whit Monday appears as `25/06`. Regional, local-only or substitute-day entries are also flagged. These are **not** authoritative recurrence rules:
- https://www.ecb.europa.eu/ecb/contacts/working-hours/html/index.en.html
- https://eures.europa.eu/eures-services/chat-eures-advisers/public-holidays-calendar_en

## Reproducible gates

```bash
python3 tool/test_discover_eures_institutional.py
python3 tool/validate_eures_research_batch.py
python3 tool/triage_bulk_institutional.py
```

`reports/eures_290_triage.json` is a generated, inspectable research report with each row classified as:
- `SOURCE_QUALITY_QUARANTINE`,
- `CIVIC_IDENTITY_SOURCE_CHECK`,
- `SHARED_HOLIDAY_DEDUP_REVIEW`,
- `OTHER_NATIONAL_SOURCE_CHECK`.

The classification is *provisional* (keyword heuristic), with `admissionReady=false` for **all** rows. No records are promoted automatically.

## Adoption rule for the 1,000 distinct-record goal

After successful merges #76 and #78, main contains **479 canonical observances**. **521 more distinct canonical identities** are needed to reach 1,000. This EU source provides a candidate discovery pool rather than 290 additions.

For the next canonical batch, select country-unique civic commemorations, then require:
1. Country-specific competent government law / current official calendar for correct designation and geographical coverage;
2. canonical-ID / title / synonym reconciliation against existing GLOBAL and NATIONAL records;
3. deterministic rule across 2026–2028, explicitly distinguishing observed days and regional/municipal holidays;
4. English canonical title and non-empty IT/ES/FR/DE/PT localizations with review status;
5. source-backed introductory year or `null`; six-locale rich history stays non-reviewed until approved;
6. source-bound CI, Web smoke and protected PR merge; no APK / Android physical / store publishing.

**Do not claim 1,000 achieved until the exact source-generated catalog has 1,000 unique IDs, CI passes and that commit is merged.**
