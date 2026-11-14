# World Days — three-country editorial research and exclusion policy
Date: 2026-11-13

## Scope and immutable source
- Factory baseline: `riccardopinato/App-Factory-Core@c5adc147046beb7024629466d10eeb799c3c2619` (CURRENT: Master v27; Golden Index v29).
- Main snapshot at entry: `World-Days@e7c9fa0fbd2e82002d294ffe348f8a57bc1bf5ab`.
- Initial inventory: PR #120, 333 distinct canonical records (PH 244, KR 57, CA 32).
- Decisions: `data/editorial/audits/ph_kr_ca_333_editorial_scope_decisions_20261113.json`.
- Machine gate: `python3 tool/validate_ph_kr_ca_editorial_scope.py`.

## Country lanes (independent research)
| Country | Input IDs | Exclude from proposed editorial/public scope | Remaining **unverified** candidates | Authority/decision |
| --- | ---: | ---: | ---: | --- |
| PH | 244 | **153** | **91** | 144 Wave11 National Artist / National Living Treasure birth-death dates; 9 explicit Wave10 biographical birth-death anniversaries excluded. Keep seven independently indexed national observances, 41 Wave10 civic/institutional candidates, 43 Wave13 national months/weeks/days; verify the individual act for each. |
| KR | 57 | 0 | **57** | 7 national-day candidates and 50 ministry-recognized commemorations; verify the particular day and legal effect separately. |
| CA | 32 | 0 | **32** | Reconcile by canonical ID with existing PR #119 research and PR #118 Wave20; do not assume all 32 already have a new independent history. |
| **Total** | **333** | **153** | **180** | These are scope counts, **not** counts of approved stories. |

The Philippine exclusions are **biographical anniversary entries**, not a ban on national days named after people. Bonifacio Day, Rizal Day and Ninoy Aquino Day remain in the review queue because the national observance is a distinct legal/civic object. Institution founding anniversaries and days named for people remain subject to separate checks; the broad NCCA index alone cannot establish that each is a statutory public holiday.

The original discovery/source material stays intact for provenance and rollback. **This PR has not filtered existing Android/Web runtime records or changed user-owned saved state.** A later catalog/publication change must explicitly and transactionally apply the approved scope with stable-ID preservation, no dangling references, a version increment and regression tests. Do not treat this triage as already removed-from-production.

## Reuse a single *origin story* where the observance is truly the same
1. Resolve identity (originating organization, founding act, official title, day/date, original purpose) **before** writing or translating.
2. A globally instituted UN/UNESCO/WHO day has one canonical origin/history; country cards link to it. Country-specific participation examples and local legal status are separate optional annotations, not rewritten origin stories.
3. A locally established national remembrance or a similar-sounding day with a separate founding act is *not* automatically the same observance.
4. Preserve six source-linked translations `en, it, es, fr, de, pt` per unique origin and use explicit locale fallback. Do not generate 3x copies.
5. No title/date fuzzy match alone may create a merge, alias or deletion. Report collisions for editorial review.

## Primary evidence spot checks completed on individual national examples

### PH — Independence Day, `ph-independence-day` (12 June)
- The National Historical Commission records the 12 June 1898 declaration at Kawit.
- Proclamation No. 252 of 3 June 1964 marked 12 June 1964 as a special public holiday.
- Republic Act No. 4166, approved on 4 August 1964, changed the date of the *legal* Independence Day from 4 July to 12 June and designated 4 July Philippine Republic Day.
- Do **not** confuse event year **1898** with modern legislative designation **1964**.
- Sources: https://philhistoricsites.nhcp.gov.ph/registry_database/site-of-the-proclamation-of-philippine-independence/ ; https://lawphil.net/executive/proc/proc1964/proc_252_1964.html ; https://issuances-library.senate.gov.ph/legislative-issuance/republic-act-no-4166

