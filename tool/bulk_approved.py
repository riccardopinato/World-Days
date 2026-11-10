#!/usr/bin/env python3
"""Deterministic loader for explicit, source+editorial-approved bulk catalog files.

Empty by default. Both GLOBAL and NATIONAL admitted records use the same
generator so future 30–50-record batches need no per-wave Python edits.
"""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
FOLDER=ROOT/"data/market/bulk_approved"
LOCALES={"en","it","es","fr","de","pt"}
PRIMARY={"PRIMARY_ORIGINATOR","OFFICIAL_GOVERNMENT"}

def approved_rows():
    records=[]
    known_ids=set()
    for path in sorted(FOLDER.glob("*.json")):
        data=json.loads(path.read_text(encoding="utf-8"))
        assert data["schemaVersion"]==1
        assert data["admissionStatus"]=="HUMAN_EDITORIAL_APPROVED_AND_SOURCE_VERIFIED"
        assert data["count"]==len(data["records"])>0
        for r in data["records"]:
            rid=r["id"]
            assert rid not in known_ids,("duplicate approved batch ID",rid)
            known_ids.add(rid)
            assert r["scope"] in ("GLOBAL","NATIONAL")
            assert r.get("country") if r["scope"]=="NATIONAL" else r.get("country") in (None,"")
            assert set(r["localizedTitles"])==LOCALES
            assert r["localizedTitles"]["en"]==r["canonicalTitleEn"]
            assert r["identityReviewed"] is True
            assert r["editorialApproval"]["status"]=="QUALIFIED_APPROVED"
            assert r["editorialApproval"]["reviewer"] and r["editorialApproval"]["evidenceUrl"].startswith("https://")
            assert r["annualRuleEvidenceUrl"].startswith("https://")
            assert r["identityEvidenceUrl"].startswith("https://")
            assert len(r["recurrenceRules"])==1
            assert r["attestations"]
            assert any(a["sourceClass"] in PRIMARY for a in r["attestations"])
            authority=r["authority"]
            assert authority["name"] and authority["type"]
            assert authority["officiality"] in {"OFFICIAL_UN","OFFICIAL_UNESCO","OFFICIAL_UN_AGENCY","OFFICIAL_WHO","OFFICIAL_INSTITUTIONAL","RECOGNIZED_INSTITUTIONAL"}
            urls=set()
            sources=[]
            for a in r["attestations"]:
                url=a["url"]
                if url in urls:continue
                urls.add(url)
                sources.append({"tier":"A_PRIMARY" if a["sourceClass"] in PRIMARY else "D_ORIGINATOR",
                     "url":url,"verifiedAt":r["sourceReviewedOn"]})
            for url in (r["annualRuleEvidenceUrl"],r["identityEvidenceUrl"]):
                if url not in urls:
                    urls.add(url)
                    sources.append({"tier":"A_PRIMARY","url":url,"verifiedAt":r["sourceReviewedOn"]})
            rec={
                "id":rid,"canonicalTitleEn":r["canonicalTitleEn"],
                "aliases":r.get("aliases",[]),"periodKind":"DAY",
                "recurrenceRules":r["recurrenceRules"],
                "scope":r["scope"],"countries":[r["country"]] if r["scope"]=="NATIONAL" else [],
                "regions":[],"authority":{"name":authority["name"],"type":authority["type"],
                  "officiality":authority["officiality"],"resolution":authority.get("resolution")},
                "categories":r.get("categories",["CULTURE"]),
                "sources":sources,"visualKey":r.get("visualKey","community"),
                "editorialStatus":"STUB",
                "notes":["Institutional metadata: identity and six display titles independently approved.",
                         "Long-form history is not automatically marked REVIEWED."],
                "lastVerifiedAt":r["sourceReviewedOn"],
                "localizedTitles":r["localizedTitles"],
            }
            if r.get("introducedYear") is not None:
                assert r.get("introducedYearSource","").startswith("https://")
                rec["introducedYear"]=r["introducedYear"]
                rec["introducedYearSource"]=r["introducedYearSource"]
                assert r["introducedYearSource"] in urls,"introduction year source must be in canonical sources"
            records.append(rec)
    return records

def approved_titles():
    rows=approved_rows()
    return {locale:{r["canonicalTitleEn"]:r["localizedTitles"][locale] for r in rows}
            for locale in ("en","it","es","fr","de","pt")}
