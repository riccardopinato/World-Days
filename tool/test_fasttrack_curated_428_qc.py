#!/usr/bin/env python3
"""Independent regression fixtures for the World Days Fast Track 428 QA rubric."""
import unittest
from fasttrack_curated_428_qc import audit_row, LANGUAGES

def fixture():
    prose = ("On 4 June 1884, a civic historical milestone helped shape an official "
             "commemoration in Estonia. The modern observance is distinct from the "
             "event itself, and the legal introduction year requires separate evidence. "
             "This is an explanatory test paragraph written for schema evaluation.")
    return ({
        "id": "ee-example", "schemaVersion": 1, "review": "PENDING",
        "country": "EE", "date": "06-04", "documentedIntroductionYear": None,
        "authority": "Estonian national archive", "status": "AI_DRAFT_SIX_LOCALE_SOURCE_CHECKED",
        "runtimeRichEditorialApproved": False,
        "sourceEvidence": [{"url": "https://www.riigiteataja.ee/en/akt/example",
                            "claim": "This fixture stands in for a named legal calendar source."}],
        "narratives": {lang: prose + " " + lang for lang in LANGUAGES},
    }, {"ee-example": {"id": "ee-example", "countries": ["EE"], "recurrenceRules": [
        {"kind": "FIXED_DATE", "month": 6, "day": 4}], "introducedYear": None}})

class FastTrackGateTests(unittest.TestCase):
    def test_baseline_never_certifies_facts(self):
        row, catalog = fixture()
        result = audit_row(row, catalog)
        self.assertEqual(result["outcome"], "OFFLINE_QA_PASS_SOURCE_AND_SEMANTIC_REVIEW_REQUIRED")
        self.assertTrue(result["sixLocales"])
    def test_missing_locale_hold(self):
        row, catalog = fixture()
        del row["narratives"]["pt"]
        self.assertEqual(audit_row(row, catalog)["outcome"], "HOLD")
    def test_scope_hold_individual(self):
        row, catalog = fixture()
        row["scopeDecision"] = {"status": "HOLD_NOT_A_RECOGNIZED_CIVIC_DAY"}
        self.assertEqual(audit_row(row, catalog)["outcome"], "HOLD")
    def test_wrong_date_review(self):
        row, catalog = fixture()
        row["date"] = "04-03"
        result = audit_row(row, catalog)
        self.assertEqual(result["outcome"], "REVIEW")
        self.assertIn("CALENDAR_DATE_CONFLICT", result["reviews"])
    def test_evidence_pending_review(self):
        row, catalog = fixture()
        row["sourceEvidence"][0]["verificationStatus"] = "PENDING_DIRECT_SOURCE_REVIEW"
        self.assertEqual(audit_row(row, catalog)["outcome"], "REVIEW")
    def test_english_fallback_hold(self):
        row, catalog = fixture()
        row["narratives"]["it"] = row["narratives"]["en"]
        self.assertEqual(audit_row(row, catalog)["outcome"], "HOLD")

if __name__ == "__main__":
    unittest.main()
