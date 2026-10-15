#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml"

if not MANIFEST.exists():
    raise SystemExit("AndroidManifest.xml missing; run bootstrap first")

text = MANIFEST.read_text(encoding="utf-8")
permission = '<uses-permission android:name="android.permission.INTERNET"/>'

if permission not in text:
    marker = "<application"
    if marker not in text:
        raise SystemExit("Android manifest application marker missing")
    text = text.replace(marker, f"    {permission}\n\n    {marker}", 1)
    MANIFEST.write_text(text, encoding="utf-8")

print("native content-pack config ok")
