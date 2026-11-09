#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path

TOOL = Path(__file__).with_name("summarize_saved_profile.py")
spec = importlib.util.spec_from_file_location("saved_profile", TOOL)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SHA = "a" * 40


def fixture():
    return {
        f"saved_scroll_{n}_favorites": {
            "frame_count": 24,
            "average_frame_build_time_millis": 4.5 + n / 1000,
            "90th_percentile_frame_build_time_millis": 8.5,
        }
        for n in (0, 50, 150, 296)
    }


class ReportTest(unittest.TestCase):
    def test_accepts_four_real_engine_summaries(self):
        output = module.normalize(fixture(), SHA, "Android test phone", 60)
        self.assertEqual(output["scenario_count"], 4)
        self.assertEqual(output["performance_verdict"],
                         "NEEDS_MANUAL_COMPARATIVE_REVIEW")
        self.assertEqual(output["memory_cpu"], "NOT_MEASURED")

    def test_rejects_missing_scenario(self):
        payload = fixture()
        del payload["saved_scroll_296_favorites"]
        with self.assertRaisesRegex(ValueError, "missing"):
            module.normalize(payload, SHA, "Android phone", 60)

    def test_rejects_empty_or_fake_frame_timing(self):
        payload = fixture()
        payload["saved_scroll_150_favorites"] = {"frame_count": 0}
        with self.assertRaises(ValueError):
            module.normalize(payload, SHA, "Android phone", 60)

    def test_rejects_missing_sha_and_unknown_refresh(self):
        with self.assertRaises(ValueError):
            module.normalize(fixture(), "short", "Android phone", 60)
        with self.assertRaises(ValueError):
            module.normalize(fixture(), SHA, "Android phone", 0)

    def test_accepts_integration_response_wrapper(self):
        output = module.normalize({"data": fixture()}, SHA, "Android phone", 90)
        self.assertEqual(output["budget_ms"], round(1000 / 90, 3))


if __name__ == "__main__":
    unittest.main()
