#!/usr/bin/env python3
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from write_android_artifact_manifest import build_manifest


class AndroidArtifactManifestTest(unittest.TestCase):
    def test_manifest_binds_source_version_signer_and_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            apk = root / "app-arm64-v8a-release.apk"
            aab = root / "app-release.aab"
            apk.write_bytes(b"world-days-apk")
            aab.write_bytes(b"world-days-aab")

            manifest = build_manifest(
                lane="production",
                source_sha="a" * 40,
                run_id="123456",
                version_name="0.4.0",
                version_code="4",
                certificate_sha256="b" * 64,
                apk=apk,
                aab=aab,
            )

            self.assertEqual(manifest["packageId"], "com.riccardopinato.world_days")
            self.assertEqual(manifest["versionName"], "0.4.0")
            self.assertEqual(manifest["versionCode"], 4)
            self.assertEqual(manifest["sourceSha"], "a" * 40)
            self.assertEqual(manifest["workflowRunId"], 123456)
            self.assertEqual(manifest["signingCertificateSha256"], "B" * 64)
            self.assertEqual(
                manifest["artifacts"]["apk"]["sha256"],
                hashlib.sha256(b"world-days-apk").hexdigest(),
            )
            self.assertEqual(
                manifest["artifacts"]["aab"]["sha256"],
                hashlib.sha256(b"world-days-aab").hexdigest(),
            )

            encoded = json.dumps(manifest, sort_keys=True)
            self.assertIn('"lane": "production"', encoded)

    def test_invalid_identity_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            apk = root / "a.apk"
            aab = root / "a.aab"
            apk.write_bytes(b"x")
            aab.write_bytes(b"y")

            with self.assertRaises(ValueError):
                build_manifest(
                    lane="production",
                    source_sha="not-a-sha",
                    run_id="1",
                    version_name="0.4.0",
                    version_code="4",
                    certificate_sha256="c" * 64,
                    apk=apk,
                    aab=aab,
                )


if __name__ == "__main__":
    unittest.main()
