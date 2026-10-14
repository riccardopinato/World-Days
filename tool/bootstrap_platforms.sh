#!/usr/bin/env bash
set -euo pipefail

python3 tool/build_dataset.py >/dev/null
python3 tool/build_editorial.py >/dev/null
python3 tool/build_editorial_locales.py >/dev/null

if ! command -v flutter >/dev/null 2>&1; then
  echo "Flutter is required" >&2
  exit 1
fi

needs_create=0
[[ -f android/app/build.gradle.kts || -f android/app/build.gradle ]] || needs_create=1
[[ -f ios/Runner/Info.plist ]] || needs_create=1
[[ -f web/index.html ]] || needs_create=1

if [[ "$needs_create" -eq 1 ]]; then
  flutter create \
    --platforms=android,ios,web \
    --org com.riccardopinato \
    --project-name world_days \
    .
fi


# flutter create adds its default MyApp widget test; this project owns its tests.
rm -f test/widget_test.dart

python3 tool/configure_native_retention.py
