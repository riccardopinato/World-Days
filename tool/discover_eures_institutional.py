#!/usr/bin/env python3
"""Fetch EURES national holiday indexes as *unapproved* source candidates."""
import argparse,json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request,urlopen
from datetime import date
from collections import Counter
URL="https://eures.europa.eu/eures-services/chat-eures-advisers/public-holidays-calendar_en"
CODES=dict(zip("Austria Belgium Bulgaria Croatia Cyprus Czechia Denmark Estonia Finland France Germany Greece Hungary Ireland Italy Latvia Lithuania Luxembourg Malta Netherlands Norway Poland Portugal Romania Slovakia Slovenia Spain Sweden".split(),"AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL NO PL PT RO SK SI ES SE".split()))
CODES.update({"Czech Republic":"CZ","United Kingdom":"GB","Iceland":"IS","Switzerland":"CH","Liechtenstein":"LI"})
class Reader(HTMLParser):
 def __init__(self):
  super().__init__();self.heading=None;self.words=[];self.year=None;self.country=None;self.cell=None;self.cells=[];self.inrow=False;self.rows=[]
 def handle_starttag(self,tag,attrs):
  if tag in ("h2","h3","h4"):self.heading=tag;self.words=[]
  if tag=="tr":self.inrow=True;self.cells=[]
  if self.inrow and tag in ("td","th"):self.cell=[]
 def handle_data(self,txt):
  if self.heading:self.words.append(txt)
  if self.cell is not None:self.cell.append(txt)
 def handle_endtag(self,tag):
  if tag==self.heading:
   t=" ".join(" ".join(self.words).split())
   if t in CODES:self.country=t
   elif "2026" in t:self.year=2026
   elif "2027" in t:self.year=2027
   self.heading=None
  if tag in ("td","th") and self.cell is not None:self.cells.append(" ".join(" ".join(self.cell).split()));self.cell=None
  if tag=="tr":
   if self.inrow and len(self.cells)>=2:self.rows.append((self.year,self.country,self.cells[0],self.cells[1]))
   self.inrow=False
def parse(html):
 p=Reader();p.feed(html);out={};bad=[]
 for year,country,raw,title in p.rows:
  if year!=2026 or country not in CODES or raw.lower()=="date":continue
  match=re.fullmatch(r"(\d{1,2})/(\d{1,2})",raw.strip())
  try:
   if not match:raise ValueError(raw)
   day,month=map(int,match.groups());when=date(2026,month,day).isoformat()
  except ValueError:bad.append({"country":country,"date":raw,"title":title});continue
  key=(CODES[country],title.casefold(),when)
  out[key]={"country":CODES[country],"titleEn":title,"observed2026":when,"sourceUrl":URL,"status":"DISCOVERY_ONLY","primaryLegalSource":None,"recurrenceRule":None,"introducedYear":None,"editorialStatus":"NOT_REVIEWED"}
 return list(out.values()),bad
def reconcile(rows, catalog):
 """Classify probable duplicates conservatively; never claim automatic uniqueness."""
 norm=lambda v: re.sub(r"[^a-z0-9]+","-",v.casefold()).strip("-")
 known={}
 for row in catalog.get("records",[]):
  for title in [row.get("canonicalTitleEn",""),*row.get("aliases",[])]:
   if title:known.setdefault(norm(title),[]).append((row["id"],row.get("scope")))
 for row in rows:
  matches=known.get(norm(row["titleEn"]),[])
  row["probableExistingIds"]=sorted({x[0] for x in matches})
  if matches: row["dedupStatus"]="MATCHED_EXISTING_TITLE_OR_ALIAS"
  elif norm(row["titleEn"]) in {"national-holiday","national-day","public-holiday","holiday","independence-day","labour-day","new-year-s-day","christmas-day","easter-monday"}:
   row["dedupStatus"]="GENERIC_TRANSNATIONAL_LABEL_REQUIRES_IDENTITY_REVIEW"
  else:row["dedupStatus"]="UNMATCHED_TITLE_PENDING_MANUAL_ENTITY_REVIEW"
 return rows

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--html",type=Path);ap.add_argument("--output",type=Path,default=Path("reports/eures_candidate_batch.json"));args=ap.parse_args()
 if args.html:html=args.html.read_text(encoding="utf8")
 else:
  with urlopen(Request(URL,headers={"User-Agent":"WorldDaysResearch/1.0"}),timeout=25) as r:html=r.read(5000000).decode("utf8")
 rows,bad=parse(html)
 catalog=Path("assets/data/official_core.json")
 if catalog.exists(): rows=reconcile(rows,json.loads(catalog.read_text(encoding="utf8")))
 else:
  for row in rows:row["dedupStatus"]="CANONICAL_CATALOG_NOT_AVAILABLE"
 assert rows,"No rows found: manual source inspection required"
 result={"schemaVersion":1,"scope":"RESEARCH_ONLY_NO_RUNTIME_IMPORT","source":URL,"totalCandidates":len(rows),"countryCounts":dict(Counter(x["country"] for x in rows)),"dedupStatusCounts":dict(Counter(x["dedupStatus"] for x in rows)),"invalidDates":bad,"records":rows,"policy":"A 2026 holiday is not a proven annual recurrence or a unique international day; country primary sources, localization, duplicates and editorial require separate validation."}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf8");print("DISCOVERY",len(rows))
if __name__=="__main__":main()
