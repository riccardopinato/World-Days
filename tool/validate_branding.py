#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
assert (ROOT / "assets/branding/world_days_icon.svg").is_file()
assert (ROOT / "launcher_icons.yaml").is_file()

android = ROOT / "android/app/src/main/res/mipmap-mdpi/ic_launcher.png"
ios = ROOT / "ios/Runner/Assets.xcassets/AppIcon.appiconset/Contents.json"
assert android.is_file(), android
assert ios.is_file(), ios

print("branding validation ok")
