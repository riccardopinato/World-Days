#!/usr/bin/env python3
"""Write deterministic exact-artifact identity evidence for Android release lanes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

PACKAGE_ID = "com.riccardopinato.world_days"
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA40_RE = re.compile(r"^[0-9a-fA-F]{40}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise ValueError(f"artifact does not exist: {path}")
    return {
        "fileName": path.name,
        "sha256": _sha256(path),
        "bytes": path.stat().st_size,
    }


def build_manifest(
    *,
    lane: str,
    source_sha: str,
    run_id: str,
    version_name: str,
    version_code: str,
    certificate_sha256: str,
    apk: Path,
    aab: Path,
) -> dict[str, object]:
    if lane not in {"signed-qa", "production"}:
        raise ValueError(f"unsupported lane: {lane}")
    if not SHA40_RE.fullmatch(source_sha):
        raise ValueError("source SHA must be a 40-character Git SHA")
    if not str(run_id).isdigit():
        raise ValueError("workflow run ID must be numeric")
    if not SEMVER_RE.fullmatch(version_name):
        raise ValueError("versionName must be MAJOR.MINOR.PATCH")
    if not str(version_code).isdigit() or int(version_code) <= 0:
        raise ValueError("versionCode must be a positive integer")
    if not SHA256_RE.fullmatch(certificate_sha256):
        raise ValueError("signing certificate SHA-256 must contain 64 hex characters")

    return {
        "schemaVersion": 1,
        "lane": lane,
        "packageId": PACKAGE_ID,
        "versionName": version_name,
        "versionCode": int(version_code),
        "sourceSha": source_sha.lower(),
        "workflowRunId": int(run_id),
        "signingCertificateSha256": certificate_sha256.upper(),
        "artifacts": {
            "apk": _artifact(apk),
            "aab": _artifact(aab),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--lane", required=True, choices=("signed-qa", "production"))
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--version-name", required=True)
    parser.add_argument("--version-code", required=True)
    parser.add_argument("--certificate-sha256", required=True)
    parser.add_argument("--apk", required=True, type=Path)
    parser.add_argument("--aab", required=True, type=Path)
    args = parser.parse_args()

    manifest = build_manifest(
        lane=args.lane,
        source_sha=args.source_sha,
        run_id=args.run_id,
        version_name=args.version_name,
        version_code=args.version_code,
        certificate_sha256=args.certificate_sha256,
        apk=args.apk,
        aab=args.aab,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"release manifest ok: lane={args.lane} "
        f"version={args.version_name}+{args.version_code} "
        f"source={args.source_sha}"
    )


if __name__ == "__main__":
    main()
