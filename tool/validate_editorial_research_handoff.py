#!/usr/bin/env python3
"""Keep the research-writing backlog separate from the editorial signoff backlog."""
from editorial_research_handoff import load_handoff
from editorial_origin_completion_waves import _read_origin, build
from editorial_1111_source_audit_queue import build as build_audit

audit = build_audit()
all_ids = {r["id"] for r in audit["rows"]}
ledger = load_handoff(all_ids)
merged = set(_read_origin())
draft = ledger["six_locale_draft_ids"]
excluded = ledger["out_of_scope_ids"]
blocked = ledger["source_blocked_ids"]
already = ledger["previous_main_wave20_ids"]
assert len(all_ids) == 1111
assert len(merged) == 325, "refresh expected count when new waves merge"
assert drafted_overlap := (merged & draft)
assert drafted_overlap == already and len(drafted_overlap) == 18
assert not (excluded & draft)
assert not (excluded & merged), "excluded canonical IDs have unexpectedly gained source origins"
assert blocked <= all_ids - (merged | draft | excluded)
expected_pending = all_ids - (merged | draft | excluded)
assert len(expected_pending) == 478
assert blocked <= expected_pending and len(blocked) == 7
idx, files = build()
assert idx["outstandingOriginResearch"] == len(expected_pending)
assert idx["researchHandoff"]["unmergedSixLocaleResearchDrafts"] == 173
assert idx["researchHandoff"]["newDraftOriginsNotYetCountedOnMain"] == 155
assert idx["researchHandoff"]["alreadyCountedBilingualOnMain"] == 18
assert idx["researchHandoff"]["scopeExcludedBiographical"] == 153
assert idx["researchHandoff"]["pendingQualifiedHumanReview"] == 173
assert idx["researchHandoff"]["qualifiedHumanCertified"] == 0
assert idx["individuallyOriginResearched"] == 325
assert idx["batchCount"] == 5
assert not any(d["observanceId"] in draft | excluded
               for f in files.values() for d in f["dossiers"])
print("PASS: 1111 catalog; 325 main researched + 155 external new drafts + "
      "153 scope exclusions = 478 pending research; 173 human reviews pending, "
      "7 PH source blocks; zero new editorial certifications")
