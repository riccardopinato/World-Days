#!/usr/bin/env python3
"""Independent final verification of the cohort01 Fast Track bulk import."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets/data"
REPORTS = ROOT / "reports/editorial_curated_428_origin_research"
LANGS = ("en", "it", "es", "fr", "de", "pt")
read = lambda p: json.loads(p.read_text(encoding="utf-8"))

report = read(REPORTS / "fasttrack_bulk_c01_runtime_import.json")
ledger = read(ROOT / "data/editorial/reviews/curated_428_fasttrack_c01_bulk_20261127.json")
assert report["mode"] == "APP_FACTORY_FAST_TRACK_AI_BATCH_NO_HUMAN_SIGNOFF"
assert report["candidateCount"] == ledger["candidateCount"] == len(ledger["records"])
ids = report["integratedIds"]
assert len(ids) == len(set(ids)) == report["batchAiEditorialReviewedIntegrated"]
assert report["holdCount"] + len(ids) == ledger["candidateCount"]
assert report["contextualBefore"] == 426
assert report["contextualAfter"] == 426 - len(ids)
assert report["richEditorialAfter"] == 521 + len(ids)
assert report["humanCertified"] is False
assert report["sourceSpecificHistoricalPagesAllIndividuallyReopened"] is False
assert report["sourceIntegrityVerified"] is True
core = read(ASSETS / "official_core.json")
assert core["datasetVersion"] == report["contentPackVersion"]
canonical = {row["id"]: row for row in core["records"]}
assert len(canonical) == 947 and set(ids) <= set(canonical)
main_order = None
for lang in LANGS:
    pack = read(ASSETS / f"editorial_{lang}.json")
    assert pack["datasetVersion"] == report["contentPackVersion"]
    rows = pack["entries"]
    seq = [row["observanceId"] for row in rows]
    assert len(seq) == len(set(seq)) == pack["entryCount"] == 947
    if main_order is None:
        main_order = seq
    else:
        assert seq == main_order, ("changed_order", lang)
    selected = {row["observanceId"]: row for row in rows if row["observanceId"] in ids}
    assert set(selected) == set(ids)
    for oid, row in selected.items():
        assert row["status"] == "AI_SOURCE_REVIEWED_SIX_LOCALE", (lang, oid)
        assert len(row["origin"].strip()) >= 180, (lang, oid)
        assert row["institutionalSourceUrls"]
        prov = row["aiEditorialProvenance"]
        assert prov["reviewLevel"] == "AI_EDITORIAL_REVIEWED"
        assert not prov["humanSignoff"]
        assert not prov["allHistoricPagesIndependentlyReopened"]
    assert sum(row["status"] == "AI_CONTEXTUAL_SIX_LOCALE" for row in rows) == 426 - len(ids), lang
    assert sum(row["status"] != "AI_CONTEXTUAL_SIX_LOCALE" for row in rows) == 521 + len(ids), lang
print("FASTTRACK_C01_BULK_LOCALE_VALIDATION_PASS", len(ids), "x", len(LANGS),
      "holds", report["holdCount"])
