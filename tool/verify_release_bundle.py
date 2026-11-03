#!/usr/bin/env python3
"""Verify byte-identical Android release artifacts and draft a blocked QA handoff.

Verifies claimed manifest provenance and file hashes, not the cryptographic APK
signature: the latter requires apksigner and Play signing/certificate evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from write_android_artifact_manifest import (
    PACKAGE_ID,
    SEMVER_RE,
    SHA40_RE,
    SHA256_RE,
)


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_bundle(
    *,
    manifest_path: Path,
    apk_path: Path,
    aab_path: Path,
    expected_source_sha: str,
    expected_certificate_sha256: str,
) -> dict:
    if not SHA40_RE.fullmatch(expected_source_sha):
        raise ValueError("invalid expected source SHA")
    if not SHA256_RE.fullmatch(expected_certificate_sha256):
        raise ValueError("invalid expected signer SHA-256")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        raise ValueError("unsupported artifact manifest schema")
    if data.get("lane") not in {"production", "signed-qa"}:
        raise ValueError("unsupported artifact lane")
    if data.get("packageId") != PACKAGE_ID:
        raise ValueError("unexpected Android application ID")
    if data.get("sourceSha") != expected_source_sha.lower():
        raise ValueError("source SHA differs from approved candidate")
    if data.get("signingCertificateSha256") != expected_certificate_sha256.upper():
        raise ValueError("signing certificate fingerprint mismatch")
    version = data.get("versionName")
    code = data.get("versionCode")
    run_id = data.get("workflowRunId")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        raise ValueError("invalid versionName")
    if type(code) is not int or code <= 0:
        raise ValueError("invalid versionCode")
    if type(run_id) is not int or run_id <= 0:
        raise ValueError("invalid workflowRunId")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("artifact entries missing")
    for key, path in (("apk", apk_path), ("aab", aab_path)):
        record = artifacts.get(key)
        if not isinstance(record, dict) or not path.is_file():
            raise ValueError(f"missing {key} file or manifest record")
        if record.get("fileName") != path.name:
            raise ValueError(f"{key} filename does not match manifest")
        size = path.stat().st_size
        if size <= 0 or record.get("bytes") != size:
            raise ValueError(f"{key} size mismatch or empty artifact")
        digest = record.get("sha256")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise ValueError(f"{key} manifest digest missing")
        if _hash_file(path) != digest.lower():
            raise ValueError(f"{key} SHA-256 differs from manifest")
    return data


def blocked_handoff(data: dict) -> str:
    apk = data["artifacts"]["apk"]
    aab = data["artifacts"]["aab"]
    return f"""# World Days — exact-artifact QA handoff

**VERDICT: BLOCKED / NOT CERTIFIED**
Generating this file certifies only manifest/file hash agreement.
Physical, store, signature and privacy gates remain independent.

- Version: {data["versionName"]}+{data["versionCode"]}
- Package: {data["packageId"]}
- Source SHA: {data["sourceSha"]}
- Workflow run: {data["workflowRunId"]}
- Build lane: {data["lane"]}
- Direct APK manifest certificate SHA-256: {data["signingCertificateSha256"]}
- APK: {apk["fileName"]} | SHA-256: {apk["sha256"]} | bytes: {apk["bytes"]}
- AAB: {aab["fileName"]} | SHA-256: {aab["sha256"]} | bytes: {aab["bytes"]}

## Remaining gates — do not assume PASS

- [ ] Independently verify the direct APK certificate using apksigner.
- [ ] Compare upload key and Play app-signing certificate as applicable.
- [ ] Verify Play versionCode greater than every previously uploaded build.
- [ ] Install exactly this APK on a real Android device and record its hash.
- [ ] Run permission-denied, timed notification, reboot and update reconciliation.
- [ ] Run Home Widget add, midnight rollover, market/locale and deep-link QA.
- [ ] Verify offline startup, search, translation, favorites and sharing.
- [ ] Verify UMP consent/privacy choices and ads request suppression.
- [ ] Install this AAB through Play internal testing with an authorized tester.
- [ ] Verify Remove Ads product, purchase/pending/cancel/restart/restore/acknowledgement.
- [ ] Confirm policy, Data Safety, app-ads.txt root URL and Play store listing.
- [ ] Record screenshot/video, device model, OS and exact artifact evidence.

The signed source alone does not establish device or store certification.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--apk", required=True, type=Path)
    parser.add_argument("--aab", required=True, type=Path)
    parser.add_argument("--expected-source-sha", required=True)
    parser.add_argument("--expected-certificate-sha256", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = verify_bundle(
        manifest_path=args.manifest,
        apk_path=args.apk,
        aab_path=args.aab,
        expected_source_sha=args.expected_source_sha,
        expected_certificate_sha256=args.expected_certificate_sha256,
    )
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(blocked_handoff(data), encoding="utf-8")
    print(f"artifact hash and manifest identity PASS: {data['versionName']}+{data['versionCode']} — device/store NOT VERIFIED")


if __name__ == "__main__":
    main()
