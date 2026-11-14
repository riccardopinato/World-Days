#!/usr/bin/env python3
"""Regression: source-linked queue handles a partial last batch and completion."""
from unittest.mock import patch
import editorial_origin_wave100 as first
import editorial_origin_completion_waves as full

def fake_audit(n):
    rows = []
    for i in range(1111):
        unfinished = i < n
        rows.append({
            "id": f"simulated-day-{i:04d}",
            "canonicalTitleEn": f"Simulated Day {i:04d}",
            "scope": "GLOBAL",
            "countries": [],
            "periodKind": "FIXED",
            "introducedYear": None,
            "recordAuthority": "Simulated test institution",
            "sourceUrls": ["https://example.org/fixture/" + str(i)],
            "sourceTiers": ["A_PRIMARY"],
            "sourceQualityGate": "CANONICAL_LINK_PRESENT_INDIVIDUAL_STORY_STILL_TO_REVIEW",
            "storyPublished": not unfinished,
            "researchDraft": None,
            "editorialStage": "NOT_RESEARCHED" if unfinished else "RUNTIME_REVIEWED",
            "missingEditorialEvidence": ["ORIGIN_HISTORY"],
        })
    return {
        "rows": rows,
        "catalogTotal": len(rows),
        "catalogVersion": "test-only",
        "publishedEnglishRichStories": 1111 - n,
    }

for n in (99, 7, 0):
    audit = fake_audit(n)
    approved = [r["id"] for r in audit["rows"] if r["storyPublished"]]
    empty_handoff = {"six_locale_draft_ids": set(), "out_of_scope_ids": set(), "previous_main_wave20_ids": set(), "source_ref": "fixture"}
    with patch.object(first, "load_handoff", return_value=empty_handoff), \
         patch.object(full, "load_handoff", return_value=empty_handoff), \
         patch.object(first, "build_audit", return_value=audit), \
         patch.object(full, "build_audit", return_value=audit), \
         patch.object(full, "_read_origin", return_value=approved):
        first_wave = first.build()
        assert first_wave["recordCount"] == n
        assert first_wave["targetCount"] == n
        assert len(set(d["observanceId"] for d in first_wave["dossiers"])) == n
        index, files = full.build()
        assert index["outstandingOriginResearch"] == n
        assert index["individuallyOriginResearched"] == 1111 - n
        assert index["batchSizes"] == ([n] if n else [])
        assert sum(p["recordCount"] for p in files.values()) == n
        assert len(files) == (1 if n else 0)
print("PASS: 99-item, 7-item and zero-item final research queues work without fabrication")
