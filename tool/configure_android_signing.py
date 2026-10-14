#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android"
APP_GRADLE = ANDROID / "app/build.gradle.kts"
KEY_PROPERTIES = ANDROID / "key.properties"


def main() -> None:
    if not KEY_PROPERTIES.is_file():
        print("stable signing not configured: internal/debug lane")
        return
    if not APP_GRADLE.is_file():
        raise RuntimeError("android_kotlin_gradle_missing")

    text = APP_GRADLE.read_text(encoding="utf-8")
    if "worldDaysKeystoreProperties" in text:
        print("stable signing already configured")
        return

    imports = (
        "import java.io.FileInputStream\n"
        "import java.util.Properties\n\n"
    )
    text = imports + text

    plugins_end = text.find("}\n\n", text.find("plugins {"))
    if plugins_end < 0:
        raise RuntimeError("plugins_block_not_found")
    plugins_end += 3

    properties = (
        "val worldDaysKeystoreProperties = Properties()\n"
        "val worldDaysKeystorePropertiesFile = rootProject.file(\"key.properties\")\n"
        "FileInputStream(worldDaysKeystorePropertiesFile).use {\n"
        "    worldDaysKeystoreProperties.load(it)\n"
        "}\n\n"
    )
    text = text[:plugins_end] + properties + text[plugins_end:]

    build_types = "    buildTypes {\n"
    signing = (
        "    signingConfigs {\n"
        "        create(\"worldDaysRelease\") {\n"
        "            keyAlias = worldDaysKeystoreProperties[\"keyAlias\"] as String\n"
        "            keyPassword = worldDaysKeystoreProperties[\"keyPassword\"] as String\n"
        "            storeFile = worldDaysKeystoreProperties[\"storeFile\"]?.let { file(it as String) }\n"
        "            storePassword = worldDaysKeystoreProperties[\"storePassword\"] as String\n"
        "        }\n"
        "    }\n\n"
    )
    if build_types not in text:
        raise RuntimeError("build_types_block_not_found")
    text = text.replace(build_types, signing + build_types, 1)

    debug_signing = '            signingConfig = signingConfigs.getByName("debug")'
    release_signing = (
        '            signingConfig = signingConfigs.getByName("worldDaysRelease")'
    )
    if debug_signing not in text:
        raise RuntimeError("default_debug_signing_not_found")
    text = text.replace(debug_signing, release_signing, 1)

    APP_GRADLE.write_text(text, encoding="utf-8")
    print("stable Android signing configured")


if __name__ == "__main__":
    main()
