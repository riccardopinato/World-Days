#!/usr/bin/env python3
"""Verify canonical 281-unwritten queue in 100+100+81 disjoint production blocks.

These are QUEUES, never count their IDs as authored, AI-reviewed or published.
"""
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
WAVES=ROOT/"data/editorial/waves"
QUEUES=ROOT/"reports/editorial_curated_428_origin_research"
RESEARCH=ROOT/"data/editorial/research"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
index=load(WAVES/"curated_428_unwritten_fasttrack_index_20261127.json")
assert index["originalBacklog"]==428
assert index["preparedResearchIds"]==147 and index["unwrittenCount"]==281
assert index["disjoint"] is True and len(index["blocks"])==3
canonical=load(ROOT/"assets/data/official_core.json")
all_catalog={r["id"] for r in canonical["records"]}
assert len(all_catalog)==947
original=[]
for n,size in zip(range(1,6),(100,100,100,100,28)):
    q=load(QUEUES/f"cohort_{n:02d}_ordered_ids.json")
    assert len(q["ids"])==size
    original.extend(q["ids"])
assert len(original)==len(set(original))==428 and set(original)<=all_catalog
prepared=[]
for n,count in ((1,100),(2,14),(3,15),(4,9),(5,9)):
    files=list(RESEARCH.glob(f"curated_428_cohort{n:02d}_*.json"))
    assert len(files)==count
    for p in files: prepared.append(load(p)["id"])
assert len(prepared)==len(set(prepared))==147
unwritten=[id for id in original if id not in set(prepared)]
assert len(unwritten)==281
blocks=[]
for i,size in enumerate((100,100,81),1):
    p=WAVES/f"curated_428_unwritten_fasttrack_block_{i:02d}.json"
    b=load(p)
    assert b["mode"]=="APP_FACTORY_CORE_V27_FAST_TRACK_AI_BLOCK100"
    assert b["contentWritten"]==0 and b["sourceVerificationRequired"]
    assert b["status"]=="RESEARCH_REQUIRED_NO_SIX_LOCALE_DOSSIER_WRITTEN"
    assert b["locales"]==["en","it","es","fr","de","pt"]
    assert b["count"]==len(b["canonicalIds"])==size
    blocks.extend(b["canonicalIds"])
assert blocks==unwritten and len(blocks)==len(set(blocks))==281
assert not set(blocks)&set(prepared)
by_source=Counter()
lookup={}
for n in range(1,6):
    q=load(QUEUES/f"cohort_{n:02d}_ordered_ids.json")
    lookup.update({id:n for id in q["ids"]})
for id in blocks: by_source[lookup[id]]+=1
assert dict(by_source)=={2:86,3:85,4:91,5:19}
print("FASTTRACK_UNWRITTEN_BLOCKS_PASS", [100,100,81],
      "prepared",len(prepared),"unwritten",len(unwritten),"no_overlap")
