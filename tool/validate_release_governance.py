#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBSPEC = ROOT / "pubspec.yaml"
PRODUCTION_WORKFLOW = ROOT / ".github" / "workflows" / "android-production-release.yml"
SIGNED_QA_WORKFLOW = ROOT / ".github" / "workflows" / "android-signed-qa.yml"

pubspec = PUBSPEC.read_text(encoding="utf-8")
workflow = PRODUCTION_WORKFLOW.read_text(encoding="utf-8")
signed_qa_workflow = SIGNED_QA_WORKFLOW.read_text(encoding="utf-8")

match = re.search(
    r"^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\+([1-9][0-9]*)\s*$",
    pubspec,
    flags=re.MULTILINE,
)
assert match, "pubspec version must be MAJOR.MINOR.PATCH+positiveBuildNumber"

version_name, version_code = match.groups()
assert int(version_code) >= 4, "versionCode must not regress below the post-0.3 production floor"

assert 'refs/heads/main' in workflow, "production workflow must require main"
assert 'WORLD_DAYS_VERSION_NAME' in workflow
assert 'WORLD_DAYS_VERSION_CODE' in workflow
assert '--build-name "$WORLD_DAYS_VERSION_NAME"' in workflow
assert '--build-number "$WORLD_DAYS_VERSION_CODE"' in workflow
assert '--build-number "$GITHUB_RUN_NUMBER"' not in workflow
assert 'versionName=%s' in workflow
assert 'versionCode=%s' in workflow
assert 'write_android_artifact_manifest.py' in workflow
assert 'production-artifact-manifest.json' in workflow

assert 'WORLD_DAYS_VERSION_NAME' in signed_qa_workflow
assert 'WORLD_DAYS_VERSION_CODE' in signed_qa_workflow
assert '--build-name "$WORLD_DAYS_VERSION_NAME"' in signed_qa_workflow
assert '--build-number "$WORLD_DAYS_VERSION_CODE"' in signed_qa_workflow
assert '--build-number "$GITHUB_RUN_NUMBER"' not in signed_qa_workflow
assert 'write_android_artifact_manifest.py' in signed_qa_workflow
assert 'signed-qa-artifact-manifest.json' in signed_qa_workflow

print(
    f"release governance ok: versionName={version_name} "
    f"versionCode={version_code} productionSource=main"
)
