# World Days — Owner-delegated AI editorial certification
Effective: 2026-11-14. Scope: six-language World Days content (EN/IT/ES/FR/DE/PT).

## Decision

At the owner's explicit request on 2026-11-14, **GPT-6 acts as the operational AI editorial reviewer** of source-linked historic stories. Do not repeatedly ask the owner to obtain separate human translation/historical signoff for routine editorial fact checking. The prior 173-item human-reviewed-queue remains intact as historic evidence and schema compatibility; it is *not* used as a compulsory blocker for performing AI source review.

AI review must **never** impersonate a human editor or falsely set `qualifiedEditorSignoff=true`. Represent the result honestly as `AI_CERTIFIED`, with evidence and the immutable source snapshot, versus `HOLD_SOURCE_DISPUTE` or `AI_REVIEW_QUEUED`. AI-certified content is not the same as app deployment or a claim of external professional legal advice.

## Evidence gate for AI_CERTIFIED

1. Confirm stable canonical ID, country, period/date and whether it is a true national observance rather than a personal birth/death anniversary or third-party calendar listing.
2. Independently check the original authority/legislative text and event history; use at least two primary documents when possible. Never infer an establishment/first-celebration year from a 2026 index; use `null` if absent.
3. Check EN master narrative and individually inspect all six localizations for crucial details (names, exact years, origin vs statute, promoter, purpose and 3+ facts). Include dates and culturally sensitive framing.
4. Keep a per-item evidence list, source PR/head/path/blob SHA, AI reviewer identity and review date; invalidate certificate if the source draft subsequently changes.
5. Conflict, missing primary support or conflicting laws -> HOLD, not automatic approval. AI can research and correct, then rerun review itself.
6. **Never** auto-publish `AI_CERTIFIED` narratives in app/runtime without corresponding import/status compatibility, source rights/provenance, CI and the repository's release gates.

## First actual decisions: 14 November 2026

Machine-readable evidence ledger: `data/editorial/reviews/ph_kr_ca_173_ai_editorial_certification_20261114.json`.
Validator: `tool/validate_ph_kr_ca_173_ai_editorial_certification.py`.

- **AI_CERTIFIED: 4 / 173**.
  - `ca-ribbon-skirt-day`: 2020 Isabella Kulak incident, Royal Assent S-219 Dec 2022, first national Jan 4 2023, six languages aligned.
  - `kr-march-first-independence-movement-day`: independence movement Mar 1 1919, provisional calendar Dec 1919, early commemorations 1920 and National Holidays Act Oct 1 1949 confirmed by ministry/archival law.
  - `ph-ninoy-aquino-day`: assassination 1983, Republic Act 9256 (2004) and 2026 special nonworking national designation source verified.
  - `ph-independence-day`: original incorrect `firstObservedYear:1964` corrected to `null` on source PR #120. Six original texts now include Proclamation 28 on 12 June **1962**; Republic Act 4166 separately passed in Aug **1964**, with original 1898 historical declaration.
- **HOLD_SOURCE_DISPUTE: 8**. These are the eight unresolved Philippine date/founding/legal conflicts already documented inside the original 173-item queue. They are unapproved until fact correction.
- **AI_REVIEW_QUEUED: 161**. Not yet individually certified. No mass approval from having six draft languages.
- Existing **7 additional Philippine ID/source blockers** remain outside the 173.

Certified here means factual/editorial **AI-reviewed**, not human reviewed, not app-published. This operational status may be promoted by subsequent guarded editorial import work after provenance, required product approvals, exact-head CI and release safety. Unresolved issues remain HOLD instead of repeatedly requiring end-user intervention.

## Sources actually consulted for four AI decisions

