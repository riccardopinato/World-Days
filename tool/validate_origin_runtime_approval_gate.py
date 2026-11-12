#!/usr/bin/env python3
"""Fail closed: source-researched draft origins are NOT six-locale approved rich editorial."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = json.loads((ROOT / "assets/data/origin_review_index.json").read_text(encoding="utf-8"))
catalog = json.loads((ROOT / "assets/data/official_core.json").read_text(encoding="utf-8"))
registry = json.loads((ROOT / "data/editorial/registry/pending_origin_story_prs_20261112.json").read_text(encoding="utf-8"))
dart = (ROOT / "lib/features/detail/observance_detail_page.dart").read_text(encoding="utf-8")
entries = index["records"]
assert index["recordCount"] == len(entries) == len(catalog["records"])
assert index["reviewedRichOriginCount"] >= 57
assert all(item.get("runtimeRichEditorialApproved") is False for item in entries), "Unapproved origin content reached the rich-publication lane"
assert "entry['runtimeRichEditorialApproved'] != true" in dart, "Origin panel missing approval gate"
assert "snapshot.data?[observanceId]?['runtimeRichEditorialApproved'] == true" in dart, "Missing-history fallback must remain visible for drafts"
batches = registry["batches"]
assert len(batches) == registry["pendingPrCount"] and len(batches) >= 0
assert len({batch["pr"] for batch in batches}) == len(batches)
ids = [oid for batch in batches for oid in batch["observanceIds"]]
assert len(ids) == registry["pendingUniqueDraftCount"]
assert len(ids) == len(set(ids)), "Duplicate pending observance IDs"
canonical = {item["id"] for item in catalog["records"]}
assert set(ids) <= canonical, "Unregistered observance outside canonical catalog"
researched_ids = {entry["observanceId"] for entry in entries if entry["primaryResearch"] is not None}
assert not set(ids) & researched_ids, "A researched origin on main cannot remain marked as an open PR draft"
assert all(batch["storyCount"] == len(batch["observanceIds"]) for batch in batches)
assert all(batch["sourceLinkedDraftLocales"] == ["en", "it"] for batch in batches)
assert all(batch["qualifiedSixLocaleApproval"] is False and batch["runtimeRichEditorialApproved"] is False for batch in batches)
print("ORIGIN_RUNTIME_APPROVAL_GATE PASS", "researched", index["reviewedRichOriginCount"], "pending_pr_stories", len(ids), "runtime_approved", 0)
