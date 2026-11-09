#!/usr/bin/env python3
"""Authoritative editorial coverage inventory from generated, immutable IDs.

The output is research planning evidence, NOT editorial content approval.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build():
    catalog = json.loads((ROOT / "assets/data/official_core.json").read_text(encoding="utf-8"))
    reviewed = json.loads((ROOT / "assets/data/editorial_en.json").read_text(encoding="utf-8"))
    candidate = json.loads(
        (ROOT / "data/editorial/candidates/wave04_sources_20261109.json")
        .read_text(encoding="utf-8")
    )
    known = {r["id"] for r in catalog["records"]}
    reviewed_ids = {r["observanceId"] for r in reviewed["entries"]}
    candidate_ids = {r["id"] for r in candidate["records"]}
    assert len(known) == len(catalog["records"]) >= 296
    assert len(reviewed_ids) == len(reviewed["entries"]) == 56
    assert len(candidate_ids) == len(candidate["records"]) == 8
    assert reviewed_ids.isdisjoint(candidate_ids)
    assert reviewed_ids | candidate_ids <= known
    rows = []
    for record in catalog["records"]:
        oid = record["id"]
        stage = (
            "RUNTIME_REVIEWED" if oid in reviewed_ids else
            "WAVE04_DRAFT_PENDING_HUMAN" if oid in candidate_ids else
            "NOT_RESEARCHED"
        )
        rows.append({
            "id": oid,
            "canonicalTitleEn": record["canonicalTitleEn"],
            "editorialStage": stage,
            "scope": record.get("scope"),
            "authority": (record.get("authority") or {}).get("name"),
            "sourceUrls": [s["url"] for s in record.get("sources", [])
                           if s.get("url")],
            "provenIntroducedYear": record.get("introducedYear"),
            "statusCaveat": "DRAFT source is not a reviewed article"
            if stage == "WAVE04_DRAFT_PENDING_HUMAN" else None,
        })
    counts = dict(Counter(row["editorialStage"] for row in rows))
    return {
        "schemaVersion": 1,
        "catalogVersion": catalog["datasetVersion"],
        "catalogTotal": len(rows),
        "coverage": counts,
        "generationMethod": "Deterministic join by canonical observance ID; no generated historical stories.",
        "notes": [
            "WAVE04_DRAFT_PENDING_HUMAN is not counted as runtime reviewed.",
            "An empty introducedYear means unknown and must display *.",
            "Source URLs are provenance pointers; a batch story needs individual review.",
        ],
        "items": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "reports/editorial_gap_manifest.json")
    args = parser.parse_args()
    report = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("editorial gap manifest: " + json.dumps(report["coverage"], sort_keys=True))


if __name__ == "__main__":
    main()
