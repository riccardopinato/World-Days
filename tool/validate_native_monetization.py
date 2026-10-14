#!/usr/bin/env python3
from __future__ import annotations

import plistlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = (ROOT / "android/app/src/main/AndroidManifest.xml").read_text(
    encoding="utf-8"
)
match = re.search(
    r'android:name="com\.google\.android\.gms\.ads\.APPLICATION_ID"'
    r'\s+android:value="([^"]+)"',
    manifest,
)
assert match, "Android AdMob app ID missing"
assert re.fullmatch(r"ca-app-pub-\d{16}~\d{10}", match.group(1)), match.group(1)

with (ROOT / "ios/Runner/Info.plist").open("rb") as handle:
    info = plistlib.load(handle)
ios_id = str(info.get("GADApplicationIdentifier", ""))
assert re.fullmatch(r"ca-app-pub-\d{16}~\d{10}", ios_id), ios_id

print("native monetization validation ok")
