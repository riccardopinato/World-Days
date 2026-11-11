#!/usr/bin/env python3
"""Research-only probe: Wikidata P837 calendar recurrence names (CC0 source).
Run with network when available. Never publishes Wikidata records into app.
"""
import json,urllib.request,urllib.parse,re,sys,time
QUERY="""SELECT DISTINCT ?item ?itemLabel ?dayLabel ?countryLabel WHERE {
  ?item wdt:P837 ?day .
  ?item rdfs:label ?itemLabel .
  FILTER(LANG(?itemLabel) = "en")
  ?day rdfs:label ?dayLabel .
  FILTER(LANG(?dayLabel) = "en")
  OPTIONAL { ?item wdt:P17 ?country . ?country rdfs:label ?countryLabel . FILTER(LANG(?countryLabel) = "en") }
  FILTER(REGEX(STR(?itemLabel), "day|festival|holiday|anniversary|celebration|feast|week|memorial|observance", "i"))
  FILTER(REGEX(STR(?dayLabel), "January|February|March|April|May|June|July|August|September|October|November|December", "i"))
} LIMIT 1000"""
URL="https://query.wikidata.org/sparql?"+urllib.parse.urlencode({"query":QUERY,"format":"json"})
def main():
 req=urllib.request.Request(URL,headers={"Accept":"application/sparql-results+json","User-Agent":"WorldDays-research/0.1 (documentation only; source metadata QA)"})
 try:
  with urllib.request.urlopen(req,timeout=30) as r:
   data=json.load(r)
 except Exception as exc:
  print("WDQS_PROBE_BLOCKED:",repr(exc));return
 rows=data.get("results",{}).get("bindings",[])
 print("WDQS_PROBE_TOTAL",len(rows))
 import datetime
 MONTHS={name:i for i,name in enumerate(("January","February","March","April","May","June","July","August","September","October","November","December"),1)}
 match=0
 for row in rows:
  x={k:v.get("value") for k,v in row.items()}
  day=(x.get("dayLabel") or "").strip()
  m=re.fullmatch(r"([A-Za-z]+) ([1-9]|[12][0-9]|3[01])",day)
  if not m:
   m=re.fullmatch(r"([1-9]|[12][0-9]|3[01]) ([A-Za-z]+)",day)
   if not m:continue
   mday=int(m.group(1));month=MONTHS.get(m.group(2))
  else:
   mday=int(m.group(2));month=MONTHS.get(m.group(1))
  if month is None:continue
  try:datetime.date(2026,month,mday)
  except ValueError:continue
  label=x.get("itemLabel") or ""
  if not label or re.fullmatch(r"Q[0-9]+",label):continue
  if not re.search(r"(day|festival|holiday|anniversary|celebration|feast|week|memorial|observance)",label,re.I):continue
  x["month"]=month;x["day"]=mday;x["item"]=x["item"].rsplit("/",1)[-1]
  print("WDQS_RECORD",json.dumps(x,ensure_ascii=False,separators=(",",":")))
  match+=1
 print("WDQS_FILTERED_DATE_LABEL_MATCHES",match)
 print("WDQS_RESEARCH_ONLY: no automatic catalog publication.")
if __name__=="__main__":main()
