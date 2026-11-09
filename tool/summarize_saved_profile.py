#!/usr/bin/env python3
"""Normalize a real Flutter integration_test on-device FrameTiming report.

Does NOT infer device runs, performance PASS, FPS, memory or CPU when absent.
"""
import argparse
import datetime as dt
import json
import re
from pathlib import Path

COUNTS = (0, 50, 150, 296)
METRIC = "average_frame_build_time_millis"


def normalize(payload, source_sha, device, refresh_hz):
    if isinstance(payload, dict) and "data" in payload:
        payload = payload["data"]
    if not isinstance(payload, dict):
        raise ValueError("invalid Flutter integration response")
    results = []
    for count in COUNTS:
        key = f"saved_scroll_{count}_favorites"
        item = payload.get(key)
        if not isinstance(item, dict):
            raise ValueError(f"required physical device scenario missing: {key}")
        frame_count = item.get("frame_count")
        if frame_count is not None and (
            not isinstance(frame_count, (int, float)) or frame_count <= 0
        ):
            raise ValueError(f"invalid frame count: {key}")
        metric = item.get(METRIC)
        if not isinstance(metric, (int, float)) or metric < 0:
            raise ValueError(f"no measured FrameTiming: {key}.{METRIC}")
        results.append({
            "favorite_count": count,
            "report_key": key,
            "raw_engine_summary": item,
            "frame_build_mean_ms": metric,
        })
    if not re.fullmatch(r"[0-9a-fA-F]{40}", source_sha):
        raise ValueError("source SHA must be full 40-hex")
    if not 30 <= refresh_hz <= 240:
        raise ValueError("refresh_hz out of range")
    if not device.strip():
        raise ValueError("device description required")
    return {
        "schema_version": 1,
        "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_sha": source_sha.lower(),
        "device": device,
        "display_refresh_hz": refresh_hz,
        "budget_ms": round(1000 / refresh_hz, 3),
        "scenario_count": len(results),
        "evidence_level": "PHYSICAL_ENGINE_FRAME_TIMINGS_RECORDED_BY_USER",
        "performance_verdict": "NEEDS_MANUAL_COMPARATIVE_REVIEW",
        "memory_cpu": "NOT_MEASURED",
        "android_notification_widget_billing": "NOT_VERIFIED",
        "results": results,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("response_json", type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--source-sha", required=True)
    p.add_argument("--device", required=True)
    p.add_argument("--refresh-hz", type=int, required=True)
    a = p.parse_args()
    raw = json.loads(a.response_json.read_text(encoding="utf-8"))
    report = normalize(raw, a.source_sha, a.device, a.refresh_hz)
    a.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"saved profile captured {report['scenario_count']} device scenarios;"
          f" not a physical acceptance verdict; file={a.output}")


if __name__ == "__main__":
    main()
