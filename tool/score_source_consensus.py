#!/usr/bin/env python3
"""Batch source-consensus certification for precise *2026 dates*, NOT event identity.

Key distinction: five mirrors of one decree count as one source-origin, while a
single directly inspected originator calendar can establish its own 2026 date.
The engine must NEVER grant annual recurrence, officiality, semantics, or
translation/publishing approval merely from matching website claims.
"""
from collections import Counter, defaultdict
from datetime import date
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = ROOT / "data/research/source_consensus_attestations_20261109.json"
DEFAULT_CATALOG_EVIDENCE = ROOT / "data/research/primary_2026_calendar_verified_20261109.json"
DEFAULT_OUT = ROOT / "reports/research_date_consensus_2026.json"
TRUSTED = {"PRIMARY_GOVERNMENT", "PRIMARY_ORIGINATOR"}
INDEPENDENT = {"REPUTABLE_INDEPENDENT"}
ALL_CLASSES = TRUSTED | INDEPENDENT | {"SECONDARY_AGGREGATOR"}

def assess(row: dict) -> dict:
    claimed = row["occurrence2026"]
    assert date.fromisoformat(claimed).year == 2026
    assert row["title"].strip() and row["country"].strip() and row["researchFile"].strip()
    raw = row["attestations"]
    assert isinstance(raw, list) and raw, "At least one inspectable citation is required"
    url_seen, grouped, conflicts = set(), defaultdict(list), []
    for att in raw:
        assert set(("url","publisher","documentOrigin","authorityClass","reportedDate","displayedEvent","checkedOn")) <= set(att)
        url = att["url"]
        parts = urlsplit(url)
        assert parts.scheme == "https" and parts.netloc and not parts.username
        assert url not in url_seen, "duplicate URL"
        url_seen.add(url)
        assert att["publisher"].strip() and att["documentOrigin"].strip()
        assert att["displayedEvent"].strip(), "URL alone is not a checked occurrence"
        assert len(att["displayedEvent"].strip()) >= 5
        assert att["authorityClass"] in ALL_CLASSES
        assert date.fromisoformat(att["checkedOn"]).year >= 2026
        assert date.fromisoformat(att["reportedDate"]).year == 2026
        grouped[att["documentOrigin"]].append(att)
        if att["reportedDate"] != claimed:
            conflicts.append({
                "documentOrigin":att["documentOrigin"],
                "reportedDate":att["reportedDate"],
                "publisher":att["publisher"],
                "url":url,
            })
    # Same document origin can be distributed by 1, 2, or 50 different sites.
    origin_classes = {
        origin: {a["authorityClass"] for a in entries}
        for origin,entries in grouped.items()
    }
    primary_origins = sum(bool(classes & TRUSTED) for classes in origin_classes.values())
    reputable_origins = sum(bool(classes & INDEPENDENT) for classes in origin_classes.values())
    if conflicts:
        status = "CONFLICT_NEEDS_REVIEW"
    elif primary_origins:
        status = "DATE_2026_CONFIRMED_BY_ORIGINATOR"
    elif reputable_origins >= 3:
        status = "DATE_2026_SECONDARY_CONSENSUS_REVIEW"
    else:
        status = "DATE_2026_INSUFFICIENT_PRIMARY_EVIDENCE"
    return {
        "researchFile":row["researchFile"],
        "title":row["title"],
        "country":row["country"],
        "date2026":claimed,
        "status":status,
        "rawWebPages":len(raw),
        "independentDocumentOrigins":len(grouped),
        "primaryOrigins":primary_origins,
        "reputableIndependentOrigins":reputable_origins,
        "conflicts":conflicts,
        "originGroups":[{"origin":name,"publishers":sorted({x["publisher"] for x in rows}),"evidenceURLs":[x["url"] for x in rows]} for name,rows in sorted(grouped.items())],
        "identityUniqueCertified":False,
        "annualRecurrenceCertified":False,
        "translatedEditorialCertified":False,
        "runtimeAdmission":"RESEARCH_ONLY",
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,default=DEFAULT_EVIDENCE)
    parser.add_argument("--official-register",type=Path,default=DEFAULT_CATALOG_EVIDENCE)
    parser.add_argument("--output",type=Path,default=DEFAULT_OUT)
    args=parser.parse_args()
    payload=json.loads(args.input.read_text(encoding="utf-8"))
    assert payload["schemaVersion"]==1
    assert payload["recordCount"]==len(payload["records"])
    catalog=json.loads(args.official_register.read_text(encoding="utf-8"))
    known={(r["researchFile"],r["title"],r["country"]):r for r in catalog["records"]}
    assert len(known)==len(catalog["records"])
    report=[]; seen=set()
    for row in payload["records"]:
        k=(row["researchFile"],row["title"],row["country"])
        assert k not in seen and k in known, k
        seen.add(k)
        assert row["occurrence2026"]==known[k]["occurrence2026"],k
        # The official register is the comparison corpus, not an extra website.
        result=assess(row)
        report.append(result)
    counts=Counter(x["status"] for x in report)
    output={
        "schemaVersion":1,
        "scope":"2026_DATE_ONLY",
        "recordCount":len(report),
        "statusCounts":dict(sorted(counts.items())),
        "disclaimer":"Even 5 websites with identical dates do not certify independent origination or recurring identity. Government decree mirrors are one origin. A primary source establishes its own 2026 date only. No automatic runtime promotion.",
        "records":report,
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("DATE CONSENSUS PASS "+json.dumps({"recordCount":len(report),"statusCounts":output["statusCounts"],"originDedupExample":{r["title"]:{"urls":r["rawWebPages"],"origins":r["independentDocumentOrigins"]} for r in report[:2]}},sort_keys=True))

if __name__=="__main__":
    main()
