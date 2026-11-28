#!/usr/bin/env python3
"""Regression tests for the six-locale source dossier gate (no runtime approval)."""
import copy
import json
import unittest

from tool.validate_fasttrack_source_dossier import git_blob_sha, validate

LOCALES = ("en", "it", "es", "fr", "de", "pt")


def record():
    return {
        "id": "test-national-day",
        "date": "12-02",
        "eventYear": 1971,
        "sources": ["https://example.org/historical-document"],
        "texts": {
            language: ("In 1971 the assembly met to establish a new federation. "
                       "The proclamation followed earlier negotiations among regional leaders. "
                       "Its anniversary commemorates the founding decision, while later "
                       "accessions are treated as separate historical events. "
                       "The distinction is essential for an accurate chronology.")
            for language in LOCALES
        },
        "humanCertified": False,
        "aiAuthored": True,
        "editorialState": "HOLD_SOURCE_REVIEW",
    }


def check(records, sha_override=None):
    raw = json.dumps({"records": records}, ensure_ascii=False).encode("utf-8")
    return validate(raw, sha_override or git_blob_sha(raw))


class FastTrackSourceDossierTests(unittest.TestCase):
    def test_valid_six_locales_remains_structure_only(self):
        self.assertEqual(check([record()]), [])

    def test_source_sha_mismatch_fails_closed(self):
        self.assertIn("SOURCE_SHA_MISMATCH", check([record()], "0" * 40))

    def test_duplicate_canonical_id_is_rejected(self):
        self.assertIn("records[1]: DUPLICATE_ID", check([record(), copy.deepcopy(record())]))

    def test_missing_locale_is_rejected(self):
        item = record()
        del item["texts"]["pt"]
        self.assertIn("records[0]: INCOMPLETE_LOCALES", check([item]))

    def test_no_human_certification_claim(self):
        item = record()
        item["humanCertified"] = True
        self.assertIn("records[0]: CERTIFICATION_FLAGS", check([item]))

    def test_no_automatic_runtime_promotion(self):
        item = record()
        item["editorialState"] = "APPROVED"
        self.assertIn("records[0]: NOT_IN_HOLD", check([item]))

    def test_uppercase_placeholder_rejected(self):
        item = record()
        item["texts"]["en"] += " TODO"
        self.assertIn("records[0]: PLACEHOLDER_en", check([item]))

    def test_natural_spanish_todo_is_not_placeholder(self):
        item = record()
        item["texts"]["es"] += " El proceso abarcó todo el territorio."
        self.assertEqual(check([item]), [])

    def test_invalid_calendar_date_rejected(self):
        item = record()
        item["date"] = "13-40"
        self.assertIn("records[0]: INVALID_DATE", check([item]))

    def test_non_https_source_rejected(self):
        item = record()
        item["sources"] = ["http://example.org"]
        self.assertIn("records[0]: MISSING_HTTPS_SOURCES", check([item]))


if __name__ == "__main__":
    unittest.main()
