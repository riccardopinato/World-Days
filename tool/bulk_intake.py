#!/usr/bin/env python3
"""Batch intake: source-first, deduplicated, fail-closed, never self-approves editorial work."""
import argparse,json,re
from collections import Counter,defaultdict
from datetime import date,timedelta
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
LOCALES={"en","it","es","fr","de","pt"}
PRIMARY={"PRIMARY_ORIGINATOR","OFFICIAL_GOVERNMENT"}
KINDS={"FIXED_DATE","NTH_WEEKDAY","LAST_WEEKDAY"}

def normalized(s):return re.sub(r"[^a-z0-9]","",s.casefold().replace("’","'"))
def day(rule,year):
    m=rule["month"];kind=rule["kind"]
    if kind=="FIXED_DATE":return date(year,m,rule["day"]).isoformat()
    if kind=="NTH_WEEKDAY":
        d=date(year,m,1)
        assert 1<=rule["weekday"]<=7 and 1<=rule["occurrence"]<=5
        result=d+timedelta(days=(rule["weekday"]-d.isoweekday())%7+7*(rule["occurrence"]-1))
        assert result.month==m,"fifth weekday does not exist"
        return result.isoformat()
    if kind=="LAST_WEEKDAY":
        d=(date(year+1,1,1) if m==12 else date(year,m+1,1))-timedelta(days=1)
        while d.isoweekday()!=rule["weekday"]:d-=timedelta(days=1)
        return d.isoformat()
    raise ValueError("unsupported recurrence")
