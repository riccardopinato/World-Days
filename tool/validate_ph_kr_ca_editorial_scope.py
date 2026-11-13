#!/usr/bin/env python3
"""Scope gate for three-country editorial research; NOT human certification."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "data/editorial/audits"
inventory = json.loads((AUDIT / "ph_kr_ca_333_certification_inventory_20261113.json").read_text(encoding="utf-8"))
scope = json.loads((AUDIT / "ph_kr_ca_333_editorial_scope_decisions_20261113.json").read_text(encoding="utf-8"))
source = inventory["records"]
decisions = scope["decisions"]
assert scope["schemaVersion"] == 1
assert inventory["inventoryTotal"] == 333
assert len(source) == len(decisions) == 333
assert len({r["id"] for r in source}) == 333
assert len({d["id"] for d in decisions}) == 333
expected = {r["id"]: r for r in source}
assert set(expected) == {d["id"] for d in decisions}

counts = Counter()
for item in decisions:
    base = expected[item["id"]]
    assert item["country"] == base["country"]
    assert item["title"] == base["title"]
    assert item["sourceFile"] == base["sourceFile"]
    assert item["editorialCertification"] == "NOT_CERTIFIED"
    assert item["verifiedHumanSixLocales"] is False
    assert item["decision"] in {
        "EXCLUDE_FROM_EDITORIAL_AND_FUTURE_PUBLIC_CATALOG",
        "RETAIN_AS_UNCERTIFIED_CANDIDATE",
    }
    is_bio = (
        base["country"] == "PH"
        and (
            base["id"].startswith("ph-w11-")
            or (
                base["id"].startswith("ph-w10-")
                and any(term in base["title"].lower().split() for term in ("birth", "death"))
            )
        )
    )
    is_excluded = item["decision"].startswith("EXCLUDE")
    assert is_bio == is_excluded, base["id"]
    if is_excluded:
        assert item["reason"] == "BIOGRAPHICAL_BIRTH_DEATH_ANNIVERSARY"
    counts[item["country"], "excluded" if is_excluded else "remaining"] += 1

assert counts == {
    ("PH", "excluded"): 153,
    ("PH", "remaining"): 91,
    ("KR", "remaining"): 57,
    ("CA", "remaining"): 32,
}, counts
assert scope["counts"]["total"] == 333
assert scope["counts"]["excluded"] == 153
assert scope["counts"]["remaining"] == 180
print("PASS: PH 153 excluded + 91 retained; KR 57 retained; CA 32 retained; no human certification claimed")
