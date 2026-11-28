# Curated 428 origin queue — cross-cohort evidence audit (2026-11-19)

## Reproducible input
GitHub Actions run [44582444152](https://github.com/riccardopinato/World-Days/actions/runs/44582444152), artifact `14560316058` (`world-days-curated-428-origin-cohorts`), generated from PR #154 head `f3c75b43b198fc3d825f7f530f3f477a02555ab7`. All five JSON cohort files were read and compared together; this report is an audit of a generated **research queue**, not evidence of completed origin histories.

## Full-queue findings
- **428 records / 428 distinct canonical IDs** across five disjoint cohorts (100/100/100/100/28); no duplicate IDs between cohorts.
- **428/428 have localized display titles in exactly EN, IT, ES, FR, DE, PT.** This does *not* establish that any original historical story has been translated.
- **0/428 have `documentedIntroductionYear`, `historicalFoundingEvidence`, or `individualOriginalStoryEN` populated.** All 428 remain `ORIGIN_SOURCE_RESEARCH_NOT_YET_COMPLETE`; none is promoted by this audit.
- **55 distinct source-index URLs** across 428 records. Source-index presence is not individual origin provenance. Source lists must be checked against each claim, not inherited wholesale.
- Highest-reuse source indexes: Australian DFAT national-days index **156** records; EURES public-holidays calendar **56**; Slovak government holiday index **26**; Czech law consolidated page **18**; Italian government ceremonial-days index **18**. These are *discovery/recognition pointers*, not proof of a historical founding date for every record.

| Cohort | IDs | Country distribution | Distinct indexed URLs |
|---|---:|---|---:|
| 01 | 100 | CZ 27, SK 26, FI 21, IT 21, EE 5 | 9 |
| 02 | 100 | PL 17, EE 14, MT 10, FR 9, AR 8, LT 8, CY 7, LV 7, PH 7, PT 7, GB 6 | 25 |
| 03 | 100 | Multiple national markets (including NO, US, ZA) | 23 |
| 04 | 100 | Broad international national-day index | 2 |
| 05 | 28 | Broad international national-day index | 1 |

The distinct-source counts are **per cohort** and must not be added to obtain the 55 global URLs because sources recur across cohorts.

## Product-boundary review (no automatic exclusion)
The queue contains four IDs with personal birthday/death wording:
- `cz-jan-amos-comenius-birthday` — check whether legally recognized Education/Teachers' Day context makes this a civic observance; a birth date alone is insufficient.
- `sk-ludovit-stur-birthday` — check distinct statutory civic designation before publication.
- `sk-milan-rastislav-stefanik-death-anniversary` — **retain**: Slovak statutory memorial day under Act 241/1993, §3, per `docs/CATALOG_RELEVANCE_POLICY_20261119.md`.
- `us-washingtons-birthday` — **retain**: federal civic holiday, not a biographical-calendar import.

## Fail-closed editorial production gates
For each ID, separately verify (1) present-day civic/official recognition, (2) historical event or campaign origin, (3) initial institution/proclamation year **only when evidenced**, (4) date-selection rationale where available, and (5) original EN story with equivalent IT/ES/FR/DE/PT copy. A date from a holiday index is not a founding year. Missing evidence means `unknown`/null or individual HOLD, not fabricated certainty. Do not set `runtimeRichEditorialApproved` from a queue audit. Keep excluded archive identities out of the published catalog. Before merge, run exact-head Python/schema/locale parity, Flutter analyze/tests, Web build, and applicable review gates.

**Net newly researched historical origins: 0. Net newly certified: 0.**
