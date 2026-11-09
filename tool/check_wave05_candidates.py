#!/usr/bin/env python3
"""Wave05 research gate: AST-safe title/ID collision screening.

Research-only: a PASS does not certify candidate admission or source validity.
No generated assets, Flutter runtime, APK or Play workflow is modified.
"""
import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data/research/wave05_four_official_candidates_20261109.json"
BUILD = ROOT / "tool/build_dataset.py"
MARKET = ROOT / "data/market"
CALLS = {
    "fixed", "rng", "nth", "lastwd", "multi_nth",
    "override", "consumer_fixed", "consumer_nth", "add",
}

def normalize(value):
    return re.sub(r"[^a-z0-9]+", " ", value.lower().replace("’", "'")).strip()

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("’", "'")).strip("-")

def global_titles():
    tree = ast.parse(BUILD.read_text(encoding="utf-8"), filename=str(BUILD))
    titles = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id not in CALLS or not node.args:
            continue
        arg = node.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            titles.append(arg.value)
    return titles

def nested_market_titles():
    titles = []
    for path in sorted(MARKET.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        def walk(value):
            if isinstance(value, dict):
                if isinstance(value.get("canonicalTitleEn"), str):
                    titles.append(value["canonicalTitleEn"])
                for sub in value.values():
                    walk(sub)
            elif isinstance(value, list):
                for sub in value:
                    walk(sub)
        walk(payload)
    return titles

def main():
    payload = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    assert payload["candidateOnly"] is True
    assert payload["recordCount"] == len(payload["records"])
    existing = global_titles() + nested_market_titles()
    normalized = {normalize(title) for title in existing}
    slugs = {slug(title) for title in existing}
    ids = set()
    for candidate in payload["records"]:
        title = candidate["canonicalTitleEn"]
        ident = candidate["id"]
        assert ident not in ids, ("candidate duplicate ID", ident)
        ids.add(ident)
        assert ident == slug(title), ("ID mismatch", ident, title)
        assert normalize(title) not in normalized, ("already existing title", title)
        assert ident not in slugs, ("already existing slug", ident)
        assert set(candidate["localizedTitles"]) == {"en","it","es","fr","de","pt"}
        assert candidate["localizedTitles"]["en"] == title
        assert all(candidate["localizedTitles"].values())
        assert candidate["runtimeAdmission"].startswith("BLOCKED")
    print(
        f"RESEARCH SCREEN PASS: {len(payload['records'])} nonmatching candidate titles "
        f"against {len(existing)} source titles. NOT a full 456-ID semantic audit, "
        "NOT runtime-admitted, NOT CI-certified."
    )

if __name__ == "__main__":
    main()
