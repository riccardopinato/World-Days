# World Days

**Discover what the world observes today.**

World Days is an English-first, multilingual Flutter consumer app for international and world observances. The product keeps canonical verified observances separate from editorial/discovery candidates and preserves provenance for every record.


### Localized observance titles
World Days keeps stable canonical observance IDs while displaying all 296 current titles in English, Italian, Spanish, French, German and Portuguese. The title packs are static and bundled at build time, so language switching and search stay fully offline. Search accepts both localized and canonical English titles.

## Current implementation

This repository starts from the verified World Days product/data foundation and the App Factory baseline `23c5b0f6b5f02a93e03bb36106f12575a58129d3`.

Implemented in this first real repository pass:
- bundled official catalog and 2026 occurrence index;
- deterministic recurrence engine;
- Today, Calendar, Discover, Saved and Settings navigation;
- observance detail/source transparency;
- local favorites, recents, streak and profile preferences;
- EN/IT/ES/FR/DE/PT UI localization plus reviewed editorial locale packs;
- responsive Material 3 theme;
- lightweight visual-key artwork across Today, cards and detail;
- themed Discover collections and locally generated share cards;
- configurable daily/weekly/favorite/category local reminders with notification diagnostics;
- Android Today Home Screen Widget backed by a 45-day offline projection;
- deterministic notification/widget deep links;
- branded World Days launcher icon;
- UMP-gated top adaptive AdMob banner in QA test-traffic mode;
- public production privacy policy hosted with the Web Preview;
- stable Android release identity workflow for future in-place APK updates;
- dataset, recurrence and retention projection tests;
- GitHub Actions for real Flutter analyze/test/Web/Android validation.

Provider-sensitive monetization and production signing remain layered after the green Flutter baseline. Native notifications/widget are now implemented in Step 9 but require exact-artifact physical-device acceptance before certification.

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
