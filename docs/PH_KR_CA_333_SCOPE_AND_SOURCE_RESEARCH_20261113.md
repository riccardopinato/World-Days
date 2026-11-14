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


## South Korea candidate origin completion — 14 November 2026

**Research milestone (NOT qualified editorial certification): all `57/57` retained South Korean national candidate IDs now have a traced six-language AI historical origin draft.**

All original prior source dossiers remain on their source PRs, with exact-head provenance; added research on PR #120 remains additive, no copies of the source PR118 drafts into new canonical IDs. The initial 333-identity scope and the 153 excluded Philippine biographical entries remain unchanged.

### Last 27 Korean origin dossiers authored in this sprint

Five new sources batches under `data/editorial/research_batches/`:

| Research file | Count | Distinct national origin records |
| --- | ---: | --- |
| `kr_contemporary_5_six_locales_20261114.json` | 5 | King Sejong Birthday (2024 legal day), North Korean Defectors Day (2024), Fallen Military Service Members (2023), Couples Day (2007), Culture Day (1973, third Saturday October since 2006) |
| `kr_economy_6_six_locales_20261114.json` | 6 | Commerce and Industry Day (1964 precursor; third Wednesday March), Consumers Day (1979 law / 1982 civic / 1996 statutory), Trade Day (1964 / 1988 rename / 2012 move), Farmers Day (1996 / 1997 rename), Local Autonomy and Balanced Development Day (2012 / 2023 merger), Taxpayers Day (1969 / 1973 merger) |
| `kr_social_6_six_locales_20261114.json` | 6 | Workers Day (1963 law / 1994 May 1 date), Korean Public Health Day (1953 WHO precursor / 1973 national merger), Science Day (1969), Teachers Day (1958 youth activities / 1965 May 15 / 1982 statutory), Parents Day (1956 Mothers Day / 1973 broadened), Seniors Day (1997, Oct 2 distinct from UN Oct 1) |
| `kr_institutions_5_six_locales_20261114.json` | 5 | Corrections Day (1959 / 1973 merge / 2002 separate revival), Information and Communications Day (1956 / 1972 date / 1996 rename), Oceans Day (1996), Police Day (1957 / 1973 statutory), Armed Forces Day (1956) |
| `kr_memory_society_5_six_locales_20261114.json` | 5 | Righteous Armies remembrance (2010), Sports Day (1969 / 2023 rename), Veterans Association Day (1965 / 2002 new date), West Sea Defense Day (2016 first national ceremony), World Koreans Day (2007) |
| **Total newly authored** | **27** | **27 independent canonical candidate IDs** |

