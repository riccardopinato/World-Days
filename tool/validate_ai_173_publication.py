#!/usr/bin/env python3
"""Regression check for the 173 user-delegated AI-certified runtime editorials.

The original 56 reviewed entries and their historical validators remain intact.
Never confuse AI editorial review with qualified human review or physical release.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("en", "it", "es", "fr", "de", "pt")
LEDGER = ROOT / "data/editorial/reviews/ph_kr_ca_173_ai_editorial_certification_20261114.json"
REPORT = ROOT / "reports/ai_173_runtime_import.json"
SPECIAL = {
    "ca-raoul-wallenberg-day",
    "ph-w13-panagyaman-rice-festival-month",
    "ph-w13-w-a-t-c-h-time-consciousness-and-honesty-month",
}
def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

ledger = load(LEDGER)
expected = {r["observanceId"] for r in ledger["records"]}
assert len(expected) == 173
report = load(REPORT)
assert report["addedAiEditorialCount"] == 173
assert report["editorialTotal"] == 229
assert report["existingEditorialCount"] == 56
assert report["byCountry"] == {"CA": 32, "KR": 57, "PH": 84}
assert report["sourceIdentityEnforced"] is True
assert set(report["publicationCorrections"]) == SPECIAL

original_reference = None
for locale in LOCALES:
    doc = load(ROOT / f"assets/data/editorial_{locale}.json")
    entries = doc["entries"]
    ids = [r["observanceId"] for r in entries]
    assert len(ids) == len(set(ids)) == doc["entryCount"] == 229
    certified = {r["observanceId"]: r for r in entries if r["status"] == "AI_CERTIFIED"}
    assert set(certified) == expected, (locale, len(certified), sorted(expected - set(certified))[:5])
    assert sum(r["status"] != "AI_CERTIFIED" for r in entries) == 56
    assert doc["aiEditorialCertifiedCount"] == 173
    assert doc["aiEditorialReviewer"] == "GPT-6_AI_EDITORIAL_REVIEW"
    if original_reference is None:
        original_reference = ids
    else:
        assert ids == original_reference, (locale, "locale order mismatch")
    for oid, record in certified.items():
        assert record["locale"] == locale
        assert record["origin"].strip() and record["summary"].strip()
        assert record["hook"].strip()
        assert len(record["quickFacts"]) >= 2
        assert record["waysToTakePart"] == [], "No unverified actions may be invented"
        assert record["whyItMatters"] == "", "Unverified editorial extensions are not allowed"
        pr = record["aiEditorialProvenance"]
        assert pr["sourceHead"] and len(pr["sourceHead"]) == 40
        assert pr["sourceBlobSha"] and len(pr["sourceBlobSha"]) == 40
        assert pr["evidenceUrls"]
        assert pr["publicationCorrection"] == report["publicationCorrections"].get(oid)
    raoul = certified["ca-raoul-wallenberg-day"]
    assert "2001" in raoul["origin"] and "2002" in raoul["origin"]
    for oid in SPECIAL - {"ca-raoul-wallenberg-day"}:
        assert certified[oid]["aiEditorialProvenance"]["legalRecurrenceCaveat"] is True

print("AI_173_RUNTIME_EDITORIAL_OK: 173 AI-certified x 6 locales, 56 legacy retained, 3 corrections")
