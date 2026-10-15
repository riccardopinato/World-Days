# World Days — Release governance

Date: 2026-10-15
Factory baseline: 47c47f49a7b46812e3bd6f1231c3524f2b52b826

## 1. Release source identity

Production Android artifacts must be built only from the repository's `main` branch.

The `Production Android Release` workflow fails closed when `GITHUB_REF` is not `refs/heads/main`.

A green development workflow, a signed artifact, a physical-device PASS and a Play-distributed artifact are separate evidence levels. Never transfer a higher validation level to rebuilt bytes without new evidence.

## 2. Version identity

`pubspec.yaml` is the canonical source for both Android release identities:

```
version: MAJOR.MINOR.PATCH+BUILD
```

Rules:
- `MAJOR.MINOR.PATCH` is the user-visible versionName.
- `BUILD` is the Android versionCode and must be a positive integer.
- Every artifact intended for Google Play must use a versionCode greater than every versionCode previously uploaded to Play for this package.
- The production workflow reads both values from the checked-out `pubspec.yaml`; it must not substitute `GITHUB_RUN_NUMBER`.
- A version/build change is a source change and therefore receives normal PR/CI review.
- Do not reuse a versionCode for a different Play artifact.

Historical signed production baseline:
- versionName: 0.3.0
- versionCode: 3
- workflow run: 38702763793
- source SHA: 16a1b744d9f6d5e6d256a2b749aa680c26c31d58

Therefore the next Play/internal-test candidate must use versionCode **4 or higher**.

## 3. Version-name policy

Use semantic versioning for the public app version:
- PATCH: fixes, content/data corrections and low-risk polish without a material product-scope change.
- MINOR: new user-facing capabilities or material subsystem changes that remain backward-compatible.
- MAJOR: reserved for a deliberately incompatible product/data contract change.

Pre-1.0 releases may use MINOR increments for substantial milestones.

## 4. Changelog convention

`CHANGELOG.md` is the canonical human-readable change history.

Use:
- `## [Unreleased]` while work is not frozen;
- `## [X.Y.Z] - YYYY-MM-DD` when a release candidate is frozen.

Record user-facing or release-relevant changes, not every internal commit.

## 5. Tag convention

Final release tag:

```
vMAJOR.MINOR.PATCH
```

Create the tag only after the exact source SHA has completed Phase J certification. The tag must point to that certified source SHA.

If certification fails after a versionCode has already been uploaded to Play, increment BUILD before the next Play artifact. Do not move a published release tag to different source bytes.

## 6. Evidence convention

Final release evidence path:

```
evidence/releases/vMAJOR.MINOR.PATCH+BUILD.md
```

Minimum fields:
- versionName;
- versionCode;
- source SHA;
- package id;
- workflow run;
- APK/AAB names;
- APK/AAB SHA-256;
- signing fingerprint;
- distribution channel;
- device/runtime evidence references;
- Play billing evidence reference;
- privacy/store metadata snapshot;
- verdict: CERTIFIED / NOT CERTIFIED / BLOCKED.

## 7. Main protection — repository-admin gate

Desired repository rule:
- require pull request before merging to `main`;
- require the `Development checks` / `validate` check to pass;
- require branch to be up to date before merge where practical;
- block force pushes;
- block branch deletion.

Current connector cannot administer branch protection and receives HTTP 403 for that endpoint. This remains a repository-owner/admin action and must not be reported as completed until verified in GitHub settings.

## 8. Android-first v1 boundary

World Days v1 production scope is:
- Android;
- Flutter Web Preview.

iOS production signing, App Store Connect, iOS AdMob production configuration and iOS physical/store certification are post-v1.

## 9. Monetization / analytics boundary

V1 production monetization:
- one safe top anchored adaptive banner;
- UMP/privacy choices;
- one-time lifetime Remove Ads product.

Inline adaptive ads and interstitials are post-v1.

V1 has no separate first-party analytics SDK/event pipeline. Any future analytics addition reopens privacy/Data Safety review before release.
