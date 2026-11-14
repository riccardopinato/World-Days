# World Days — Top five national authoring backlog (2026-11-14)

Exact calculation from the **1111 canonical records** at `main@056efe355b19640cbbc1dfd5cb9755cbf053e6f6`, including research handoff from PR #121.

**Country rank (remaining NEW origin-story authoring, not human approval):**
1. Czechia `CZ`: **28** pending (28 total; 0 researched in main).
2. Slovakia `SK`: **27** pending (29 total; 2 already researched in main).
3. Italy `IT`: **24** pending (27 total; 3 already researched in main).
4. Finland `FI`: **22** pending (23 total; 1 already researched in main).
5. Estonia `EE`: **20** pending (20 total; 0 researched in main).

These top five contain **121** pending of the **461** national candidates. Another 17 globally scoped IDs comprise the remaining **478** new historical research targets in the current editorial scope.

Deterministic generator: `tool/report_country_authoring_backlog.py`; output artifact `reports/country_authoring_backlog_20261114.json` in the Development checks run. It excludes the exact 173 prepared six-locale draft IDs already captured, 153 PH biographies out of editorial scope, and main researched origin IDs. No country labels assigned to global stories.

## Initial bounded source-first wave: five stories × six languages

File: `data/editorial/research_batches/top5_country_first_five_six_locale_20261114.json`

| Country | Exact canonical ID | Date / recurrence | Verified event and legal distinction |
| --- | --- | --- | --- |
| CZ | `cz-independent-state-restoration` | Jan 1 | 1993 state independence / Act 245/2000 statutory state holiday |
| SK | `sk-czechoslovak-state-day` | Oct 28 | 1918 shared Czechoslovak state creation / currently national state holiday, **not a day off** |
| IT | `italian-republic-day` | Jun 2 | 1946 referendum / Law 260/1949 national holiday |
| FI | `fi-finnish-independence-day` | Dec 6 | 1917 parliamentary independence declaration / exact founding year of annual celebration not claimed |
| EE | `ee-restoration-of-independence-day` | Aug 20 | 1991 Supreme Council restoration vote (69 yes), legal continuity with 1918 state |

Each ID has original **EN/IT/ES/FR/DE/PT** `heading`, `origin` narrative, `promoter`, `purpose`, and **3 contextual facts**, at least two institutional first-party sources, a legal/year separation note and explicit unknown first annual celebration year. These are **30 AI-written localized drafts**, *not* 30 native-approved publications.

Provenance leads, checked 2026-11-14:
- Czech law: https://e-sbirka.gov.cz/eli/cz/sb/2000/245/2026-05-13 ; Constitution: https://e-sbirka.gov.cz/sb/1993/1?odkazId=209235361&predmetneDatum=2027-07-01
- Slovak government current state holidays: https://www.vlada.gov.sk/slovensko/statne-sviatky/ ; historical note: https://www.vlada.gov.sk/tlacove-spravy/den-vzniku-samostatneho-ceskoslovenskeho-statu/
- Italy Senate 2026: https://www.senato.it/CESUS/2026/2giugno/ ; Law 260/1949: https://www.normattiva.it/atto/caricaDettaglioAtto?atto.codiceRedazionale=049U0260&atto.dataPubblicazioneGazzetta=1949-05-31&tipoDettaglio=vigente
- Finnish civic/Parliamentary source: https://finland.fi/life-society/main-outlines-of-finnish-history/ ; independence day statute: https://www.finlex.fi/en/legislation/collection/2025/1259
- Estonia Riigikogu: https://www.riigikogu.ee/en/press-releases/celebrations-of-the-30th-anniversary-of-the-restoration-of-estonias-independence-at-toompea/

## Acceptance

The authoring queue remains **478 pending** until these research drafts have been successfully adopted and deduplicated on an approved branch. Once incorporated into the source-researched registry, the same five IDs must not be counted again. Historical/linguistic human signoff remains 0/5 and runtime rich publication is unchanged.

Pending follow-ups: 116 remaining stories in these five countries, plus other national/global stories, full item-by-item legal/source checks, qualified review in six languages and guarded merge. Never confuse original event date, legally established annual observance or the date of a first ceremony.
