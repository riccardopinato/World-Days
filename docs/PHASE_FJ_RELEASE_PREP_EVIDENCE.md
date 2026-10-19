# Phase F/J — Exact-artifact release preparation evidence

Date: 2026-10-19  
Repository: riccardopinato/World-Days  
Branch: phase-fj-exact-artifact-prep  
Base source: 44720a125db88386180f31951f9cf167c555b8a4  
Base app version: 0.4.0+4

## Purpose

This change set does not certify World Days for release.

It closes repository-side preparation gaps so the final physical and Play validation can be tied to exact bytes rather than inferred from source or a rebuilt artifact.

## Exact-artifact manifest

New tool:

`tool/write_android_artifact_manifest.py`

For both Signed Android QA and Production Android Release it records:

- schema version;
- lane;
- package id;
- versionName;
- versionCode;
- source SHA;
- workflow run ID;
- signing certificate SHA-256;
- APK filename, SHA-256 and byte size;
- AAB filename, SHA-256 and byte size.

The manifest is deterministic and excludes timestamps so identity is based on artifact and build provenance rather than wall-clock data.

Automated coverage:

`tool/test_release_evidence.py`

It verifies:

- source/version/signer fields are preserved;
- APK/AAB hashes are computed from bytes;
- invalid source identity fails closed.

Development checks execute this test.

## Signed QA identity hardening

Before this phase, Signed Android QA substituted `GITHUB_RUN_NUMBER` as Android versionCode.

It now:

- reads versionName/versionCode from committed `pubspec.yaml`;
- passes both explicitly to Flutter APK/AAB builds;
- records both in signing evidence;
- emits `signed-qa-artifact-manifest.json`.

This makes QA artifact identity comparable with the production lane and avoids a workflow-run-number identity that cannot represent the committed source version.

## Production evidence hardening

Production Android Release already used source-controlled version identity.

It now additionally emits:

`production-artifact-manifest.json`

The manifest is uploaded beside the APK, AAB, signer evidence and checksum text file.

The final Phase F/J candidate should use the APK and AAB from the same Production Android Release run.

## Governance regression guard

`tool/validate_release_governance.py` now also requires:

- Signed QA to use `WORLD_DAYS_VERSION_NAME` / `WORLD_DAYS_VERSION_CODE`;
- no Signed QA `--build-number "$GITHUB_RUN_NUMBER"`;
- both signed lanes to invoke the exact-artifact manifest writer;
- both signed lanes to upload their expected manifest.

## Dependency-lock determinism

The first PR CI exposed a time-dependent lock drift during platform scaffold generation: `flutter create` performed an implicit package resolution and refreshed transitive packages before the explicit lock check.

The release preparation now prevents that class of drift:

- `tool/bootstrap_platforms.sh` invokes `flutter create --no-pub`;
- Development checks, Pages deploy, Signed Android QA and Production Android Release use `flutter pub get --enforce-lockfile`;
- the committed `pubspec.lock` remains the dependency source of truth instead of being opportunistically refreshed during CI.

This is a CI reproducibility fix, not a dependency upgrade.

## Accessibility pre-certification

The compact large-text mobile navigation now has:

- explicit ordered focus traversal;
- numeric focus order matching Today → Calendar → Discover → Saved → Settings;
- automated minimum 48dp touch-target assertions for all five controls.

This reduces, but does not replace, Phase J physical screen-reader/focus/contrast QA.

## Physical QA contract

`docs/STEP_9_PHYSICAL_QA.md` was upgraded into the Phase F exact-candidate checklist.

It now requires:

- pre-test APK hash verification against the production manifest;
- exact artifact identity fields;
- no evidence transfer after rebuild;
- notification permission/channel diagnostics;
- daily/favorite/category delivery;
- notification deep links;
- reboot and N→N+1 reconciliation;
- widget pin/content/date rollover/locale-market/tap/process-death scenarios;
- same-candidate smoke around retention controls.

## External gates still open

This preparation does not close:

- Play one-time product creation/activation;
- Play internal-test upload;
- license/internal tester setup;
- Remove Ads sandbox purchase/restore/finalization evidence;
- physical-device Phase F execution;
- GitHub main branch protection;
- direct live privacy-URL verification;
- Phase J exact-candidate certification;
- Play store readiness.

## Verdict

Repository-side F/J preparation: **READY FOR CI**.

Release certification: **NOT CERTIFIED / BLOCKED on external Play + physical gates**.
