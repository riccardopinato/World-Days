#!/usr/bin/env python3
"""Rank pending *national* story authoring by canonical country with PR handoff exclusions.

Uses generated 1111+ canonical IDs and main source origins. Unmerged six-locale
research is excluded from NEW authoring only, not counted as human certified.
Global observances have no single owner country and are not assigned here.
"""
import json
from collections import defaultdict
from pathlib import Path
from editorial_1111_source_audit_queue import build as build_audit
from editorial_origin_completion_waves import _read_origin
from editorial_research_handoff import load_handoff

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports/country_authoring_backlog_20261114.json"

def build():
    audit = build_audit()
    rows = audit["rows"]
    ids = {r["id"] for r in rows}
    assert len(ids) == audit["catalogTotal"] >= 1111
    main = set(_read_origin())
    handoff = load_handoff(ids)
    draft = handoff["six_locale_draft_ids"]
    excluded = handoff["out_of_scope_ids"]
    assert handoff["previous_main_wave20_ids"] <= main & draft
    groups = defaultdict(lambda: {"total": 0, "mainResearched": 0,
        "preparedUnmergedDraft": 0, "outOfScope": 0, "pendingNewResearch": 0,
        "pendingIds": []})
    global_count = 0
    for r in rows:
        if r["scope"] == "GLOBAL":
            assert not r["countries"]
            global_count += 1
            continue
        assert r["scope"] == "NATIONAL" and len(r["countries"]) == 1, r["id"]
        country = r["countries"][0]
        g = groups[country]
        g["total"] += 1
        rid = r["id"]
        if rid in excluded:
            g["outOfScope"] += 1
        elif rid in main:
            g["mainResearched"] += 1
        elif rid in draft:
            g["preparedUnmergedDraft"] += 1
        else:
            g["pendingNewResearch"] += 1
            g["pendingIds"].append({
                "id": rid, "title": r["canonicalTitleEn"],
                "sourceLeads": r["sourceUrls"],
                "sourceQualityGate": r["sourceQualityGate"],
                "recurrence": r["periodKind"],
            })
    ranking = sorted(
        ({"country": code, **g} for code,g in groups.items()),
        key=lambda g: (-g["pendingNewResearch"], g["country"]),
    )
    assert sum(g["total"] for g in ranking) + global_count == len(rows)
    assert sum(g["pendingNewResearch"] for g in ranking) <= (
        len(ids) - len(main | draft | excluded))
    return {
        "schemaVersion": 1, "asOf": "2026-11-14",
        "mainResearched": len(main), "externalSixLocaleAIDraft": len(draft),
        "historicalWave20Overlap": len(main & draft),
        "outOfEditorialScope": len(excluded),
        "globalNoCountryCount": global_count,
        "catalogTotal": len(rows),
        "interpretation": "Per-country pending NEW source research, NOT final human editorial certification.",
        "ranking": ranking,
    }

if __name__ == "__main__":
    result = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("COUNTRY_BACKLOG_TOP10", json.dumps([
        {"country": r["country"], "pending": r["pendingNewResearch"],
         "main": r["mainResearched"],"draft": r["preparedUnmergedDraft"],
         "outOfScope": r["outOfScope"],"total":r["total"],
         "firstIds":[d["id"] for d in r["pendingIds"][:10]]}
        for r in result["ranking"][:10]],ensure_ascii=False))
    print("COUNTRY_BACKLOG_TOTALS", json.dumps({
        "countryCount": len(result["ranking"]),
        "nationalPending": sum(r["pendingNewResearch"] for r in result["ranking"]),
        "globalRecords": result["globalNoCountryCount"],
        "catalog": result["catalogTotal"],
    }))
