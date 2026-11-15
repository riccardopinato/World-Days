#!/usr/bin/env python3
"""Non-AI preflight: exact 183 existing original histories awaiting 4 locales."""
import json
from collections import Counter
from pathlib import Path
from ai_183_translate import source_inventory

ROOT=Path(__file__).resolve().parents[1]
rows=source_inventory()
assert len(rows)==183
assert all({"en","it"} <= set(x["locale"]) <= {"en","it","es","fr","de","pt"} for x in rows.values())
existing_four={oid:sorted(set(r["locale"])-{"en","it"}) for oid,r in rows.items() if set(r["locale"])-{"en","it"}}
assert all(x["sources"] for x in rows.values())
assert existing_four=={"ie-w13-eures-st-brigid-s-day":["de","es","fr","pt"]}, "unexpected prior-language source drift"
counts=Counter(x["observanceId"].split("-")[0] for x in rows.values())
manifest={
 "reviewState":"183_EN_IT_SOURCE_DOSSIERS_AWAIT_AI_TRANSLATION",
 "catalogCount":1111,
 "historicallyPrepared":485,
 "alreadySixLocaleRich":319,
 "exactMissingFourLocales":183,
 "translationsToAuthor":sum(4-len(set(r["locale"])-{"en","it"}) for r in rows.values()),
 "previouslySourceTranslatedCount":sum(len(set(r["locale"])-{"en","it"}) for r in rows.values()),
 "outputLanguages":["es","fr","de","pt"],
 "ids":sorted(rows),
 "previouslyLocalizedInsideResearchSource":existing_four,
}
out=ROOT/"reports/ai_183_canonical_input_manifest.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
import py_compile
for script in ("tool/publish_ai_183_translations.py","tool/validate_ai_183_translations.py"):
 py_compile.compile(str(ROOT/script),doraise=True)
print("AI183_SOURCE_INVENTORY_PASS",len(rows),"stories",manifest["translationsToAuthor"],"missing four-locale texts", "already existed:",manifest["previouslySourceTranslatedCount"])
