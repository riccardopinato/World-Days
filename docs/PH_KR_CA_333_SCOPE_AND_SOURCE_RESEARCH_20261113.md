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
| Philippines | 91 | **7** | **2** | **82** |
| South Korea | 57 | **6** | **7** | **44** |
| Canada | 32 | **32** | **0** | **0** |
| **Total** | **180** | **45** | **9** | **126** |

### Eleven new fully localized research dossiers in this PR
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

**Six original locales** for every new dossier: English master plus Italian, Spanish, French, German and Portuguese. Each narrative includes heading, substantive history/origin, promoter, significance, three facts, and at least two evidence URLs. The eleven dossiers are stored in five JSON research files under `data/editorial/research_batches/` and are validated by `tool/validate_ph_kr_ca_180_origin_coverage.py`.

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
