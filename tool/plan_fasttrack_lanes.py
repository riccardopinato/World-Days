#!/usr/bin/env python3
"""Build disjoint Fast Track research lanes from canonical queues and explicit status IDs.

No historical approval, integration, or certification is inferred from filenames.
Example:
 python tool/plan_fasttrack_lanes.py --integrated-json /tmp/integrated.json --hold-json /tmp/hold.json --lanes 4 --output /tmp/lanes.json
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVES = ROOT / "data/editorial/waves"
QUEUE_PATHS = [WAVES / f"curated_428_unwritten_fasttrack_block_0{i}.json" for i in (2, 3)]


def ids_from_file(path, key=None):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if key is not None:
        data = data[key]
    if not isinstance(data, list) or any(not isinstance(x, str) or not x for x in data):
        raise ValueError(f"{path}: expected nonempty string IDs in JSON array")
    if len(set(data)) != len(data):
        raise ValueError(f"{path}: duplicate IDs")
    return data


def plan(blocks, integrated, holds, lanes):
    if lanes not in (2, 3, 4):
        raise ValueError("lanes must be 2, 3, or 4")
    if integrated & holds:
        raise ValueError("integrated and HOLD IDs overlap")
    queue = [item for block in blocks for item in block]
    if len(queue) != len(set(queue)):
        raise ValueError("canonical IDs overlap across wave02/wave03")
    eligible = [item for item in queue if item not in integrated and item not in holds]
    # Contiguous chunks preserve queue priority and are pairwise disjoint.
    size, remainder = divmod(len(eligible), lanes)
    result = []
    cursor = 0
    for i in range(lanes):
        n = size + (i < remainder)
        batch = eligible[cursor:cursor + n]
        cursor += n
        result.append({"lane": i + 1, "count": len(batch), "canonicalIds": batch})
    assert sum(x["count"] for x in result) == len(eligible)
    assert len(set(x for lane in result for x in lane["canonicalIds"])) == len(eligible)
    return {
        "status": "PLANNING_ONLY_NOT_SOURCE_OR_RUNTIME_CERTIFICATION",
        "queueRaw": len(queue),
        "queueUnique": len(set(queue)),
        "integratedInQueue": len(set(queue) & integrated),
        "holdInQueue": len(set(queue) & holds),
        "eligibleUnresolved": len(eligible),
        "statusIdsOutsideQueue": sorted((integrated | holds) - set(queue)),
        "lanes": result,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integrated-json", required=True, type=Path)
    parser.add_argument("--hold-json", required=True, type=Path)
    parser.add_argument("--lanes", type=int, choices=(2, 3, 4), default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    blocks = [ids_from_file(p, "canonicalIds") for p in QUEUE_PATHS]
    result = plan(blocks, set(ids_from_file(args.integrated_json)), set(ids_from_file(args.hold_json)), args.lanes)
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
