#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android" / "app" / "src" / "main"
ANDROID_APP = ROOT / "android" / "app"
IOS_APP_DELEGATE = ROOT / "ios" / "Runner" / "AppDelegate.swift"

PERMISSIONS = """    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
"""

WIDGET_LAUNCH_FILTER = """            <intent-filter>
                <action android:name="es.antonborri.home_widget.action.LAUNCH" />
            </intent-filter>
"""

RECEIVERS = """        <receiver
            android:exported="false"
            android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver" />
        <receiver
            android:exported="false"
            android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
                <action android:name="android.intent.action.QUICKBOOT_POWERON" />
                <action android:name="com.htc.intent.action.QUICKBOOT_POWERON" />
            </intent-filter>
        </receiver>
        <receiver
            android:name=".WorldDaysWidgetProvider"
            android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/world_days_widget_info" />
        </receiver>
"""

WIDGET_PROVIDER = r'''package com.riccardopinato.world_days

import android.appwidget.AppWidgetManager
import android.content.Context
import android.content.SharedPreferences
import android.net.Uri
import android.widget.RemoteViews
import es.antonborri.home_widget.HomeWidgetLaunchIntent
import es.antonborri.home_widget.HomeWidgetProvider
import org.json.JSONObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class WorldDaysWidgetProvider : HomeWidgetProvider() {
    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray,
        widgetData: SharedPreferences
    ) {
        val raw = widgetData.getString("world_days_schedule_json", "{}") ?: "{}"
        val schedule = runCatching { JSONObject(raw) }.getOrElse { JSONObject() }
        val todayKey = SimpleDateFormat("yyyy-MM-dd", Locale.US).format(Date())
        val item = schedule.optJSONObject(todayKey)

        val date = item?.optString("date")?.takeIf { it.isNotBlank() }
            ?: SimpleDateFormat("dd/MM", Locale.US).format(Date())
        val title = item?.optString("title")?.takeIf { it.isNotBlank() }
            ?: "World Days"
        val subtitle = item?.optString("subtitle")?.takeIf { it.isNotBlank() }
            ?: "Open World Days to explore"
        val observanceId = item?.optString("id").orEmpty()

        appWidgetIds.forEach { widgetId ->
            val views = RemoteViews(
                context.packageName,
                R.layout.world_days_widget
            ).apply {
                setTextViewText(R.id.world_days_widget_date, date)
                setTextViewText(R.id.world_days_widget_title, title)
                setTextViewText(R.id.world_days_widget_subtitle, subtitle)

                val uri = if (observanceId.isNotBlank()) {
                    Uri.parse(
                        "worlddays://observance/${Uri.encode(observanceId)}"
                    )
                } else {
                    Uri.parse("worlddays://today")
                }
                val launchIntent = HomeWidgetLaunchIntent.getActivity(
                    context,
                    MainActivity::class.java,
                    uri
                )
                setOnClickPendingIntent(
                    R.id.world_days_widget_root,
                    launchIntent
                )
            }
            appWidgetManager.updateAppWidget(widgetId, views)
        }
    }
}
'''

WIDGET_LAYOUT = r'''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/world_days_widget_root"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@drawable/world_days_widget_background"
    android:gravity="center_vertical"
    android:orientation="vertical"
    android:padding="18dp">

    <TextView
        android:id="@+id/world_days_widget_date"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="14/10"
        android:textColor="#E8ECFF"
        android:textSize="13sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/world_days_widget_title"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="7dp"
        android:ellipsize="end"
        android:maxLines="2"
        android:text="World Days"
        android:textColor="#FFFFFF"
        android:textSize="20sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/world_days_widget_subtitle"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="6dp"
        android:ellipsize="end"
        android:maxLines="1"
        android:text="Open World Days to explore"
        android:textColor="#E8ECFF"
        android:textSize="12sp" />

</LinearLayout>
'''

WIDGET_BACKGROUND = r'''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <gradient
        android:angle="0"
        android:endColor="#7A4EEA"
        android:startColor="#3157D8" />
    <corners android:radius="24dp" />
</shape>
'''

WIDGET_INFO = r'''<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:description="@string/world_days_widget_description"
    android:initialLayout="@layout/world_days_widget"
    android:minHeight="92dp"
    android:minWidth="190dp"
    android:previewLayout="@layout/world_days_widget"
    android:resizeMode="horizontal|vertical"
    android:updatePeriodMillis="3600000"
    android:widgetCategory="home_screen" />
'''

STRINGS = r'''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="world_days_widget_description">Today on World Days</string>
</resources>
'''

