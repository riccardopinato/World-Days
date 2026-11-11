# Wave11 — UN/UNESCO primary-source discovery audit (2026-11-11)

Status: **RESEARCH ONLY; zero canonical admissions from this note**. Never interpret a source calendar row as a net-new canonical identity until the current generated 711-ID catalog and all staged candidates have been compared by meaning, aliases, scope, and date. Do not add country variants of a global observance.

## Primary evidence / candidates for cross-catalog review

| Candidate identity | Date / rule | Primary authority | Evidence | Review gate |
|---|---|---|---|---|
| International Day for the Prevention of and Fight against All Forms of Transnational Organized Crime | 15 November, fixed | UN General Assembly, A/RES/78/267 (2024) | https://www.un.org/en/observances/fight-against-transnational-crime-day | Check existing canonical identity, alias and 2026–2029; founding year 2024 is directly attested. |
| International Day of the Mediterranean Diet | 16 November, fixed | UN General Assembly, A/RES/80/174 | https://www.un.org/en/observances/list-days-weeks | Check existing canonical identity, source resolution and scope; no invented introduction year. |
| World Conjoined Twins Day | 24 November, fixed | UN General Assembly, A/RES/78/313 | https://www.un.org/en/observances/list-days-weeks | Check aliases and current global IDs before admission. |
| International Day for the Elimination of Child, Early and Forced Marriage | 27 November, fixed | UN General Assembly, A/RES/80/309 | https://www.un.org/en/observances/list-days-weeks | Check existing canonical identity, actual resolution, year and date. |
| International Day of Engagement in Science for Sustainable Development | 27 November, fixed | UNESCO international days listing | https://www.unesco.org/es/days/list | Official UNESCO English list confirms this exact title and 27 November; check existing identity and founding instrument; do not infer founding year. |
| International Day of Caves and Karst | 13 September, fixed | UNESCO international days listing | https://www.unesco.org/es/days/list | Check current generated catalog and designation source. |
| World Coding Day | 29 October, fixed | UNESCO international days listing | https://www.unesco.org/es/days/list | UNESCO English list confirms World Coding Day (29 October); retain International Day of Coding only as an unverified alias, not a second identity. |
| World Futures Day | 2 December, fixed | UNESCO international days listing | https://www.unesco.org/es/days/list | Check existing identity and designation authority. |

## Important conflict — do not import unreviewed date

UNESCO's current English international-days index also displays **6 November** for the International Day against Violence and Bullying at School, including Cyberbullying; while its English upcoming-days listing shows **5 November 2026**. The annual rule is the **first Thursday of November**, which is 5 November in 2026, 4 November in 2027, 2 November in 2028, and 1 November in 2029. Neither a permanent 5-November nor a permanent 6-November fixed-date rule is valid. Require the primary proclamation/UNESCO observance page and test movable dates before any edit.

## Required follow-up

1. Run exact-ID and semantic cross-check against generated main catalog and branch research data. Mark each candidate EXISTING, ALIAS, NEW_VERIFIED or REJECTED with evidence; this file intentionally makes no net-new claim.
2. Obtain the primary resolution/UNESCO observance page and test 2026–2029 recurrence before publication. A list entry alone is not a reviewed story.
3. On admission use six locale keys with explicit English fallback, accurate officiality, introduced year null when unproven, and STUB narrative.
4. Keep PR #85 draft until ≥400 genuinely admitted net-new canonical IDs, exact-head CI and reviews pass. Continue beyond 1111 thereafter.

## English UNESCO primary-index reconciliation — 2026-11-11

Source: https://www.unesco.org/en/days/list (accessed 2026-11-11). The English list directly confirms **International Day for Caves and Karst** (13 September), **World Coding Day** (29 October), **International Day of Engagement in Science for Sustainable Development** (27 November), and **World Futures Day** (2 December). This corrects two candidate English names, not four new admissions. UNESCO's same English index lists the anti-bullying observance at 6 November, conflicting with its movable first-Thursday observance convention; the index alone must not override the year-specific rule. Until original proclamation and recurrence are reconciled, **exclude the disputed date from import**. No record should be counted twice for translated aliases.

Catalog comparison remains **BLOCKED** until the canonical generated catalog is available from the actual repository build artifacts or its authoritative source inputs. The attempted `assets/data/official_core.json` fetch returned 404 on both main and the PR branch; do not claim a zero-overlap result from this absence.

## Canonical source-code cross-check — 2026-11-11 (follow-up)

**Resolved the previously reported missing-artifact blocker for these eight candidates.** The authoritative global input is `tool/build_dataset.py` on `main`, not `assets/data/official_core.json` (which does not exist at that path). Exact canonical titles were inspected directly in the generator. All **8/8** candidates in the table above are **ALREADY PRESENT** as `fixed(...)` declarations in `main`, with matching month/day and institutional classification. They are **EXISTING, not NEW_VERIFIED**; do not admit a second copy or count any toward the +400 goal.

| Candidate (same order as above) | Classification | Existing main generator declaration |
|---|---|---|
| Fight against Transnational Organized Crime | EXISTING | `fixed('International Day for the Prevention of and Fight against All Forms of Transnational Organized Crime',11,15,'A/RES/78/267')` |
| Mediterranean Diet | EXISTING | `fixed('International Day of the Mediterranean Diet',11,16,'A/RES/80/174')` |
| Conjoined Twins | EXISTING | `fixed('World Conjoined Twins Day',11,24,'A/RES/78/313')` |
| Child, Early and Forced Marriage | EXISTING | `fixed('International Day for the Elimination of Child, Early and Forced Marriage',11,27,'A/RES/80/309')` |
| Engagement in Science for Sustainable Development | EXISTING | `fixed('International Day of Engagement in Science for Sustainable Development',11,27,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)` |
| Caves and Karst | EXISTING | `fixed('International Day for Caves and Karst',9,13,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)` |
| World Coding Day | EXISTING | `fixed('World Coding Day',10,29,'42 C/Resolution 15','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)` |
| World Futures Day | EXISTING | `fixed('World Futures Day',12,2,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)` |

**Result:** 8 source-calendar candidates screened, **8 already present**, **0 net-new identities**, **0 admissions**; no date corrections required for these eight. This is an exact source-code declaration check, not a complete semantic audit of all 711 IDs or the NCCA candidates. The separate UNESCO bullying-date discrepancy remains excluded pending primary rule verification. Preserve the draft PR and the 1,111-minimum gate.
