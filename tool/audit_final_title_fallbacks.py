#!/usr/bin/env python3
"""Audit final five locale display-title equality after all 359 updates.

English-equal display titles are NOT automatically untranslated: native proper
names, names of institutions, brands and commemorations can be identical.
Generated report is a review queue, not new published content.
"""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=R/"assets/data/official_core.json"
cat=json.loads(source.read_text(encoding="utf-8"))
assert len(cat["records"])==947
LANG=("it","es","fr","de","pt")
items=[]
for r in cat["records"]:
 matches=[lang for lang in LANG if r["localizedTitles"][lang]==r["localizedTitles"]["en"]]
 if matches:
  items.append({"id":r["id"],"title":r["canonicalTitleEn"],
                "scope":r["scope"],"country":r["countries"],
                "sameAsEnglishLocales":matches,
                "sourceUrls":[s["url"] for s in r["sources"]]})
report={"catalog":947,"fallbackCandidateIDs":len(items),
        "identicalTitleCountsPerLocale":{l:sum(l in r["sameAsEnglishLocales"] for r in items) for l in LANG},
        "meaning":"Candidate only: identical proper nouns may be correct; do not claim untranslated without review",
        "items":items}
p=R/"reports/final_title_english_equal_audit_20261119.json"
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("WORLD_DAYS_FINAL_TITLE_FALLBACK_AUDIT",json.dumps(report,ensure_ascii=False))
