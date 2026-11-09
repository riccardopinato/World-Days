# Wave07 — Three Indian civic holidays, stacked after PR #65 and PR #66

**Scope:** Metadata-only addition with complete EN/IT/ES/FR/DE/PT display titles, no unreviewed long-form story promoted as human-approved and no native publishing. Current main remains **456**; PR #65 is +6 to **462**; PR #66 is +7 to **469**; Wave07 proposes +3 to **472** (285 GLOBAL, 187 NATIONAL, India national entries 2→5). The branch is stacked on `content/wave06-japan-seven-official-20261109`.

| Canonical ID | Event | 2026 | 2027/2028 law-derived dates |
| --- | --- | --- | --- |
| `india-republic-day` | Republic Day | 26 January | 26 January |
| `india-independence-day` | Independence Day | 15 August | 15 August |
| `india-gandhi-jayanti` | Gandhi Jayanti | 2 October | 2 October |

Official India Post all-India 2026 holiday register: https://www.indiapost.gov.in/holidays-list . Second government-source calendar: https://www.ursc.gov.in/holidays.jsp . The two calendars confirm these three different national civic dates in 2026; annual dates in 2027–2028 follow the fixed commemorative day and do not claim already published future 2027/2028 holidays.

These are national **India-specific identities**, not global copies: Republic Day (adoption of republic, 1950), Independence Day (1947) and Gandhi Jayanti (Mahatma Gandhi's birth anniversary) are separate from each other. Gandhi Jayanti is closely associated with the global International Day of Non-Violence; the national holiday's own history and official source are retained, and it must not be presented as an invented separate global observance.

**Introduced year:** `null` / displayed `*` because 2026 holiday registers do NOT establish the year of first government holiday designation. The 1947, 1950 and 1869 historical dates in description are not misrepresented as legal first-adoption years.

**Quality and approval gates:** `tool/market_wave07.py` enforces source URLs, all six display locales and fixed 2026–2028 date vectors; `tool/validate_wave07_content.py` checks identity, counts, year evidence, officiality, 2026 occurrences and STUB editorial status. Main generator, coverage, Dart UI tests and Web build must be green on exact branch HEAD. **Native-language approval and rich historical stories remain outstanding; no automatic human review claim or merge.** APK, Android signing and Google Play suspended. Merge only after PR #65 and #66 pass their real gate and merge, then rebase this branch as needed.
