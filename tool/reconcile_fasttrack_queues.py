#!/usr/bin/env python3
"""Conservative Fast Track queue reconciliation; no inferred certification.

Usage:
 python tool/reconcile_fasttrack_queues.py --integrated-json path/to/ids.json --hold-json path/to/ids.json
The supplied files must contain JSON arrays of canonical ID strings. Do not feed
historical bootstrap counters or guess integration from a filename.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVES = ROOT / "data/editorial/waves"
QUEUE_FILES = [
    WAVES / f"curated_428_unwritten_fasttrack_block_0{i}.json"
    for i in (1, 2, 3)
]

def read_ids(path, key=None):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if key is not None:
        data = data[key]
    if not isinstance(data, list) or not all(isinstance(x, str) and x for x in data):
        raise ValueError(f"{path}: expected a JSON list of nonempty canonical IDs")
    if len(data) != len(set(data)):
        raise ValueError(f"{path}: duplicate canonical IDs")
    return data

def reconcile(integrated, holds):
    if integrated & holds:
        raise ValueError(f"Integrated/HOLD overlap: {sorted(integrated & holds)}")
    blocks = [read_ids(path, "canonicalIds") for path in QUEUE_FILES]
    queue = [item for block in blocks for item in block]
    occurrences = {item: [i + 1 for i, block in enumerate(blocks) if item in block] for item in set(queue)}
    duplicates = {item: waves for item, waves in occurrences.items() if len(waves) > 1}
    unique = set(queue)
    outside = (integrated | holds) - unique
    # These are queue-relative, not necessarily the complete 428-ID catalog.
    return {
        "queueRaw": len(queue),
        "queueUnique": len(unique),
        "blockSizes": [len(b) for b in blocks],
        "duplicateAcrossBlocks": duplicates,
        "integratedInQueue": len(integrated & unique),
        "holdInQueue": len(holds & unique),
        "unresolvedInQueue": len(unique - integrated - holds),
        "unresolvedIds": sorted(unique - integrated - holds),
        "statusIdsOutsideQueue": sorted(outside),
        "status": "EXPLICIT_INPUTS_ONLY_NOT_RUNTIME_CERTIFICATION",
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integrated-json", required=True, type=Path)
    parser.add_argument("--hold-json", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = reconcile(set(read_ids(args.integrated_json)), set(read_ids(args.hold_json)))
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")

if __name__ == "__main__":
    main()
