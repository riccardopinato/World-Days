#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
OUT = ROOT / "web" / "content"
BASE_URL = "https://riccardopinato.github.io/World-Days/content"

FILES = [
    "official_core.json",
    "occurrences_2026.json",
    "editorial_en.json",
    "editorial_it.json",
    "editorial_es.json",
    "editorial_fr.json",
    "editorial_de.json",
    "editorial_pt.json",
]

def load_json(name):
    path = DATA / name
    if not path.exists():
        raise SystemExit(f"missing generated content file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

files = {name: load_json(name) for name in FILES}
seed = files["official_core.json"]
version = str(seed.get("datasetVersion", "")).strip()
if not version or not re.fullmatch(r"[A-Za-z0-9._-]+", version):
    raise SystemExit("invalid datasetVersion for remote content pack")

payload = {
    "schemaVersion": 1,
    "packId": "world-days-catalog",
    "version": version,
    "generatedAt": seed.get("generatedAt", ""),
    "files": files,
}

payload_bytes = (
    json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    + "\n"
).encode("utf-8")

sha256 = hashlib.sha256(payload_bytes).hexdigest()
filename = f"world-days-content-{version}.json"
manifest = {
    "schemaVersion": 1,
    "packId": "world-days-catalog",
    "version": version,
    "kind": "catalog",
    "sizeBytes": len(payload_bytes),
    "sha256": sha256,
    "payloadUrl": f"{BASE_URL}/{filename}",
    "generatedAt": seed.get("generatedAt", ""),
}

OUT.mkdir(parents=True, exist_ok=True)
for stale in OUT.glob("world-days-content-*.json"):
    stale.unlink()

(OUT / filename).write_bytes(payload_bytes)
(OUT / "manifest.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print(
    f"content pack built: version={version} "
    f"bytes={len(payload_bytes)} sha256={sha256}"
)
