#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "discovery" / "snapshot_summary.json"
BACKLOG = ROOT / "data" / "discovery" / "discovery_backlog.json"
EXPECTED = {
    "giornatemondiali",
    "wikipedia_it",
    "unric_it",
    "rai_scuola",
    "pineta",
    "unesco_it",
    "coe_compass",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    snapshot = load(SNAPSHOT)
    sources = {item["sourceId"]: item["count"] for item in snapshot.get("sources", [])}
    missing = EXPECTED - sources.keys()
    assert not missing, f"missing source snapshots: {sorted(missing)}"

    for source_id in ("giornatemondiali", "wikipedia_it", "rai_scuola", "pineta", "coe_compass"):
        assert sources.get(source_id, 0) > 0, f"no observations extracted from {source_id}"

    backlog = load(BACKLOG)
    items = backlog.get("items", [])
    ids = [item["candidateId"] for item in items]
    assert len(ids) == len(set(ids)), "duplicate candidate ids"
    assert backlog.get("candidateCount") == len(items), "candidate count mismatch"
    assert backlog.get("observationCount", 0) >= len(items), "observation count smaller than candidates"
    assert len(items) >= 100, f"unexpectedly small discovery backlog: {len(items)}"

    for item in items:
        assert item.get("status") == "DISCOVERY_UNVERIFIED", item.get("candidateId")
        assert item.get("publishByDefault") is False, item.get("candidateId")
        assert item.get("sources"), item.get("candidateId")
        assert item.get("rawTitlesIt"), item.get("candidateId")
        assert item.get("reviewNeeded"), item.get("candidateId")
        for source in item["sources"]:
            assert source.get("sourceUrl", "").startswith("https://")

    print(
        f"discovery ok: {backlog['observationCount']} observations, "
        f"{len(items)} candidates, {len(sources)} sources"
    )


if __name__ == "__main__":
    main()