The **West Sea Defense Day** legal decree was published **22 March 2016** and the first national ceremony took place **25 March 2016**; the movable date is **fourth Friday of March**. It commemorates distinct episodes from **2002** and **2010**, and does not imply these events share the same anniversary. Government source: [Ministry of Patriots and Veterans Affairs announcement](https://www.mpva.go.kr/mpva/selectBbsNttView.do?bbsNo=16&integrDeptCode=&key=77&nttNo=5130&pageIndex=1&searchCnd=all&searchCtgry=&searchKrwd=).

**Source quality**: the [MOIS institutional history](https://www.mois.go.kr/frt/sub/a06/b08/nationalHoliday_4/screen.do) and [MOIS commemorative-day list](https://www.mois.go.kr/chd/sub/a05/feteDay/screen.do) are two views from **one** government institution, not two independent factual-review confirmations. Government milestone sources are attached per ID. Rich story bodies do not include internal QA status language; qualified-review flags stay in metadata.

**Recurrence gate**: the newly authored 27 IDs are checked against the original `data/market/wave10_hundred_kr_ph_20261111.json` calendar rules, preserving movable dates: third Wednesday March (Commerce), fourth Friday April (fallen service members), third Saturday October (Culture), fourth Friday March (West Sea). Same-date distinct observances, particularly **King Sejong Birthday and Teachers Day (May 15)**, are not automatically merged.

### Actual per-ID coverage as of this source branch

| Country | Retained candidates | Source-linked AI story in all six languages | Missing source-linked origin |
| --- | ---: | ---: | ---: |
| Philippines | 91 | 9 | **82** |
| South Korea | 57 | **57** | **0** |
| Canada | 32 | **32** | **0** |
| **All** | **180** | **98** | **82** |

Since this PR began, **55** new source-backed six-locale originals were authored; **9** PR118 EN/IT originals were extended with four additional locale drafts. Two PH/KR source research pilots on PR120 predate the 55 new stories. Total source-scoped government chronology/category spot-check records: **59**. **Human-certified: 0**. None of PR118, PR119, PR120 have been merged into main; no downstream runtime has been updated by this source-research work.

### Remaining release blockers and next factual work
1. **82 Philippine candidate origins** require history research and six-locale drafts or source-proven equivalence mapping; do not certify by nationality merely because one international day has many country views.
2. Official-source errata on the PR118 English/Italian Bonifacio Act 2946 date (Senate metadata discrepancy) and Bataan/Day of Valor (1956 presidential special holiday vs 1961 recurring legal-holiday act).
3. Independent qualified factual and native-language review **for all six locales**, licensing/source-usage clearance and explicit human signoff where required.
4. Reconciliation of original source branches PR118/119 into one deployable canonical data model, real app UI integration, and appropriate build/release gate. Successful CI on research files alone does **not** publish stories or approve them.


## Philippines national proclamation sprint — 25 original origins, 14 November 2026

**Scope:** after the previous Korean 57/57 and Canadian 32/32 research closure, the Philippine 91 retained candidate IDs were individually queued for new original histories. **25** uniquely sourced Philippine canonical origin records were added this turn, each in EN, IT, ES, FR, DE, PT; they remain AI-assisted **drafts pending qualified native-language and factual human reviews**.

### Original source dossiers created on this PR

| Six-locale research batch | Record count | Specific official/legal provenance |
| --- | ---: | --- |
| `ph_months_heritage_rights_6_six_locales_20261114.json` | 6 | Food Month 2018 Proc469, Literature Month 2015 Proc968, History Month 2012 Proc339, Museums/Galleries Month 1991 Proc798, Children's Month **2015 RA10661**, National Indigenous Peoples Month 2009 Proc1906 |
| `ph_months_language_society_6_six_locales_20261114.json` | 6 | National Bible Month 2017 Proc124, Filipino Values Month 1994 Proc479, Peace Consciousness Month 2004 Proc675, Women's Role in History Month 1988 Proc227, Language Month 1997 Proc1041, Rice Awareness Month 2004 Proc524 |
| `ph_statutory_civic_4_six_locales_20261114.json` | 4 | National Women's Day **RA6949 1990 working special holiday**, Indigenous Peoples Thanksgiving Day 2003 Proc486, Philippine Earth Day **annual since Proc1481 2008** after one-year proclamations in 1990 and 2007, NCCA founding anniversary **RA7356 1992** |
| `ph_book_health_protection_4_six_locales_20261114.json` | 4 | National Book Week 24–30 Nov **1936 Proc109**, Nutrition Month July 1974 **PD491 sec 7** replacing March Nutrition Week, **18-day** VAW Campaign 25 Nov–12 Dec **2006 Proc1172**, Order of National Artists founding **1972 Proc1001** (distinct from individual artist biography) |
| `ph_books_culture_ecology_5_six_locales_20261114.json` | 5 | Library/Information Services Month 1991 Proc837, Traditional/Alternative Health Month 2004 Proc698 (earlier RA8423 1997), Book Development Month **1999 Proc120** with earlier 1997/1998 campaigns and **move June→November from 2008 by Proc1436 s.2007**, Culture Consciousness Week 1–7 July **1973 Proc1148**, Tamaraw protection Month October **2002 Proc273** |
| **New original Philippine AI drafts** | **25** | **25 distinct canonical IDs, 150 locale narratives** |

*Source role:* Original presidential proclamations and statute text are linked per record. The NCCA calendar is used to cross-check **current month/day rules**, not as proof of every older introduction year. A law with a *specific year only* cannot be silently converted into a permanent annual designation. LawPhil reproduces government issuances; LawPhil and the original decree displayed there are not two independent editorial reviewers. Human source/translation signoff remains **zero**.

### Fixed date/period and origin integrity

The validator cross-checks all **25** records against the original `data/market/wave13_ncca_eures_100_20261111.json` and `data/market/wave10_hundred_kr_ph_20261111.json` recurrence rules. The set contains **17 month-long observances, 5 days or institutional anniversaries, 2 seven-day weeks, and 1 eighteen-day campaign**, with 1993 and 1990 earlier commemorations tracked distinctly in corresponding dossiers.

- **National Children's Month**: 1993 **October** under Proc267; **Nov** since RA10661 approved **29 May 2015** (which repeals the previous proclamations). The NCCA date listing uses an inconsistent "2014" shorthand; primary enacted law 2015 takes precedence.
- **Indigenous Peoples**: individual **29 October Thanksgiving Day** from 2003 Proc486 is *not the same original event* as the **whole month of October** under 2009 Proc1906. Both refer to the earlier 1997 Indigenous Peoples Rights Act and share a history cluster, but retain their own canonical IDs.
- **Women's recognition**: March 1988 Women's Role in History Month (Proc227) differs from **8 March National Women's Day, a special *working* holiday** (RA6949 1990). Neither implies a general nonworking holiday. A Senate approval-date header conflicts with the signed text's exact day; our six-language copy uses year 1990, not a disputed day.
- **Book history**: National Book Week **24–30 November** (1936 Proc109); National Book Development Month originally **June** (permanent from 1999, observed in earlier 1997/98 years), shifted to **November starting 2008** (2007 Proc1436); April 2015 National Literature Month (Proc968) is a separate literary-arts observance.
- **Peace**: National Peace Consciousness Week was 28 February–6 March (2002 Proc161); September month **from 2004** (Proc675) replaced that older period.
- **Anti-violence campaign**: Philippine **18 days from 25 November to 12 December** (2006 Proc1172) extends the earlier international **16 days from 25 November to 10 December**. The date crosses the month boundary; it is not a single week.
- **Nutrition**: July month from **PD491 sec.7 1974** replaced the old Nutrition Week in March.
- **Philippine Earth Day**: original one-year presidential proclamations in **1990** and **2007** precede the recurring **22 April from 2008 Proc1481**; the national decree does not create the international Earth Day.
- **National Artists**: **27 April 1972 Proc1001** established a governmental artistic distinction and first named Fernando Amorsolo; this is distinct from the personal birth/death dates excluded from new PH editorial scope.
- **Tamaraw**: special protection of an endemic Mindoro species, **October since 2002** Proc273; not a generic international endangered-species day.
- **National culture**: annual 1–7 July Week designated **1973 Proc1148** and followed by official agency action Memorandum Circular No. 644 in June 1973.

### Explicitly unresolved primary-source conflicts

Tracked in `data/editorial/audits/ph_open_legal_source_conflicts_20261114.json` (4 individual IDs):
1. `ph-w13-national-punctuality-and-civility-consciousness-month`: Proc1638 explicitly declares **November 2008**, but the current NCCA source lists the month as recurring annually. **Do not infer permanent statutory annual recurrence from the one-year decree**; no full source-verified origin draft yet.
2. `ph-w13-week-of-the-philippine-eagle`: Proc79 under the **1999** index and heading is internally transcribed as signed **1998**. Exact legal sign-year must be checked against authoritative original, rather than guessing based on officeholder. No full source-verified six-locale draft yet.
3. `ph-w10-philippine-national-women-s-day`: RA6949 Senate metadata date (9 Apr 1990) differs from signed statutory text (10 Apr 1990); **year-only used** in published-unapproved draft and human approval locked.
4. `ph-w13-national-children-s-month-philippines`: NCCA calendar year shorthand 2014 differs from primary **RA10661 approved May 2015**; the six-language origin draft follows the act and documents older 1993 October status. Qualified approval still locked pending discrepancy signoff.

### Count snapshot and release status

| Country | Retained candidates | Six-locale original/history drafts | Lacking a linked six-locale original history |
| --- | ---: | ---: | ---: |
| Philippines | 91 | **34** | **57** |
| South Korea | 57 | **57** | **0** |
| Canada | 32 | **32** | **0** |
| **Combined** | **180** | **123** | **57** |

The aggregate **123** includes earlier linked PR118/119 histories, original dossiers authored on PR120, and additional PR118 locale translations on PR120. All remain **source-linked AI drafts**, not qualified editorial approvals. **0 human-certified**; PR118, PR119 and this PR120 remain **Draft/unmerged**, and **nothing is released to main or the runtime**. Next priority is the other 57 Philippine IDs, including the two blocked by original legal-source conflicts.


## Philippines-only law and institution sprint — 41 unique origins, 14 November 2026

**Explicit geographical focus:** only Philippines this sprint. The Korean 57/57 and Canadian 32/32 candidate source drafts were not rewritten. **41** individual Philippine canonical candidate origin records were authored as six substantial AI research locales each (**246 source-linked locale narratives**), in eight new research batches on PR #120:

| File under `data/editorial/research_batches/` | Original PH candidates | Focus |
| --- | ---: | --- |
| `ph_civic_holidays_8_six_locales_20261114.json` | 8 | First Republic, China/Spain diplomatic relationships, literacy, teaching, flag display, school reading, indigenous national day |
| `ph_civic_months_6_six_locales_20261114.json` | 6 | Public service, rule of law, December volunteers, Oct10 local government, overseas Filipinos, tropical fabrics |
| `ph_seafarer_coconut_republic_balagtas_4_six_locales_20261114.json` | 4 | Seafarers, seven-day Coconut Week, historic July4 Republic Day, Balagtas |
| `ph_heroes_awards_5_six_locales_20261114.json` | 5 | Mabini Tanauan law, Living Treasures award 1992, Graciano López Jaena, Iglesia ni Cristo, Jose Abad Santos |
| `ph_local_heritage_honors_4_six_locales_20261114.json` | 4 | Julian Felipe **Cavite City only** legal nonworking, animal kindness 1958, Gabriela Silang and Lakandula honors 2003 (one code, different merit criteria) |
| `ph_institutions_military_legislature_5_six_locales_20261114.json` | 5 | Philippine Army 1897, Film Council 2002, National Museum 1901, Senate and House 1916 bicameral Jones Act (House has 1907 predecessor) |
| `ph_heritage_friendship_archives_5_six_locales_20261114.json` | 5 | British Friendship **2000 December → 2008 October**, National Archives Day 1995 after 1901 Archives Bureau, Puerto Princesa Nov11 following 2011 nature vote, Military Academy 1898 restored 1998, National Library 1887 |
| `ph_language_fisherfolk_magsaysay_independence_4_six_locales_20261114.json` | 4 | Filipino Language Commission law **1991 not 1981**, Fisherfolks Day 2000 following 1999 community petition, Magsaysay annual memorial 1966 and 1968 pre-weekend school shift, Linggo ng Kalayaan June6–12 1992 |
| **Sum** | **41** | **41 separate canonical IDs; 246 full drafted locale stories** |

### Philippine source conflicts and publishing blocks

The scoped file `data/editorial/audits/ph_open_legal_source_conflicts_20261114.json` documents **12** individual conflicting histories or date/year interpretations, cross-linked to primary public sources. **Six must not get a source-certified original until resolved or explicitly corrected in original national market dataset**:
1. **DepEd founding**: NCCA says **20 December**, but DepEd officially celebrated its 126th foundation anniversary **23 June 2024** for the **23 June 1898** revolutionary government institution; 20 December 1863 is a different education-decree milestone.
2. **Made-in-the-Philippines Products Week**: NCCA retains **17–23 August** from Proc76 **1936**, but Proc756 **30 Sept 1941** explicitly superseded it with **14–20 February from 1942**. An original source-supported current calendar cannot simply preserve the superseded August week.
3. **Volunteerism Month (May)**: Proc1778 from **May 2009** uses "the month of May" without explicit annual recurrence; distinguish from **National Volunteers Month every December** under Proc55 **1998**; need later official confirmation for the May yearly calendar.
4. **NHCP founding**: NCCA and a government budget summary use **26 May 2010**, while signed RA10086 (Senate and Supreme Court) was **12 May 2010**, and implementing rules record effectivity in June 2010; May26 requires a separately sourced historical referent, not an inferred passage date.
5. **National punctuality/civility month**: signed Proc1638 says **November 2008**, unlike the recurring annual NCCA item.
6. **Philippine Eagle Week**: Proc79 indexed/signed-heading **1999**, transcribed last line **1998**; exact signature year needs source reconciliation.

**Another six** are written as transparent drafts but qualified editorial approval remains blocked by source metadata discrepancies or historical interpretation:
- Commission on Filipino Language established through RA7104 **14 August 1991**, not “1981” as NCCA index; a 1999 Presidential executive order confirms 1991.
- National Children's Month is **November since RA10661 approved 29 May 2015**, after October 1993, not “2014” in NCCA calendar.
- Reading Day RA10556 was approved **15 May 2013**, not NCCA's “2012”; November27 is subject to preceding-Friday school observance if weekend.
- National Women's Day RA6949 index vs signed exact **April 1990** approval-date discrepancy; draft reports the uncontroversial year.
- December National Volunteers Month Proc55 **5 Dec 1998**, although a later DepEd memo erroneously reports 1988; primary decree 1998 controls draft.
- July4 Republic Day RA4166 originally put it in the holiday list in **1964**, but **1987 Executive Order292** regular-holiday list omits July4; do not label it a permanent national nonworking holiday now.

**Cross-jurisdiction boundaries that must be preserved**: Philippine–Spanish Friendship Jun30 **national special working** but **special nonworking in Aurora**; Mabini Jul23 **special working only in Tanauan**; Julian Felipe Jan28 **special nonworking only in Cavite City**; other provincial one-off historical proclamations are not national perpetual holidays. The two different honors in EO236 2003 share legal origin but not award criteria. Senate Aug29 1916 Jones Act legal creation vs Oct16 first sitting; House had a Philippine Assembly predecessor Oct16 1907. Military Academy Oct25 1898 founding line replaced prior Feb17 1905 anniversary under 1998 proclamation. Library Aug12 1887 Museo-Biblioteca is separate from public library opening March9 1900.

### Latest mechanically checked candidate coverage on this branch

| Country | Scope | Six-locale AI source drafts | Without full origin |
| --- | ---: | ---: | ---: |
| Philippines | **91** | **75** | **16** |
| South Korea | 57 | 57 | 0 |
| Canada | 32 | 32 | 0 |
| **TOTAL** | **180** | **164** | **16** |

The remaining **16 PH candidate IDs** consist of six explicitly held legal/date source conflicts and ten other source investigation candidates; their status is traceable in the 180-ID matrix. The 164 six-locale histories include originals from linked draft source PRs #118/#119, **121 new original six-locale dossiers** on PR #120 and 2 earlier pilot originals, plus 9 four-locale overlays referencing original PR118 English/Italian stories. **Human-certified editorial 0, independently reviewed native-language 0, source PRs remain Draft/unmerged, runtime 0 new publication.** Do not treat mechanically passing code/dataset CI as historical approval.


## Philippines-only movable civic dates — four more original six-locale histories

After the previous **41** Philippine original narratives in this single-country sprint, a further **4** unique PH canonical source histories have been authored in `data/editorial/research_batches/ph_civic_environment_movable_4_six_locales_20261114.json`, all six languages (24 new article texts; sprint total **45 unique PH stories / 270 localized narratives**). Source primary legal documents and NCCA exact calendar entries were cross-referenced:

| Canonical ID | Statutory/first historical year | Precise canonical recurrence | Primary authority |
| --- | --- | --- | --- |
| `ph-w13-conflict-resolution-day-philippines` | **2006**, Proc1152 | **THIRD_THURSDAY_OCTOBER**, not a fixed date | Presidential Proclamation 1152 of Oct9 2006, referring to RA9285 of 2004 |
| `ph-w13-unknown-citizens-day` | **1936**, Commonwealth Act152 | **SECOND_SUNDAY_JANUARY**, not a fixed date | Commonwealth Act 152, Nov9 1936; honors ordinary citizens, not the birth of a named public figure |
| `ph-w13-w-a-t-c-h-time-consciousness-and-honesty-month` | **2009**, Proc1782 | `JUNE` in NCCA market catalog; **legal yearly recurrence not expressly stated** by original 2009 proclamation | [Presidential Proclamation 1782](https://lawphil.net/executive/proc/proc2009/proc_1782_2009.html), with civic actions in the second June week; additional human review required |
| `ph-w13-world-clean-and-green-week-philippines` | **1993**, Proc244 | **SEP17_SEP23** | Presidential Proclamation 244, also establishing the separate whole September cleanup month |

**Important technical gate:** new Philippine original-history research runs a per-ID comparison to the source `NTH_WEEKDAY` recurrence rules in the original Wave13 market archive for both movable days. These are explicitly different from `FIXED_DATE` and `FIXED_RANGE`; the validator must not freeze a date from a single calendar year. The additional W.A.T.C.H. June annual legal recurrence uncertainty is recorded as an **unresolved** item in `data/editorial/audits/ph_open_legal_source_conflicts_20261114.json`, increasing the documented legal/source discrepancies from 12 to **13**. Its source-linked AI draft is **not human certified**.

### Updated source-research matrix at this exact branch stage

| Country | Retained ID candidates | Source-linked AI history in six languages | Still missing |
| --- | ---: | ---: | ---: |
| Philippines | **91** | **79** | **12** |
| South Korea | 57 | 57 | 0 |
| Canada | 32 | 32 | 0 |
| **TOTAL** | **180** | **168** | **12** |

PR #120 has **125 newly authored original six-locale AI dossiers** (plus 2 older pilot full original histories and 9 PR118 locale overlays; exact origin link and source ownership preserved), all pending independent native-language and historical human review. **Human-approved 0; PR remains Draft and unmerged; no runtime build publication.** Exactly 12 Philippine IDs still lack source-linked full originals, including six held specifically due to documentary contradictions.



## Final Philippine source-first sprint milestone: 84 of 91 originals

The work in this continuous **Philippines-only** turn has now authored **50 unique PH six-language AI original-history research dossiers (300 new localized narratives)** across the nine original batches above plus the following:

- `ph_civic_environment_movable_4_six_locales_20261114.json` (4): **third Thursday of October** Conflict Resolution Day (2006 Proc1152), **second Sunday in January** Unknown Citizens' Day (1936 Commonwealth Act152), June W.A.T.C.H. Month (2009 Proc1782, permanent annual legal recurrence not proven), **17–23 September** World Clean and Green Week (1993 Proc244).
- `ph_edsa_life_unweek_3_six_locales_20261114.json` (3): **22–25 February** EDSA People Power Commemoration Week (2007 Proc1224, not four automatic days off); **third Sunday of January** Sanctity and Protection of Human Life Day (2003 Proc490, distinct from still-unverified Childrens Day on same Sunday); **18–24 October** United Nations Week (2003 Proc483 makes permanent the specific-week celebration after Proc276 in 2002).
- `ph_panagyaman_theater_2_six_locales_20261114.json` (2): April **Panagyaman Rice Festival Month**, with Proc606 only declaring **April 2004** and the ongoing annual legal basis **unverified**, despite NCCA recurring calendar; **21–27 March** UNESCO–ITI World Theatre Week expressly established every year by 2007 Proc1262, connected but not identical to international single World Theatre Day on 27 March.

**Research coverage now PH84/91, KR57/57 and CA32/32, total 173/180 six-locale source-linked AI historical drafts; 7 Philippines candidates remain without such a draft.** The branch PR120 now contains **130 new six-locale original records**, plus two prior pilots and nine translation overlays referencing source Wave20; *every* draft still requires independent qualified historical/native-language human signoff. Human certified **0**, PR **Draft**, main app unmodified. The legal discrepancy registry now contains **14** individual source conflicts, including annual-recurrence uncertainty for W.A.T.C.H. and Panagyaman.

### Seven unresolved Philippine original-source IDs to handle separately before release

| Source canonical ID | Why no six-locale source-certified history yet | Required evidence/next decision |
| --- | --- | --- |
| `ph-w10-philippine-department-of-education-founding-anniversary` | NCCA **20 December** vs DepEd institution anniversary **23 June 1898**; Dec20 refers to a different earlier school reform in 1863 | Match canonical observance identity to a single official event and correct national date or preserve a distinctly named 1863 predecessor |
| `ph-w10-philippine-national-historical-commission-founding-anniversary` | NCCA **26 May** vs signed **RA10086 12 May 2010** (institution predecessors 1965/1972) | Identify an official 26 May event independent of the act or correct the canonical date |
| `ph-w13-children-s-day-philippines-january` | NCCA shows **third Sunday of January**, same as Proc490 **Sanctity/Protection of Human Life Day**; no checked independent Philippine national Children's Day statute supporting this January recurrence | Verify distinct original law or mark catalog duplicate/mislabeled national observance. National Children's Month is separate November from RA10661 (2015) |
| `ph-w13-made-in-the-philippines-product-week` | NCCA Aug17–23 from Proc76 1936 conflicts with the later **Proc756 1941**, which moved the week to **Feb14–20 from 1942** | Check the latest controlling statute before revising the canonical recurrence; cannot certify superseded August dates |
| `ph-w13-national-punctuality-and-civility-consciousness-month` | Proc1638 says **November 2008**, not unambiguously **every** November | Obtain source for enduring annual government observance; otherwise classify the original as a year-specific 2008 campaign |
| `ph-w13-volunteerism-month-philippines` | Proc1778 says **May 2009**, not explicitly **every May**; different from **December National Volunteers Month** (Proc55 1998) | Verify current annual May legal basis and retain separate canonical IDs for May and December |
| `ph-w13-week-of-the-philippine-eagle` | Proc79 document indexed/headed **1999** but final transcribed signing year **1998**, so exact original date unverified | Inspect authentic official source signed version and confirm later annual continuity before full historical signoff |

Technical validation of original `NTH_WEEKDAY`, `FIXED_RANGE`, and `FIXED_DATE` rules for all new PH research records is now required; 14 open-source conflicts remain separately gated. A Draft research story is *not* equivalent to certified historical information or an app release.

