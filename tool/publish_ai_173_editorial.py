#!/usr/bin/env python3
"""Append the 173 SHA-pinned, user-delegated AI editorial reviews to runtime packs.

Run AFTER the legacy 56-item editorial generation and validation. The certified
source snapshots are vendored, allowing strictly offline use. Existing source
PRs and the original immutable AI review ledger are NOT rewritten or merged.
This is AI editorial review, not human signoff or an APK/Store certification.
"""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("en", "it", "es", "fr", "de", "pt")
SOURCES = (
    ("CA", "ai_173_ca_20261115.json", 32),
    ("KR", "ai_173_kr_20261115.json", 57),
    ("PH", "ai_173_ph_a_20261115.json", 39),
    ("PH", "ai_173_ph_b_20261115.json", 45),
)
SOURCE_DIR = ROOT / "data/editorial/published"
LEDGER = ROOT / "data/editorial/reviews/ph_kr_ca_173_ai_editorial_certification_20261114.json"
CATALOG = ROOT / "assets/data/official_core.json"
ASSETS = ROOT / "assets/data"
REPORT = ROOT / "reports/ai_173_runtime_import.json"
CORRECTIONS = {
    "ca-raoul-wallenberg-day": "2001_DESIGNATION_2002_FIRST_ANNUAL_SIX_LANGUAGES",
    "ph-w13-panagyaman-rice-festival-month": "CULTURAL_CONTINUITY_NOT_INDEFINITE_STATUTORY_OR_PAID_HOLIDAY",
    "ph-w13-w-a-t-c-h-time-consciousness-and-honesty-month": "CULTURAL_CONTINUITY_NOT_INDEFINITE_STATUTORY_OR_PAID_HOLIDAY",
}
PROMOTER_LABEL = {
    "en": "Originating or supporting institutions",
    "it": "Enti promotori o sostenitori",
    "es": "Instituciones promotoras o participantes",
    "fr": "Institutions à l'origine ou associées",
    "de": "Initiierende oder beteiligte Institutionen",
    "pt": "Instituições promotoras ou participantes",
}

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    ledger = read(LEDGER)
    certs = {x["observanceId"]: x for x in ledger["records"]}
    assert len(certs) == 173 and all(x["status"] == "AI_CERTIFIED" for x in certs.values())
    assert ledger["summary"]["AI_CERTIFIED"] == 173
    assert ledger["summary"]["appRuntimePublishedByThisLedger"] == 0, (
        "Immutable historical certification ledger cannot claim a later release"
    )
    canonical = {x["id"] for x in read(CATALOG)["records"]}
    assert len(canonical) >= 1111

    records = {}
    by_country = Counter()
    for country, filename, count in SOURCES:
        path = SOURCE_DIR / filename
        pack = read(path)
        assert pack["schemaVersion"] == 1 and pack["scope"] == "PH_KR_CA_173"
        assert pack["country"] == country
        assert pack["sourceLedgerSha"] == "9b30d37c0bd75ddc0e4548085b8dfbbcbfbded5d"
        assert pack["count"] == len(pack["records"]) == count
        for rec in pack["records"]:
            oid = rec["observanceId"]
            assert oid not in records and oid in canonical, ("duplicate/unknown", oid)
            assert rec["country"] == country and rec["reviewStatus"] == "AI_CERTIFIED"
            cert = certs[oid]
            for field, source_field in (
                ("sourcePR", "sourcePR"), ("sourceHead", "sourceHead"),
                ("sourceFile", "sourceFile"), ("sourceBlobSha", "sourceBlobSha"),
                ("reviewedAt", "reviewDate"),
            ):
                assert rec[field] == cert[source_field], (oid, field)
            assert rec["evidenceUrls"] == cert["sourceEvidence"], oid
            assert rec["sources"] and all(
                urlsplit(url).scheme == "https" and urlsplit(url).netloc
                for url in rec["sources"]
            ), oid
            assert set(rec["locale"]) == set(LOCALES), oid
            for language in LOCALES:
                localized = rec["locale"][language]
                assert all(
                    isinstance(localized.get(field), str) and localized[field].strip()
                    for field in ("heading", "origin", "promoter", "purpose")
                ), (oid, language)
                assert len(localized["origin"].strip()) >= 90, (oid, language)
                assert 2 <= len(localized["facts"]) <= 5, (oid, language)
                assert all(len(fact.strip()) >= 20 for fact in localized["facts"]), (oid, language)
            assert rec.get("publicationCorrection") == CORRECTIONS.get(oid), oid
            records[oid] = rec
            by_country[country] += 1

    assert set(records) == set(certs), "Only 173 individually AI-certified IDs may enter runtime"
    assert by_country == {"CA": 32, "KR": 57, "PH": 84}, by_country
    raoul = records["ca-raoul-wallenberg-day"]
    assert raoul["introducedYear"] == 2001 and raoul["firstObservedYear"] == 2002
    for locale in LOCALES:
        assert "2001" in raoul["locale"][locale]["origin"]
        assert "2002" in raoul["locale"][locale]["origin"]
    for oid in list(CORRECTIONS)[1:]:
        assert records[oid].get("legalRecurrenceCaveat") is True, oid
        assert records[oid]["country"] == "PH", oid

    for locale in LOCALES:
        path = ASSETS / f"editorial_{locale}.json"
        pack = read(path)
        assert pack["schemaVersion"] == 2 and pack["locale"] == locale
        originals = pack["entries"]
        original_ids = {x["observanceId"] for x in originals}
        assert len(originals) == len(original_ids) == 56, "Legacy editorials must be retained"
        assert original_ids.isdisjoint(records), "Cannot overwrite an already published editorial"
        enriched = []
        for oid in sorted(records):
            source = records[oid]
            text = source["locale"][locale]
            note = text["promoter"].strip()
            origin = text["origin"].strip() + (
                "\n\n" + PROMOTER_LABEL[locale] + ": " + note if note else ""
            )
            enriched.append({
                "observanceId": oid,
                "locale": locale,
                "translationOf": "en" if locale != "en" else None,
                "status": "AI_CERTIFIED",
                "hook": text["heading"].strip(),
                "summary": text["purpose"].strip(),
                "whyThisDate": "",
                "origin": origin,
                "whyItMatters": "",
                "quickFacts": [x.strip() for x in text["facts"]],
                "waysToTakePart": [],  # Never invent participation actions
                "relatedObservanceIds": [],
                "lastReviewedAt": source["reviewedAt"],
                "sourcePolicy": "User-delegated AI editorial source review; not external human certification.",
                "aiEditorialProvenance": {
                    "sourcePR": source["sourcePR"],
                    "sourceHead": source["sourceHead"],
                    "sourceFile": source["sourceFile"],
                    "sourceBlobSha": source["sourceBlobSha"],
                    "evidenceUrls": source["evidenceUrls"],
                    "publicationCorrection": source.get("publicationCorrection"),
                    "legalRecurrenceCaveat": source.get("legalRecurrenceCaveat", False),
                },
            })
        pack["entries"] = originals + enriched
        pack["entryCount"] = len(pack["entries"])
        pack["aiEditorialCertifiedCount"] = len(enriched)
        pack["aiEditorialReviewer"] = "GPT-6_AI_EDITORIAL_REVIEW"
        path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "AI_EDITORIAL_INTEGRATED_IN_BUILD_NOT_PHYSICAL_RELEASE_CERTIFICATION",
        "catalogTotal": len(canonical),
        "existingEditorialCount": 56,
        "addedAiEditorialCount": len(records),
        "editorialTotal": 56 + len(records),
        "byCountry": dict(by_country),
        "languages": list(LOCALES),
        "publicationCorrections": CORRECTIONS,
        "sourceLedgerBlobSha": "9b30d37c0bd75ddc0e4548085b8dfbbcbfbded5d",
        "sourceIdentityEnforced": True,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("AI_173_IMPORT", json.dumps(report, sort_keys=True))

if __name__ == "__main__":
    main()
