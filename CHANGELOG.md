# Changelog

All notable user-facing and release-relevant changes to World Days are recorded here.

## [Unreleased]

### Added
- Complete six-locale Verified Overview coverage for all 296 launch observances.
- Saved retention hub for favorites, followed categories, reminder subscriptions and recents.
- Explicit neutral Around-the-World country browsing and empty states.
- Durable Google Play purchase-completion recovery for lifetime Remove Ads.
- Verified remote content-pack update/rollback flow.

### Changed

- Civil-day calculations now advance by local calendar dates across March/October DST, rather than adding fixed 24-hour durations; Today refreshes on local midnight and app resume.
- Anchored adaptive banner requests revalidate ad eligibility through asynchronous loading; revoking consent or activating Remove Ads invalidates stale requests.
- Remote content manifests are bounded (64 KiB), remote redirects are rejected and older numeric catalog versions cannot silently replace newer installed versions.
- The current Flutter lockfile is preserved during native platform bootstrapping, with strict pre/post-bootstrap Android admission.

- V1 scope is Android-first with Flutter Web Preview; iOS production release is post-v1.
- V1 advertising is limited to the safe top anchored adaptive banner.
- First-party analytics/event collection is deferred beyond v1.
- Production Android release artifacts derive versionName/versionCode from `pubspec.yaml` and can only be built from `main`.
- Signed QA now uses the same source-controlled Android version identity instead of GitHub workflow run numbers.
- Privacy Policy now documents Google Play Billing and mobile GitHub Pages catalog-update requests.

### Quality
- Integrated [PR #44](https://github.com/riccardopinato/World-Days/pull/44)
  into protected `main` with 104 Flutter plus 9 Europe/Rome DST
  regression tests on the integrated candidate.
- Added real ObservanceCard responsive/large-text visual tests and
  focus-traversal assertions for standard phone and desktop navigation.
- Added production fail-closed GitHub ruleset preflight and independent
  APK/AAB checksum/manifest verifier; physical/store QA remains separate.
- Expanded automated coverage to 80 Flutter tests before Phase I.
- Added full-catalog recurrence, content, retention, billing, remote-content and responsive/accessibility regressions.
- Added machine-readable exact-artifact manifests for signed QA/production APK+AAB outputs.
- Added deterministic release-evidence tests plus explicit compact-navigation focus-order and >=48dp touch-target assertions.
- CI platform bootstrap no longer performs implicit dependency resolution; release/deploy lanes resolve once and fail if `pubspec.lock` changes.
- Refreshed only the two transitive lock entries required by the current resolver: `in_app_purchase_storekit 0.4.14` and `shared_preferences_android 2.5.0`.
