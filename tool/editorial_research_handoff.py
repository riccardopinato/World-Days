#!/usr/bin/env python3
"""Source-pinned PH/KR/CA research handoff; never grants editorial certification.

The external PRs contain AI research drafts, not runtime-published or
human-approved content. This registry skips re-authoring the exact canonical
IDs while preserving editorial, locale and source-review work as open.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/editorial/registry/ph_kr_ca_source_research_handoff_20261114.json"
SIX = frozenset(("en", "it", "es", "fr", "de", "pt"))

def load_handoff(catalog_ids=None):
    doc = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert doc["schemaVersion"] == 1
    assert doc["mainBaselineSha"] == "e7c9fa0fbd2e82002d294ffe348f8a57bc1bf5ab"
    assert doc["sourceAuditSha"] == doc["dependencies"]["120"]["sha"]
    assert set(doc["dependencies"]) == {"118", "119", "120"}
    assert all(v["status"] == "DRAFT_UNMERGED" and len(v["sha"]) == 40
               for v in doc["dependencies"].values())
    entries = doc["retainedCandidates"]
    excluded = doc["excludedFromFutureEditorialResearch"]
    assert len(entries) == 180 and len(excluded) == 153
    assert len({r["id"] for r in entries + excluded}) == 333
    counts = Counter()
    drafted = set()
    blocked = set()
    wave20_overlap = set()
    for r in entries:
        assert r["country"] in {"PH", "KR", "CA"}
        assert r["qualifiedHistoricalReview"] is False
        assert r["qualifiedNativeLocaleReview"] is False
        assert r["runtimePublished"] is False
        if r["status"] == "SIX_LOCALE_AI_DRAFT_PENDING_QUALIFIED_REVIEW":
            assert set(r["locales"]) == SIX
            assert r["sourcePr"] in {118, 119, 120}
            assert isinstance(r["sourceFile"], str) and r["sourceFile"].startswith("data/editorial/")
            drafted.add(r["id"])
            if r["mainBilingualWave20"]:
                assert r["sourcePr"] == 118
                wave20_overlap.add(r["id"])
            counts[(r["country"], "drafted")] += 1
        else:
            assert r["status"] == "SOURCE_OR_IDENTITY_BLOCKED"
            assert r["country"] == "PH" and r["locales"] == []
            assert r["sourcePr"] is None and r["sourceFile"] is None
            blocked.add(r["id"])
            counts[(r["country"], "blocked")] += 1
    out_of_scope = set()
    for r in excluded:
        assert r["country"] == "PH"
        assert r["status"] == "OUT_OF_EDITORIAL_SCOPE_BIOGRAPHICAL"
        assert r["reason"] == "BIOGRAPHICAL_BIRTH_DEATH_ANNIVERSARY"
        out_of_scope.add(r["id"])
    assert len(drafted) == 173 and len(blocked) == 7
    assert len(wave20_overlap) == 18 and len(out_of_scope) == 153
    assert counts == {("PH", "drafted"): 84, ("PH", "blocked"): 7,
                      ("KR", "drafted"): 57, ("CA", "drafted"): 32}
    assert doc["summary"]["qualifiedHumanApproved"] == 0
    assert doc["summary"]["richRuntimePublishedFromThisHandoff"] == 0
    if catalog_ids is not None:
        assert drafted | blocked | out_of_scope <= set(catalog_ids), (
            "handoff ID missing from canonical catalog"
        )
    return {
        "six_locale_draft_ids": drafted,
        "source_blocked_ids": blocked,
        "out_of_scope_ids": out_of_scope,
        "previous_main_wave20_ids": wave20_overlap,
        "source_ref": doc["sourceAuditSha"],
    }

if __name__ == "__main__":
    s = load_handoff()
    print("RESEARCH_HANDOFF", json.dumps({
        "draftsSixLocale": len(s["six_locale_draft_ids"]),
        "sourceBlocked": len(s["source_blocked_ids"]),
        "outOfEditorialScope": len(s["out_of_scope_ids"]),
        "alreadyBilingualWave20": len(s["previous_main_wave20_ids"]),
        "humanCertified": 0,
    }, sort_keys=True))
