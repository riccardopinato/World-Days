# World Days — Active roadmap

Only open/future work is listed here.

## Runtime certification residual
- physical Android QA for Today / Calendar / Discover / Saved / Settings;
- physical notification permission, delivery after idle/reboot and notification-tap deep-link;
- Android Home Screen Widget add/update/click validation;
- Android/iOS share-sheet validation;
- iOS notification permission/delivery validation;
- final responsive/dark/font-scale visual pass on physical devices.

These checks do not block source development, but they remain mandatory before Store Ready certification.

## Step 8 — Monetization
- re-check current Google Mobile Ads / UMP / store-billing provider guidance;
- UMP consent gate before any ad request;
- mobile-only adaptive banner and inline placements with Web no-op;
- conservative interstitial controller only at natural completion points;
- test traffic during development;
- lifetime Remove Ads entitlement with Premium = no ad request;
- sandbox purchase/restore validation and app-ads.txt/store readiness.

## Step 9 — Remote catalog updates
- production content hosting;
- versioned manifest + checksum verification;
- download to staging, schema/provenance validation and atomic activation;
- rollback to last-known-good pack;
- bundled offline fallback always available;
- yearly themes and newly verified observances through the same pipeline.

## Step 10 — Production release
- permanent Android signing identity and first production signing run;
- exact-artifact APK/AAB QA and SHA-256 evidence;
- update-in-place validation;
- Play Console / App Store metadata, privacy policy and Data Safety;
- final physical-device certification and Store Ready evidence bundle.
