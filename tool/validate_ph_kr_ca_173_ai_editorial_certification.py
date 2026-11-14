#!/usr/bin/env python3
"""Validate evidence-scoped AI editorial certification without human impersonation.

AI_CERTIFIED is an editorial research certificate, not runtime publication.
Source/version changes invalidate prior per-source certification. Unreviewed
and disputed entries must remain unapproved.
"""
import json
import hashlib
import os
import sys
from urllib.request import Request, urlopen
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
queue_bytes = QUEUE.read_bytes()
queue_git_blob_sha = hashlib.sha1(
    b"blob " + str(len(queue_bytes)).encode("ascii") + b"\0" + queue_bytes
).hexdigest()
assert d["sourceReviewQueueBlobSha"] == queue_git_blob_sha, (
    "historical queue changed: re-run AI review before accepting a certificate"
)
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
assert d["reviewBatchHistory"][0]["count"] == 10
assert len(d["reviewBatchHistory"][0]["ids"]) == 10
assert len(d["reviewBatchHistory"]) == 2
assert d["reviewBatchHistory"][1]["count"] == 7
assert len(d["reviewBatchHistory"]) == 3
assert d["reviewBatchHistory"][2]["count"] == 10
assert len(d["reviewBatchHistory"][1]["ids"]) == 7
expected = {
    "ca-ribbon-skirt-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2022, 2023),
    "kr-march-first-independence-movement-day": ("KR", "135f652773ca0f8d0b0d96dcd4fb64fac0e3165e", 1949, 1920),
    "ph-ninoy-aquino-day": ("PH", "dce081d073bad6dea6d471b5aa72224588802ea1", 2004, None),
    "ph-independence-day": ("PH", "135f652773ca0f8d0b0d96dcd4fb64fac0e3165e", 1964, None),
    "ca-air-disaster-victims-remembrance": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2020, 2021),
    "ca-terrorism-victims-remembrance": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", 2005, 2005),
    "ca-national-seniors-day": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", 2010, 2011),
    "ca-national-child-day": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 1993, None),
    "ca-emancipation-day": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", 2021, None),
    "ca-remembrance-day": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 1931, 1919),
    "ca-violence-against-women-remembrance": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 1991, None),
    "canada-national-indigenous-peoples-day": ("CA", "863db0e6c7ff952ca060d5e8c6c2f0cae2c54494", 1996, None),
    "canada-national-acadian-day": ("CA", "863db0e6c7ff952ca060d5e8c6c2f0cae2c54494", 2003, 1881),
    "ca-persons-day": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", 1979, 1979),
    "ca-lincoln-alexander-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2014, 2015),
    "ca-red-dress-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", None, 2010),
    "ca-dutch-heritage-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2019, None),
    "ca-saint-jean-baptiste-day": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", None, None),
    "ca-great-upheaval-commemoration": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", None, None),
    "ca-indigenous-veterans-day": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 1994, 1994),
    "ca-sir-john-a-macdonald-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2002, None),
    "canada-national-flag-day": ("CA", "951808461a115c768de29fa9c4696f28cf8b40b3", 1996, 1996),
    "canada-truth-and-reconciliation-day": ("CA", "951808461a115c768de29fa9c4696f28cf8b40b3", 2021, 2021),
    "canada-multiculturalism-day": ("CA", "951808461a115c768de29fa9c4696f28cf8b40b3", 2002, None),
    "ca-canada-day": ("CA", "951808461a115c768de29fa9c4696f28cf8b40b3", 1879, 1868),
    "ca-vimy-ridge-battle-anniversary": ("CA", "951808461a115c768de29fa9c4696f28cf8b40b3", 2003, 2003),
    "ca-armenian-genocide-remembrance": ("CA", "951808461a115c768de29fa9c4696f28cf8b40b3", 2015, None),
    "ca-british-home-child-day": ("CA", "951808461a115c768de29fa9c4696f28cf8b40b3", 2018, None),
    "ca-armed-forces-day": ("CA", "951808461a115c768de29fa9c4696f28cf8b40b3", 2002, 2002),
    "ca-covid-19-national-observance": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2021, 2021),
    "ca-holodomor-memorial-day": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 2008, None),
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
assert count == {"AI_CERTIFIED":31,"HOLD_SOURCE_DISPUTE":8,"AI_REVIEW_QUEUED":134}
for name,num in count.items():
    assert d["summary"][name] == num
philippines = rows["ph-independence-day"]
assert philippines["firstObservedYear"] is None
assert any("84843" in url for url in philippines["sourceEvidence"])
assert philippines["sourceHead"] == "521a59452178b7e2f0b074e5057e964af8515feb"
# Exact live source-version gate: a once-correct AI certificate is never valid
# after an unreviewed PR head or source blob update.  Uses the GitHub API on CI;
# local static validation remains available without performing network requests.
if "--verify-remote" in sys.argv:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise AssertionError("--verify-remote requires GITHUB_TOKEN")
    base = "https://api.github.com/repos/riccardopinato/World-Days"
    def api(path):
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "World-Days-AI-Editorial-Source-Gate/1",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        req = Request(base + path, headers=headers)
        with urlopen(req, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))

    # Only fetch reviewed source PRs; all other drafts are intentionally queued.
    certified = [x for x in rows.values() if x["status"] == "AI_CERTIFIED"]
    heads = {}
    blob_cache = {}
    for row in certified:
        pr = row["sourcePR"]
        if pr not in heads:
            obj = api("/pulls/" + str(pr))
            assert obj["state"] == "open" and not obj["merged"], ("source PR closed/merged", pr)
            heads[pr] = obj["head"]["sha"]
        assert heads[pr] == row["sourceHead"], (
            "source PR changed after AI review; invalidate and recertify", pr,
            row["sourceHead"], heads[pr])
        key = (pr, row["sourceFile"])
        if key not in blob_cache:
            import urllib.parse
            encoded = "/".join(urllib.parse.quote(p, safe="") for p in row["sourceFile"].split("/"))
            obj = api("/contents/" + encoded + "?ref=" + heads[pr])
            assert obj.get("type") == "file"
            blob_cache[key] = obj["sha"]
        assert blob_cache[key] == row["sourceBlobSha"], (
            "source file blob changed after review", row["observanceId"])
    print("PASS: live GitHub PR head and source blob verification for",
          len(certified), "AI-certified stories across", len(heads), "source PRs")

print("PASS: 173 AI-research editorial decisions: 31 AI_CERTIFIED, 8 source-HOLD, "
      "134 awaiting AI review, 0 human signoffs, 0 runtime publications")
