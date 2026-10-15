#!/usr/bin/env python3
import hashlib
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_MANIFEST = ROOT / "web" / "content" / "manifest.json"
REMOTE_MANIFEST_URL = (
    "https://riccardopinato.github.io/World-Days/content/manifest.json"
)
ATTEMPTS = 18
DELAY_SECONDS = 5
TIMEOUT_SECONDS = 15


def fetch_bytes(url: str, *, max_bytes: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "World-Days-CI/1.0",
            "Cache-Control": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        if response.status != 200:
            raise RuntimeError(f"http_{response.status}:{url}")
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise RuntimeError(f"response_exceeds_byte_cap:{url}")
        return data


def main() -> None:
    expected = json.loads(LOCAL_MANIFEST.read_text(encoding="utf-8"))
    expected_size = int(expected["sizeBytes"])
    expected_sha = str(expected["sha256"])
    expected_version = str(expected["version"])
    payload_url = str(expected["payloadUrl"])

    last_error: Exception | None = None
    for attempt in range(1, ATTEMPTS + 1):
        try:
            manifest_bytes = fetch_bytes(
                REMOTE_MANIFEST_URL,
                max_bytes=64 * 1024,
            )
            remote = json.loads(manifest_bytes.decode("utf-8"))
            if remote.get("version") != expected_version:
                raise RuntimeError(
                    f"version_not_propagated:{remote.get('version')}"
                )
            if remote.get("sha256") != expected_sha:
                raise RuntimeError("remote_manifest_sha_mismatch")
            if int(remote.get("sizeBytes", -1)) != expected_size:
                raise RuntimeError("remote_manifest_size_mismatch")
            if remote.get("payloadUrl") != payload_url:
                raise RuntimeError("remote_manifest_payload_url_mismatch")

            payload = fetch_bytes(payload_url, max_bytes=expected_size)
            if len(payload) != expected_size:
                raise RuntimeError(
                    f"remote_payload_size_mismatch:{len(payload)}"
                )
            actual_sha = hashlib.sha256(payload).hexdigest()
            if actual_sha != expected_sha:
                raise RuntimeError("remote_payload_sha_mismatch")

            decoded = json.loads(payload.decode("utf-8"))
            if decoded.get("version") != expected_version:
                raise RuntimeError("remote_payload_version_mismatch")
            if decoded.get("packId") != "world-days-catalog":
                raise RuntimeError("remote_payload_pack_id_mismatch")

            print(
                "remote content smoke ok: "
                f"version={expected_version} bytes={expected_size} "
                f"sha256={expected_sha}"
            )
            return
        except (
            OSError,
            ValueError,
            RuntimeError,
            urllib.error.URLError,
        ) as error:
            last_error = error
            print(
                f"remote content smoke attempt {attempt}/{ATTEMPTS} "
                f"not ready: {error}"
            )
            if attempt < ATTEMPTS:
                time.sleep(DELAY_SECONDS)

    raise SystemExit(f"remote content smoke failed: {last_error}")


if __name__ == "__main__":
    main()
