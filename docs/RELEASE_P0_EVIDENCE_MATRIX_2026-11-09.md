# World Days — P0 release gate, exact-source readiness matrix

**Date:** 2026-11-09. **Target:** Android first, store v1; package \`com.riccardopinato.world_days\`.
**Scope:** Readiness/preflight only. No publication or simulated provider PASS.
**Factory:** \`App-Factory-Core@2b3ae9e01764b7504980efca34f2543949dc7b89\`, Master v27/Index v29.
**Initial observed source:** \`World-Days@6dd691649b3abeb8168b2ced08afc072a2a22832\`. This file is NOT a certification for subsequent commits.

## Gate matrix (distinct types of evidence)

| Gate | Evidence already verified | Outstanding proof | Status |
|---|---|---|---|
| Repository/source | Protected-main PR, \`flutter analyze\`, 159 Flutter tests + 9 Rome DST on PR #53; main run #42544032701 SUCCESS; Web Preview #42544032678 SUCCESS | Rerun exact HEAD after every source/content change | PASS only for pinned old source |
| Android ARM64 internal compile | Main run #42544032701 Android ARM64 compiled | Internal artifact is not production signed by pinned keystore; no device test | SOURCE BUILD PASS ONLY |
| Production-signed APK + AAB | \`.github/workflows/android-production-release.yml\` has main-only, signer check and shared SHA-256 artifact manifest | Launch on final main via *explicit manual workflow_dispatch*, inspect run success, signer, APK/AAB SHA, versionName and versionCode; same artifact for physical QA | NOT VERIFIED on final candidate |
| Signed QA path | \`.github/workflows/android-signed-qa.yml\` exists (manual only, no production AdMob IDs) | Run if needed, collect immutable provenance | NOT EXECUTED |
| Google Play one-time Remove Ads | Billing adapter code and fail-closed tests exist | Owner action to configure \`world_days_remove_ads_lifetime\`; Play internal tester, Play-installed AAB, purchase/pending/cancel/restore/ack/ads suppression evidence | BLOCKED — PLAY CONSOLE |
| Physical notifications & Home Widget | Source tests and mocks, Phase F checklist exist | Exact-signed APK on a real Android device: permission, schedules, reboot/update, widget pin/taps/date/locale, screenshot/log evidence | BLOCKED — DEVICE |
| AdMob / GDPR / Store | UMP source, privacy page, separate test/production IDs | Verify **root** \`app-ads.txt\` via HTTP and AdMob crawler; Play Data Safety, content rating, support, screenshots, app signing | NOT VERIFIED — PROVIDERS |
| Saved 296 favorites performance | 296 favorite widget stress test passed in CI (604 delegate children / 6 visible card); reproducible physical profile harness included in this PR | Connect clean Android test phone and capture FrameTiming 0/50/150/296, plus memory/CPU separate | DEVICE_NOT_VERIFIED |

## Safe operator sequence: sign once, verify exact bytes, then Play

1. Obtain the maximum versionCode already accepted by Play Console. Do **not** assume \`0.4.0+4\` can be uploaded again. If a bump is needed, use a separate reviewed source PR before locking the candidate.
2. Close all approved source/content changes and freeze one SHA; run full development checks and lint/test on that exact commit.
3. In GitHub Actions, manually open **Production Android Release** on \`main\` — do not enable automatic production publishing. Ensure required secrets are present through their configured protections, never copy keystores/secrets into chat.
4. Check the **single** run's \`production-artifact-manifest.json\`, \`artifact-sha256.txt\`, \`signing-evidence.txt\` and \`phase-fj-physical-qa-handoff.md\`: verify source SHA, package, code, APK+AAB hash and pinned signer fingerprint. Failed/missing run = BLOCKED.
5. Download the exact APK to a separate clean testing phone; verify hash locally before install. Do not uninstall an existing app with user data to bypass a signature mismatch.
6. Execute \`docs/STEP_9_PHYSICAL_QA.md\` and \`docs/SAVED_ANDROID_PROFILE_RUNBOOK_2026-11-09.md\`, with per-scenario PASS/FAIL/BLOCKED and device details, no inferred physical PASS.
7. Configure the Play non-consumable product on the correct package, upload **same-run AAB** to internal testing and perform a **Play-installed** purchase/restore test with authorized testers. Validate product id \`world_days_remove_ads_lifetime\` in code and Console.
8. Verify \`app-ads.txt\` at the **developer site root**, not just \`/World-Days/app-ads.txt\`; confirm domain ownership/crawler state. Confirm the privacy URL, Play Data Safety, age/content rating, app signing, languages and screenshots.
9. Only after all proofs are attached to issue #43, issue a release certification bound to source+APK+AAB SHA; keep the Store release manual.

## Non-goals / safeguards

- No new subscription, no change to ads consent or billing engine, no new cloud service, no API secrets, no Store publish from this PR.
- A signed QA AAB may be installable only through Play, but it is not evidence of a successful Play-installed purchase.
- Source/build green does not certify actual local notification delivery, Home Screen Widget behavior, Store or device frame timings.
- \`app-ads.txt\` root could not be verified conclusively through public read tooling at the time of this assessment: status NOT_VERIFIED, not a proven 404.
- Production release stays blocked until issue #43 is closed with external evidence.

**Linked blockers:** [#43 — release readiness](https://github.com/riccardopinato/World-Days/issues/43), [#54 — Saved physical profile](https://github.com/riccardopinato/World-Days/issues/54).
