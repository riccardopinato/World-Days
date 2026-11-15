#!/usr/bin/env python3
"""Non-AI preflight: exact 183 existing original histories awaiting 4 locales."""
import json
from collections import Counter
from pathlib import Path
from ai_183_translate import source_inventory

ROOT=Path(__file__).resolve().parents[1]
rows=source_inventory()
assert len(rows)==183
assert all(set(x["locale"])=={"en","it"} for x in rows.values()), "unexpected pretranslated rows"
assert all(x["sources"] for x in rows.values())
counts=Counter(x["observanceId"].split("-")[0] for x in rows.values())
manifest={
 "reviewState":"183_EN_IT_SOURCE_DOSSIERS_AWAIT_AI_TRANSLATION",
 "catalogCount":1111,
 "historicallyPrepared":485,
 "alreadySixLocaleRich":319,
 "exactMissingFourLocales":183,
 "translationsToAuthor":183*4,
 "outputLanguages":["es","fr","de","pt"],
 "ids":sorted(rows),
}
out=ROOT/"reports/ai_183_canonical_input_manifest.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("AI183_SOURCE_INVENTORY_PASS",len(rows),"stories",183*4,"missing translations")