KEEP_RESOURCES = r'''<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools"
    tools:keep="@mipmap/ic_launcher" />
'''


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def patch_android_manifest() -> None:
    path = ANDROID / "AndroidManifest.xml"
    text = path.read_text(encoding="utf-8")

    if "android.permission.POST_NOTIFICATIONS" not in text:
        manifest_start = text.find("<manifest")
        if manifest_start < 0:
            raise RuntimeError("invalid_android_manifest")
        manifest_close = text.find(">", manifest_start)
        if manifest_close < 0:
            raise RuntimeError("invalid_android_manifest")
        text = (
            text[: manifest_close + 1]
            + "\n"
            + PERMISSIONS
            + text[manifest_close + 1 :]
        )

    if "es.antonborri.home_widget.action.LAUNCH" not in text:
        activity_start = text.find('android:name=".MainActivity"')
        if activity_start < 0:
            raise RuntimeError("main_activity_not_found")
        activity_close = text.find("</activity>", activity_start)
        if activity_close < 0:
            raise RuntimeError("main_activity_close_not_found")
        text = (
            text[:activity_close]
            + WIDGET_LAUNCH_FILTER
            + text[activity_close:]
        )

    if ".WorldDaysWidgetProvider" not in text:
        app_close = text.find("</application>")
        if app_close < 0:
            raise RuntimeError("application_close_not_found")
        text = text[:app_close] + RECEIVERS + text[app_close:]

    path.write_text(text, encoding="utf-8")


def patch_android_gradle() -> None:
    kts = ANDROID_APP / "build.gradle.kts"
    groovy = ANDROID_APP / "build.gradle"

    if kts.exists():
        text = kts.read_text(encoding="utf-8")
        text = text.replace("JavaVersion.VERSION_11", "JavaVersion.VERSION_17")
        text = text.replace("JavaVersion.VERSION_1_8", "JavaVersion.VERSION_17")
        if "isCoreLibraryDesugaringEnabled = true" not in text:
            marker = "    compileOptions {\n"
            if marker not in text:
                raise RuntimeError("android_compile_options_not_found")
            text = text.replace(
                marker,
                marker + "        isCoreLibraryDesugaringEnabled = true\n",
                1,
            )
        if "multiDexEnabled = true" not in text:
            marker = "    defaultConfig {\n"
            if marker not in text:
                raise RuntimeError("android_default_config_not_found")
            text = text.replace(
                marker,
                marker + "        multiDexEnabled = true\n",
                1,
            )
        if "coreLibraryDesugaring(" not in text:
            text = text.rstrip() + (
                "\n\ndependencies {\n"
                "    coreLibraryDesugaring("
                "\"com.android.tools:desugar_jdk_libs:2.1.4\""
                ")\n"
                "}\n"
            )
        kts.write_text(text, encoding="utf-8")
        return

    if groovy.exists():
        text = groovy.read_text(encoding="utf-8")
        text = text.replace("JavaVersion.VERSION_11", "JavaVersion.VERSION_17")
        text = text.replace("JavaVersion.VERSION_1_8", "JavaVersion.VERSION_17")
        if "coreLibraryDesugaringEnabled true" not in text:
            marker = "    compileOptions {\n"
            if marker not in text:
                raise RuntimeError("android_compile_options_not_found")
            text = text.replace(
                marker,
                marker + "        coreLibraryDesugaringEnabled true\n",
                1,
            )
        if "multiDexEnabled true" not in text:
            marker = "    defaultConfig {\n"
            if marker not in text:
                raise RuntimeError("android_default_config_not_found")
            text = text.replace(
                marker,
                marker + "        multiDexEnabled true\n",
                1,
            )
        if "coreLibraryDesugaring " not in text:
            text = text.rstrip() + (
                "\n\ndependencies {\n"
                "    coreLibraryDesugaring "
                "'com.android.tools:desugar_jdk_libs:2.1.4'\n"
                "}\n"
            )
        groovy.write_text(text, encoding="utf-8")
        return

    raise RuntimeError("android_app_gradle_not_found")


def patch_ios_app_delegate() -> None:
    if not IOS_APP_DELEGATE.exists():
        return
    text = IOS_APP_DELEGATE.read_text(encoding="utf-8")
    if "import UserNotifications" not in text:
        text = text.replace(
            "import UIKit\n",
            "import UIKit\nimport UserNotifications\n",
            1,
        )
    hook = (
        "    UNUserNotificationCenter.current().delegate = "
        "self as? UNUserNotificationCenterDelegate\n"
    )
    if "UNUserNotificationCenter.current().delegate" not in text:
        marker = "    GeneratedPluginRegistrant.register(with: self)\n"
        if marker not in text:
            raise RuntimeError("ios_plugin_registrant_marker_not_found")
        text = text.replace(marker, marker + hook, 1)
    IOS_APP_DELEGATE.write_text(text, encoding="utf-8")


def main() -> None:
    patch_android_manifest()
    write(
        ANDROID
        / "kotlin"
        / "com"
        / "riccardopinato"
        / "world_days"
        / "WorldDaysWidgetProvider.kt",
        WIDGET_PROVIDER,
    )
    write(ANDROID / "res" / "layout" / "world_days_widget.xml", WIDGET_LAYOUT)
    write(
        ANDROID / "res" / "drawable" / "world_days_widget_background.xml",
        WIDGET_BACKGROUND,
    )
    write(
        ANDROID / "res" / "xml" / "world_days_widget_info.xml",
        WIDGET_INFO,
    )
    write(ANDROID / "res" / "values" / "world_days_retention_strings.xml", STRINGS)
    write(ANDROID / "res" / "raw" / "world_days_keep.xml", KEEP_RESOURCES)
    patch_android_gradle()
    patch_ios_app_delegate()
    print("native retention config ok")


if __name__ == "__main__":
    main()
