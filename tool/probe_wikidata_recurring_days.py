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
} LIMIT 1000"""
URL="https://query.wikidata.org/sparql?"+urllib.parse.urlencode({"query":QUERY,"format":"json"})
def main():
 req=urllib.request.Request(URL,headers={"Accept":"application/sparql-results+json","User-Agent":"WorldDays-research/0.1 (documentation only; source metadata QA)"})
 try:
  with urllib.request.urlopen(req,timeout=28) as r:
   data=json.load(r)
 except Exception as exc:
  print("WDQS_PROBE_BLOCKED:",repr(exc));return
 rows=data.get("results",{}).get("bindings",[])
 print("WDQS_PROBE_TOTAL",len(rows))
 for row in rows[:25]:
  print("WDQS_SAMPLE",json.dumps({k:v.get("value") for k,v in row.items()},ensure_ascii=False))
 print("WDQS_RESEARCH_ONLY: no automatic catalog publication.")
if __name__=="__main__":main()
