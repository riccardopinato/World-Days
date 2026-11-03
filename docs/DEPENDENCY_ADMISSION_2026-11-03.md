# World Days — Flutter 3.47.3 Android dependency-admission gate

Date: 2026-11-03. This replaces the stale independent #36 admission
proposal without reverting main's November 3 Golden v28 lockfile.

The previous root-cause diagnosis in #35 was valid: Flutter platform
creation may replace an application's committed `pubspec.lock` with
template contents even using `--no-pub`. PR #40 preserves the current
committed lock bytes across scaffolding; **it does not downgrade the
existing transitive dependencies**.

`.github/workflows/dependency-admission-android.yml` runs only on PRs
changing the manifest, lockfile, bootstrap script or the workflow itself.
It enforces the committed lock before/after native scaffolding, rejects
any diff, compiles an Android ARM64 release-mode APK, hashes and uploads
that non-production-signed artifact. This is **not** Play signing, store
billing or device certification.

Version 0.5.5 of `in_app_purchase_android` is already part of current
main's lockfile. Its Play Billing 9.1 behavior requires actual Play
internal-test acceptance (Phase E/J) independent of Android compile.
