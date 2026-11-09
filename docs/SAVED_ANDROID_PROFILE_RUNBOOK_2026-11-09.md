# World Days — Saved 296 favorites, Android physical profiling

**Gate:** P2, World Days issue #54. This runbook is executable only on a *clean, disposable physical Android test device* with Flutter SDK 3.47.3. This is not a runtime PASS report.

## Safety and provenance
- **Do not run on a phone that has the user's installed World Days app or real user data.** The integration driver deploys a test APK under the app's package name; its signing identity can conflict with an existing stable release. Never uninstall the stable app or clear data as a workaround.
- The fixture loads the existing bundled 296-record catalog and places favorites in memory through the fake repository/testing adapters. It makes no production user-data changes, purchases, AdMob calls, cloud writes, or Play transactions.
- Never store personal records in trace/log uploads; the fixture uses only institutional observance titles.
- Record source HEAD SHA, Flutter SDK, git tree status, connected Android model, OS version, refresh rate, power mode, device temperature and battery conditions before interpreting results.
- No production QA certification or store release follows from this test. Run the exact-signed production candidate separately for native notification and widget checks.

## Preparation and commands

From a clean World-Days clone on a workstation with Flutter and Android tooling:

```bash
git fetch origin main
git checkout main
git rev-parse HEAD
git status --porcelain
flutter --version
flutter devices
python3 tool/build_dataset.py
python3 tool/build_editorial.py
python3 tool/build_editorial_locales.py
./tool/bootstrap_platforms.sh
flutter pub get --enforce-lockfile
flutter gen-l10n

# Replace DEVICE_ID with the identifier of a CLEAN physical Android test phone.
flutter drive --profile --no-dds   --device-id DEVICE_ID   --driver test_driver/saved_device_profile_driver.dart   --target integration_test/saved_device_profile_test.dart
```

A profile-mode run produces `build/integration_response_data.json`. The driver and fixture are **not included in production UI**, and this workflow is intentionally not part of the ordinary `flutter test` gate.

Each of **0, 50, 150 and 296 favorites** has its own report key: `saved_scroll_N_favorites`. The test repeats 5 scrolling gestures after a warmup and captures engine `FrameTiming` via `IntegrationTestWidgetsFlutterBinding.watchPerformance`.

After the driver returns PASS, run:

```bash
python3 tool/summarize_saved_profile.py   build/integration_response_data.json   --output saved_device_profile_evidence.json   --source-sha "$(git rev-parse HEAD)"   --device "MODEL AND ANDROID VERSION"   --refresh-hz 60
```

Attach the resulting JSON, original integration response, Flutter driver output, exact source SHA and device details to [#54](https://github.com/riccardopinato/World-Days/issues/54). Avoid publishing personal or device identifiers. Generate no PASS entry until the actual tool executes.

## Interpretation / gate
- Compare identical source, catalog count and device conditions between runs. Check engine build/raster p90/p99 where emitted, percentage over the actual frame budget, and initial visible response. Repeat complete runs at least three times on the same device; ideally assess two different Android performance classes.
- Memory RSS and CPU require separate Android/DevTools/profiler readings; this integration-test harness does NOT measure them. Record `NOT_MEASURED` if absent.
- If 296 saved records cause sustained user-visible frame drops or unacceptable initial load relative to 50, compare a scoped `ListView.builder` branch against the same device and corpora, preserving selection, reminders, history and accessible semantics.
- No monotonic performance degradation found? Retain the simpler existing implementation; close the optimization candidate as `DEFERRED_NO_EVIDENCE` and keep #54 until signed artifact device acceptance if required.
- Emulator performance, GitHub-hosted widget pump and physical device profiling are separate evidence levels. Do not conflate them.

**Status at creation (2026-11-09):** DEVICE_NOT_VERIFIED. CI stress evidence for 296 records exists, but no connected physical Android device was accessible in this Chat.
