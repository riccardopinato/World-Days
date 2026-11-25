#!/usr/bin/env python3
"""Deterministic negative tests for the research-catalog overlap screen."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_research_candidates import audit, normalize, unqualify


def record(ident, title, country=None, aliases=None):
    return {
        "id": ident,
        "canonicalTitleEn": title,
        "aliases": aliases or [],
        "localizedTitles": {
            "en": title,
            "it": "Giornata della lingua" if ident == "language-day" else title,
            "es": title, "fr": title, "de": title, "pt": title,
        },
        "scope": "NATIONAL" if country else "GLOBAL",
        "countries": [country] if country else [],
    }

def candidate(title, country=None, ident=None, source="https://example.org/source"):
    r = {"canonicalTitleEn": title, "source": source, "date": {"month": 11, "day": 5}}
    if country:
        r["country"] = country
    if ident:
        r["id"] = ident
    return r

class ScreeningTests(unittest.TestCase):
    def setUp(self):
        self.catalog = [
            record("world-language-day", "World Language Day"),
            record("language-day", "Language Day", aliases=["Language Celebration"]),
            record("ca-national-day", "National Day (Canada)", country="CA"),
        ]

    def run_audit(self, records, count=None):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "wave-test.json"
            path.write_text(json.dumps({
                "candidateOnly": True,
                "recordCount": len(records) if count is None else count,
                "records": records,
            }), encoding="utf-8")
            return audit(self.catalog, [path])

    def test_unicode_normalization(self):
        self.assertEqual(normalize("Journée—d'Été"), "journee d ete")
        self.assertEqual(unqualify("National Day (Canada)"), "national day")

    def test_same_id(self):
        report = self.run_audit([candidate("Different label", ident="world-language-day")])
        self.assertEqual(report["candidateResults"][0]["status"], "DIRECT_CATALOG_OVERLAP")

    def test_global_exact(self):
        report = self.run_audit([candidate("World Language Day", "PH")])
        self.assertEqual(report["candidateResults"][0]["status"], "DIRECT_CATALOG_OVERLAP")

    def test_localized_collision(self):
        report = self.run_audit([candidate("Giornata della lingua", "CA")])
        self.assertEqual(report["candidateResults"][0]["status"], "DIRECT_CATALOG_OVERLAP")

    def test_alias_collision(self):
        report = self.run_audit([candidate("Language Celebration", "TH")])
        self.assertEqual(report["candidateResults"][0]["status"], "DIRECT_CATALOG_OVERLAP")

    def test_other_country_homonym_not_direct(self):
        report = self.run_audit([candidate("National Day (Canada)", "KR")])
        result = report["candidateResults"][0]
        self.assertNotEqual(result["status"], "DIRECT_CATALOG_OVERLAP")
        self.assertTrue(result["crossCountryHomonyms"])

    def test_candidate_repeated_title(self):
        report = self.run_audit([candidate("New Days", "CA"), candidate("New Days", "CA")])
        self.assertEqual(report["crossWaveRepeatedCountryTitles"], 2)

    def test_candidate_in_other_country_not_false_duplicate(self):
        report = self.run_audit([candidate("New Days", "CA"), candidate("New Days", "KR")])
        self.assertEqual(report["crossWaveRepeatedCountryTitles"], 0)

    def test_count_failure(self):
        with self.assertRaisesRegex(ValueError, "Candidate count mismatch"):
            self.run_audit([candidate("New Days", "CA")], count=2)

    def test_source_failure(self):
        with self.assertRaisesRegex(ValueError, "Missing HTTPS source"):
            self.run_audit([candidate("New Days", "CA", source="http://example.com/x")])

    def test_invalid_date_failure(self):
        bad = candidate("New Days", "CA")
        bad["date"]["month"] = 13
        with self.assertRaises(ValueError):
            self.run_audit([bad])

if __name__ == "__main__":
    unittest.main()
