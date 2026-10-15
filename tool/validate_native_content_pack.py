#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml"

if not MANIFEST.exists():
    raise SystemExit("AndroidManifest.xml missing")

text = MANIFEST.read_text(encoding="utf-8")
required = '<uses-permission android:name="android.permission.INTERNET"/>'
if required not in text:
    raise SystemExit("Android INTERNET permission missing for remote content packs")

print("native content-pack validation ok")