### KR — March First Independence Movement Day, `kr-march-first-independence-movement-day` (1 March)
- Government veterans' ministry places the nonviolent independence demonstrations on **1 March 1919**.
- South Korean government historical address describes Provisional Government designation in its December 1919 calendar and inaugural memorial activity in **1920**.
- MOIS records the postwar National Days Act in **1949**; it is a separate legal stage.
- Sources: https://www.mpva.go.kr/english/contents.do?key=1007 ; https://www.mois.go.kr/frt/sub/a06/b08/nationalHoliday/screen.do ; https://overseas.mofa.go.kr/au-sydney-en/brd/m_2362/view.do?seq=760627

### CA — National Ribbon Skirt Day, existing canonical `ca-ribbon-skirt-day` (4 January)
- Bill S-219 received Royal Assent **15 December 2022**; the first annual observance was **4 January 2023**.
- The Canadian government identifies Isabella Kulak's experience as an impetus. This is a specific Canadian legislative observance; it is **not** a generic UN day.
- This origin is **already drafted in six locales in PR #119**. No new duplicate has been created here.
- Sources: https://www.canada.ca/en/crown-indigenous-relations-northern-affairs/news/2022/12/bill-s-219-an-act-respecting-a-national-ribbon-skirt-day-receives-royal-assent.html ; https://publications.aws.tpsgc-pwgsc.cloud-nuage.canada.ca/site/eng/9.918672/publication.html

NCCA index (official source as discovery, not proof of public holiday): https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/
Korean government national days / commemorations: https://www.mois.go.kr/chd/sub/a05/feteDay/screen.do
Canadian Heritage calendar: https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days.html

## Draft deliverables, not human certification
- This PR: `data/editorial/research_batches/ph_kr_two_national_days_six_locale_research_20261113.json` contains **2 original source-backed six-locale drafts** (PH + KR). Their provenance, dates, promoters, purposes and three facts per language are machine-checked.
- PR #119: source research for 46 Canadian index references, including 23 newly drafted Canadian-origin canonical articles and previously drafted international-origin material. The 46 indexed references are **not** 46 distinct new canonical stories, and some depend on PR #118.
- PR #118: Wave20 remains a separate draft translation dependency; no reauthoring of identical canonical histories.
- **Qualified native-language/factual human signoffs in this three-country work: 0.** `runtimeRichEditorialApproved=false`; no claim of 180 completed stories, no automatic merging/deploy/release.

## Remaining gates
1. Inspect remaining 180 retained IDs one by one for actual eligibility, original authority and valid recurrence.
2. Map shared-origin matches across the full canonical catalog, including international authorities.
3. Research each individual founding/first-observed milestone; unknown years remain null/asterisk.
4. Supply all six substantive locale stories *per distinct canonical identity*, not per market.
5. Obtain explicit qualified factual and native-language editorial signoff; machine schema checks do not substitute for it.
6. Validate generated dataset, locale parity, CI exact head, no duplicate IDs/changes to saved state, and merge only approved bounded PRs.


## Incremental research sprint — 14 November 2026

The separate per-candidate reconciliation is committed at
`data/editorial/audits/ph_kr_ca_180_origin_coverage_matrix_20261114.json`.

This matrix is the basis for further original-source editorial research.
It records the actual number of locales in the referenced branch, **not**
an assumption from an open PR title.

| Country | Retained candidates | Six-locale AI draft | EN/IT draft | No origin draft |
| --- | ---: | ---: | ---: | ---: |
| Philippines | 91 | **9** | **0** | **82** |
| South Korea | 57 | **18** | **0** | **39** |
| Canada | 32 | **32** | **0** | **0** |
| **Total** | **180** | **59** | **0** | **121** |

