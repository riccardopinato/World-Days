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
        self.assertEqual(exact_years("en las décadas de 1930 y 1940"), set())
        self.assertEqual(exact_years("nas décadas de 1930 e 1940"), set())
        self.assertEqual(exact_years("des années 1930 et 1940"), set())
        self.assertEqual(exact_years("Les années 2024-2033"), {"2024", "2033"})
        self.assertEqual(exact_years("la Décennie couvre les années 2024–2033"),
                         {"2024", "2033"})
        self.assertEqual(exact_years("Proclamé en 2025"), {"2025"})
        self.assertEqual(exact_years("Law 20/2022 adopted in 2022"), {"2022"})

    def test_unverified_first_ceremony_does_not_assert_year(self):
        source = ("The event occurred in 1944. Act 241/1993 recognised it. "
                  "An individually evidenced inaugural 1993 or 1994 memorial "
                  "ceremony remains unknown.")
        self.assertEqual(exact_years(source), {"1944", "1993"})
        # Explicit chronology outside an uncertain first-ceremony clause persists.
        self.assertEqual(exact_years("The first event was held in 1994."),
                         {"1994"})
        self.assertEqual(exact_years("The first ceremony in 1994 remains unverified."),
                         set())

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
