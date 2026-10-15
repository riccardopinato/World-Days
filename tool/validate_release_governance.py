#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBSPEC = ROOT / "pubspec.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "android-production-release.yml"

pubspec = PUBSPEC.read_text(encoding="utf-8")
workflow = WORKFLOW.read_text(encoding="utf-8")

match = re.search(
    r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\+([1-9][0-9]*)\s*$",
    pubspec,
    flags=re.MULTILINE,
)
assert match, "pubspec version must be MAJOR.MINOR.PATCH+positiveBuildNumber"

version_name, version_code = match.groups()
assert int(version_code) > 0

assert 'refs/heads/main' in workflow, "production workflow must require main"
assert 'WORLD_DAYS_VERSION_NAME' in workflow
assert 'WORLD_DAYS_VERSION_CODE' in workflow
assert '--build-name "$WORLD_DAYS_VERSION_NAME"' in workflow
assert '--build-number "$WORLD_DAYS_VERSION_CODE"' in workflow
assert '--build-number "$GITHUB_RUN_NUMBER"' not in workflow
assert 'versionName=%s' in workflow
assert 'versionCode=%s' in workflow

print(
    f"release governance ok: versionName={version_name} "
    f"versionCode={version_code} productionSource=main"
)
