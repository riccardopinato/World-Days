# World Days

**Discover what the world observes today.**

World Days is an English-first, multilingual Flutter consumer app for international and world observances. V1 production scope is Android-first with a Flutter Web Preview; iOS production release is post-v1. The product keeps canonical verified observances separate from editorial/discovery candidates and preserves provenance for every record.


### Localized observance titles
World Days keeps stable canonical observance IDs while displaying all 296 current titles in English, Italian, Spanish, French, German and Portuguese. The title packs are static and bundled at build time, so language switching and search stay fully offline. Search accepts both localized and canonical English titles.

## Current implementation

This repository uses App Factory baseline `47c47f49a7b46812e3bd6f1231c3524f2b52b826` (Master v26.6 / Golden Index v18).

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
- source-bound production Android workflow: main-only, pubspec versionName/versionCode, signer/hash evidence;
- verified Remote Content Pack v1 with HTTPS manifest, SHA-256 gate, staged activation, rollback and immutable bundled fallback;
- dataset, recurrence, retention, entitlement and remote-content failure/rollback tests;
- GitHub Actions for real Flutter analyze/test/Web/Android validation.

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

Production Android builds are accepted only from `main` and derive `versionName` / `versionCode` from the committed `pubspec.yaml`. GitHub branch-protection administration remains a repository-owner gate because the connected GitHub integration does not have Admin permission.
