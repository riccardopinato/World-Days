## Pipeline massiva istituzionale — ingestione 30–50 giornate (10 novembre 2026)

È disponibile una pipeline **source-first** per importare lotti da 30–50 ricorrenze in un solo file JSON e una sola PR, senza modifiche manuali ripetute ai conteggi dei test Python/Dart. Vedi [manuale operativo](docs/BULK_INTAKE_INSTITUTIONAL_PIPELINE_20261110.md).

- `tool/bulk_intake.py`: confronto degli alias con il catalogo, date 2026–2028, una sola origine documentale per siti che copiano lo stesso atto, conflitti, fonti primarie, sei lingue e verifica editoriale. I record incompleti restano in ricerca.
- `data/intake/institutional_batch_template.json`: modello sicuro iniziale, **zero nuovi record ammessi**. `data/market/bulk_approved/` accetta solo file passati esplicitamente dai gate e dal revisore.
- `tool/catalog_source_contract.py`: totalizza da baseline 456 + manifest delle wave + nuovi file approvati e genera versione progressiva; test Python e Flutter derivano i valori correnti mantenendo i minimi storici.
- Due CI: una veloce per fonti/duplicati e quella completa Flutter + Web, entrambe senza pubblicazione Android/Play.

**Stato reale:** il ramo di infrastruttura parte dalla PR #73, il cui catalogo proposto è 511 (292 globali e 219 nazionali) ma `main` resta 456. Questa pipeline non aggiunge nuove giornate né autorizza merge o deploy; le traduzioni e storie richiedono la revisione editoriale realmente prevista.


---

## FAST02 Wave09 — six Asian markets, 12 national civic observances (2026-11-10)

The dependency PR #68 proposes **504 unique source records** (285 global, 219 national) after PR #67's 492. Bangladesh, Indonesia, Cambodia, Malaysia, Vietnam and Laos become selectable (34 markets total) with all six supported country-name translations, 12 fixed annual civic metadata records, original government 2026 sources and explicit 2026–2028 fixed-date tests. The original main branch is **456** pending qualified editorial review and ordered merges. The 12 new records remain `STUB`, not human-reviewed long stories. [Read country/source and quality boundaries](docs/CATALOG_FAST02_12_CIVIC_SIX_COUNTRIES_20261110.md). No APK, Play or public production deploy.


---

## Lotto unico Wave05–08: 36 nuove ricorrenze, proposta 492 (9 novembre 2026)

La PR #67 verso `main` incorpora ora 3 UNESCO, 10 Giappone, 3 India e **20 commemorazioni canadesi** in un solo ciclo CI/revisione. Totale proposto **492** (285 globali, 207 nazionali), Canada **5→25** e gli stessi 28 Paesi. Origine canonica delle 20 nuove date: [calendario Canadian Heritage e fonti legislative](docs/CATALOG_WAVE08_CANADA_20_20261109.md). È una verifica dei **metadati e della data fissa**; 36 titoli nelle sei lingue necessitano ancora revisione editoriale e le nuove storie lunghe restano STUB. Main rimane a 456 fino a merge autorizzato. Nessun APK, Play o deploy produzione.

---

## Consolidamento Wave05–07 — 16 nuove ricorrenze in una sola PR verso main (9 novembre 2026)

Le Wave05, Wave06 e Wave07 sono consolidate in **un solo lotto di review verso main**: il catalogo di questo branch è **472 (285 GLOBAL + 187 NATIONAL)** contro **456 su main**. Le precedenti indicazioni 'stacked PR #65/#66' descrivono il precedente processo di sviluppo e NON il nuovo gate di merge. Una sola revisione editoriale e una sola CI exact-head verificano le 16 giornate; nessuna lingua è autoapprovata. Dettaglio: [dossier di review consolidata](docs/CATALOG_WAVE05_07_CONSOLIDATED_REVIEW_20261109.md). Nessun deploy APK/Play o produzione.

---

## Wave07 — Three national civic holidays of India (stacked)

[Wave07 government-source dossier](docs/CATALOG_WAVE07_INDIA_2026-11-09.md): metadata-only three Indian fixed-date civic identities (Republic Day, Independence Day and Gandhi Jayanti) add three records on top of Wave06, proposing **472 unique** (285 global + 187 national), India 2→5. Parent PR #65 and stacked PR #66 must merge first, and qualified native-language/editorial approval remains pending. No live app release, APK, Play, or public Web deployment.


---

## Wave06 — seven further Japanese statutory holidays, stacked on Wave05 (9 November 2026)

[Wave06 source and test dossier](docs/CATALOG_WAVE06_JAPAN_SEVEN_2026-11-09.md). Independent stacked source PR adds seven Japanese holidays beyond PR #65 (**462 → 469**, 285 global and 184 national), with legal recurrent dates, original Cabinet Office authority, six offline language titles and structured test gates. Japanese country layer rises from six to 13; all 28 country selectors remain available. 2028 dates are computed from Article 2 law, not incorrectly described as an already published 2028 public holiday calendar.

**Neither PR #65 nor its dependent Wave06 is merged or released on main; main remains 456.** Editorial/native-speaker approval for the newly displayed titles and full narratives is pending, and all seven are STUBs. Keep APK, signing, Play and production deploy suspended.


---

## Wave05 candidate integration — UNESCO + Japan (9 November 2026)

This source branch proposes a **metadata-only** additive catalog change: **456 → 462 distinct observances** (**285 GLOBAL + 177 NATIONAL**, unchanged 28 country choices). Six entries are backed by original UNESCO/Japan government sources with full EN/IT/ES/FR/DE/PT display titles and 2026–2028 recurrence checks. All original 456 IDs are retained; **56 rich stories remain reviewed**, new entries are `STUB`, and qualified native-language/editorial approval is still required for full stories. **Main remains 456 until an independently checked merge**; nothing has been deployed to production. APK, Android signing and Google Play remain suspended.

[Wave05 provenance, expected totals and gates](docs/CATALOG_WAVE05_UNESCO_JAPAN_2026-11-09.md).

---

# World Days

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
