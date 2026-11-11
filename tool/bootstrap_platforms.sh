#!/usr/bin/env bash
set -euo pipefail

python3 tool/build_dataset.py >/dev/null
python3 tool/build_editorial.py >/dev/null
# Required by pubspec.yaml for Web, QA, production and local entry points.
python3 tool/build_origin_review_index.py >/dev/null
python3 tool/validate_origin_review_index.py >/dev/null
python3 tool/build_editorial_locales.py >/dev/null
python3 tool/build_content_pack.py >/dev/null

if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter is required" >&2
  exit 1
fi

needs_create=0
[[ -f android/app/build.gradle.kts || -f android/app/build.gradle ]] || needs_create=1
[[ -f ios/Runner/Info.plist ]] || needs_create=1
[[ -f web/index.html ]] || needs_create=1

# Flutter platform scaffolding must never silently replace the committed
# dependency lock (observed with Flutter 3.47.3 and --no-pub).
lock_snapshot="$(mktemp)"
cp pubspec.lock "$lock_snapshot"
trap 'rm -f "$lock_snapshot"' EXIT

if [[ "$needs_create" -eq 1 ]]; then
  flutter create \
    --platforms=android,ios,web \
    --org com.riccardopinato \
    --project-name world_days \
    --no-pub \
    .
fi

# Restore source-controlled resolution before explicit flutter pub get.
if ! cmp -s pubspec.lock "$lock_snapshot"; then
  cp "$lock_snapshot" pubspec.lock
fi

# flutter create adds its default MyApp widget test; this project owns its tests.
rm -f test/widget_test.dart

python3 tool/configure_native_retention.py
python3 tool/configure_native_monetization.py
python3 tool/configure_native_content_pack.py
python3 tool/configure_android_signing.py

