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
assert 0 < int(manifest["sizeBytes"]) <= 16 * 1024 * 1024
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
    # Remote transport removes only the unused duplicate SHA/URL provenance,
    # never original source narratives or localized facts. Full metadata is
    # retained in the bundled generated editorials and Git review ledgers.
    bundled = json.loads((ROOT / f"assets/data/editorial_{locale}.json").read_text(encoding="utf-8"))
    assert len(bundled["entries"]) == len(entries) == 947
    fasttrack_report = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_runtime_import.json"
    additional_fasttrack = (
        json.loads(fasttrack_report.read_text(encoding="utf-8"))["aiReviewedAndAppBuildIntegrated"]
        if fasttrack_report.exists() else 0
    )
    bulk_report = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_bulk_c01_runtime_import.json"
    bulk_count = (
        json.loads(bulk_report.read_text(encoding="utf-8"))["batchAiEditorialReviewedIntegrated"]
        if bulk_report.exists() else 0
    )
    prepared85_report = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_prepared85_runtime_import.json"
    prepared85_count = (
        json.loads(prepared85_report.read_text(encoding="utf-8"))["fasttrackNewIntegrated"]
        if prepared85_report.exists() else 0
    )
    wave01_report = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_wave01_runtime_import.json"
    wave01_count = (
        json.loads(wave01_report.read_text(encoding="utf-8"))["aiReviewedIntegrated"]
        if wave01_report.exists() else 0
    )
    batch02_report = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_wave01_batch02_runtime_import.json"
    batch02_count = (
        json.loads(batch02_report.read_text(encoding="utf-8"))["integratedNew"]
        if batch02_report.exists() else 0
    )
    batch03_report = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_wave01_batch03_runtime_import.json"
    batch03_count = (
        json.loads(batch03_report.read_text(encoding="utf-8"))["integratedNew"]
        if batch03_report.exists() else 0
    )
    batch04_report = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_wave01_batch04_runtime_import.json"
    batch04_count = (
        json.loads(batch04_report.read_text(encoding="utf-8"))["integratedNew"]
        if batch04_report.exists() else 0
    )
    batch05_report = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_wave01_batch05_runtime_import.json"
    batch05_count = (
        json.loads(batch05_report.read_text(encoding="utf-8"))["integratedNew"]
        if batch05_report.exists() else 0
    )
    assert sum("aiEditorialProvenance" in row for row in bundled["entries"]) == 446 + additional_fasttrack + bulk_count + prepared85_count + wave01_count + batch02_count + batch03_count + batch04_count + batch05_count
    for row in bundled["entries"]:
        row.pop("aiEditorialProvenance", None)
    assert pack == bundled, ("remote_payload_drift", locale)
    assert all("aiEditorialProvenance" not in row for row in entries), locale

print(
    f"content pack validation ok: version={manifest['version']} "
    f"records={len(records)} occurrences={len(occurrences)}"
)
