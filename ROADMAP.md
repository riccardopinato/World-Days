# World Days — Active roadmap

Execution numbering reflects the current implementation sequence. Product scope remains governed by `docs/PRODUCT_BIBLE.txt`.

## Completed through Step 8.2

Steps 1–7 established the real Flutter/CI baseline, verified catalog expansion, reviewed multilingual editorial content, market/Around-the-World layers and the current consumer shell.

### Step 8 — Visual Content Upgrade
- deterministic `visualKey` for every generated catalog record;
- reusable first-party procedural illustration system;
- editorial Today/detail hero treatment and richer observance cards;
- themed Discover collections;
- locally generated 4:5 PNG share cards;
- visual/media licensing contract with offline fallback;
- localization parity and visual/widget regression coverage.

### Step 8.1 — Share Card Refinement
- removed the officiality pill from exported 4:5 share artwork;
- preserved the established visual baseline and local PNG sharing pipeline.

### Step 8.2 — Complete Observance Title Localization
- all 296 current observance titles available offline in EN/IT/ES/FR/DE/PT;
- canonical IDs and English source titles remain stable across locale changes;
- English fallback for unsupported/missing locales;
- multilingual search covers canonical English, localized titles and aliases;
- dataset generation fails closed on missing, extra or empty title translations.

## Step 9 — Retention / native layer
- notification reliability Golden review against current providers;
- daily/weekly/category/favorite reminders;
- Android Home Screen Widget;
- physical notification/deep-link/widget QA.

## Step 10 — Monetization
- UMP + AdMob adaptive placements using test traffic until production;
- lifetime Remove Ads entitlement;
- sandbox billing/consent validation and no-ad-request premium behavior.

## Step 11 — Remote catalog updates
- production content hosting;
- signed/versioned manifest, checksum, staging, atomic activation and rollback;
- annual campaign/theme overrides.

## Step 12 — Production release
- permanent Android signing identity and first production signing run;
- exact-artifact QA, APK/AAB hashes and update-in-place;
- Play Console, Data Safety, privacy/store assets and release.
