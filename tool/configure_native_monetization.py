#!/usr/bin/env python3
from __future__ import annotations

import os
import plistlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID_MANIFEST = ROOT / "android/app/src/main/AndroidManifest.xml"
IOS_INFO = ROOT / "ios/Runner/Info.plist"

ANDROID_TEST_APP_ID = "ca-app-pub-3940256099942544~3347511713"
IOS_TEST_APP_ID = "ca-app-pub-3940256099942544~1458002511"
APP_ID_RE = re.compile(r"^ca-app-pub-\d{16}~\d{10}$")


def production_mode() -> bool:
    return os.getenv("WORLD_DAYS_ADS_PRODUCTION_NATIVE", "").lower() in {
        "1",
        "true",
        "yes",
    }


def app_id(name: str, fallback: str) -> str:
    value = os.getenv(name, "").strip() or fallback
    if not APP_ID_RE.fullmatch(value):
        raise RuntimeError(f"invalid_{name.lower()}")
    if production_mode() and value.startswith("ca-app-pub-3940256099942544~"):
        raise RuntimeError(f"production_{name.lower()}_uses_google_test_id")
    return value


def patch_android(value: str) -> None:
    text = ANDROID_MANIFEST.read_text(encoding="utf-8")
    name = "com.google.android.gms.ads.APPLICATION_ID"
    if name in text:
        text = re.sub(
            r'(<meta-data\s+android:name="'
            + re.escape(name)
            + r'"\s+android:value=")[^"]+("/>)',
            rf"\g<1>{value}\2",
            text,
            count=1,
        )
    else:
        app_close = text.find("</application>")
        if app_close < 0:
            raise RuntimeError("android_application_close_not_found")
        meta = (
            '        <meta-data\n'
            f'            android:name="{name}"\n'
            f'            android:value="{value}" />\n'
        )
        text = text[:app_close] + meta + text[app_close:]
    ANDROID_MANIFEST.write_text(text, encoding="utf-8")


def patch_ios(value: str) -> None:
    with IOS_INFO.open("rb") as handle:
        payload = plistlib.load(handle)
    payload["GADApplicationIdentifier"] = value
    with IOS_INFO.open("wb") as handle:
        plistlib.dump(payload, handle, sort_keys=False)


def main() -> None:
    android_id = app_id("ADMOB_ANDROID_APP_ID", ANDROID_TEST_APP_ID)
    ios_id = app_id("ADMOB_IOS_APP_ID", IOS_TEST_APP_ID)
    patch_android(android_id)
    patch_ios(ios_id)
    lane = "production" if production_mode() else "test"
    print(f"native AdMob config ok ({lane} lane)")


if __name__ == "__main__":
    main()
