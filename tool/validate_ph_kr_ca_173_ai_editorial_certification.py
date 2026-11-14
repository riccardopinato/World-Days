#!/usr/bin/env python3
"""Validate evidence-scoped AI editorial certification without human impersonation.

AI_CERTIFIED is an editorial research certificate, not runtime publication.
Source/version changes invalidate prior per-source certification. Unreviewed
and disputed entries must remain unapproved.
"""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from editorial_research_handoff import load_handoff

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/editorial/reviews/ph_kr_ca_173_qualified_review_queue_20261114.json"
LEDGER = ROOT / "data/editorial/reviews/ph_kr_ca_173_ai_editorial_certification_20261114.json"
q = json.loads(QUEUE.read_text(encoding="utf-8"))
d = json.loads(LEDGER.read_text(encoding="utf-8"))
handoff = load_handoff()
assert d["schemaVersion"] == 1 and d["asOf"] == "2026-11-14"
assert d["reviewerIdentity"] == "GPT-6_AI_EDITORIAL_REVIEW"
assert d["reviewAuthority"] == "USER_DELEGATED_AI_EDITORIAL_REVIEW_2026-11-14"
assert len(d["sourceReviewQueueBlobSha"]) == 40
assert d["summary"]["qualifiedHumanSignoffs"] == 0
assert d["summary"]["appRuntimePublishedByThisLedger"] == 0
src = {r["id"]: r for r in q["records"]}
rows = {r["observanceId"]: r for r in d["records"]}
assert len(rows) == len(src) == 173
assert set(rows) == set(src) == handoff["six_locale_draft_ids"]
assert Counter(x["country"] for x in rows.values()) == {"PH":84,"KR":57,"CA":32}
assert d["summary"]["byCountry"] == {"PH":84,"KR":57,"CA":32}
expected = {
    "ca-ribbon-skirt-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2022, 2023),
    "kr-march-first-independence-movement-day": ("KR", "135f652773ca0f8d0b0d96dcd4fb64fac0e3165e", 1949, 1920),
    "ph-ninoy-aquino-day": ("PH", "dce081d073bad6dea6d471b5aa72224588802ea1", 2004, None),
    "ph-independence-day": ("PH", "135f652773ca0f8d0b0d96dcd4fb64fac0e3165e", 1964, None),
}
count = Counter()
for rid, row in rows.items():
    original = src[rid]
    assert row["country"] == original["country"]
    assert row["sourcePR"] == original["sourcePr"]
    assert row["sourceFile"] == original["sourceFile"]
    assert len(row["sourceHead"]) == 40
    assert set(row["locales"]) == {"en","it","es","fr","de","pt"}
    count[row["status"]] += 1
    if rid in expected:
        code, blob, established, first = expected[rid]
        assert row["status"] == "AI_CERTIFIED"
        assert row["country"] == code
        assert row["sourceBlobSha"] == blob
        assert row["establishedYear"] == established
        assert row["firstObservedYear"] == first
        assert row["reviewedBy"] == "GPT-6" and row["reviewDate"] == "2026-11-14"
        assert row["reviewMethod"] == "MODEL_EDITORIAL_FACT_AND_TRANSLATION_CHECK"
        assert set(row["locales"].values()) == {"AI_CHECKED"}
        assert all(row["checks"].values())
        assert len(row["sourceEvidence"]) >= 2
        assert all(urlsplit(u).scheme == "https" and urlsplit(u).hostname
                   for u in row["sourceEvidence"])
        assert len(row["factsConfirmed"]) >= 3
        assert len(row["notes"]) >= 70
        assert row["sourceConflict"] is None, rid
    else:
        assert row["status"] == ("HOLD_SOURCE_DISPUTE" if original["unresolvedSourceRisk"]
                                 else "AI_REVIEW_QUEUED")
        assert row["reviewedBy"] is None and row["reviewDate"] is None
        assert row["checks"] is None
        assert row["sourceBlobSha"] is None
        assert set(row["locales"].values()) == {"NOT_CHECKED"}
assert count == {"AI_CERTIFIED":4,"HOLD_SOURCE_DISPUTE":8,"AI_REVIEW_QUEUED":161}
for name,num in count.items():
    assert d["summary"][name] == num
philippines = rows["ph-independence-day"]
assert philippines["firstObservedYear"] is None
assert any("84843" in url for url in philippines["sourceEvidence"])
assert philippines["sourceHead"] == "521a59452178b7e2f0b074e5057e964af8515feb"
print("PASS: 173 AI-research editorial decisions: 4 AI_CERTIFIED, 8 source-HOLD, "
      "161 awaiting AI review, 0 human signoffs, 0 runtime publications")
