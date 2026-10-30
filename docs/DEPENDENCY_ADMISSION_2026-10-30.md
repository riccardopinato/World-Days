# Flutter 3.47.3 dependency lock admission — 2026-10-30

**Status: PROPOSED / NOT ADMITTED FOR RELEASE.** This change belongs to a dedicated dependency PR, independent of the test-only Design-App Visual QA pilot (#34). No direct `pubspec.yaml` constraints, application source, data schema or feature flags are changed.

## Reproducible provenance
- Base: `main@622e5c2f00c08b0905207c6765c9b51e199e706f`.
- CI reproducer: https://github.com/riccardopinato/World-Days/actions/runs/41082944034 (Development checks, `flutter pub get`, Flutter 3.47.3).
- The original CI diagnostic says "Changed 111 dependencies", but the **actual committed lockfile diff changes exactly seven transitive packages** (versions and pub.dev SHA-256 hashes); no package is added/removed. The 111 number is resolver output, not 111 lockfile version changes.
- Candidate lockfile blob: `67b95e7eea87920c0dbb8bbd7f64520bd9ebbbb8`, copied verbatim from the seven CI diff hunks.

## Exact transitive changes and admission review

| Package | Previous -> candidate | License | Change surface |
| --- | --- | --- | --- |
| `in_app_purchase_android` | 0.5.4 -> **0.5.5** | BSD-3-Clause | **HIGH: Play Billing 8.0.0 -> 9.1.0; minimum Android SDK 23; billingUnavailable behavior. Candidate is marked UNLISTED on pub.dev (2026-10-30). Do not release or merge solely on static CI.** |
| `in_app_purchase_storekit` | 0.4.14 -> 0.4.15 | BSD-3-Clause | iOS StoreKit 2 exposes SK2Transaction; confirm restore/completion behavior. |
| `jni` | 1.1.0 -> 1.1.1 | BSD-3-Clause | ProGuard consumer rules for suspend-function Kotlin classes. |
| `posix` | 6.5.2 -> 6.5.4 | MIT | Native string/buffer hardening (6.5.3) and documentation/lints (6.5.4). |
| `shared_preferences_android` | 2.5.0 -> 2.5.4 | BSD-3-Clause | JNI/R8, DataStore and deferred disk I/O changes; verify persisted favorites, locale/market, reminders and entitlement after app update. |
| `web` | 1.1.1 -> 1.1.2 | BSD-3-Clause | Dart 3.13 dart-fix migrations; no direct app API change. |
| `webview_flutter_wkwebview` | 3.27.0 -> 3.27.2 | BSD-3-Clause | iOS/macOS minimum version restored to iOS 13/macOS 10.15; warning fixes. |

Provider changelogs:
- https://pub.dev/packages/in_app_purchase_android/changelog
- https://pub.dev/packages/in_app_purchase_storekit/changelog
- https://pub.dev/packages/shared_preferences_android/changelog
- https://pub.dev/packages/jni/changelog
- https://pub.dev/packages/posix/changelog
- https://pub.dev/packages/web/changelog
- https://pub.dev/packages/webview_flutter_wkwebview/changelog

## Admission gates (do not bypass)
- [ ] Exact-head Development checks **GREEN**, including unchanged lockfile check, analyze, all tests and Web build.
- [ ] Independent dependency vulnerability/advisory audit (not yet executed; license/changelog review is not an OSV clearance).
- [ ] Confirm whether unlisted `in_app_purchase_android 0.5.5` is an intentional supported release; prefer a listed compatible version if viable. **Fail closed** on uncertain Play Billing upgrade.
- [ ] Test purchase pending/cancel/error, completion/restart, restore and Remove Ads on Play internal testing with exact signed candidate. Verify new `billingUnavailable` handling.
- [ ] Test persisted preferences after upgrade on real Android, and iOS StoreKit/restore on real supported device if shipping iOS.
- [ ] Record exact-source APK/AAB SHA-256, signing identity, size delta and provenance; do not infer device or store PASS from CI.

This PR is a candidate for dependency admission, not approval for production. World-Days #35 stays open until the dependency and release gates are verified.
