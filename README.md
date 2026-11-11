# World Days

## Wave10 — 100 national institutional-calendar additions (PR pending)

The next exact 100-record source batch adds **50 commemorative days** listed by South Korea's Ministry of the Interior and Safety and **50 artist/cultural anniversaries and remembrance dates** indexed by the Philippine National Commission for Culture and the Arts. Proposed catalog: **611 → 711 unique canonical identities** (**289 global + 422 national**) with 36 country choices unchanged.

Authority: [Korean Ministry of the Interior and Safety official commemorations](https://www.mois.go.kr/chd/sub/a05/feteDay/screen.do); [Philippine National Commission for Culture and the Arts official significant-date index](https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/). **Philippine artist birthday/death anniversaries are cultural calendar dates, NOT new legally designated public holidays.** Source status, Korean original titles, recurrence rules and source-classification boundaries are retained in the batch; NCCA's live page may deny automated access, so its web-index extract needs direct-page verification before final editorial certification.

Six localization keys are present, but EN fallback in IT/ES/FR/DE/PT is flagged `ENGLISH_FALLBACK_NATIVE_REVIEW_PENDING` for all 100. `introducedYear` remains absent unless separately established. The new 100 are `editorialStatus=STUB`, preserving the 56 existing source-reviewed long-form narratives. This is a catalog-only PR with no APK/signing/device/Play activity.


## Wave09 — 73 national observances; 100 new canonical records across Wave08 + Wave09 (PR pending)

This proposal adds **73 primary-institutional national calendar identities** in **Slovakia (23), Czechia (18), Poland (13), Sweden (9), Norway (5), Finland (5)**. Existing source-approved Wave08 contributes **27 new Canadian identities**. After a green CI and merge, these two waves together will have introduced **100 new canonical records** from the 511-record baseline, resulting in **611** (**289 global + 322 national**) with **36 markets** unchanged.

Direct source authorities: [Slovak Government memorial-days law summary](https://www.vlada.gov.sk/slovensko/statne-sviatky/), [Czech Ministry legal text 245/2000](https://ppropo.mpsv.cz/zakon_245_2000), [Polish Culture Ministry official state-flag schedule](https://www.gov.pl/web/kultura/obowiazek-wywieszania-flagi-panstwowej-rp), [Swedish Riksdag flag-day regulation](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/forordning-1982270-om-allmanna-flaggdagar_sfs-1982-270/), [Norwegian Government state flag regulations](https://www.regjeringen.no/no/dep/ud/dep/diplomatiske-forbindelser-og-protokoll/norges-flagg-forskrift/id449230/), [University of Helsinki Almanac Office 2026](https://almanakka.helsinki.fi/en/flag-days-and-holidays/flag-days-in-2026).

**Localization debt disclosed:** EN titles are currently intentional fallback texts in IT/ES/FR/DE/PT for the 73 Wave09 additions. UI works in six locales, but these **73 localized title translations have not yet been prepared or certified**. The new 73 remain `editorialStatus=STUB`, all founding years are unknown until independently supported, and the existing **56 reviewed long-form stories** are unchanged. No APK, Android signing, device, Play or production release.


## Canadian Heritage Wave08 — 27 national commemorations (PR pending)

A Canadian Government institutional-calendar batch proposes 27 additional Canadian civic/remembrance entries in the offline source generator, with six display-title locales and review-gated source metadata. Proposed catalog **538 unique = 289 global + 249 national**, with Canada increasing **5 → 32** records. No new country option, billing, APK, device or Play publishing. All 27 entries remain rich-editorial STUB without fabricated establishment years.

Originating index: https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days.html . This includes national and recognized community observances, not necessarily statutory public holidays; do not conflate jurisdictional significance with holiday entitlement. Source-specific establishment acts and native-locale editorial approval are distinct future gates. Reviewed long-form narratives remain **56**. Do not claim these new records are on main until the protected CI and PR merge succeed.


## Wave07 — 32 documented national days across five additional markets (PR pending)

The proposed source pack `2026.11.10.3` adds **32 canonical national observances** in **Estonia (17), Latvia (5), Lithuania (6), Iceland (3), Luxembourg (1)**. Distinct source-level identities grow **479 → 511**, with **289 global + 222 national** records, **36 country choices**, and English plus IT/ES/FR/DE/PT display titles. Previous IDs, favorite identity and calendar visuals remain untouched. **This is a PR proposal until reviewed, validated and merged**.

Primary sources: [Estonia national and flag days](https://www.eesti.ee/en/artikkel/republic-of-estonia/republic-of-estonia/national-public-and-school-holidays); [Latvian Ministry of Foreign Affairs](https://www.mfa.gov.lv/en/latvian-national-holidays); [Lithuanian Seimas labour code, Article 123](https://e-seimas.lrs.lt/portal/legalActPrint/lt?actualEditionId=bappumbxwA&category=TAD&documentId=10c6bfd07bd511e6a0f68fd135e6f40c&jfwid=-zl0c8j43x); [Central Bank of Iceland 2026](https://cb.is/about-the-bank/public-holidays-in-iceland); [Luxembourg Labour Inspectorate](https://itm.public.lu/en/conditions-travail/conges/jours-feries.html).

Unknown first-established years remain `null`, not guesses. Rich editorial remains **56 reviewed**, all new 32 entries `STUB`, **430 still NOT_RESEARCHED_LONG_FORM**, **70 supported introduced years**, **441 unknown**. Localized display titles are implementation drafts, not professional native-linguistic certifications. No APK, signing, Android physical QA, Play Store or release actions authorized.


## Wave06 primary-national catalog — 16 source-backed observances in 3 new markets (PR pending)

Wave06 proposal adds **16 fixed-date national observances** across **Malta (8), Croatia (4) and Cyprus (4)**, sourced from government or competent public-authority 2026 holiday calendars. Proposed catalog **479 canonical identities = 289 global + 190 national**, with **31 market choices** and complete six-language display-title coverage. Original 463 IDs remain stable. The seven UNESCO/WHO additions in PR #76 have been merged; this change is **not yet merged**.

The 16 Wave06 entries have `editorialStatus=STUB` and no fabricated introduction years. Existing **56 source-reviewed rich histories** remain unchanged. The tally of sourced introduction years stays **70**, with **409 unknown** (displaying `*`). **398 catalog entries are still classified NOT_RESEARCHED_LONG_FORM**, excluding separate candidate stages. Translations require qualified linguistic acceptance before asserting editorial approval. No APK, signing, native device certification, billing or Play release.

[Source batch](data/market/wave06_primary_mt_hr_cy_20261110.json) · [dedicated validator](tool/market_wave06.py) · [generated catalog gate](tool/validate_wave06_generated.py).


## Institutional Wave05 — seven global admissions (10 November 2026, PR pending)

Candidate version `2026.11.10.1` adds **7 institutionally documented global records** (UNESCO ×6, WHO ×1) to the deterministic catalog: **463 distinct records** = **289 global + 174 national**. Existing IDs are retained, and all seven title translations are supplied in EN/IT/ES/FR/DE/PT. Exactly **five** new establishment-year fields are supported by originator documentation; two are intentionally left unknown. Source-reviewed **Rich Editorial remains 56**, with **382 records** lacking approved long-form stories; 70 introduction years have documented sources and the remaining 393 display `*`. All seven new entries remain editorial **STUB**; translated display titles are pending native-language certification.

This is **source-code PR state only** until exact-head CI and merge. The Wave04 section below is a historical baseline. Owner pause on APK/signing/Android physical QA/Play release stays in force.


## Content-first Wave04 — 456 distinct observances, 28 countries (9 November 2026)

[Wave04 source and methodology](docs/CATALOG_WAVE04_15_COUNTRIES_2026-11-09.md). The offline catalog is expanded from 373 to **456 canonical identities**: **282 global** entries preserved and **174 national/institutionally recognized** entries (+83). The country selector grows from 13 to **28 countries**, adding Czechia, Slovakia, Norway, Finland, Sweden, Poland, Ireland, Netherlands, South Africa, Philippines, New Zealand, Singapore, South Korea, Argentina and Peru. New titles are localized for EN/IT/ES/FR/DE/PT, and fixed/movable recurrence rules are source-gated.

**Truth and editorial distinction:** 56 Rich Editorial stories currently REVIEWED and shipped; 25 complete six-locale candidate drafts remain **PENDING qualified human/source review**, not runtime approved; 375 records still lack researched in-depth narratives. 65 introduced years are source-supported, unknown 391 show `*`. The new metadata records are not misrepresented as 83 approved histories. The Finnish Almanac customary flag days are *institutionally recognized*, not government-established statutory holidays.

Content revision **2026.11.09.4**, original 373 IDs and user preferences preserved. The 1,000+ unique-date ambition remains **open (544+ new sourced records still required)**.

**Owner pause:** APK creation/signing, Android physical certification, Play Billing and Google Play release all remain SUSPENDED. Only source Flutter CI and Web Preview may run. Old figures farther down this README remain historical snapshots, not the latest source truth.

## Content Wave03 — 13 countries, 373 verified-identity observances (9 November 2026)

Source candidate built by [World Days Country Wave03](docs/COUNTRY_WAVE03_SIX_NEW_MARKETS_2026-11-09.md): **373 canonical observances** = **282 GLOBAL + 91 NATIONAL**, adding 19 primary-source country records beyond the previous 354. Six additional selectable countries **Canada, Australia, Brazil, Mexico, India and Japan** bring the total to **13** countries. Their names and all record titles are available across EN/IT/ES/FR/DE/PT. National observances and shared global days remain separate in country browsing. Content version **2026.11.09.3**.

- 64 introduction years with explicit official evidence; 309 unknown founding years render as `*`. Workday substitute holidays are NOT treated as new commemorative dates.
- **56 Rich Editorial articles REVIEWED and shipped**; **25 stories now have six-language candidate texts** (150 editions: 8 Wave04, 9 Country Wave01, 8 Country Wave02). These are AI-assisted drafts requiring **qualified human factual and linguistic review**, not runtime-approved articles. Remaining **292** canonical IDs lack researched long-form narratives. [Exact editorial matrix](docs/EDITORIAL_25_SIX_LOCALE_DRAFT_QA_2026-11-09.md).
- The Wave03 dataset and 25-story completeness are validated in CI, with inspectable country/year/review-state artifacts. Existing 354 IDs, offline fallback and user preferences are preserved.
- **APK/signing, physical Android certification and Google Play publication remain ON HOLD** under the current product decision. Web source QA and Web Preview are allowed. Do not infer a signed mobile release from green Flutter CI.

Older counters below this heading are past snapshots and do not override this source state.

## Content-first update — Wave02, 9 November 2026

The catalog now builds **354 distinct source-linked observances** (282 GLOBAL + **72 NATIONAL**) following a second wave of **15** national/civic dates: Spain +4 (total 8), Germany +2 (total 4), Portugal +5 (total 9), United Kingdom +4 (total 8). Italy 25, France 9 and United States 9 remain unchanged. Each new entry has official institutional provenance, a correct fixed recurrence and unique titles in **EN/IT/ES/FR/DE/PT**.

- Content revision **2026.11.09.2**; original 339 IDs untouched. Country browsing keeps separate international and national sections.
- **56 REVIEWED** historical articles in the runtime. Another **25 are DRAFT only**: Wave04 8 (six locales), Country Wave01 9 (EN/IT) and Country Wave02 8 (EN/IT). **273** records still lack researched long-form histories; their source-overview remains available.
- **51** formal establishment years have a source; unknown years remain *.
- [Wave02 complete source-by-source ledger and history status](docs/CATALOG_GROWTH_COUNTRY_WAVE02_2026-11-09.md). Human historical and translation approval is required before publishing drafts.
- **APK production, signing, Android certification and Google Play are ON HOLD** by user decision; the new Flutter source/CI checks are allowed. This source update does not certify hardware or Store behavior.

Earlier content totals further down this README describe historical phases, not the latest main.

## Country catalog expansion — 9 November 2026

**Source feature:** [World Days catalog growth and history program](docs/CATALOG_GROWTH_COUNTRY_STORIES_2026-11-09.md). Source-only development, **APK and Google Play / Android certification currently ON HOLD by user request**.

- Offline canonical seed now builds **339 distinct observances (282 GLOBAL + 57 NATIONAL)**, adding 43 government-backed national/civic dates to the previous 296 without changing existing IDs or saved preferences. Seven markets: IT 25, ES 4, FR 9, DE 2, PT 4, GB 4, US 9. National and international sections are deliberately distinct.
- The new country discovery screen offers **All / National / Global** filters with counts and lazy list construction (no eager 300-card widget tree). Dates include fixed and nth/last-weekday rules; official documentation backs each new record and six-locale titles. Country overview content remains useful offline.
- Rich Editorial reviewed **56/339**. There are 8 six-language Wave04 draft stories plus 9 new EN/IT country-history drafts pending editorial and translation approval; **266** are still without a researched full narrative. Verified formal founding years = **41/339**; unknowns display *.
- The app's previous verified previews, ad settings, favorites, reminders, billing and existing remote-pack semantics are retained; content revision **2026.11.09.1** is monotonic. These changes are **not** proof of Android device behavior or publication readiness.

Older counters in this README are historical snapshots; use this section and the live sources/tests for the current state.

## Verified source status — 9 November 2026

The [five-maxi-step Audit 360](docs/AUDIT_2026-11-09_FIVE_MAXISTEPS_360.md) separates implemented source and CI evidence from physical device, Play Store and editorial review.

- The canonical catalog includes **296 observances** with offline six-locale title/overview support.
- **56/296 Rich Editorial articles** are already reviewed across EN/IT/ES/FR/DE/PT. Eight additional historical narratives in six locales were authored as **draft editorial candidates only** ([Wave04 review gate](docs/EDITORIAL_WAVE04_CANDIDATES_2026-11-09.md)); **232 records** still lack a researched full story. Source-proven introduction years remain **35/296**; proposed new years are not published.
- The around-the-world 390px layout issue #52 is fixed. Saved 296-favorite widget test is green in CI, but actual Android scrolling FPS/jank and RAM remain **NOT MEASURED**. The physical profile instrumentation is in [#54 runbook](docs/SAVED_ANDROID_PROFILE_RUNBOOK_2026-11-09.md).
- Production Release remains **BLOCKED** by [#43](https://github.com/riccardopinato/World-Days/issues/43) until Play Billing sandbox, owner controls, signed exact-source APK/AAB, notifications/widget on a physical phone and Play/AdMob declarations are documented. The source ARM64 build is not production signing.

Historical numbers and dates farther down this README describe older phases and must not override the statuses in this section.

**Discover what the world observes today.**

World Days is an English-first, multilingual Flutter consumer app for international and world observances. V1 production scope is Android-first with a Flutter Web Preview; iOS production release is post-v1. The product keeps canonical verified observances separate from editorial/discovery candidates and preserves provenance for every record.


### Localized observance titles
World Days keeps stable canonical observance IDs while displaying all 296 current titles in English, Italian, Spanish, French, German and Portuguese. The title packs are static and bundled at build time, so language switching and search stay fully offline. Search accepts both localized and canonical English titles.

## Delivery status — 3 November 2026

The scoped stabilization changes from
[PR #44](https://github.com/riccardopinato/World-Days/pull/44)
are merged on protected `main`. Automated Flutter tests, timezone
regressions and Web/Android build checks are distinct from production
release certification.

**World Days is NOT yet published/certified.** The next external
release gates are tracked in
[issue #43](https://github.com/riccardopinato/World-Days/issues/43):
a Play-installed test AAB, one-time Remove Ads purchase/restore,
exact-source signed artifact, real Android notification/widget tests,
AdMob verification and Play Data Safety/Store metadata. A release
must not be tagged until these are recorded against the identical
source/artifact hashes.

## Current implementation

The foundation references App Factory baseline `47c47f49a7b46812e3bd6f1231c3524f2b52b826` (Master v26.6 / Golden Index v18). The Golden v28 CivilDate reference was integrated as a scoped, byte-identical vendored source pilot in PR #38; this is **not** a full migration of every app subsystem to Factory v28.

Implemented in this first real repository pass:
- bundled canonical catalog and 2026 occurrence index;
- semantic category taxonomy independent from visual artwork keys;
- deterministic recurrence engine;
- Today, Calendar, Discover, Saved and Settings navigation;
- observance detail/source transparency;
- local favorites, recents, streak and profile preferences;
- EN/IT/ES/FR/DE/PT UI localization plus 296/296 localized Verified Overviews and reviewed rich editorial locale packs;
- responsive Material 3 theme;
- lightweight visual-key artwork across Today, cards and detail;
- themed Discover collections and locally generated share cards;
- configurable daily/weekly/favorite/category local reminders with notification diagnostics;
- Android Today Home Screen Widget backed by a 45-day offline projection;
- deterministic notification/widget deep links;
- branded World Days launcher icon;
- UMP-gated top adaptive AdMob banner with separate QA/test and production lanes; inline/interstitial ads are outside v1;
- public production privacy policy hosted with the Web Preview;
- permanent Android release identity with verified production APK/AAB signer continuity;
- provider-agnostic lifetime Remove Ads entitlement core plus official Flutter store-billing adapter;
- source-bound signed Android workflows: pubspec versionName/versionCode plus machine-readable source/signer/APK/AAB identity manifests;
- verified Remote Content Pack v1 with HTTPS manifest, SHA-256 gate, staged activation, rollback and immutable bundled fallback;
- dataset, recurrence, retention, entitlement and remote-content failure/rollback tests;
- GitHub Actions for real Flutter analyze/test/Web/Android validation with explicit dependency resolution and a fail-on-lock-drift gate.

Production UMP consent, Privacy Choices, banner serving and permanent Android signing have prior physical/CI validation. V1 has no separate first-party analytics SDK/event pipeline. Remove Ads code paths include non-consumable purchase, restore, pending/cancel/error handling, durable provider-finalization recovery and ad-request suppression; the Play one-time product and sandbox evidence remain open. Remote Content Pack v1 + G.1 hardening are implemented with bundled fallback, pinned GitHub Pages origin, hard-capped streamed downloads, staged rollback and hosted checksum smoke validation. Native notifications/widget still require exact-artifact physical-device acceptance. Verified Overview coverage is 296/296 in EN/IT/ES/FR/DE/PT; Rich Editorial remains a separate curated layer at 28/296 reviewed records. The post-Phase-G audit reopens exact-artifact certification for the current main SHA; see `docs/AUDIT_2026-10-15_POST_PHASE_G.md` and `ROADMAP.md`.

## Privacy

Canonical public Privacy Policy:

https://riccardopinato.github.io/World-Days/privacy.html

## Bootstrap

The repository can generate missing standard Flutter platform scaffolding deterministically:

```bash
python3 tool/build_dataset.py
./tool/bootstrap_platforms.sh
flutter pub get
flutter gen-l10n
flutter analyze
flutter test
flutter run
```

Web preview:

```bash
flutter build web --release --base-href "/World-Days/"
```

## Data

- `assets/data/official_core.json`: canonical verified/institutional seed.
- `assets/data/occurrences_2026.json`: generated full-year occurrence index.
- Discovery-source ingestion is a later content PR; the first CI baseline uses only the canonical generated catalog.

A discovery listing is never promoted to an official badge merely because an editorial calendar lists it.


## Visual content

Step 8 uses a deterministic first-party procedural illustration system as the guaranteed offline visual layer. The same visual keys drive Today/detail heroes, observance cards, Discover collections and generated 4:5 share cards.

Third-party photography is optional and cannot ship without creator, source, license, attribution and checksum metadata. See `docs/VISUAL_CONTENT_POLICY.md`.


## Remote content updates

Mobile builds can consume a versioned World Days catalog pack from GitHub Pages.
The app pins payloads to the approved GitHub Pages content origin, streams them
through the manifest byte cap, and verifies expected byte size, SHA-256 and the
full catalog domain contract before switching the active pack. Activation keeps
a previous verified version for rollback; if remote content is unavailable or
invalid, bundled assets remain usable. Web intentionally stays bundled-only.

See `docs/REMOTE_CONTENT_PACK.md`.


## Release governance

Release identity and evidence conventions are defined in `docs/RELEASE_GOVERNANCE.md`. Privacy/Data Safety engineering inputs are frozen in `docs/DATA_SAFETY_INPUTS.md`.

Production Android builds are accepted only from `main` and derive `versionName` / `versionCode` from the committed `pubspec.yaml`. Signed QA uses the same source-controlled version identity instead of the workflow run number. Both signed lanes emit an exact-artifact manifest binding source SHA, workflow run, signer and APK/AAB hashes; see `docs/PHASE_FJ_RELEASE_PREP_EVIDENCE.md`. GitHub branch-protection administration remains a repository-owner gate because the connected GitHub integration does not have Admin permission.


## Template Notion — riferimenti

[Catalogo Template Notion](docs/TEMPLATE_NOTION/README.md): ricerca su modelli potenzialmente adattabili a World Days, nessuna importazione o funzionalità attivata.
