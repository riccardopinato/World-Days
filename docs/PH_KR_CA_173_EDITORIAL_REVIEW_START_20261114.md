# World Days — 173 final editorial-review dossiers (started, not approved)

Snapshot: 2026-11-14, source PR #118 / #119 / #120 (all Draft and unmerged). This is **separate** from writing new national stories.

## Registry and factual review gates

The exact 173-ID record is at `data/editorial/reviews/ph_kr_ca_173_qualified_review_queue_20261114.json`. Each entry contains source PR/head/path, all six draft locales, first-party origin links, proposed event and founding years, legal/source conflicts where known, six language review slots, and explicit *no human approval/no publication* flags.

- PH: 84 dossiers awaiting final editorial review; 7 further original drafts remain source-blocked and are not part of the 173.
- KR: 57 awaiting final editorial review.
- CA: 32 awaiting final editorial review.
- **14** Philippine historical/legal conflicts remain in the upstream research register, **8** concern draft-ready IDs in this 173-ID review queue.
- Independent AI first-party factual spot checks **started for four** selected IDs (Canada Ribbon Skirt, Korea March First, Philippines Independence Day, Philippines Ninoy Aquino Day). All four six-locale narrative files had six distinguishable original texts and matched documented numerical year tokens and 3 contextual facts per locale. This is structural QA, **not professional native-language approval**.

## Blocking new finding: Philippines Independence Day

Existing source draft `ph-independence-day` (PR #120) has `firstObservedYear: 1964`. But presidential Proclamation No. **28** dated 12 May **1962** expressly declared **12 June 1962** a special public holiday to commemorate Philippine Independence Day.

Source: https://lawphil.net/executive/proc/proc1962/proc_28_1962.html

Further official documents:
- Proclamation No. 252/1964: https://lawphil.net/executive/proc/proc1964/proc_252_1964.html
- Republic Act No. 4166/1964: https://lawphil.net/statutes/repacts/ra1964/ra_4166_1964.html
- Historical 1898 date: https://philhistoricsites.nhcp.gov.ph/registry_database/site-of-the-proclamation-of-philippine-independence/

**Disposition:** block factual approval of this draft. Preserve distinct 1898 declaration and 1964 formal statutory date change, but do not assert the first-ever June-12 Independence Day observance occurred in 1964. Correct the upstream first-observed field (null unless separately proven), re-evaluate wording in all locales, obtain independent editorial review before any publication.

## Other first-party prechecks (not final approvals)

- `kr-march-first-independence-movement-day`: 1 March 1919 movement, provisional calendar Dec 1919, first commemorations 1920; 1949 statutory national-day declaration still needs detailed legal review. Official sources: https://www.mpva.go.kr/english/contents.do?key=1007 and https://overseas.mofa.go.kr/au-sydney-en/brd/m_2362/view.do?seq=760627.
- `ca-ribbon-skirt-day`: Bill S-219 Royal Assent 15 December 2022, Jan 4 annual observance and Isabella Kulak's advocacy verified through Canadian original sources https://www.canada.ca/en/crown-indigenous-relations-northern-affairs/news/2022/12/bill-s-219-an-act-respecting-a-national-ribbon-skirt-day-receives-royal-assent.html and https://publications.aws.tpsgc-pwgsc.cloud-nuage.canada.ca/site/eng/9.918672/publication.html.
- `ph-ninoy-aquino-day`: RA9256 (25 Feb 2004), fixed 21 August, special non-working national holiday, corroborated by https://lawphil.net/statutes/repacts/ra2004/ra_9256_2004.html and 2026 proclamation https://lawphil.net/executive/proc/proc2025/proc_1006_2025.html. Exact first annual event date is not independently verified.

## Final certification contract

No AI-authored or automated validation may impersonate a named qualified native editor or historical reviewer. A FINAL-certified entry requires: (1) exact-source legal/date/origin check, including variations and first observed vs legal designation; (2) no outstanding source conflict; (3) six individually vetted localized histories with native review; (4) provenance and rights; (5) named reviewer, review date and content fingerprint; (6) exact-head CI and approved publication PR.

Current completed human signoffs: **0 / 173**. The four prechecks are useful groundwork, NOT a completed certificate. PR #118/#119/#120 are not merged, and app main/runtime remain unchanged by this review PR.
