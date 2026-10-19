# World Days — Phase F exact-candidate physical QA

Status: **NOT VERIFIED / OPEN** until the exact release-candidate APK is exercised on a physical Android device.

This checklist follows the App Factory Release Reality & Physical Validation boundary. CI, Flutter widget tests, Web Preview and emulator/AppLab evidence do not replace device evidence for notification delivery, Android channels, reboot/update behavior or Home Screen widgets.

## Exact-artifact rule

Physical evidence is valid only for the APK whose hash is recorded below.

Do not rebuild after testing and transfer the PASS to new bytes. If source, signing, build inputs or artifact bytes change, generate a new artifact manifest and rerun the affected physical checks.

The preferred final candidate is the ARM64 APK emitted in the **same Production Android Release run** as the AAB uploaded to Play internal testing. This binds the direct-device APK and Play AAB to one source SHA, one version identity and one workflow run.

## Artifact record

Fill from the generated `production-artifact-manifest.json`:

- Version name:
- Version code:
- Source SHA:
- Workflow run ID:
- Package: `com.riccardopinato.world_days`
- APK filename:
- APK SHA-256:
- AAB filename:
- AAB SHA-256:
- Direct APK signer SHA-256:
- Device model:
- Android version:
- Launcher:
- Test date:

Before starting, independently hash the downloaded APK and confirm it matches the manifest.

## Notification scenarios

1. **Permission denied**
   - Disable notification permission.
   - Enable a reminder in World Days.
   - Expected: app remains usable; no data loss; UI reports notifications disabled.

2. **Permission granted**
   - Grant notification permission.
   - Enable daily reminder.
   - Expected: health reports permission/channel ready and pending count becomes non-zero.

3. **Immediate diagnostic**
   - Settings → Test notifications.
   - Expected: immediate notification appears.

4. **Scheduled diagnostic**
   - Keep app backgrounded for the diagnostic delay.
   - Expected: scheduled test notification appears without keeping the app foregrounded.

5. **Daily / favorite / category delivery**
   - Enable each supported reminder class and allow at least one real scheduled delivery.
   - Expected: correct localized payload and no duplicate delivery.

6. **Notification tap / deep link**
   - Tap daily/favorite/category notifications.
   - Expected: exact observance detail opens where an observance ID exists; generic/weekly payload opens the intended Today/Calendar target.

7. **Channel blocked**
   - Disable the World Days reminder channel in Android system settings.
   - Expected: World Days reports the blocked channel and core app remains functional.

8. **Reboot reconciliation**
   - Keep at least one pending reminder and reboot the device.
   - Expected: reminder projection is restored/reconciled when the app next starts and no duplicate schedules are created.

9. **N → N+1 update reconciliation**
   - Install a permanent-signature N build with reminders configured.
   - Install the candidate N+1 build in place without clearing app data.
   - Expected: preferences survive, schedules reconcile and no duplicate reminders are created.

## Home Screen Widget scenarios

1. **Pin widget**
   - Pin from Settings or launcher.
   - Expected: launcher pin/add flow succeeds on a supported launcher.

2. **Today content**
   - Expected: widget shows current date, localized first observance title and count/subtitle.

3. **Widget tap / deep link**
   - Expected: displayed observance opens; an empty-day widget opens Today.

4. **Date rollover**
   - Keep the widget overnight without opening World Days.
   - Expected: widget advances to the next date from the offline projection on system refresh.

5. **Locale / market refresh**
   - Change language and market in World Days.
   - Expected: widget refreshes using the new localized/market-filtered projection.

6. **Process-death smoke**
   - Remove World Days from recents, leave the widget on the launcher and invoke a widget refresh/tap.
   - Expected: no broken/blank widget state and target routing still works.

## Candidate smoke around retention

On the same APK also verify:

- cold launch and repeated warm launch;
- Today → detail → favorite → Saved;
- Calendar navigation;
- Settings opens without overflow at large text;
- notification permission/settings links;
- widget action from Settings;
- no unexpected ad overlap with system/retention controls.

These are not a substitute for the broader Phase J regression; they detect physical-only breakage before certification.

## Evidence classification

- **PASS**: scenario executed on the exact recorded APK and observed result matches expected.
- **FAIL**: observed app behavior is wrong.
- **BLOCKED**: device/launcher/system configuration prevents execution.
- **NOT VERIFIED**: not yet executed.

For each scenario record: result, timestamp, short observation and screenshot/video filename when useful.

## AppLab boundary

AppLab/emulator evidence remains non-blocking for these physical scenarios. A hosted runtime PASS cannot certify Android notification delivery, channel state, reboot/update reconciliation or launcher-widget behavior.

## Phase F exit rule

Phase F closes only when all blocking notification/widget scenarios above are PASS on the exact candidate, or a documented non-product platform limitation is explicitly classified BLOCKED and accepted before Phase J.