### Sixteen new fully localized research dossiers in this PR
- `ph-national-heroes-day` — original Act No. 3827 (1931), later last-Monday rule.
- `ph-ninoy-aquino-day` — Republic Act No. 9256 (2004), special non-working holiday.
- `ph-edsa-people-power-anniversary` — NHCP historical marker; special **working** day under 2026 proclamation.
- `ph-w13-national-heritage-month` — Proclamation No. 439 (2003), annual **May** heritage-awareness month.
- `ph-rizal-day` — 1898 national mourning decree, Act No. 345 (1902) public-holiday designation.
- `ph-w13-rizal-month` — Proclamation No. 126 (2001), annual **December** cultural month; distinct from 30 December public holiday.
- `kr-hangeul-day` — Hangeul national-day addition **2005**; public holiday resumed **2013**.
- `kr-constitution-day` — 1948 constitution, National Days Act 1949; public holiday **restored 2026**.
- `kr-liberation-day` — 1945 independence/liberation; 1948 government inauguration; 1949 national day.
- `kr-national-foundation-day` — Dangun/Gojoseon founding **legend**, distinct from verifiable event; national day Act 1949.
- `kr-memorial-day` — 1956 presidential decree and first annual observance; distinct from the five celebratory national days.

- `kr-w10-february-28-democracy-movement-remembrance` — Daegu students' protest of 28 February 1960; statutory commemoration from 6 February 2018.
- `kr-w10-march-8-democracy-uprising-remembrance` — Daejeon student protests, 8 March 1960; statutory day from 2 November 2018.
- `kr-w10-march-15-democratic-uprising-remembrance` — Masan demonstrations of 15 March 1960; statutory recognition 12 March 2010.
- `kr-w10-may-18-democratization-movement-remembrance` — Gwangju 1980; independent civic commemorations from 1981; legal national day created 9 May 1997.
- `kr-w10-donghak-peasant-revolution-remembrance-day` — 1894 peasant revolution; Hwangtohyeon anniversary selected 2018; first national ceremony under 2019 designation on 11 May 2019.


**Six original locales** for every new dossier: English master plus Italian, Spanish, French, German and Portuguese. Each narrative includes heading, substantive history/origin, promoter, significance, three facts, and at least two evidence URLs. The sixteen dossiers are stored in seven JSON research files under `data/editorial/research_batches/` and are validated by `tool/validate_ph_kr_ca_180_origin_coverage.py`.

### Correctness details that must survive downstream adoption
- The 153 Philippine biographical anniversaries are excluded from *proposed editorial scope*, but historical figures' **legally established national days** (Ninoy Aquino Day, Rizal Day, Bonifacio Day) are not excluded.
- The Korean 1949 National Days Act originally covered **four** days; Hangeul Day was added in **2005**. Do not populate 1949 as the legal introduction of Hangeul Day.
- Constitution Day in Korea regained its public holiday classification in **2026**. Old claims that it is not a public holiday are stale.
- The EDSA anniversary in the **2026 Philippine proclamation** is a special **working** day; do not label it a nationwide regular non-working holiday.
- National Foundation Day invokes a **founding legend**, never certify the legend as a historically documented foundation year.
- A NATIONAL MONTH, a NATIONAL DAY, a public holiday and an INSTITUTIONAL COMMEMORATION are distinct catalog classes.
- No new story has been merged to `main`, published in runtime or approved by a qualified human reviewer.

### Evidence and acceptance
Official sources include the Philippine Senate Legislative Reference Bureau, the Supreme Court E-Library, the NCCA/Philippine NHCP, the Presidential Communications Office, the Korean MOIS, Korean Ministry of Patriots and Veterans Affairs and official Korean legislation translations. Per-record URLs appear in the research JSON rather than relying on a single unqualified national calendar link.

Machine acceptance now enforces:
`python3 tool/validate_ph_kr_ca_editorial_scope.py` plus
`python3 tool/validate_ph_kr_ca_180_origin_coverage.py`.

**Approval is still pending qualified factual/legal and native six-locale editorial reviews; this process cannot be substituted by AI translations or CI.** Source-linked drafting improves evidence and readiness, but does not activate `runtimeRichEditorialApproved`.

