#!/usr/bin/env python3
"""Adversarial regression tests for source-origin deduplication and 2026 calendar dates."""
from copy import deepcopy
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from score_source_consensus import assess

def claim(url="https://gov.example.org/calendar",publisher="Official",origin="gazette-2026",kind="PRIMARY_GOVERNMENT",when="2026-11-09"):
    return {"url":url,"publisher":publisher,"documentOrigin":origin,
        "authorityClass":kind,"reportedDate":when,"displayedEvent":"National Independence Day","checkedOn":"2026-11-09"}

def row(attestations):
    return {"country":"KH","title":"Independence Day (Cambodia)",
        "researchFile":"wave09_asia_cambodia_vietnam_2026.json",
        "occurrence2026":"2026-11-09","attestations":attestations}

class SourceConsensusTests(unittest.TestCase):
    def test_one_direct_government_calendar_suffices_for_2026_date(self):
        r=assess(row([claim()]))
        self.assertEqual(r["status"],"DATE_2026_CONFIRMED_BY_ORIGINATOR")
        self.assertFalse(r["identityUniqueCertified"])
        self.assertFalse(r["annualRecurrenceCertified"])
        self.assertEqual(r["runtimeAdmission"],"RESEARCH_ONLY")

    def test_five_reposts_of_same_decree_are_one_origin(self):
        claims=[claim(url=f"https://mirror{i}.example.org/holidays",publisher=f"Mirror {i}",origin="gazette-2026",kind="SECONDARY_AGGREGATOR") for i in range(5)]
        r=assess(row(claims))
        self.assertEqual(r["rawWebPages"],5)
        self.assertEqual(r["independentDocumentOrigins"],1)
        self.assertEqual(r["status"],"DATE_2026_INSUFFICIENT_PRIMARY_EVIDENCE")

    def test_five_independent_secondary_sites_cannot_claim_originator_status(self):
        claims=[claim(url=f"https://news{i}.example.org/holiday",publisher=f"Publisher {i}",origin=f"original-report-{i}",kind="REPUTABLE_INDEPENDENT") for i in range(5)]
        r=assess(row(claims))
        self.assertEqual(r["status"],"DATE_2026_SECONDARY_CONSENSUS_REVIEW")
        self.assertEqual(r["independentDocumentOrigins"],5)
        self.assertEqual(r["primaryOrigins"],0)
        self.assertFalse(r["translatedEditorialCertified"])

    def test_two_government_sites_sharing_document_origin_count_once(self):
        a=claim()
        b=claim(url="https://law.example.org/2026",publisher="Law Commission")
        r=assess(row([a,b]))
        self.assertEqual(r["independentDocumentOrigins"],1)
        self.assertEqual(r["primaryOrigins"],1)
        self.assertEqual(r["status"],"DATE_2026_CONFIRMED_BY_ORIGINATOR")

    def test_date_conflict_overrides_10_confirming_sites(self):
        good=[claim(url=f"https://gov{i}.example.org/holidays",publisher=f"Gov {i}",origin=f"gazette-{i}") for i in range(10)]
        bad=claim(url="https://gov.example.net/conflict",publisher="Other Government",origin="another-gazette",when="2026-11-10")
        r=assess(row([*good,bad]))
        self.assertEqual(r["status"],"CONFLICT_NEEDS_REVIEW")
        self.assertEqual(r["conflicts"][0]["reportedDate"],"2026-11-10")

    def test_missing_actual_event_excerpt_fails(self):
        a=claim();a["displayedEvent"]=""
        with self.assertRaises(AssertionError):assess(row([a]))

    def test_duplicate_url_cannot_inflate_source_count(self):
        a=claim()
        with self.assertRaisesRegex(AssertionError,"duplicate URL"):assess(row([a,deepcopy(a)]))

    def test_five_aggregators_are_not_five_independent_authorities(self):
        claims=[claim(url=f"https://site{i}.example.org",origin=f"site{i}",kind="SECONDARY_AGGREGATOR") for i in range(5)]
        self.assertEqual(assess(row(claims))["status"],"DATE_2026_INSUFFICIENT_PRIMARY_EVIDENCE")

    def test_bad_scheme_fails(self):
        with self.assertRaises(AssertionError):assess(row([claim(url="http://gov.example.org/2026")]))

if __name__=="__main__":unittest.main()
