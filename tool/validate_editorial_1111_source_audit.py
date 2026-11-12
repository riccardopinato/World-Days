#!/usr/bin/env python3
"""Validate an exact-ID, honest editorial queue, without granting review status."""
from pathlib import Path
import json
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
f=ROOT/"reports/editorial_1111_source_audit_queue.json"
raw=json.loads(f.read_text(encoding="utf-8"))
rows=raw["rows"]
assert raw["schemaVersion"]==1
assert raw["catalogTotal"]==len(rows)>=1111
assert len(set(r["id"] for r in rows))==len(rows)
assert sum(r["storyPublished"] for r in rows)==raw["publishedEnglishRichStories"]>=56
assert sum(r["researchDraft"] is not None for r in rows)==raw["irishPrimarySourcedDraftStories"]
assert sum(raw["priorityCounts"].values())==len(rows)
assert sum(raw["stageCounts"].values())==len(rows)
assert all(r["sourceUrls"] and all(s.startswith("https://") for s in r["sourceUrls"]) for r in rows)
assert all(r["sourceQualityGate"] for r in rows)
assert all(r["missingEditorialEvidence"] for r in rows), "founder always needs independent evidence"
assert all(r["researchDraft"] is None or
           r["researchDraft"]["status"]=="NOT_PUBLISHED_NOT_REVIEWED"
           for r in rows)
assert all(r["storyPublished"] == (r["editorialStage"]=="RUNTIME_REVIEWED") for r in rows)
assert all(r["introducedYear"] is None or
           isinstance(r["introducedYear"],int)
           for r in rows)
assert set(raw["firstResearchQueue"]).issubset({r["id"] for r in rows if not r["storyPublished"]})
assert len(raw["firstResearchQueue"])<=50
assert not any(r.get("approvedEnglishContent",{}).get("historicalProposer") for r in rows), "never infer a proposer from authority"
k={r["id"]:r for r in rows}
assert k["ie-st-brigids-day"]["researchDraft"] is not None or k["ie-st-brigids-day"]["storyPublished"]
assert k["ie-w13-eures-st-brigid-s-day"]["introducedYear"]==2023
print("PASS: indexed all",len(rows),"canonical days; reviewed=",raw["publishedEnglishRichStories"],"Irish primary-source drafts=",raw["irishPrimarySourcedDraftStories"],"no fabricated founder/history claims")
