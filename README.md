# World Days

**Discover what the world observes today.**

World Days is an English-first, multilingual Flutter consumer app for international and world observances. The product keeps canonical verified observances separate from editorial/discovery candidates and preserves provenance for every record.

## Current implementation

This repository starts from the verified World Days product/data foundation and the App Factory baseline `fa3c0679de393f1cb13c2fed2be314d1a1269353`.

Implemented in this first real repository pass:
- bundled official catalog and 2026 occurrence index;
- deterministic recurrence engine;
- Today, Calendar, Discover, Saved and Settings navigation;
- observance detail/source transparency;
- local favorites, recents, streak and profile preferences;
- EN/IT/ES/FR/DE/PT UI localization foundation;
- responsive Material 3 theme;
- dataset tests and recurrence tests;
- GitHub Actions for real Flutter analyze/test/Web/Android validation.

Provider-sensitive modules such as AdMob, purchases, production signing and native widgets are intentionally layered only after the first Flutter CI baseline is green.

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
