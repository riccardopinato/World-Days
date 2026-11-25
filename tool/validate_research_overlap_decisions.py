#!/usr/bin/env python3
"""Validate 20 explicit research decisions against the GENERATED catalog/2026 index.

Only duplicate research classification. Does not authorize content admission.
Run after build_dataset.py and audit_research_candidates.py.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "reports/research_semantic_audit.json"
DECISIONS = ROOT / "data/research/semantic_overlap_decisions_20261109.json"
CATALOG = ROOT / "assets/data/official_core.json"
OCCURRENCES = ROOT / "assets/data/occurrences_2026.json"

def main():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    payload = json.loads(DECISIONS.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["records"]
    occurrence_list = json.loads(OCCURRENCES.read_text(encoding="utf-8"))["occurrences"]
    assert audit["catalogCount"] == len(catalog) == payload["catalogBaseCount"] == 456
    by_id = {r["id"]: r for r in catalog}
    dates = {}
    for item in occurrence_list:
        dates.setdefault(item["observanceId"], set()).add(item["startDate"])
    flagged = {
        (r["researchFile"], r["title"]): r
        for r in audit["candidateResults"]
        if r["status"] != "NO_AUTOMATED_CATALOG_MATCH"
    }
    decisions = payload["reviewDecisions"]
    assert len(decisions) == 20, ("expected 20 flagged candidate decisions", len(decisions))
    selected = set()
    counts = {"SAME_EXISTING_OBSERVANCE": 0, "DIFFERENT_FROM_FLAGGED_MATCH": 0}
    for d in decisions:
        key = (d["candidateFile"], d["candidateTitle"])
        assert key in flagged and key not in selected, ("missing or repeated candidate", key)
        selected.add(key)
        candidate = flagged[key]
        existing_id = d["existingId"]
        assert existing_id in by_id, existing_id
        known_matches = {m["id"] for m in candidate["directMatches"] + candidate["possibleMatches"]}
        assert existing_id in known_matches, (key, existing_id)
        existing = by_id[existing_id]
        candidate_date = candidate["occurrence2026"]
        existing_dates = dates.get(existing_id, set())
        assert candidate_date, ("candidate must provide 2026 date", key)
        assert existing_dates, ("existing record needs 2026 date", existing_id)
        assert d["decision"] in counts, d["decision"]
        assert len(d.get("reason", "")) >= 40, key
        if d["decision"] == "SAME_EXISTING_OBSERVANCE":
            assert candidate["country"] in existing["countries"], (
                "must match the same national jurisdiction", key, existing_id
            )
            assert candidate_date in existing_dates, (
                "existing record does not have the same commemoration date", key,
                candidate_date, sorted(existing_dates)
            )
        else:
            assert candidate_date not in existing_dates, (
                "claimed different despite same-date evidence", key, existing_id
            )
        counts[d["decision"]] += 1
    assert set(flagged) == selected, ("unreviewed flags", sorted(set(flagged) - selected))
    assert counts == {
        "SAME_EXISTING_OBSERVANCE": 17,
        "DIFFERENT_FROM_FLAGGED_MATCH": 3,
    }, counts
    print(
        "RESEARCH OVERLAP REVIEW PASS: 17 previously catalogued national "
        "events identified, 3 unrelated flagged matches cleared. "
        "Remaining 136 records still require primary-source, aliases and "
        "editorial semantic review; zero runtime admissions."
    )

if __name__ == "__main__":
    main()
