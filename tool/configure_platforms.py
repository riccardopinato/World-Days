#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ID = "com.riccardopinato.worlddays"


def replace_required(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    if count == 0:
        raise RuntimeError(f"Could not patch {label}")
    return updated


def configure_android() -> None:
    gradle = ROOT / "android" / "app" / "build.gradle.kts"
    manifest = ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
    if not gradle.exists() or not manifest.exists():
        raise RuntimeError("Android scaffold is missing")

    text = gradle.read_text(encoding="utf-8")
    text = replace_required(
        text,
        r'namespace\s*=\s*"[^"]+"',
        f'namespace = "{CANONICAL_ID}"',
        "Android namespace",
    )
    text = replace_required(
        text,
        r'applicationId\s*=\s*"[^"]+"',
        f'applicationId = "{CANONICAL_ID}"',
        "Android applicationId",
    )

    if "isCoreLibraryDesugaringEnabled = true" not in text:
        text = text.replace(
            "compileOptions {",
            "compileOptions {\n        isCoreLibraryDesugaringEnabled = true",
            1,
        )
    if "multiDexEnabled = true" not in text:
        text = text.replace(
            "defaultConfig {",
            "defaultConfig {\n        multiDexEnabled = true",
            1,
        )
    if 'coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")' not in text:
        text += (
            "\n\ndependencies {\n"
            '    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")\n'
            "}\n"
        )
    gradle.write_text(text, encoding="utf-8")

    src_root = ROOT / "android" / "app" / "src" / "main"
    old_kotlin = src_root / "kotlin" / "com" / "riccardopinato" / "world_days"
    if old_kotlin.exists():
        shutil.rmtree(old_kotlin)

    kotlin_dir = src_root / "kotlin" / "com" / "riccardopinato" / "worlddays"
    kotlin_dir.mkdir(parents=True, exist_ok=True)
    (kotlin_dir / "MainActivity.kt").write_text(
        """package com.riccardopinato.worlddays

import io.flutter.embedding.android.FlutterActivity

class MainActivity : FlutterActivity()
""",
        encoding="utf-8",
    )
    (kotlin_dir / "WorldDaysWidgetProvider.kt").write_text(
        """package com.riccardopinato.worlddays

import android.app.PendingIntent
import android.appwidget.AppWidgetManager
import android.content.Context
import android.content.Intent
import android.content.SharedPreferences
import android.widget.RemoteViews
import es.antonborri.home_widget.HomeWidgetProvider

class WorldDaysWidgetProvider : HomeWidgetProvider() {
    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray,
        widgetData: SharedPreferences,
    ) {
        appWidgetIds.forEach { widgetId ->
            val title = widgetData.getString("today_title", "World Days") ?: "World Days"
            val date = widgetData.getString("today_date", "") ?: ""
            val authority = widgetData.getString("today_authority", "") ?: ""

            val openIntent = Intent(context, MainActivity::class.java)
            val pendingIntent = PendingIntent.getActivity(
                context,
                widgetId,
                openIntent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
            )

            val views = RemoteViews(context.packageName, R.layout.world_days_widget).apply {
                setTextViewText(R.id.widget_date, date)
                setTextViewText(R.id.widget_title, title)
                setTextViewText(R.id.widget_authority, authority)
                setOnClickPendingIntent(R.id.widget_container, pendingIntent)
            }
            appWidgetManager.updateAppWidget(widgetId, views)
        }
    }
}
""",
        encoding="utf-8",
    )

    layout_dir = src_root / "res" / "layout"
    xml_dir = src_root / "res" / "xml"
    drawable_dir = src_root / "res" / "drawable"
    for directory in (layout_dir, xml_dir, drawable_dir):
        directory.mkdir(parents=True, exist_ok=True)

    (drawable_dir / "world_days_widget_bg.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android" android:shape="rectangle">
    <solid android:color="#F4F0FF" />
    <corners android:radius="24dp" />
    <padding android:left="18dp" android:top="16dp" android:right="18dp" android:bottom="16dp" />
</shape>
""",
        encoding="utf-8",
    )
    (layout_dir / "world_days_widget.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/widget_container"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="@drawable/world_days_widget_bg"
    android:gravity="center_vertical"
    android:orientation="vertical">

    <TextView
        android:id="@+id/widget_date"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textColor="#5E35B1"
        android:textSize="12sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/widget_title"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="4dp"
        android:ellipsize="end"
        android:maxLines="2"
        android:textColor="#1D1B20"
        android:textSize="18sp"
        android:textStyle="bold" />

    <TextView
        android:id="@+id/widget_authority"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="6dp"
        android:ellipsize="end"
        android:maxLines="1"
        android:textColor="#625B71"
        android:textSize="12sp" />
</LinearLayout>
""",
        encoding="utf-8",
    )
    (xml_dir / "world_days_widget_info.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:description="@string/app_name"
    android:initialLayout="@layout/world_days_widget"
    android:minHeight="110dp"
    android:minWidth="180dp"
    android:resizeMode="horizontal|vertical"
    android:updatePeriodMillis="86400000"
    android:widgetCategory="home_screen" />
""",
        encoding="utf-8",
    )

    m = manifest.read_text(encoding="utf-8")
    if 'android.permission.RECEIVE_BOOT_COMPLETED' not in m:
        m = m.replace(
            "<application",
            '    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>\n\n    <application',
            1,
        )

    native_block = """
        <receiver
            android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationReceiver"
            android:exported="false" />
        <receiver
            android:name="com.dexterous.flutterlocalnotifications.ScheduledNotificationBootReceiver"
            android:exported="false">
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
    if "ScheduledNotificationReceiver" not in m:
        m = m.replace("</application>", native_block + "    </application>", 1)
    manifest.write_text(m, encoding="utf-8")


def configure_ios() -> None:
    project = ROOT / "ios" / "Runner.xcodeproj" / "project.pbxproj"
    if not project.exists():
        raise RuntimeError("iOS scaffold is missing")
    text = project.read_text(encoding="utf-8")
    text = text.replace("com.riccardopinato.worldDays", CANONICAL_ID)
    text = text.replace("com.riccardopinato.world_days", CANONICAL_ID)
    project.write_text(text, encoding="utf-8")


def validate_identity() -> None:
    gradle = (ROOT / "android" / "app" / "build.gradle.kts").read_text(encoding="utf-8")
    assert f'namespace = "{CANONICAL_ID}"' in gradle
    assert f'applicationId = "{CANONICAL_ID}"' in gradle
    assert "isCoreLibraryDesugaringEnabled = true" in gradle
    assert "coreLibraryDesugaring" in gradle

    manifest = (ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml").read_text(
        encoding="utf-8"
    )
    assert "RECEIVE_BOOT_COMPLETED" in manifest
    assert "ScheduledNotificationReceiver" in manifest
    assert "WorldDaysWidgetProvider" in manifest

    activity = (
        ROOT
        / "android"
        / "app"
        / "src"
        / "main"
        / "kotlin"
        / "com"
        / "riccardopinato"
        / "worlddays"
        / "MainActivity.kt"
    )
    assert activity.exists()
    assert "package com.riccardopinato.worlddays" in activity.read_text(encoding="utf-8")

    ios = (ROOT / "ios" / "Runner.xcodeproj" / "project.pbxproj").read_text(encoding="utf-8")
    assert CANONICAL_ID in ios


def main() -> None:
    configure_android()
    configure_ios()
    validate_identity()
    print(f"platform identity/native config ok: {CANONICAL_ID}")


if __name__ == "__main__":
    main()