- Philippine historic 1962 proclamation, Supreme Court E-Library: https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/7/84843
- 1964 statutory change RA4166: https://lawphil.net/statutes/repacts/ra1964/ra_4166_1964.html
- Ninoy Aquino 2004 law RA9256: https://lawphil.net/statutes/repacts/ra2004/ra_9256_2004.html
- Presidential 2026 calendar: https://pco.gov.ph/news_releases/pbbm-issues-proclamation-declaring-regular-holidays-special-non-working-days-for-2026/
- 2026 Philippine Professional Regulation Commission: https://www.prc.gov.ph/article/prc-joins-nation-commemorating-ninoy-aquino-day
- Canada S-219 Royal Assent: https://www.canada.ca/en/crown-indigenous-relations-northern-affairs/news/2022/12/bill-s-219-an-act-respecting-a-national-ribbon-skirt-day-receives-royal-assent.html
- Canada Prime Minister first celebration: https://www.pm.gc.ca/en/news/statements/2023/01/04/statement-prime-minister-national-ribbon-skirt-day
- Korea Ministry of Patriots and Veterans Affairs: https://www.mpva.go.kr/english/contents.do?key=1007
- Korea Ministry of Foreign Affairs 2020 historic speech: https://overseas.mofa.go.kr/au-sydney-en/brd/m_2362/view.do?seq=760627
- Korean National Holidays Act No. 53/1949: https://elaw.klri.re.kr/eng_mobile/viewer.do?hseq=19634&key=1&type=part

## Second AI certification wave — 10 further Canadian items

Ten original Canadian source-linked, six-language narratives were individually
checked for historical event, adoption/first annual commemoration distinctions,
source host and calendar identity, and six-language date/facts consistency on
14 November 2026. The source PR is #119 at pinned
`3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0`.
New AI certificates:

1. National Day of Remembrance for Victims of Air Disasters (2020 order / Jan 8 2021 first).
2. National Day of Remembrance for Victims of Terrorism (2005 designation/first celebration).
3. National Seniors Day (2010 law / 2011 first).
4. National Child Day (1993 national recognition, first ceremony unknown).
5. Emancipation Day (2021 parliamentary recognition; 1834 emancipation event).
6. Remembrance Day (first armistice 1919 / modern statutory name 1931).
7. National Day of Remembrance and Action on Violence Against Women (1991 act / 1989 murders).
8. National Indigenous Peoples Day (SI/96-55 establishment / SI/2018-55 renaming).
9. National Acadian Day (1881 tradition / national federal act 2003).
10. Persons Day (1929 ruling / 1979 commemoration).

Now **14 AI_CERTIFIED, 8 HOLD, 151 remaining AI review** out of 173. Human signoffs and app runtime publication are still separate counters. The unchanged existing four historical certifications are preserved, and the CI remote source-blob/head gate remains mandatory.

## Third Canadian AI source-review wave — seven additional dossiers

Following the second wave, seven more original Canadian history dossiers were individually checked against government, Parliamentary, cultural calendars and statutory/provincial classification, with per-language chronology parity and stable origin draft blob SHA. 2026-11-14 approvals: `ca-lincoln-alexander-day`, `ca-red-dress-day`, `ca-dutch-heritage-day`, `ca-saint-jean-baptiste-day`, `ca-great-upheaval-commemoration`, `ca-indigenous-veterans-day`, `ca-sir-john-a-macdonald-day`. Confirmed distinctions include 2019 **House motion not statutory paid leave** for Dutch Heritage Day; Saint-Jean-Baptiste public holiday only in Quebec; the 1994 Winnipeg first Indigenous Veterans Day; and the 2010 Indigenous-led REDress origin. Unknown original establishment/first ceremony stays null. **21 AI_CERTIFIED / 8 source HOLD / 144 AI queued**. Runtime publication unchanged.

## Existing status reconciliation

Keep historical `humanApprovalCount=0` truthful, but do not interpret this as evidence AI cannot certify. Three separate measures: *AI editorial certified*, *human externally certified* (where relevant), and *shipped in rich app runtime*. Each has independent counters. Do not overwrite old audit snapshots; add versioned new AI decision records.
