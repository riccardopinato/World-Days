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
- V1 scope is Android-first with Flutter Web Preview; iOS production release is post-v1.
- V1 advertising is limited to the safe top anchored adaptive banner.
- First-party analytics/event collection is deferred beyond v1.
- Production Android release artifacts now derive versionName/versionCode from `pubspec.yaml` and can only be built from `main`.
- Privacy Policy now documents Google Play Billing and mobile GitHub Pages catalog-update requests.

### Quality
- Expanded automated coverage to 80 Flutter tests before Phase I.
- Added full-catalog recurrence, content, retention, billing, remote-content and responsive/accessibility regressions.
