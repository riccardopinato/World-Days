# World Days — Active roadmap

Execution numbering reflects the current implementation sequence. Product scope remains governed by `docs/PRODUCT_BIBLE.txt`.

## Completed through Step 9 implementation

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
Implementation:
- notification reliability Golden applied with timezone-aware inexact scheduling, stable IDs, health/diagnostics and deterministic reconciliation;
- daily/weekly/category/favorite reminder plans with bounded pending-notification horizon;
- notification tap and Home Widget deep-link routing;
- lightweight Android XML/RemoteViews Home Screen Widget with a 45-day offline projection;
- generated Android/iOS native setup plus CI validation.

Open evidence gate:
- physical notification/deep-link/widget QA on the exact release APK remains NOT VERIFIED;
- legacy AppLab Trusted Runtime hang remains tracked as infrastructure/non-blocking because the APK installs, launches and completes the Maestro flow before the workflow later stalls.

## Step 10 — Monetization
### Step 10.1 — Branding, signing continuity and top banner ✅ implementation
- approved World Days launcher icon pipeline for Android/iOS;
- UMP-gated large anchored adaptive banner in a dedicated top slot;
- Web Preview no-op and Google sample test traffic for QA/manual builds;
- permanent Android signing identity + signer verification workflow;
- fail-closed Android production lane for real AdMob App ID/Banner ID;
- one legacy-signing transition reinstall remains unavoidable before update-in-place continuity begins.

### Step 10.2 — Remove Ads entitlement
- lifetime Remove Ads entitlement;
- sandbox billing validation;
- Premium/Remove Ads must suppress the ad request itself, not only hide the banner.

## Step 11 — Remote catalog updates
- production content hosting;
- signed/versioned manifest, checksum, staging, atomic activation and rollback;
- annual campaign/theme overrides.

## Step 12 — Production release
- permanent Android signing identity and first production signing run;
- exact-artifact QA, APK/AAB hashes and update-in-place;
- Play Console, Data Safety, privacy/store assets and release.
