#!/usr/bin/env python3
"""Inspect actual source strength of the 604 contextual-only canonical IDs."""
from pathlib import Path
from urllib.parse import urlparse
import json
from collections import Counter
root=Path(__file__).resolve().parents[1]
cat=json.loads((root/'assets/data/official_core.json').read_text())
ed=json.loads((root/'assets/data/editorial_en.json').read_text())
rows={r['id']:r for r in cat['records']}
pending=sorted(x['observanceId'] for x in ed['entries'] if x['status']=='AI_CONTEXTUAL_SIX_LOCALE')
assert len(pending)==len(set(pending))==604
stats=Counter()
proven=[]
for oid in pending:
    r=rows[oid]
    year=r.get('introducedYear')
    yrurl=r.get('introducedYearSource')
    res=r.get('authority',{}).get('resolution')
    urls=[s['url'] for s in r['sources']]
    exact=bool(year and yrurl and yrurl in urls)
    dedicated=any('/observances/' in u or '/days/' in u or '/eli/' in u or '/law/' in u for u in urls)
    if exact:stats['verified_year']+=1
    if res:stats['formal_resolution']+=1
    if exact and res:stats['year_and_resolution']+=1
    if exact and dedicated:stats['year_and_dedicated']+=1
    if dedicated:stats['dedicated']+=1
    if exact and res and dedicated:stats['all_three']+=1
    if r['scope']=='GLOBAL':stats['global']+=1
    else:stats['national']+=1
    if exact:
        proven.append({'id':oid,'year':year,'resolution':res,'authority':r['authority']['name'],'yearSource':yrurl,'sources':urls,'country':r['countries']})
print('MASS_ORIGIN_604_SOURCE_COVERAGE',json.dumps(dict(stats),sort_keys=True))
print('MASS_ORIGIN_EXACT_YEAR_COUNT',len(proven))
print('MASS_ORIGIN_EXACT_YEAR_FIRST_120',json.dumps(proven[:120],ensure_ascii=False))
