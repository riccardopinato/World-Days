#!/usr/bin/env python3
"""World Days semantic adapter tests: English source, dedup and scope integrity."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

PATH=Path(__file__).resolve().parents[1]/"semantic_qa_adapter.py"
spec=importlib.util.spec_from_file_location("world_semantic_adapter", PATH)
adapter=importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

def record(rid, title="World Day"):
    return {"observanceId":rid,"introducedYear":2020,
        "sources":["https://www.unesco.org/"],
        "locale":{l:{"heading":title if l=="en" else f"{title} ({l})",
                     "origin":"The year 2020 introduced the day.",
                     "promoter":"UNESCO", "purpose":"Education",
                     "facts":["Established in 2020."]}
                  for l in ("en","it","es","fr","de","pt")}}

class WorldSemanticTests(unittest.TestCase):
    def test_published_dossiers_are_source_locked(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            folder=root/"data/editorial/published"
            folder.mkdir(parents=True)
            (folder/"a.json").write_text(json.dumps({"records":[record("a")]}),
                                          encoding="utf-8")
            (folder/"b.json").write_text(json.dumps({"records":[record("b")]}),
                                          encoding="utf-8")
            data=adapter.collect(root)
            self.assertEqual(len(data["records"]),2)
            self.assertEqual(data["sourceLocale"],"en")
            self.assertEqual(data["targetLocales"],["it","es","fr","de","pt"])
            self.assertEqual(data["records"][0]["protectedTerms"],["UNESCO"])
            self.assertEqual(len(data["records"][1]["translations"]),5)
            report={"adapter":"world_days_published_editorial",
                    "recordCount":2,"comparisonCount":10,
                    "certification":"NOT_CERTIFIED","results":[]}
            self.assertEqual(adapter.verify_report(report,2)["languageComparisons"],10)
    def test_conflicting_duplicates_are_exposed_not_merged(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            folder=root/"data/editorial/published"
            folder.mkdir(parents=True)
            (folder/"a.json").write_text(json.dumps({"records":[record("same")]}),
                                          encoding="utf-8")
            (folder/"b.json").write_text(json.dumps({"records":[record("same","Different")]}),
                                          encoding="utf-8")
            data=adapter.collect(root)
            self.assertEqual(len(data["records"]),1)
            self.assertEqual(len(data["sourceWarnings"]["conflictingDuplicateDossiers"]),1)
    def test_missing_source_never_accepted_as_translation(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            folder=root/"data/editorial/published"
            folder.mkdir(parents=True)
            item=record("a")
            del item["locale"]["en"]
            (folder/"a.json").write_text(json.dumps({"records":[item]}),
                                          encoding="utf-8")
            with self.assertRaises(ValueError):
                adapter.collect(root)

if __name__=="__main__":unittest.main()