def inspect(batch,canonical,market_codes):
    existing_ids={r["id"] for r in canonical}
    existing_names={normalized(s) for r in canonical for s in [r["canonicalTitleEn"],*r.get("aliases",[])] if s}
    seen=set();seen_names=set();rows=[]
    primary_hosts={urlsplit(s["url"]).hostname for r in canonical for s in r.get("sources",[]) if s.get("tier")=="A_PRIMARY"}
    for r in batch["records"]:
        issues=[];rid=r.get("id","");title=r.get("canonicalTitleEn","")
        if not rid or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",rid):issues.append("BAD_ID")
        if rid in existing_ids or rid in seen:issues.append("DUPLICATE_ID")
        seen.add(rid)
        if not title or normalized(title) in existing_names or normalized(title) in seen_names:issues.append("TITLE_OR_ALIAS_COLLISION")
        seen_names.add(normalized(title))
        if any(normalized(a) in existing_names for a in r.get("aliases",[])):issues.append("ALIAS_COLLISION")
        authority=r.get("authority",{})
        if not all(authority.get(k) for k in ("name","type","officiality")):
            issues.append("AUTHORITY_METADATA_MISSING")
        if authority.get("officiality") not in {"OFFICIAL_UN","OFFICIAL_UNESCO","OFFICIAL_UN_AGENCY","OFFICIAL_WHO","OFFICIAL_INSTITUTIONAL","RECOGNIZED_INSTITUTIONAL"}:
            issues.append("AUTHORITY_CLASS_UNSUPPORTED")
        if r.get("categories") and not set(r["categories"]).issubset({"PLANET","HEALTH","PEOPLE","LEARNING","CULTURE","FOOD","FUTURE","COMMUNITY"}):
            issues.append("BAD_SEMANTIC_CATEGORY")
        if r.get("visualKey") and r["visualKey"] not in {"planet","health","people","learning","culture","food","future","community"}:
            issues.append("BAD_VISUAL_CATEGORY")
        if not r.get("sourceReviewedOn"):
            issues.append("SOURCE_REVIEW_DATE_MISSING")
        if r.get("scope")=="NATIONAL":
            if r.get("country") not in market_codes:issues.append("UNSUPPORTED_COUNTRY")
        elif r.get("scope")!="GLOBAL" or r.get("country") not in (None,""):issues.append("BAD_SCOPE")
        t=r.get("localizedTitles",{})
        if set(t)!=LOCALES or t.get("en")!=title or not all(str(x).strip() for x in t.values()):issues.append("MISSING_LOCALES")
        try:
            rule,=r["recurrenceRules"]
            if rule["kind"] not in KINDS:raise ValueError("kind")
            dates={str(y):day(rule,y) for y in (2026,2027,2028)}
        except (KeyError,ValueError,TypeError,AssertionError):
            dates={};issues.append("INVALID_ANNUAL_RULE")
        if dates!=r.get("dateVectors"):issues.append("YEAR_VECTORS_NOT_VERIFIED")
        origins=defaultdict(set);urls=set();conflict=False
        for a in r.get("attestations",[]):
            try:
                u=urlsplit(a["url"])
                assert u.scheme=="https" and u.hostname and a["url"] not in urls
                urls.add(a["url"])
                assert a["publisher"] and len(a["originId"])>5 and len(a["eventExcerpt"])>=8
                assert a["sourceClass"] in PRIMARY|{"REPUTABLE_INDEPENDENT","SECONDARY_REPOST"}
                if a["sourceClass"] in PRIMARY and u.hostname not in primary_hosts:
                    issues.append("PRIMARY_HOST_NOT_IN_EXISTING_TRUSTED_CATALOG")
                assert date.fromisoformat(a["reportedDate"]).year==2026
                origins[a["originId"]].add(a["sourceClass"])
                if dates and a["reportedDate"]!=dates["2026"]:conflict=True
            except (KeyError,AssertionError,ValueError,TypeError):
                issues.append("BAD_SOURCE_EVIDENCE")
        first_party=sum(bool(v&PRIMARY) for v in origins.values())
        if first_party<1:issues.append("PRIMARY_ORIGINATOR_MISSING")
        if conflict:issues.append("CONTRADICTORY_DATE")
        if not r.get("annualRuleEvidenceUrl","").startswith("https://"):issues.append("ANNUAL_RULE_UNSUPPORTED")
        if r.get("introducedYear") is not None and not r.get("introducedYearSource","").startswith("https://"):issues.append("INTRODUCED_YEAR_UNSOURCED")
        if r.get("identityReviewed") is not True or not r.get("identityEvidenceUrl","").startswith("https://"):issues.append("IDENTITY_REVIEW_PENDING")
        approval=r.get("editorialApproval",{})
        if approval.get("status")!="QUALIFIED_APPROVED" or not approval.get("reviewer") or not approval.get("evidenceUrl","").startswith("https://"):
            issues.append("QUALIFIED_EDITORIAL_PENDING")
        issues=sorted(set(issues))
        rows.append({"id":rid,"title":title,"status":"ELIGIBLE" if not issues else "BLOCKED",
                     "blockers":issues,"pages":len(urls),"documentOrigins":len(origins),
                     "primaryOrigins":first_party,"dateVectors":dates})
    if len(rows)!=batch.get("count") or len(rows)>50 or batch.get("schemaVersion")!=1:raise ValueError("invalid batch schema/count")
    return {"schemaVersion":1,"batchId":batch["batchId"],"recordCount":len(rows),
            "eligible":sum(r["status"]=="ELIGIBLE" for r in rows),
            "blocked":sum(r["status"]=="BLOCKED" for r in rows),
            "records":rows,"disclaimer":"Originator calendar date is not automatic unique annual identity or human editorial approval."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--report",type=Path,default=ROOT/"reports/bulk_intake_report.json")
    p.add_argument("--emit-approved",action="store_true")
    args=p.parse_args()
    batch=json.loads(args.input.read_text(encoding="utf-8"))
    source=json.loads((ROOT/"assets/data/official_core.json").read_text(encoding="utf-8"))
    import catalog_source_contract
    existing_codes=set(re.findall(r"MarketOption\('([A-Z]{2})'",(ROOT/"lib/core/market_options.dart").read_text(encoding="utf-8")))
    report=inspect(batch,source["records"],existing_codes)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if args.emit_approved:
        assert report["eligible"]==report["recordCount"]>0 and report["blocked"]==0,report
        name=re.sub(r"[^a-z0-9]+","-",batch["batchId"].lower()).strip("-")
        target=ROOT/catalog_source_contract.read(catalog_source_contract.MANIFEST)["intakeApprovedDir"]/(name+".json")
        assert not target.exists(),("cannot overwrite approved source",target)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps({"schemaVersion":1,"batchId":batch["batchId"],
            "admissionStatus":"HUMAN_EDITORIAL_APPROVED_AND_SOURCE_VERIFIED",
            "count":len(batch["records"]),"records":batch["records"]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("APPROVED BATCH GENERATED",target)
    print("BULK INTAKE PASS",json.dumps({"records":report["recordCount"],"eligible":report["eligible"],"blocked":report["blocked"]}))
if __name__=="__main__":main()
