# World Days — Google Play release preparation (operator runbook)

Date: 2026-11-03. Status: **NOT STORE READY / EXTERNAL GATES OPEN**.
Package: `com.riccardopinato.world_days`. Android production first.
Public app name: **World Days**.

## Google Play internal test and lifetime billing

1. Confirm World Days application/package in Play Console. A different
   existing Play app does not configure this package.
2. Create **one-time purchase** `world_days_remove_ads_lifetime` with
   a permanent non-consumable Buy option. Target reference price EUR 2.99;
   use Google's localized final price. Activate product and purchase option.
3. Add the test Google account to both license testing and internal test.
4. Freeze a source SHA and increment `pubspec.yaml` versionCode beyond
   **every** uploaded build (current source 0.4.0+4 is not proof of Play quota).
5. Produce signed APK/AAB from a single Production Android Release run.
   Preserve `production-artifact-manifest.json`, SHA-256 and signer fingerprint.
6. Install the AAB via Play internal-test link (not an arbitrary sideload
   for Billing). Confirm localized price, purchase, pending, cancel, restart,
   reinstall/restore, finalization and no more AdMob requests for entitled
   users. Record account/test date and transaction behavior, but **never**
   store full transaction secrets or payment details in public issues.
7. Run Phase F physical QA against the same run's direct APK, record
   device, OS, launcher, SHA-256 and observation evidence.
8. Verify Play App Signing fingerprints and identity difference from
   direct APK/upload key where applicable.
9. Complete Play Data Safety and privacy policy on the exact dependency
   lock. Ads/UMP and Billing SDK provider processing must be disclosed
   truthfully. No first-party analytics backend in v1.
10. Set the developer website hostname and host the real AdMob-generated
    `app-ads.txt` at **https://HOST/app-ads.txt**, not solely under
    `/World-Days/app-ads.txt`. Confirm the actual crawler status.
11. Complete target audience, content rating, ads declaration, EN base
    listing, localized descriptions, real screenshot set, feature graphic,
    support details, staged rollout and release notes.

## Verification distinction

A green GitHub CI is software build/test evidence. An artifact manifest
is hash/provenance evidence. Neither proves Play Billing, Android notification
delivery, widget overnight refresh, Play signing or store declarations.

Do not publish a final release or create a `vMAJOR.MINOR.PATCH` tag
without a `CERTIFIED` verdict in the exact release Evidence Bundle.

Current action owner: Play Console/AdMob account owner and Android
physical-device tester. These steps are not remotely actionable through
the connected GitHub-only tools.
