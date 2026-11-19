# Curated origin cohort 01 — provenance audit (2026-11-19)

**Evidence:** GitHub Actions artifact `world-days-curated-428-origin-cohorts`, artifact ID `14560316058`, workflow run `44582444152`, source head `f3c75b43b198fc3d825f7f530f3f477a02555ab7`; generated `cohort_01.json`. This is a research triage document, **not 100 completed stories**.

## Verified structural properties of the 100-ID packet

- Exactly **100 unique canonical IDs** in cohort 01; country split **CZ 27, SK 26, FI 21, IT 21, EE 5**.
- All 100 records have six **localized titles**, but **0/100** have `individualOriginalStoryEN` or `historicalFoundingEvidence`; these are source-index assignments, not individual origin histories.
- The 100 records reuse only **9 distinct source URLs**. A shared national holiday statute or calendar can establish a date and legal status, but cannot by itself prove each historical origin, original founding year, or event narrative.
- Keep `AI_CONTEXTUAL_SIX_LOCALE` until a source-verified original story and five meaning-preserving localized versions exist. Do not turn on runtime approval from this audit.

## Primary source checked: Czech law 245/2000 Sb.

Official consolidated text: https://ppropo.mpsv.cz/zakon_245_2000

- Section 1 explicitly recognizes **5 July, Saints Cyril and Methodius**, **6 July, Jan Hus**, **8 May, Victory Day**, **28 September, Czech Statehood**, **28 October, Czechoslovak Independence**, **17 November, Freedom and Democracy** as state holidays (alongside 1 January). These are civic/legal observances, not merely personal anniversaries.
- Section 4(1) explicitly lists **12 March, NATO accession**, **1 May, EU accession**, **7 April, Education Day**, **15 May, Families Day**, **30 March, Flag Day**, **16 January, Jan Palach remembrance**, and several resistance/victim remembrance days as *významné dny* (significant days). Section 4(2) states significant days are working days unless also another holiday.
- The consolidated law is dated 29 June 2000 and shows later amendments through 2026. **Do not assign 2000 as each observance's original introduction year**; check the relevant amending act and historical origin independently.
- **Scope review required:** `cz-jan-amos-comenius-birthday` appears in Section 4(1) as 28 March, but the product policy excludes merely biographical birthdays. Determine whether this formally designated civic education observance should be retained under the recognized-civic exception; do not automatically delete or publish based on its title alone.
- **Source relevance review required:** `cz-czech-accession-to-nato-anniversary` and `cz-czech-accession-to-the-european-union-day` are legally listed as civic significant days; they are not automatically excluded merely because the English title contains “anniversary”.

## Next production gate

For every ID in this frozen cohort: inspect its actual legal/institutional source; separately corroborate the historical event, promoter and first recognition date (or use unknown/*); write a distinct EN history; translate and check IT/ES/FR/DE/PT; validate source-to-claim provenance, schema and dedup. If a source only proves the observance is listed, keep the origin as HOLD. Run Python, Flutter and Web CI at exact PR head before merge. No APK/deploy. 
