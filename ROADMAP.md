# World Days — Active roadmap

Only open/future work is listed here.

## Step 1 — Flutter real validation
- generate platform scaffold with the pinned Flutter toolchain;
- run `flutter pub get` and commit `pubspec.lock` after resolution is proven;
- make `flutter analyze`, `flutter test`, Web build and Android build green;
- repair every compile/runtime issue found by CI.

## Step 2 — Repository / CI baseline
- merge the validated foundation PR to `main`;
- enable stable GitHub Pages Web Preview;
- keep `main` green and move later features through PRs.

## Step 3 — Device / UX QA
- Android physical QA for all five primary destinations;
- responsive/dark/font-scale checks;
- notification deep-link and launcher tests once notifications land.

## Step 4 — Consumer catalog expansion
- verify discovery candidates against their originators;
- deduplicate aliases and classify officiality;
- expand popular/consumer observances without contaminating the official catalog.

## Step 5 — Editorial content
- original English-first summaries, history, facts, actions and related observances;
- licensed/owned visual content only.

## Step 6 — Markets / Around the World
- broaden verified country/regional layers;
- keep locale separate from market.

## Step 7 — Retention/native layer
- notification reliability Golden;
- daily/weekly/category/favorite reminders;
- Android Home Screen Widget;
- share cards and physical QA.

## Step 8 — Monetization
- UMP + AdMob adaptive placements using test traffic until production;
- lifetime Remove Ads via store product and sandbox validation.

## Step 9 — Remote catalog updates
- production content hosting;
- signed/versioned manifest, checksum, staging, atomic activation and rollback.

## Step 10 — Production release
- permanent Android signing identity and first production signing run;
- exact-artifact QA, APK/AAB hashes, update-in-place;
- Play Console, Data Safety, privacy/store assets and release.
