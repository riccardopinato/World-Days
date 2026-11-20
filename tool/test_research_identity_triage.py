#!/usr/bin/env python3
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from triage_research_identities import risks

class SemanticTriageTests(unittest.TestCase):
    def test_shared_calendar_new_year_needs_manual_review(self):
        self.assertIn("SEMANTIC_GROUP:LUNAR_NEW_YEAR",risks("Seollal","LUNISOLAR",""))
        self.assertIn("SEMANTIC_GROUP:SOUTH_ASIAN_SOLAR_NEW_YEAR",risks("Khmer New Year","SOLAR_NEW_YEAR",""))

    def test_buddhist_same_name_does_not_auto_merge(self):
        self.assertIn("SEMANTIC_GROUP:BUDDHIST_VESAK_BIRTH",risks("Buddha Purnima","LUNAR",""))

    def test_lunar_rule_requires_authority(self):
        self.assertIn("MULTIYEAR_DATE_REQUIRES_AUTHORITY",risks("Chuseok","LUNISOLAR_MULTIDAY",""))

    def test_japanese_equinox_not_hardcoded(self):
        self.assertIn("ASTRONOMICAL_OFFICIAL_ANNUAL_DECLARATION",risks("Vernal Equinox Day","EQUINOX",""))

    def test_nepal_regional_not_all_nation(self):
        self.assertIn("REGIONAL_OR_COMMUNITY_ONLY",risks("Gai Jatra","LUNISOLAR",""))

    def test_intercalary_not_annual(self):
        self.assertIn("INTERCALARY_NOT_ANNUAL",risks("Adhi Poson Full Moon Poya Day","SRI_LANKA_FULL_MOON_POYA",""))

    def test_one_off_leave_calendar_not_annually_frozen(self):
        self.assertIn("POSSIBLY_2026_ONLY_HOLIDAY",risks("Black Saturday (Philippines)","2026_ONLY",""))

    def test_plain_fixed_national_civic_day_not_semantic_blocked(self):
        self.assertEqual(risks("Vietnam National Day","FIXED",""),[])

    def test_substitute_day_warning(self):
        self.assertIn("CHECK_SUBSTITUTE_DATE_NOT_EVENT",risks("National Day","FIXED","substitute Monday is different"))

if __name__=="__main__":
    unittest.main()