### Nine Wave20 four-locale extensions without canonical-history duplication

The **nine** source-backed PR #118 Wave20 original EN/IT records have been translated into **ES/FR/DE/PT** through three additive files in `data/editorial/locale_extensions/`:

- `wave20_ph_kr_kr1_es_fr_de_pt_20261114.json` (3 Korean canonical IDs)
- `wave20_ph_kr_kr2_es_fr_de_pt_20261114.json` (3 Korean canonical IDs)
- `wave20_ph_kr_remaining_es_fr_de_pt_20261114.json` (1 Korean plus 2 Philippine canonical IDs)

All extension records pin the **one canonical English/Italian origin** on PR #118 at `477557ee6a6115e2479c2009c6daecde5a590026`. The 9 multilingual stories are complete **only when two PR-layer contributions are combined**, not standalone on PR #120 or main; they must not be copied into an independent duplicate canonical story.

### New source errata and approval locks

`data/editorial/audits/ph_kr_wave20_source_errata_20261114.json` records **two unresolved source discrepancies**:

1. **Philippine Day of Valor**: Proclamation No. 277 of 23 March **1956** declared Bataan Day 9 April 1956 a special nationwide holiday, before Republic Act No. 3022 of 6 April **1961** established the recurring legal holiday. The base PR #118 EN/IT article must incorporate this earlier official commemoration before signoff. Sources: Philippine Supreme Court E-Library Proclamation 277 and RA3022.
2. **Bonifacio Day**: the Senate legislative register's approval metadata for Act No. 2946 displays **15 February 1921**, while the full legal text says **16 February 1921**. Preserve the secure year 1921 and resolve the source discrepancy before final publication of the day-level milestone.

The three 1960 Korean movements **share a historical sequence** (and an explicit cluster ID), but are **distinct events with different local sites, dates, and statutory observance decisions**. They remain three distinct canonical commemorations, just as April 19 is separately official. Do not invent one new umbrella duplicate.

**Current snapshot**: 59/180 candidate origin stories have six-locale AI drafts (32 CA, 18 KR, 9 PH), 0 bilingual-only, 121 without a draft. New original histories created on this PR: **16**, plus **9 four-locale Wave20 translation extensions**; 20 specific official status/date classifications cross-checked. All independent qualified factual/native-language approval gates remain **open**, with **0 new human-certified stories**. No main-branch content or runtime/published catalog changes.


## Korean statutory chronology sprint — 14 November 2026, next twelve candidates

