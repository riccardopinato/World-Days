# World Days — 1,000 distinct observances: bulk-source intake

## Actual counts vs target (2026-11-10)

- **Current main (after merged PR #76): 463** canonical observances.
- The seven UNESCO/WHO source admissions in PR #76 are already merged, with green CI.
- Target: **1,000 distinct canonical observances**, so **537 further distinct records are required**.
- Existing reviewed rich articles: **56**; 1,000 titles do **not** equal 1,000 source-reviewed histories.

## Fast pipeline

1. Run `python3 tool/discover_eures_institutional.py --output reports/eures_candidate_batch.json` when network access to EU EURES is available. For replay, supply `--html <official-page-snapshot.html>`.
2. Inspect rejected/invalid dates, country counts and duplicated `(country,title,date)` before accepting the snapshot. The official source contains public holidays and may have wrong or substitute 2026 dates; the parser is **research only**.
3. Join candidates against current generated catalog by canonical title, authority, market and legal identity; remove transnational observances already represented as GLOBAL, and flag country-label synonyms.
4. For any actual admission, independently establish the country-specific public authority, official designation and recurrence over at least 2026–2028. A 2026 public-holiday observation is **not** automatically a perpetual fixed-date annual observance.
5. Add one source-pinned content batch of roughly 100–150 eligible **distinct** IDs and six-locale display titles (EN/IT/ES/FR/DE/PT), without fabricated year/history; revise counts once the generated catalog is tested.
6. Run dataset/localization/market and Flutter/Web CI. No publicity or claimed completion unless merged on `main`; no APK, signing or Play actions.

## Parallel-sized planned quotas, NOT a discovery or publication claim

| Wave | Unique verified canonical admissions required | Cumulative goal |
|---|---:|---:|
| W06 | 150 | 613 |
| W07 | 150 | 763 |
| W08 | 150 | 913 |
| W09 | 87 | 1000 |

The planned quotas depend on real source coverage; do **not** fill them with duplicate international days, one-off holiday substitution dates, non-institutional invented labels or unsourced regional days.

## Institutional sources

- [UN Days and Weeks](https://www.un.org/en/observances/list-days-weeks)
- [UNESCO Observances](https://www.unesco.org/en/days/list)
- [WHO campaigns](https://www.who.int/campaigns)
- [FAO international observances](https://www.fao.org/plant-production-protection/in-action/un-observances/)
- [EU EURES 2026–2027 holiday calendar](https://eures.europa.eu/eures-services/chat-eures-advisers/public-holidays-calendar_en)

**Important:** EU EURES is an institutional **index**, not the establishing national law for every holiday. Candidate counts from the scraper are not additions to the app. For full research, expand beyond Europe using country-government primary calendars, competent ministries and gazettes.

## Acceptance gate

`python3 tool/test_discover_eures_institutional.py` tests offline parsing and research-only isolation. Its PASS **does not certify** an actual external source response or its contents. A real remote ingestion still requires snapshot review, full deduplication and per-entry legal provenance. PR #76 is already merged; this research-only intake PR now targets main. Its CI and source-parsing gates remain mandatory.
