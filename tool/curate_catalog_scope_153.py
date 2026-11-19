#!/usr/bin/env python3
"""World Days PRODUCT-SCOPE audit and deterministic published-catalog curation.

Keep the 1111-source candidate registry for provenance and reversibility,
but publish only thematic/civic/official observances. Exclude exactly the 153
Philippine person-specific birth/death dates (144 Wave11 + 9 Wave10). This
runs AFTER all canonical 1111 source/translation pipelines and BEFORE content
pack build, on EVERY Web, Android, release and development path.

Do not exclude genuine national commemorative days just because they are named
after a person; do not mistake culture-calendar birthdays for public holidays.
"""
from collections import Counter
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets/data"
MARKET=ROOT/"data/market"
REPORTS=ROOT/"reports"
LOCALES=("en","it","es","fr","de","pt")
BEFORE=1111
EXCLUDE=153
AFTER=958
STATUS="AI_CONTEXTUAL_SIX_LOCALE"

def read(p):
    return json.loads(p.read_text(encoding="utf-8"))
def write(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def excluded_sources():
    wave11=read(MARKET/"wave11_staged_144_ph_20261111.json")["records"]
    wave10=read(MARKET/"wave10_hundred_kr_ph_20261111.json")["records"]
    assert len(wave11)==144
    assert all(x["country"]=="PH" and re.match(r"^(Birth|Death) of ",x["canonicalTitleEn"]) for x in wave11)
    w10=[r for r in wave10
         if r["country"]=="PH" and re.search(r"-(?:birth|death)-anniversary$",r["id"])]
    assert len(w10)==9,("unexpected personal birthday/death count",len(w10))
    rows=wave11+w10
    assert len(rows)==EXCLUDE and len({x["id"] for x in rows})==EXCLUDE
    return {r["id"]:{"id":r["id"],"title":r["canonicalTitleEn"],"country":"PH",
                      "reason":"PERSONAL_BIRTH_OR_DEATH_ANNIVERSARY_NOT_WORLD_DAYS_TOPIC",
                      "sourceFile":"wave11_staged_144_ph_20261111.json" if r in wave11
                                  else "wave10_hundred_kr_ph_20261111.json",
                      "originalAuthority":r["authority"],"originalSource":r["source"]}
            for r in rows}

def run():
    source_exclusions=excluded_sources()
    excluded=set(source_exclusions)
    seed=read(ASSETS/"official_core.json")
    originals=seed["records"]
    assert len(originals)==BEFORE
    ids=[r["id"] for r in originals]
    assert len(set(ids))==BEFORE and excluded<=set(ids)
    by_id={r["id"]:r for r in originals}
    assert all(by_id[x]["countries"]==["PH"] and by_id[x]["scope"]=="NATIONAL" for x in excluded)
    assert all(by_id[x]["sources"] and by_id[x]["sources"][0]["url"]==source_exclusions[x]["originalSource"] for x in excluded)
    # Full 1111-title audit, including detection of unadmitted personal dates.
    suspicious=[]
    topic_counts=Counter()
    country_counts=Counter()
    status_counts=Counter()
    known_years=0
    for row in originals:
        oid=row["id"]
        title=row["canonicalTitleEn"]
        if row["scope"]=="GLOBAL":
            topic_counts["GLOBAL"]+=1
        else:
            assert len(row["countries"])==1
            country_counts[row["countries"][0]]+=1
            topic_counts["NATIONAL"]+=1
        assert len(row["localizedTitles"])==6
        assert all(isinstance(v,str) and v.strip() for v in row["localizedTitles"].values())
        assert row["sources"] and row["recurrenceRules"]
        status_counts[str(row.get("editorialStatus","UNKNOWN"))]+=1
        known_years+=isinstance(row.get("introducedYear"),int)
        if oid not in excluded and re.search(r"(?i)(?:^birth of |^death of |\bbirth anniversary\b|\bdeath anniversary\b|\bbirthday of\b|\bdeath of\b)",title):
            suspicious.append({"id":oid,"title":title,"auditStatus":"INDIVIDUAL_MANUAL_SCOPE_REVIEW"})
    assert sum(topic_counts.values())==BEFORE
    packs={}
    for loc in LOCALES:
        p=ASSETS/f"editorial_{loc}.json"
        doc=read(p)
        all_entries=doc["entries"]
        eids=[x["observanceId"] for x in all_entries]
        assert len(eids)==len(set(eids))==doc["entryCount"]==BEFORE
        assert set(eids)==set(ids),("six-locale parity",loc)
        packs[loc]=doc
        assert all(r["status"]==STATUS for r in all_entries if r["observanceId"] in excluded),(
            "would discard a source-researched article",loc)
    # Current record status numbers: 519 existing substantial/source-oriented
    # and 592 contextual, including all 153 personal dates.
    before_status=Counter(r["status"] for r in packs["en"]["entries"])
    assert before_status[STATUS]==592,before_status
    assert sum(before_status.values())==BEFORE
    kept=[r for r in originals if r["id"] not in excluded]
    assert len(kept)==AFTER
    seed["records"]=kept
    seed["yearOverrides"]=[o for o in seed.get("yearOverrides",[])
                           if o.get("observanceId") not in excluded]
    seed["datasetVersion"]="2026.11.19.3"
    seed["coverage"]=(seed.get("coverage","")+
      " Published consumer scope excludes 153 personal birth/death anniversaries; source archival catalog remains 1111.")
    write(ASSETS/"official_core.json",seed)
    # Preserve offline date-index shape, remove all excluded occurrences.
    op=ASSETS/"occurrences_2026.json"
    occ=read(op)
    orig_occ=len(occ["occurrences"])
    occ["occurrences"]=[o for o in occ["occurrences"] if o["observanceId"] not in excluded]
    occ["occurrenceCount"]=len(occ["occurrences"])
    assert len(occ["dateIndex"])==365
    for item in occ["dateIndex"]:
        item["observanceIds"]=[oid for oid in item["observanceIds"] if oid not in excluded]
    assert not any(o["observanceId"] in excluded for o in occ["occurrences"])
    write(op,occ)
    for loc in LOCALES:
        doc=packs[loc]
        doc["entries"]=[x for x in doc["entries"] if x["observanceId"] not in excluded]
        doc["entryCount"]=len(doc["entries"])
        assert doc["entryCount"]==AFTER
        write(ASSETS/f"editorial_{loc}.json",doc)
    # Keep the runtime origin-index aligned with the public catalog. Immutable
    # historical/source dossiers in data/editorial/ remain untouched.
    idx_path=ASSETS/"origin_review_index.json"
    idx=read(idx_path)
    assert len(idx["records"])==BEFORE
    idx["records"]=[r for r in idx["records"] if r["observanceId"] not in excluded]
    assert len(idx["records"])==AFTER
    idx["recordCount"]=AFTER
    idx["sourceCatalogCount"]=AFTER
    idx["datasetVersion"]=seed["datasetVersion"]
    states=Counter(r["originResearchStatus"] for r in idx["records"])
    idx["originStatusCounts"]=dict(states)
    tiers=Counter(t for r in idx["records"] for t in r["sourceTiers"])
    idx["sourceTiersCount"]=dict(tiers)
    idx["reviewedRichOriginCount"]=states["PRIMARY_RESEARCHED_ORIGIN_IT_EN"]
    write(idx_path,idx)
    # Preserve a reproducible audit and an explicit archival reference per ID.
    after_status=Counter(r["status"] for r in packs["en"]["entries"]
                         if r["observanceId"] not in excluded)
    assert after_status[STATUS]==439,after_status
    assert sum(after_status.values())==AFTER
    assert all(x in set(ids) for x in excluded)
    audit={
        "schemaVersion":1,
        "reviewDate":"2026-11-19",
        "catalogSourceCandidatesAudited":BEFORE,
        "excludedPersonalBirthDeathAnniversaries":EXCLUDE,
        "excludedBySource":{"PH_NCCA_WAVE11":144,"PH_NCCA_WAVE10":9},
        "publishedObservances":AFTER,
        "globalPreserved":topic_counts["GLOBAL"],
        "nationalPreserved":topic_counts["NATIONAL"]-EXCLUDE,
        "sourceCountries":len(country_counts),
        "philippinesBefore":country_counts["PH"],
        "philippinesPublished":country_counts["PH"]-EXCLUDE,
        "sixLocalePackEntries":{loc:packs[loc]["entryCount"] for loc in LOCALES},
        "beforeEditorialStatusCounts":dict(before_status),
        "afterEditorialStatusCounts":dict(after_status),
        "contextualWithoutIndividualHistoricalOrigin":after_status[STATUS],
        "nonContextualEditorial":AFTER-after_status[STATUS],
        "introducedYearsInOriginalCatalog":known_years,
        "removed2026Occurrences":orig_occ-len(occ["occurrences"]),
        "outsidePolicyBiographicalCandidates":suspicious,
        "excludedIDArchivalPolicy":"SOURCE_RECORDS_RETAINED_IN_DATA_MARKET_AND_RESEARCH_NOT_PUBLISHED_IN_APP",
        "methodology":"Full ID-title/scope/year/source/translation audit. Exact 144+9 NCCA birth/death IDs excluded; national civic commemorations and organizational founding anniversaries retained.",
        "limitation":"A fully translated contextual record is not necessarily an individually researched founding history. Source index listing alone does not establish a statutory public holiday."
    }
    write(REPORTS/"world_days_catalog_relevance_audit_20261119.json",audit)
    write(REPORTS/"world_days_excluded_birth_death_20261119.json",
          {"schemaVersion":1,"count":EXCLUDE,
           "scope":"ARCHIVED_SOURCE_IDENTITIES_EXCLUDED_FROM_APP",
           "records":[source_exclusions[x] for x in sorted(excluded)]})
    print("WORLD_DAYS_CURATED_153_EXCLUDED",json.dumps({
        k:audit[k] for k in ("catalogSourceCandidatesAudited","excludedPersonalBirthDeathAnniversaries",
        "publishedObservances","globalPreserved","nationalPreserved","philippinesPublished",
        "contextualWithoutIndividualHistoricalOrigin","nonContextualEditorial",
        "removed2026Occurrences")},sort_keys=True))
    print("WORLD_DAYS_SCOPE_FURTHER_REVIEW",json.dumps(suspicious,ensure_ascii=False))

if __name__=="__main__":run()
