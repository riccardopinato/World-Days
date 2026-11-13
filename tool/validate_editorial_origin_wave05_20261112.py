#!/usr/bin/env python3
"""Nine primary-instrument-backed histories promoted from the 100-story draft corpus.

Fail closed on incorrect founding years, dates, changed identifiers, stale source
links, missing origin stories and false claims that the full six languages have
passed qualified editorial review.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "data/editorial/batches/origin_stories_wave05_20261112.json"
DRAFTS = ROOT / "data/editorial/candidates/origin_100_original_bilingual_drafts_20261112.json"
CATALOG = ROOT / "assets/data/official_core.json"
batch = json.loads(BATCH.read_text(encoding="utf-8"))
original = {x["observanceId"]: x for x in json.loads(DRAFTS.read_text(encoding="utf-8"))["drafts"]}
by_id = {x["id"]: x for x in json.loads(CATALOG.read_text(encoding="utf-8"))["records"]}
expected = {
    "world-logic-day": (2019, 2019, "40 C/Resolution 38"),
    "world-day-for-african-and-afrodescendant-culture": (2019, None, "40 C/Resolution 50"),
    "international-day-of-peaceful-coexistence": (2025, 2026, "A/RES/79/269"),
    "international-day-of-human-fraternity": (2020, 2021, "A/RES/75/200"),
    "world-pulses-day": (2018, 2019, "A/RES/73/251"),
    "international-day-of-the-arabian-leopard": (2023, None, "A/RES/77/295"),
    "international-day-of-women-and-girls-in-science": (2015, 2016, "A/RES/70/212"),
    "international-day-for-the-prevention-of-violent-extremism-as-and-when-conducive-to-terrorism": (
        2022, 2023, "A/RES/77/243"),
    "global-tourism-resilience-day": (2023, 2023, "A/RES/77/269"),
}
assert batch["schemaVersion"] == 1
assert batch["batchId"] == "ORIGIN-WAVE05-NINE-AUDITED-OF-100-20261112"
assert batch["reviewedOn"] == "2026-11-12"
assert batch["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert batch["count"] == len(batch["records"]) == len(expected) == 9
assert len({x["observanceId"] for x in batch["records"]}) == 9
assert {x["observanceId"] for x in batch["records"]} == set(expected)
assert original["world-logic-day"]["resolutionOrDecision"] == "40 C/Resolution 38"
assert all(o["publishedToApp"] is False for o in original.values())
previous = set()
for path in [
    ROOT / "data/editorial/batches/origin_stories_primary_20261111.json",
    *sorted((ROOT / "data/editorial/batches").glob("origin_stories_wave0[1-4]_*.json")),
]:
    if path.exists():
        old_batch = json.loads(path.read_text(encoding="utf-8"))
        previous |= {r["observanceId"] for r in old_batch["records"]}
assert set(expected).isdisjoint(previous), "no duplicates with existing researched stories"
for rec in batch["records"]:
    oid = rec["observanceId"]
    year, first, reference = expected[oid]
    canonical = by_id[oid]
    prior = original[oid]
    assert canonical["authority"]["resolution"] == prior["resolutionOrDecision"] == reference, oid
    assert rec["introducedYear"] == canonical["introducedYear"] == year, oid
    assert rec["firstObservedYear"] == first, oid
    assert canonical["introducedYearSource"] in rec["sources"], (oid, "founding-year evidence missing")
    assert canonical["introducedYearSource"] in {s["url"] for s in canonical["sources"]}
    assert all(u.startswith("https://") for u in rec["sources"])
    assert len(set(rec["sources"])) == len(rec["sources"])
    assert any(urlsplit(u).hostname in {"mandates.un.org", "www.unesco.org",
               "www.un.org", "wld.cipsh.international"} for u in rec["sources"])
    assert len(rec["sourceReviewNote"]) > 110
    assert {"en","it"} <= set(rec["locale"]) <= {"en","it","es","fr","de","pt"}, "unknown locale or missing original"
    assert not rec.get("runtimeRichEditorialApproved", False), "six-locale draft is not approved rich editorial"
    for supplemental_lang in set(rec["locale"]) - {"en","it"}:
        supplemental = rec["locale"][supplemental_lang]
        assert set(supplemental) == {"heading","origin","promoter","purpose","facts"}, (rec["observanceId"], supplemental_lang)
        assert len(supplemental["heading"].strip()) >= 19
        assert len(supplemental["origin"].strip()) >= 260
        assert len(supplemental["promoter"].strip()) >= 40
        assert len(supplemental["purpose"].strip()) >= 40
        assert 2 <= len(supplemental["facts"]) <= 5
        assert all(len(f.strip()) >= 25 for f in supplemental["facts"])
        # Draft translations must retain every explicit historical year in English.
        import re
        en_years = set(re.findall(r"\b(?:18|19|20)\d{2}\b", rec["locale"]["en"]["origin"]))
        translated_years = set(re.findall(r"\b(?:18|19|20)\d{2}\b", supplemental["origin"]))
        assert en_years <= translated_years, (rec["observanceId"], supplemental_lang, sorted(en_years-translated_years))
    for lang in ("en", "it"):
        entry = rec["locale"][lang]
        assert set(entry) == {"heading", "origin", "promoter", "purpose", "facts"}
        assert len(entry["heading"].strip()) >= 20, (oid, lang, "heading")
        assert len(entry["origin"].strip()) >= 320, (oid, lang, "individually sourced history")
        assert len(entry["promoter"].strip()) >= 95, (oid, lang, "promoter")
        assert len(entry["purpose"].strip()) >= 105, (oid, lang, "purpose")
        assert len(entry["facts"]) == 4, (oid, lang, "source-bound facts")
        assert all(len(f.strip()) > 45 for f in entry["facts"])
        for t in (entry["heading"], entry["origin"], entry["promoter"], entry["purpose"], *entry["facts"]):
            assert "undefined" not in t.lower(), (oid, lang, "placeholder")
            assert " null " not in t.lower(), (oid, lang, "placeholder")
    if oid == "world-logic-day":
        assert "38" in rec["locale"]["en"]["facts"][1] and "39" in rec["locale"]["en"]["facts"][1]
        assert "40 C/Resolution 39" not in rec["sourceReviewNote"]
    if oid == "world-pulses-day":
        assert rec["introducedYear"] == 2018 and rec["firstObservedYear"] == 2019
    if oid == "international-day-of-peaceful-coexistence":
        assert rec["introducedYear"] == 2025 and rec["firstObservedYear"] == 2026
print("PASS: nine individually source-researched IT/EN origin histories from 100 draft corpus; founding dates, promoters, and review boundary guarded")
