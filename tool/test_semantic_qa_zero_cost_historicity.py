#!/usr/bin/env python3
"""Offline historical-anchor triage tests; no provider or network."""
import unittest
from semantic_qa_zero_cost_historicity import triage, exact_years

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

    def test_decade_is_not_a_single_calendar_year(self):
        d = example()
        d["records"][0]["source"] = {
            "origin": "The initiative began during the early 1990s."}
        d["records"][0]["translations"] = {
            "it": {"origin": "L'iniziativa nacque negli anni Novanta."},
            "es": {"origin": "La iniciativa empezó en los años noventa."}}
        out = triage(d)
        self.assertNotIn("CANONICAL_YEAR_NOT_PRESERVED", out["codes"])

    def test_exact_years_not_decade_language_noise(self):
        self.assertEqual(exact_years("The day began in 1917."), {"1917"})
        self.assertEqual(exact_years("The 1940s and 1950s were different."), set())
        self.assertEqual(exact_years("in den 1940er-Jahren"), set())
        self.assertEqual(exact_years("negli anni 1940"), set())
        self.assertEqual(exact_years("dans les années 1940"), set())
        self.assertEqual(exact_years("en la década de 1940"), set())
        self.assertEqual(exact_years("na década de 1950"), set())
        self.assertEqual(exact_years("Law 20/2022 adopted in 2022"), {"2022"})

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
