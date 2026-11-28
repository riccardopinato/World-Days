#!/usr/bin/env python3
"""Unit tests for conservative Fast Track queue reconciliation."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reconcile_fasttrack_queues as module


class ReconcileQueuesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.paths = []
        for number, ids in enumerate((["a", "b"], ["b", "c"], ["d"]), 1):
            path = root / f"block{number}.json"
            path.write_text(json.dumps({"canonicalIds": ids}), encoding="utf-8")
            self.paths.append(path)
        patcher = patch.object(module, "QUEUE_FILES", self.paths)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_explicit_status_and_cross_block_duplicate(self):
        result = module.reconcile({"a"}, {"c"})
        self.assertEqual(result["queueRaw"], 5)
        self.assertEqual(result["queueUnique"], 4)
        self.assertEqual(result["duplicateAcrossBlocks"], {"b": [1, 2]})
        self.assertEqual(result["integratedInQueue"], 1)
        self.assertEqual(result["holdInQueue"], 1)
        self.assertEqual(result["unresolvedIds"], ["b", "d"])
        self.assertEqual(result["unresolvedInQueue"], 2)

    def test_overlap_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Integrated/HOLD overlap"):
            module.reconcile({"a"}, {"a"})

    def test_duplicate_within_block_fails_closed(self):
        self.paths[0].write_text(json.dumps({"canonicalIds": ["a", "a"]}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate canonical IDs"):
            module.reconcile(set(), set())

    def test_outside_queue_not_counted_as_integrated(self):
        result = module.reconcile({"external"}, {"c"})
        self.assertEqual(result["integratedInQueue"], 0)
        self.assertEqual(result["statusIdsOutsideQueue"], ["external"])

    def test_rejects_malformed_input(self):
        bad = Path(self.temp.name) / "bad.json"
        bad.write_text('["a", "", 4]', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "expected a JSON list"):
            module.read_ids(bad)


if __name__ == "__main__":
    unittest.main()
