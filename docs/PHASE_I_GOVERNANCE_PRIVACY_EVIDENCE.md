# Phase I — Governance / product truth / privacy evidence

Date: 2026-10-15
Repository: riccardopinato/World-Days
Branch: phase-i-governance-privacy
Factory baseline: 47c47f49a7b46812e3bd6f1231c3524f2b52b826
Master: v26.6
Golden Index: v18

## Product truth frozen for v1

Production scope:
- Android v1;
- Flutter Web Preview;
- iOS production/App Store release is post-v1.

Monetization:
- Google UMP / Privacy Choices;
- one safe top anchored adaptive banner;
- one-time lifetime Remove Ads;
- inline adaptive and interstitial formats are post-v1.

Measurement:
- no separate first-party analytics SDK/event pipeline in v1;
- KPI/event taxonomy remains a post-v1 plan, not a current collection claim.

Saved IA was already aligned in Phase A and is no longer an open product-truth mismatch.

## Release identity

Historical signed production baseline:
- versionName 0.3.0;
- versionCode 3;
- Production Android Release run 38702763793;
- source SHA 16a1b744d9f6d5e6d256a2b749aa680c26c31d58.

Current source identity:
- versionName 0.4.0;
- versionCode 4.

The production workflow now:
- fails closed unless dispatched from refs/heads/main;
- parses versionName/versionCode from committed pubspec.yaml;
- builds APK/AAB with those source-controlled values;
- records source SHA, workflow run, versionName, versionCode and signer evidence;
- no longer uses GITHUB_RUN_NUMBER as Android versionCode;
- runs the release-governance validator before building.

Development CI also validates the release-governance contract.

## Supply-chain alignment

Relevant GitHub Actions remain pinned by immutable SHA.

The Android artifact-upload lanes were aligned to App Factory Golden release baseline:
- actions/upload-artifact v7.0.2
- SHA cf430e030ddbb5b0abf93d22962f4752f3646cd9

Updated lanes:
- Development checks;
- Signed Android QA;
- Production Android Release.

## Release process

Defined in docs/RELEASE_GOVERNANCE.md:
- semantic version-name policy;
- monotonic Play versionCode policy;
- CHANGELOG.md convention;
- final release tag convention vMAJOR.MINOR.PATCH;
- exact release evidence path evidence/releases/vMAJOR.MINOR.PATCH+BUILD.md;
- minimum artifact / signer / distribution / device / billing / privacy evidence fields.

CHANGELOG.md now contains an Unreleased section.

## Privacy / Data Safety

The public Privacy Policy source now documents:
- Google Play Billing for optional lifetime Remove Ads;
- no payment-card storage by World Days;
- local entitlement state;
- minimal pending purchase-completion record used for safe provider finalization recovery;
- mobile HTTPS catalog-update requests to the official World Days GitHub Pages origin;
- no upload of favorites, recents, reminder settings or profile preferences with catalog requests;
- no separate first-party analytics backend/pipeline in v1.

Privacy Policy Last updated:
- 15 October 2026.

Engineering Data Safety inputs are frozen in docs/DATA_SAFETY_INPUTS.md for the Android-first v1 scope.

Post-merge evidence still required:
- GitHub Pages must redeploy the changed privacy source;
- the live canonical privacy URL must be checked for the 15 October 2026 text.

## External/admin gates that remain truthful

### GitHub main protection

Desired main protection is documented:
- PR required;
- Development checks/validate required;
- force push blocked;
- branch deletion blocked.

The connected GitHub integration cannot administer the branch-protection endpoint and receives HTTP 403. No repository ruleset was visible. This remains USER-ACTION / NOT VERIFIED and is not claimed complete.

### Google Play / Phase E

Repository-side billing implementation is complete, but Play catalog and sandbox evidence remain external:
- create/publish world_days_remove_ads_lifetime;
- active Buy purchase option;
- localized Play pricing;
- internal-test AAB;
- license/internal tester;
- purchase / pending / cancel / restart / restore / acknowledgement evidence.

These remain BLOCKED / NOT VERIFIED until performed in Play Console and on a Play-installed artifact.

## Validation status

Development checks #210 on functional head 6777a602308f63f6fa02760074cb7ac7331dd1f6:

- release-governance validator: PASS;
- dataset/localization/native validators: PASS;
- Flutter analyze: PASS;
- Flutter tests: **80/80 PASS**;
- Web release: PASS;
- Android ARM64 PR step: skipped by workflow design.

This evidence update is documentation-only. Final CI on the complete PR head remains required before squash merge.

Android ARM64 remains the post-merge main gate in Development checks.

## Verdict

Phase I repository implementation is complete and functionally validated.

Phase I must still retain explicit external evidence gates until:
1. final CI on the complete PR head is green;
2. the updated privacy page is live after merge;
3. main branch protection is configured/verified by a repository admin.


## Post-merge verification

Merged source:
- main SHA: `44720a125db88386180f31951f9cf167c555b8a4`.

Development checks #212:
- release/data/native validators: PASS;
- Flutter analyze: PASS;
- Flutter tests: 80/80 PASS;
- Web release: PASS;
- Android ARM64 build: PASS;
- Android ARM64 artifact upload: PASS;
- artifact digest: `sha256:618d9a167d6586bfe9f1cac8d1a5df3171d91280f5ee21b6c93c44ca1c1b2ffb`.

Deploy Web Preview #30:
- build: PASS;
- Pages artifact upload: PASS;
- deploy: PASS;
- hosted remote-content smoke: PASS;
- Pages artifact digest: `sha256:4906288acd2ca903970b4662571271ee7917c34a2ecc1de994962ffd2f1aa588`.

The deployed Pages artifact was inspected directly. Its `privacy.html` contains:
- `Last updated: 15 October 2026`;
- the Google Play Billing section;
- GitHub Pages catalog-update disclosure;
- the pending purchase-completion disclosure.

Phase I repository/deployment work is therefore complete. The only remaining Phase I item is the repository-admin branch-protection gate, still NOT VERIFIED because the connected integration lacks Admin permission.
