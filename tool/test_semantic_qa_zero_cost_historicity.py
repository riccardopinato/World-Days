#!/usr/bin/env python3
"""Offline historical-anchor triage tests; no provider or network."""
import unittest
from semantic_qa_zero_cost_historicity import triage

def example():
    return {"adapter": "world_days_published_editorial",
        "sourceWarnings": {"skipped": [], "conflictingDuplicateDossiers": []},
        "targetLocales": ["it", "es"],
        "records": [{"id": "mexico-constitution-day",
           "sourceRefs": ["https://www.gob.mx/"],
           "source": {"origin": "Promulgated in 1917 and entered into force in 1917."},
           "translations": {"it": {"origin": "Promulgata nel 1917."},
                            "es": {"origin": "Entró en vigor en 1918."}}}]}

class HistoricityTriageTests(unittest.TestCase):
    def test_year_difference_detected_not_certified(self):
        x = triage(example())
        self.assertEqual(x["recordCount"], 1)
        self.assertEqual(x["comparisonCount"], 2)
        self.assertGreaterEqual(x["findingsCount"], 2)
        self.assertEqual(x["paidAiApiCalls"], 0)
        self.assertFalse(x["semanticModelActuallyUsed"])
        self.assertEqual(x["certification"], "NOT_CERTIFIED")
        self.assertTrue(any(f["code"]=="CANONICAL_YEAR_NOT_PRESERVED"
                            and f["locale"]=="es" for f in x["findings"]))

    def test_source_provenance_warnings(self):
        d = example()
        d["records"][0]["sourceRefs"] = []
        self.assertIn("MISSING_SOURCE_PROVENANCE", triage(d)["codes"])

    def test_unrecognized_scope_fails_closed(self):
        d = example()
        d["adapter"] = "unrelated"
        with self.assertRaisesRegex(ValueError, "World Days"):
            triage(d)

    def test_partial_ingest_never_silently_passes(self):
        d = example()
        d["sourceWarnings"]["skipped"] = [{"recordId": "unread"}]
        with self.assertRaisesRegex(ValueError, "omit"):
            triage(d)

if __name__ == "__main__":
    unittest.main()
