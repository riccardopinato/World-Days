#!/usr/bin/env python3
"""Adversarial tests; all example records are synthetic, not source assertions."""
import copy,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tool"))
from bulk_intake import inspect,day

def sample():
    base="https://www.unesco.org/en/days/example"
    title="Synthetic Test Observance — Not a Real Day"
    return {
      "id":"synthetic-test-not-real","canonicalTitleEn":title,
      "authority":{"name":"Synthetic Institutional Test","type":"UNESCO","officiality":"OFFICIAL_UNESCO"},
      "sourceReviewedOn":"2026-11-10",
      "aliases":[],"scope":"GLOBAL","country":None,
      "localizedTitles":{l:title for l in ("en","it","es","fr","de","pt")},
      "recurrenceRules":[{"kind":"FIXED_DATE","month":4,"day":4}],
      "dateVectors":{str(y):f"{y}-04-04" for y in (2026,2027,2028)},
      "attestations":[{
        "url":base,"publisher":"Synthetic UNESCO Test",
        "originId":"synthetic-test-2026","sourceClass":"PRIMARY_ORIGINATOR",
        "reportedDate":"2026-04-04",
        "eventExcerpt":"Synthetic test date, not a real observance",
      }],
      "annualRuleEvidenceUrl":base,
      "identityReviewed":True,"identityEvidenceUrl":base,
      "introducedYear":None,"editorialApproval":{
        "status":"QUALIFIED_APPROVED","reviewer":"Synthetic test only",
        "evidenceUrl":base,
      },
    }
def trust_fixture():
    return {"id":"known-test-host","canonicalTitleEn":"Synthetic Host Fixture",
            "aliases":[],"sources":[{"tier":"A_PRIMARY","url":"https://www.unesco.org/en/days/fixture"}]}
def check(record,original=None):
    return inspect({"schemaVersion":1,"batchId":"synthetic-test","count":1,"records":[record]},
                   [trust_fixture(),*(original or [])],{"IT","US"})["records"][0]

class BulkGateTests(unittest.TestCase):
    def test_synthetic_complete_structural_record(self):
        self.assertEqual(check(sample())["status"],"ELIGIBLE")
    def test_duplicate_id_fail(self):
        rec=sample()
        self.assertIn("DUPLICATE_ID",check(rec,[{"id":rec["id"],"canonicalTitleEn":"Different title","aliases":[]}])["blockers"])
    def test_alias_collision_fail(self):
        rec=sample();rec["aliases"]=["World Hearing Day"]
        self.assertIn("ALIAS_COLLISION",check(rec,[{"id":"world-hearing-day","canonicalTitleEn":"World Hearing Day","aliases":[]}])["blockers"])
    def test_multiple_mirrors_are_one_origin(self):
        rec=sample()
        for i in range(4):
            ev=copy.deepcopy(rec["attestations"][0])
            ev["url"]=f"https://www.unesco.org/en/days/synthetic-mirror-{i}"
            rec["attestations"].append(ev)
        r=check(rec)
        self.assertEqual(r["pages"],5)
        self.assertEqual(r["documentOrigins"],1)
        self.assertEqual(r["primaryOrigins"],1)
    def test_one_conflicting_date_blocks_even_if_other_five_agree(self):
        rec=sample();bad=copy.deepcopy(rec["attestations"][0]);bad["url"]="https://www.unesco.org/en/days/conflict";bad["originId"]="another-source";bad["reportedDate"]="2026-04-05"
        rec["attestations"].append(bad)
        self.assertIn("CONTRADICTORY_DATE",check(rec)["blockers"])
    def test_premature_editorial_status_blocks(self):
        rec=sample();rec["editorialApproval"]={"status":"PENDING"}
        self.assertIn("QUALIFIED_EDITORIAL_PENDING",check(rec)["blockers"])
    def test_national_country_must_be_supported(self):
        rec=sample();rec["country"]="ZZ";rec["scope"]="NATIONAL"
        self.assertIn("UNSUPPORTED_COUNTRY",check(rec)["blockers"])
    def test_future_year_vector_is_required(self):
        rec=sample();rec["dateVectors"]["2028"]="2028-04-05"
        self.assertIn("YEAR_VECTORS_NOT_VERIFIED",check(rec)["blockers"])
    def test_missing_primary_authority_blocks(self):
        rec=sample();rec["attestations"][0]["sourceClass"]="SECONDARY_REPOST"
        self.assertIn("PRIMARY_ORIGINATOR_MISSING",check(rec)["blockers"])
    def test_calendar_rules(self):
        self.assertEqual(day({"kind":"LAST_WEEKDAY","month":1,"weekday":7},2027),"2027-01-31")
        self.assertEqual(day({"kind":"NTH_WEEKDAY","month":11,"weekday":4,"occurrence":1},2028),"2028-11-02")
    def test_batch_fifty_synthetic_distinct_records(self):
        batch=[]
        for i in range(50):
            r=sample();r["id"]=f"synthetic-test-{i}";r["canonicalTitleEn"]+=f" {i}";r["localizedTitles"]={l:r["canonicalTitleEn"] for l in r["localizedTitles"]};batch.append(r)
        result=inspect({"schemaVersion":1,"batchId":"synthetic-50","count":50,"records":batch},[trust_fixture()],set())
        self.assertEqual(result["recordCount"],50)
        self.assertEqual(result["eligible"],50)
    def test_empty_template_is_safe(self):
        result=inspect({"schemaVersion":1,"batchId":"empty-template","count":0,"records":[]},[],set())
        self.assertEqual(result["eligible"],0)

if __name__=="__main__":unittest.main()
