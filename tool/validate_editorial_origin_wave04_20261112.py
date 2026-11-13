#!/usr/bin/env python3
"""Validate Wave04 source-backed origin articles, old six-locale drafts never promoted.

The source-audit validates precise institutional links and transparent chronology;
it does not certify native-language editing or external physical/runtime behavior.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
old = json.loads((ROOT / "data/editorial/batches/un_primary_2026_11_03_02.json").read_text(encoding="utf-8"))
new = json.loads((ROOT / "data/editorial/batches/origin_stories_wave04_20261112.json").read_text(encoding="utf-8"))
catalog = json.loads((ROOT / "assets/data/official_core.json").read_text(encoding="utf-8"))
raw = {r["id"]: r for r in old["entries"]}
provenance = {r["id"]: r for r in old["establishment"]}
canonical = {r["id"]: r for r in catalog["records"]}
first = {
    "international-mother-language-day": 2000,
    "international-day-of-happiness": None,
    "world-autism-awareness-day": 2008,
    "international-day-of-families": 1994,
    "international-youth-day": None,
    "international-day-of-democracy": None,
    "international-day-of-older-persons": None,
    "international-day-of-persons-with-disabilities": None,
    "international-volunteer-day-for-economic-and-social-development": None,
    "international-anti-corruption-day": None,
    "international-literacy-day": 1967,
    "world-refugee-day": 2001,
    "international-day-of-peace": 1982,
    "human-rights-day": None,
}
assert len(first) == len(provenance) == len(raw) == 14
assert set(first) == set(raw) == set(provenance)
assert old["batchId"] and old["reviewedAt"]
assert len(canonical) == len(catalog["records"]) >= 1111
assert new["batchId"] == "ORIGIN-WAVE04-UN-UNESCO-14-20261112"
assert new["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE"
assert new["reviewedOn"] == "2026-11-12"
assert new["count"] == len(new["records"]) == 14
assert set(r["observanceId"] for r in new["records"]) == set(first)
assert len(set(r["observanceId"] for r in new["records"])) == 14
allowed = {"www.un.org", "mandates.un.org", "digitallibrary.un.org",
           "www.unesco.org", "www.unv.org", "www.unhcr.org"}
for rec in new["records"]:
    rid = rec["observanceId"]
    prior = raw[rid]["translations"]
    evidence = provenance[rid]
    official = canonical[rid]
    assert set(prior) == {"en","it","es","fr","de","pt"}, rid
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
    assert rec["introducedYear"] == evidence["year"] == official["introducedYear"], rid
    assert official["introducedYearSource"] == evidence["source"], ("year source",rid)
    assert rec["firstObservedYear"] == first[rid], rid
    if first[rid] is not None:
        assert first[rid] >= rec["introducedYear"], rid
    assert evidence["source"] in rec["sources"], ("missing original source",rid)
    assert len(rec["sources"]) == len(set(rec["sources"])), rid
    assert len(rec["sourceReviewNote"]) >= 80
    for url in rec["sources"]:
        parsed = urlsplit(url)
        assert parsed.scheme == "https" and parsed.hostname in allowed, (rid,url)
    for lang in ("en","it"):
        current = rec["locale"][lang]
        previous = prior[lang]
        assert previous["origin"] in current["origin"], (rid,lang,"preserved original researched origin")
        assert previous["whyThisDate"] == current["facts"][0], (rid,lang,"date rationale preserved")
        if previous.get("whyItMatters"):
            assert previous["whyItMatters"] in current["purpose"], (rid,lang,"historic significance preserved")
        else:
            assert rid in {"world-refugee-day", "international-day-of-peace", "human-rights-day"}
            assert len(current["purpose"].split()) >= 20, (rid, lang, "new factual significance required")
        if previous.get("summary"):
            assert previous["summary"] in current["origin"], (rid,lang,"original summary preserved")
        else:
            assert rid in {"world-refugee-day", "international-day-of-peace", "human-rights-day"}
            assert len(current["origin"]) >= len(previous["origin"]) + 150, (rid,lang,"new summary required")
        assert all("undefined" not in str(value) and "null " not in str(value)
                   for value in current.values()), (rid,lang,"missing source text leaked into narrative")
        assert len(current["heading"].strip()) >= 20
        assert len(current["origin"].strip()) >= 170
        assert len(current["promoter"].strip()) >= 60
        assert len(current["purpose"].strip()) >= 75
        assert 2 <= len(current["facts"]) <= 5
        assert all(len(f.strip()) >= 45 for f in current["facts"])
print("PASS: 14 original IT/EN institutional origin histories; prior six-locale texts remain candidate drafts")
