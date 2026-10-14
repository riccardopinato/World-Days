# World Days — Step 9 Physical QA

Status: **NOT VERIFIED / OPEN** until the exact Step 9 APK is exercised on a physical Android device.

This checklist follows the App Factory Release Reality & Physical Validation draft. CI, Web Preview and emulator/AppLab evidence do not replace device evidence for notification delivery or Home Screen widgets.

## Artifact record

- Source SHA: fill after Step 9 merge.
- APK SHA-256: fill from the exact artifact physically tested.
- Variant: Android ARM64 release.
- Package: com.riccardopinato.world_days.
- Device / Android version: fill during test.

## Notification scenarios

1. Permission denied
   - Disable notification permission.
   - Enable a reminder in World Days.
   - Expected: app remains usable; no data loss; UI reports notifications disabled.

2. Permission granted
   - Grant notification permission.
   - Enable daily reminder.
   - Expected: health shows permission/channel ready and pending count becomes non-zero.

3. Immediate diagnostic
   - Settings → Test notifications.
   - Expected: immediate notification appears.

4. Scheduled diagnostic
   - Keep app backgrounded for the diagnostic delay.
   - Expected: scheduled test notification appears.

5. Notification tap / deep link
   - Tap a daily/favorite/category notification.
   - Expected: exact observance detail opens; generic/weekly payload opens Today/Calendar.

6. Channel blocked
   - Disable the World Days reminder channel in Android system settings.
   - Expected: World Days reports the reminder channel blocked and core app remains functional.

7. Reboot / app update
   - Keep at least one pending reminder, reboot or install update-in-place.
   - Expected: scheduled projection remains/reconciles when the app next starts.

## Home Screen Widget scenarios

1. Pin widget from Settings.
   - Expected: launcher pin dialog appears on supported launchers.

2. Today content.
   - Expected: widget shows current date, localized first observance title and count/subtitle.

3. Widget tap.
   - Expected: World Days opens the displayed observance; empty-day widget opens Today.

4. Date rollover.
   - Keep widget overnight without opening the app.
   - Expected: widget selects the next date from the bundled 45-day projection on system refresh.

5. Locale / market refresh.
   - Change language or market in World Days.
   - Expected: widget refreshes with the same selection rules and new localized/market-filtered content.

## Evidence classification

- PASS: scenario executed on exact APK and observed result matches expected.
- FAIL: observed app behavior is wrong.
- BLOCKED: device/launcher/system configuration prevents execution.
- NOT VERIFIED: not yet executed.

## Open AppLab note

The Step 8.2 AppLab Trusted Runtime path remains non-blocking/open: the APK installs, launches and completes the Maestro app flow, but the AppLab runtime workflow later hangs and is cancelled by GitHub. Treat this as AppLab infrastructure evidence, not a World Days product FAIL.
