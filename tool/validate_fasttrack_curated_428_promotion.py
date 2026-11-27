#!/usr/bin/env python3
"""Verify the reviewed cohort reached the app bundles in all six locales."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/data"
REPORT = ROOT / "reports/editorial_curated_428_origin_research/fasttrack_runtime_import.json"
LEDGER = ROOT / "data/editorial/reviews/curated_428_fasttrack_czech_civic_ai_review_20261127.json"
LANGS = ("en", "it", "es", "fr", "de", "pt")

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

report, ledger = load(REPORT), load(LEDGER)
ids = {r["observanceId"] for r in ledger["records"]}
assert report["aiReviewedAndAppBuildIntegrated"] == len(ids) == 2
assert set(report["integratedIds"]) == ids
assert report["originRichInAppBuild"] == 521
assert report["contextualOriginsRemainingInAppBuild"] == 426
official = load(ASSETS / "official_core.json")
assert official["datasetVersion"] == report["contentPackVersion"]
original_order = None
for lang in LANGS:
    pack = load(ASSETS / f"editorial_{lang}.json")
    assert pack["datasetVersion"] == report["contentPackVersion"], lang
    entries = pack["entries"]
    seq = [r["observanceId"] for r in entries]
    assert len(seq) == len(set(seq)) == pack["entryCount"] == 947
    if original_order is None:
        original_order = seq
    else:
        assert seq == original_order, lang
    selected = {r["observanceId"]: r for r in entries if r["observanceId"] in ids}
    assert set(selected) == ids, lang
    for oid, row in selected.items():
        assert row["status"] == "AI_SOURCE_REVIEWED_SIX_LOCALE", (lang, oid)
        assert len(row["origin"].strip()) >= 180, (lang, oid)
        assert len(row["whyThisDate"].strip()) >= 85, (lang, oid)
        assert "not independently established" not in row["whyThisDate"].lower(), (lang, oid)
        assert "1999" in row["whyThisDate"] if "nato" in oid else "2004" in row["whyThisDate"], (lang, oid)
        assert row["aiEditorialProvenance"]["reviewLevel"] == "AI_EDITORIAL_REVIEWED"
        assert not row["aiEditorialProvenance"]["humanSignoff"]
    assert sum(r["status"] == "AI_CONTEXTUAL_SIX_LOCALE" for r in entries) == 426, lang
    assert sum(r["status"] != "AI_CONTEXTUAL_SIX_LOCALE" for r in entries) == 521, lang
print("FASTTRACK_CURATED_REVIEWED_APP_BUILD_PASS", len(ids), "records x", len(LANGS), "locales")
