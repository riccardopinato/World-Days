#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "content"
manifest_path = OUT / "manifest.json"

if not manifest_path.exists():
    raise SystemExit("missing web/content/manifest.json")

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
assert manifest["schemaVersion"] == 1
assert manifest["packId"] == "world-days-catalog"
assert manifest["kind"] == "catalog"
assert 0 < int(manifest["sizeBytes"]) <= 5 * 1024 * 1024
assert re.fullmatch(r"[0-9a-f]{64}", manifest["sha256"])

uri = urlparse(manifest["payloadUrl"])
assert uri.scheme == "https"
assert uri.netloc == "riccardopinato.github.io"
assert uri.query == ""
assert uri.fragment == ""
assert uri.path.startswith("/World-Days/content/")
filename = Path(uri.path).name
assert re.fullmatch(r"world-days-content-[A-Za-z0-9._-]+\.json", filename)
assert uri.path == f"/World-Days/content/{filename}"
payload_path = OUT / filename
assert payload_path.exists(), payload_path
payload_bytes = payload_path.read_bytes()

assert len(payload_bytes) == manifest["sizeBytes"]
assert hashlib.sha256(payload_bytes).hexdigest() == manifest["sha256"]

payload = json.loads(payload_bytes.decode("utf-8"))
assert payload["schemaVersion"] == 1
assert payload["packId"] == manifest["packId"]
assert payload["version"] == manifest["version"]

files = payload["files"]
required = {
    "official_core.json",
    "occurrences_2026.json",
    "editorial_en.json",
    "editorial_it.json",
    "editorial_es.json",
    "editorial_fr.json",
    "editorial_de.json",
    "editorial_pt.json",
}
assert set(files) == required

seed = files["official_core.json"]
records = seed["records"]
assert seed["datasetVersion"] == manifest["version"]
assert records
ids = [item["id"] for item in records]
assert len(ids) == len(set(ids))
known = set(ids)
for record in records:
    assert record.get("sources"), ("missing sources", record.get("id"))
    assert str(record.get("lastVerifiedAt") or "").strip(), (
        "missing lastVerifiedAt",
        record.get("id"),
    )
    assert record.get("recurrenceRules"), ("missing recurrence rules", record.get("id"))
    for source in record["sources"]:
        assert str(source.get("url") or "").strip(), (
            "missing source URL",
            record.get("id"),
        )
        assert str(source.get("verifiedAt") or "").strip(), (
            "missing source verifiedAt",
            record.get("id"),
        )

occurrences = files["occurrences_2026.json"]["occurrences"]
assert all(item["observanceId"] in known for item in occurrences)

for locale in ("en", "it", "es", "fr", "de", "pt"):
    pack = files[f"editorial_{locale}.json"]
    entries = pack.get("entries", [])
    assert all(item["observanceId"] in known for item in entries)

print(
    f"content pack validation ok: version={manifest['version']} "
    f"records={len(records)} occurrences={len(occurrences)}"
)