Source-of-truth for this wave: [Republic of Korea Ministry of the Interior and Safety — official statutory commemorations timeline](https://www.mois.go.kr/frt/sub/a06/b08/nationalHoliday_4/screen.do), plus linked Ministry of Patriots and Veterans Affairs reports and the [government's current commemorative-day index](https://www.mois.go.kr/chd/sub/a05/feteDay/screen.do). The two MOIS pages are **one government authority**, not two independent authority confirmations.

### Individual chronology fact patterns and source filenames

All 12 are **original AI six-locale research drafts**, each with heading, evidence-linked narrative, originating institution, purpose, and 3 factual notes, with no invented first-ceremony year:

| Canonical ID | Event or precursor | Government recognition or material date correction | New dossier |
| --- | --- | --- | --- |
| `kr-w10-june-10-democracy-movement-remembrance` | 10 June 1987 pro-democracy protests | Statutory day 2 May 2007 | `kr_june10_two_histories_six_locales_20261114.json` |
| `kr-w10-june-10-independence-movement-remembrance` | 10 June 1926 anti-colonial independence protests | Statutory day 15 Dec 2020 | same file |
| `kr-w10-provisional-government-establishment-day` | Provisional Charter 11 Apr 1919; later declaration 13 Apr 1919 | Statutory day 30 Dec 1989; date changed from 13 to 11 Apr in 2018 | `kr_provisional_jeju_two_six_locales_20261114.json` |
| `kr-w10-jeju-april-3-victims-remembrance-day` | Jeju events of the late 1940s | Statutory memorial designation March 2014, after 2013 legislative process | same file |
| `kr-w10-korean-war-remembrance-day` | War outbreak 25 June 1950; 1953 armistice | Statutory day 30 Mar 1973; designation renamed June 2013 | `kr_war_martyrs_two_six_locales_20261114.json` |
| `kr-w10-patriotic-martyrs-remembrance-day` | 1905 Eulsa Treaty; 1939 Provisional Government collective remembrance | Statutory day 9 May 1997 | same file |
| `kr-w10-railway-day-in-korea` | Gyeongin railway opening 18 Sep 1899 | Modern day 1964, integrated 1973; date changed to 28 June in 2018 | `kr_rail_cyber_two_six_locales_20261114.json` |
| `kr-w10-information-security-day-in-korea` | National information-security awareness campaign | Statutory day 22 Oct 2012; **second Wednesday of July**, movable | same file |
| `kr-w10-reserve-forces-day` | Reserve force established 1 Apr 1968; unit anniversary 1969 | Day legally established 1970; **first Friday of April** since 2006 | `kr_reserve_disability_two_six_locales_20261114.json` |
| `kr-w10-day-of-persons-with-disabilities-in-korea` | Korean rehabilitation association chose 20 Apr in 1972; government observed from 1981 | Legal welfare basis 1989; statutory commemoration 9 Mar 1994 | same file |
| `kr-w10-student-independence-movement-remembrance-day` | Gwangju student movement 3 Nov 1929 | Student Day 1953, statutory restoration 1984, renamed 2006 | `kr_students_law_two_six_locales_20261114.json` |
| `kr-w10-law-day-in-korea` | Court organization law of 25 Apr 1895 | Law Day established 1964 on 1 May; moved to 25 Apr in 2003 | same file |

**Canonical-origin decisions to preserve:**
- **Same calendar date, distinct origins**: 10 June 1926 anti-colonial independence protests and 10 June 1987 democratic protests are *not* duplicates. Each retains its original ID, chronology, year, distinct organizing ministry and legal commemoration. The shared `originClusterId` enables showing both in a date view without merging their histories.
- **Same topic, distinct national observance**: Korean 20 April Day of Persons with Disabilities is historically distinct from the UN's 3 December international observance. Do not blindly merge or rewrite a common origin.
- **Same place name, distinct era and event**: the 1929 student independence movement at Gwangju is not the May 1980 Gwangju democracy movement. Both get individual historical stories.
- **Moveable dates**: Information Security Day is second Wednesday in July; Reserve Forces Day is first Friday in April. The year-to-year calendar must compute the legal recurrence, not freeze the 2026 date.
- **Corrected event-date pair**: Provisional Government foundation commemoration was shifted from 13 April to 11 April in **2018**; Railway Day shifted from 18 September to 28 June in **2018**; Law Day from 1 May to 25 April in **2003**.
- **Legal status**: statutory commemorations must not be silently labeled regular public holidays. Human factual/native approval is still pending for every AI-authored locale.

### Updated strict per-ID coverage after this wave

| Country | Retained candidates | AI drafts in all six locales | No full origin history |
| --- | ---: | ---: | ---: |
| Philippines | 91 | 9 | 82 |
| South Korea | 57 | **30** | **27** |
| Canada | 32 | 32 | 0 |
| **Total** | **180** | **71** | **109** |

New six-locale original histories authored on PR #120 now **28** (previous 16 + these 12), in addition to 9 translations-overlay completions of prior PR #118 EN/IT records. Legal/date category spot-checks expanded from 20 to **32**. **Qualified native-language and independent historical approvals remain ZERO**. PR stays Draft, main runtime catalog unchanged. The next major research targets are the remaining 27 Korean official days plus the 82 Philippine candidate records; some may be rejected or linked to already existing global origins on detailed source examination.
