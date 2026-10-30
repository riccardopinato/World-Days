# Flutter 3.47.3 lockfile drift — root cause and rejected dependency admission

Date: 2026-10-30. **Status: ROOT CAUSE REPRODUCED / NO DEPENDENCY UPGRADE APPROVED.**

## Root cause (independently reproduced)
- Existing World Days `pubspec.lock` contains 112 locked packages (878 lines).
- The platform bootstrap calls `flutter create --no-pub .` to regenerate Android/iOS/Web scaffold. **Despite `--no-pub`, this command overwrites the app lockfile with a 74-line Flutter template lockfile**.
- Exact proof: [strict-lock diagnostic workflow](https://github.com/riccardopinato/World-Days/actions/runs/41083986503) — `flutter pub get --enforce-lockfile` **passed before** platform scaffolding; `git diff --exit-code -- pubspec.lock` **failed immediately after** scaffolding, before any explicit post-scaffold dependency resolution.
- The original development workflow then ran `flutter pub get` on the template lock, which reconstructed the graph and opportunistically updated seven transitive packages. The resolver's **111 changed dependencies** was primarily the template-to-app reconstruction, **not** 111 new package upgrades.
- Original failure: https://github.com/riccardopinato/World-Days/actions/runs/41082944034.

## Corrective design
- `tool/bootstrap_platforms.sh` preserves the exact existing `pubspec.lock` bytes in a temporary file, invokes Flutter platform creation, restores the bytes if Flutter replaced the lock, then removes the temporary file.
- The original lockfile blob **`68b7cc13d6bf5fbe058857f740b386789198101c`** is retained. **Zero** direct or transitive dependency versions are changed by this PR.
- Independent CI validates `flutter pub get --enforce-lockfile` **before and after** platform creation, checks `git diff --exit-code -- pubspec.lock`, analyzes/tests/builds Web, and compiles a non-production Android ARM64 release-mode APK with SHA-256/byte-size evidence.
- `--enforce-lockfile` is the strict fail-closed gate; restoring the pre-existing lockfile is not permission to change its dependency graph.
- No production app behavior, data, entitlements, billing integration or package constraints are intentionally changed.

## Seven opportunistic transitive changes **REJECTED** (not in this PR)
The initial post-scaffold resolution would have upgraded:
- `in_app_purchase_android` 0.5.4 → 0.5.5 (**Play Billing 8 → 9**, different billingUnavailable semantics);
- `in_app_purchase_storekit` 0.4.14 → 0.4.15;
- `jni` 1.1.0 → 1.1.1;
- `posix` 6.5.2 → 6.5.4;
- `shared_preferences_android` 2.5.0 → 2.5.4;
- `web` 1.1.1 → 1.1.2;
- `webview_flutter_wkwebview` 3.27.0 → 3.27.2.

Those packages have separate provider changelogs and licensing, but **no dependency admission or Play Billing upgrade is requested here**. Existing `in_app_purchase_android 0.5.4` and candidate 0.5.5 both appear unlisted on pub.dev, so the unlisted flag alone was not a new candidate regression.

## Gates
- [ ] Exact-head strict-lock pre/post scaffold PASS, no lock diff.
- [ ] Exact-head Development checks PASS (validators, analyze, tests, Web).
- [ ] Exact-head Android compile/size evidence PASS; artifact is **not** production-signed or device-certified.
- [ ] Pilot #34 full CI GREEN on an integrated head **after** this PR merges; do not merge pilot based on isolated widget tests.
- [ ] Hardware/Play release acceptance remains a separate later gate.

Source of truth: `App-Factory-Core/CURRENT.yaml` v27 pinned at `f8ec5a324823d79353a056f0d4c12d2979a18b4e`; project roadmap and Product Bible still govern release.
