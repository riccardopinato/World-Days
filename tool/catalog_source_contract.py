#!/usr/bin/env python3
"""Independent source-defined counts instead of per-wave magic number edits.

The 456-ID main baseline is pinned; subsequent additions are counted from
individual source files and the (optional) explicitly approved bulk directory.
New source batches only require adding a source declaration, not changing each
Python and Flutter test's integer expectations.
"""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"data/catalog_source_contract.json"
def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))
def dataset_version():
    d=read(MANIFEST)
    base=d["datasetVersionBase"]
    parts=base.split(".")
    assert len(parts)==4 and all(p.isdigit() for p in parts)
    approved=list((ROOT/d["intakeApprovedDir"]).glob("*.json"))
    return ".".join([*parts[:3],str(int(parts[3])+len(approved))])

def contract():
    d=read(MANIFEST)
    base=d["base"]
    assert base["total"]==base["global"]+base["national"]==456
    assert len(set(d["globalStageIds"]))==len(d["globalStageIds"])
    extra_ids=set(d["globalStageIds"])
    bycountry=Counter()
    added_global=0
    for stage in d["nationalWaves"]:
        src=read(ROOT/stage["file"])
        rows=src["records"]
        assert len(rows)==stage["count"] and src["count"]==len(rows),(stage["file"],len(rows))
        assert len({r["id"] for r in rows})==len(rows),stage["file"]
        for r in rows:
            assert r["id"] not in extra_ids,("declared source collision",r["id"])
            extra_ids.add(r["id"])
            if stage["country"]:
                assert r["country"]==stage["country"],r["id"]
            bycountry[r["country"]]+=1
    for file in sorted((ROOT/d["intakeApprovedDir"]).glob("*.json")):
        src=read(file)
        assert src["schemaVersion"]==1 and src["admissionStatus"]=="HUMAN_EDITORIAL_APPROVED_AND_SOURCE_VERIFIED"
        assert src["count"]==len(src["records"])
        for r in src["records"]:
            assert r["id"] not in extra_ids,("bulk collision",r["id"])
            extra_ids.add(r["id"])
            if r["scope"]=="NATIONAL":bycountry[r["country"]]+=1
            else:
                assert r["scope"]=="GLOBAL"
                added_global+=1
    return {
        "global":base["global"]+len(d["globalStageIds"])+added_global,
        "national":base["national"]+sum(bycountry.values()),
        "baseTotal":base["total"],
        "sourceDeclaredIds":len(extra_ids),
        "nationalAdditionalByCountry":dict(sorted(bycountry.items())),
        "sourceManifest":str(MANIFEST.relative_to(ROOT)),
    }
def expected_totals():
    result=contract()
    result["total"]=result["global"]+result["national"]
    return result
def validate_catalog(catalog, require_current=True):
    expected=expected_totals()
    records=catalog["records"]
    ids=[r["id"] for r in records]
    assert len(ids)==len(set(ids)), "duplicate canonical IDs"
    scopes=Counter(r["scope"] for r in records)
    assert len(ids)==expected["total"],("catalog vs source contract",len(ids),expected["total"])
    assert scopes["GLOBAL"]==expected["global"],(scopes,expected)
    assert scopes["NATIONAL"]==expected["national"],(scopes,expected)
    if require_current:
        assert set(read(MANIFEST)["globalStageIds"]).issubset(set(ids)), "missing institutional global ID"
        for row in read(MANIFEST)["nationalWaves"]:
            assert {x["id"] for x in read(ROOT/row["file"])["records"]}.issubset(set(ids)),row["file"]
    return expected
if __name__=="__main__":
    catalog=read(ROOT/"assets/data/official_core.json")
    print("CATALOG SOURCE CONTRACT PASS",json.dumps(validate_catalog(catalog),sort_keys=True))
