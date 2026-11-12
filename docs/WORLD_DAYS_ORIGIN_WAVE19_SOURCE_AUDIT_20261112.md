# World Days — Wave19 Individual Primary-Source Audit (2026-11-12)

## Scope

Seven distinct canonical IDs previously without independently sourced origin stories in the original 100 bilingual draft archive. Historical source research and bilingual original writing only. **Neither a calendar-index link nor an automated test establishes independent historical accuracy of every assertion or professional six-language review.** No six-locale review or rich runtime approval is claimed. Blank first-observance/founding fields are intentional factual limits.

| # | Canonical observance ID | Formal year | First observed | Primary/originator links | Languages with content |
|---:|---|---:|---:|---:|---|
| 1 | `international-day-of-solidarity-with-detained-and-missing-staff-members` | * | 1986 | 3 | EN, IT |
| 2 | `international-wellness-day` | 2026 | 2026 | 4 | EN, IT |
| 3 | `international-day-of-greening-the-planet` | 2026 | * | 3 | EN, IT |
| 4 | `international-day-in-memory-of-the-victims-of-earthquakes` | 2025 | 2026 | 3 | EN, IT |
| 5 | `time-of-remembrance-and-reconciliation-for-those-who-lost-their-lives-during-the-second-world-war` | 2004 | 2005 | 2 | EN, IT |
| 6 | `world-oceans-day` | 2008 | 2009 | 4 | EN, IT, ES, FR, DE, PT |
| 7 | `international-day-of-the-tropics` | 2016 | * | 3 | EN, IT |

## Document-specific historical checks

1. **25 March — Detained and missing UN staff:** UN memorial history specifically says observed **since 1986**, remembering Alec Collett abducted on 25 March **1985**. Resolution **A/RES/49/59** is a **1994 staff-safety convention**, NOT an individually documented decision establishing the observance. Formal introducedYear remains **null**, firstObservedYear=1986. No individual founding proposer invented.
2. **15 April — Wellness:** UN General Assembly **A/RES/80/249**, adopted **10 March 2026**. Official UN Web TV recorded the first event on **17 April 2026**, distinct from the designated calendar date of the 15th. 143 yes, 1 no, 0 abstentions in the official voting record. Why precisely 15 April was chosen is **not evidenced**.
3. **22 April — Greening the Planet:** **A/RES/80/300**, adopted **31 August 2026**, invites UNEP to facilitate observance. Original draft A/80/L.105 sponsors: Kazakhstan, Armenia and Mongolia. No observance under this newly adopted UN act can be established as having already occurred before the 2026 adoption. The 2027 occurrence is future; firstObservedYear **null**, not a fabricated 2026/2027 event. Date overlap with Mother Earth Day is not independently proven as the legislative rationale.
4. **29 April — Earthquake victims:** **A/RES/79/285**, adopted **29 April 2025**. UN institutional message explicitly calls **29 April 2026** the first observance. UNDRR facilitates it, consistent with Sendai risk-reduction priorities. Exact historical rationale for selection of 29 April is **not independently demonstrated**.
5. **8–9 May — WWII remembrance and reconciliation:** UN **A/RES/59/26** adopted **22 November 2004**. Both 8 and 9 May allowed, as the 2005 sixtieth anniversary approached. A solemn UN meeting was expressly mandated for May 2005. This is not a claim that every country shares a single national victory day.
6. **8 June — World Oceans Day:** established for UN observance through **A/RES/63/111 (2008)** with first UN celebration **2009**; 1992 civil-society Global Forum/Oceans Institute of Canada is a historical predecessor. Reuses existing prior research from draft PR #99; existing ES/FR/DE/PT content is **translation draft**, NOT native-reviewed.
7. **29 June — Tropics:** the official founding act is **A/RES/70/267 (14 June 2016)**, *not* A/RES/71/279 (which concerns MSMEs). The date recalls the first State of the Tropics Report of **29 June 2014**, produced with twelve research institutions. The first independently verifiable annual ceremony is not established, so firstObservedYear is **null**.

## Data lineage and release gates

- Wave19 new source-backed file: `data/editorial/batches/origin_stories_wave19_20261112.json`, seven unique IDs.
- Detailed original bilingual copy and primary URLs: `docs/WORLD_DAYS_ORIGIN_WAVE19_07_STORIES_IT_EN_20261112.md`.
- The unchanged baseline App Factory CURRENT.yaml was read once at the start of the execution; active Master v27, Golden Index v29.
- Canonical `tool/build_dataset.py` fixes the Tropics resolution and adds **five new individually evidenced establishment years** (Wellness 2026, Greening 2026, Earthquake victims 2025, WWII remembrance 2004, Tropics 2016). World Oceans Day already had the original 2008 year; the detained/missing staff day keeps the formally unknown founding year.
- `tool/validate_origin_100_original_drafts_20261112.py` must accept **one** successor with null formal founding year only where first observation and explicit source research explain that lack of act. It must not invent a date to satisfy a validator.
- CI should include the specific Wave19 validator, source-corpus coverage, Flutter analyze/test and Web build. All newly researched history remains `runtimeRichEditorialApproved=false` pending qualified approval of EN/IT and native ES/FR/DE/PT.
- Do not modify the initial four primary origin stories retroactively. No APK, Play, deploy, publication, or broad unfounded historical certification.

## Next block

Once the seven records merge, the **100 original bilingual archival drafts** have source-researched successors, but the full catalog still has **886** missing individual histories (unless catalog membership changes). Rebuild the next queue based on main and continue in batches of up to 100, marking national-index-only EURES/DFAT/NCCA entries blocked pending individual jurisdiction/originator sources.
