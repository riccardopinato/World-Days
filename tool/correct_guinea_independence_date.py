#!/usr/bin/env python3
"""Correct Guinea Independence Day from 1 October to 2 October (1958).

The legacy DFAT diplomatic source projection placed GN on 1 October. Independent
official Finland MFA national-day index, UN diplomatic documentation, and
Guinea historical chronology consistently establish 2 October. Preserve the
original source snapshot, add the corrective source in the consumer catalog.
"""
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/"assets/data"
URL="https://um.fi/national-days"
ID="gn-dfat-national-day"
def rd(p):return json.loads(p.read_text(encoding="utf-8"))
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def main():
 path=A/"official_core.json"
 cat=rd(path)
 assert len(cat["records"])==947 and cat["datasetVersion"]=="2026.11.19.6"
 record=next(x for x in cat["records"] if x["id"]==ID)
 assert record["countries"]==["GN"] and record["canonicalTitleEn"]=="Independence Day — Guinea"
 assert len(record["recurrenceRules"])==1
 rule=record["recurrenceRules"][0]
 assert rule=={"kind":"FIXED_DATE","month":10,"day":1},rule
 rule["day"]=2
 assert all(s["url"]!=URL for s in record["sources"])
 record["sources"].append({"tier":"B_INSTITUTIONAL","url":URL,"verifiedAt":"2026-11-19"})
 record["lastVerifiedAt"]="2026-11-19"
 record["notes"].append("National-day correction: documented 2 October 1958; Australian diplomatic index source projection 1 October superseded in consumer calendar; original source archived.")
 wr(path,cat)
 occ_path=A/"occurrences_2026.json"
 occ=rd(occ_path)
 matches=[o for o in occ["occurrences"] if o["observanceId"]==ID]
 assert len(matches)==1
 assert matches[0]["startDate"]==matches[0]["endDate"]=="2026-10-01"
 matches[0]["startDate"]=matches[0]["endDate"]="2026-10-02"
 old=next(x for x in occ["dateIndex"] if x["date"]=="2026-10-01")
 new=next(x for x in occ["dateIndex"] if x["date"]=="2026-10-02")
 assert ID in old["observanceIds"] and ID not in new["observanceIds"]
 old["observanceIds"].remove(ID)
 new["observanceIds"]=sorted(set(new["observanceIds"]+[ID]))
 wr(occ_path,occ)
 idx_path=A/"origin_review_index.json"
 ledger=rd(idx_path)
 entry=next(x for x in ledger["records"] if x["observanceId"]==ID)
 assert URL not in entry["canonicalSourceUrls"]
 entry["canonicalSourceUrls"].append(URL)
 entry["sourceTiers"].append("B_INSTITUTIONAL")
 ledger["sourceTiersCount"]=dict(Counter(x for r in ledger["records"] for x in r["sourceTiers"]))
 wr(idx_path,ledger)
 report={"id":ID,"sourceCalendarOriginal":"2026-10-01",
         "consumerCalendarCorrected":"2026-10-02",
         "historicalIndependenceYear":1958,"archivalMarketSourceUnmodified":True,
         "addedInstitutionalSource":URL,
         "status":"INDEPENDENT_NATIONAL_DATE_CORRECTION"}
 out=ROOT/"reports/guinea_national_day_20261119.json"
 out.parent.mkdir(parents=True,exist_ok=True)
 wr(out,report)
 print("GUINEA_OCT_2_INDEPENDENCE_CORRECTION",report)
if __name__=="__main__":main()
