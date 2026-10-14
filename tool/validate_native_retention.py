#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = (ROOT / "android/app/src/main/AndroidManifest.xml").read_text(
    encoding="utf-8"
)
required_manifest = [
    "android.permission.POST_NOTIFICATIONS",
    "android.permission.RECEIVE_BOOT_COMPLETED",
    "ScheduledNotificationReceiver",
    "ScheduledNotificationBootReceiver",
    "WorldDaysWidgetProvider",
    "world_days_widget_info",
    "es.antonborri.home_widget.action.LAUNCH",
]
for token in required_manifest:
    assert token in manifest, token

required_files = [
    "android/app/src/main/kotlin/com/riccardopinato/world_days/WorldDaysWidgetProvider.kt",
    "android/app/src/main/res/layout/world_days_widget.xml",
    "android/app/src/main/res/drawable/world_days_widget_background.xml",
    "android/app/src/main/res/xml/world_days_widget_info.xml",
    "android/app/src/main/res/values/world_days_retention_strings.xml",
]
for relative in required_files:
    assert (ROOT / relative).is_file(), relative

provider = (ROOT / required_files[0]).read_text(encoding="utf-8")
for token in [
    "HomeWidgetProvider",
    "HomeWidgetLaunchIntent",
    "world_days_schedule_json",
    "worlddays://observance/",
]:
    assert token in provider, token

app_delegate = (ROOT / "ios/Runner/AppDelegate.swift").read_text(
    encoding="utf-8"
)
assert "import UserNotifications" in app_delegate
assert "UNUserNotificationCenter.current().delegate" in app_delegate

print("native retention validation ok")
