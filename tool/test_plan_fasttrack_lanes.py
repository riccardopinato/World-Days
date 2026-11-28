#!/usr/bin/env python3
"""Unit tests for disjoint Fast Track lane planner."""
import unittest
from plan_fasttrack_lanes import plan


class LanePlannerTests(unittest.TestCase):
    def test_disjoint_and_complete(self):
        blocks = [[f"a{i}" for i in range(100)], [f"b{i}" for i in range(81)]]
        for n in (2, 3, 4):
            result = plan(blocks, {"a0", "b0"}, {"a1", "b1"}, n)
            ids = [x for lane in result["lanes"] for x in lane["canonicalIds"]]
            self.assertEqual(len(ids), 177)
            self.assertEqual(len(set(ids)), 177)
            self.assertEqual(result["integratedInQueue"], 2)
            self.assertEqual(result["holdInQueue"], 2)
            self.assertNotIn("a0", ids)
            self.assertNotIn("b1", ids)

    def test_overlapping_statuses_rejected(self):
        with self.assertRaises(ValueError):
            plan([["a"], ["b"]], {"a"}, {"a"}, 2)

    def test_duplicate_queue_rejected(self):
        with self.assertRaises(ValueError):
            plan([["a"], ["a"]], set(), set(), 2)

    def test_external_status_not_miscounted(self):
        result = plan([["a"], ["b"]], {"outside"}, set(), 2)
        self.assertEqual(result["eligibleUnresolved"], 2)
        self.assertEqual(result["statusIdsOutsideQueue"], ["outside"])


if __name__ == "__main__":
    unittest.main()
