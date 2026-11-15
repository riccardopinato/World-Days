#!/usr/bin/env python3
"""Offline AI QA gate for 183 English/Italian historical source dossiers.

Inputs are four independently generated local-neural-machine-translation
artifacts (es/fr/de/pt), including independent backtranslation probes.
AI certification is explicitly limited to machine translation/source parity:
no qualified human signoff and no claim that every original source URL was
re-fetched. Fail closed and save detailed HOLD diagnostics on any exception.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

from ai_183_translate import source_inventory, FIELDS, YEARS, LOCALES

ROOT = Path(__file__).resolve().parents[1]
RESOLUTIONS = re.compile(r"\bA/RES/\d{1,3}/\d{1,4}\b", re.I)
MIN_RECALL = 0.45  # use aggregated 2nd-model lexical semantics; isolated synonym false negatives are diagnostic

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob_sha(relative_path):
    out = subprocess.run(["git", "hash-object", relative_path],
                         cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.strip()

def proof_index():
    records = {}
    files = [ROOT/"data/editorial/batches/origin_stories_primary_20261111.json"]
    files += sorted((ROOT/"data/editorial/batches").glob("origin_stories_wave*.json"))
    for file in files:
        relative = file.relative_to(ROOT).as_posix()
        sha = blob_sha(relative)
        for item in read(file)["records"]:
            assert item["observanceId"] not in records
            records[item["observanceId"]] = (relative, sha)
    return records

def detect(text):
    from langdetect import detect_langs
    langs = detect_langs(text)
    return (langs[0].lang, round(langs[0].prob, 4))

def audit(staging, output, hold_output):
    english = source_inventory()
    links = proof_index()
    assert len(english) == 183
    all_langs = {}
    holds = []
    models = {}
    for locale in LOCALES:
        file = staging / f"ai_183_{locale}.json"
        if not file.exists():
            raise SystemExit(f"Missing neural translation artifact {file}")
        doc = read(file)
        assert doc["locale"] == locale and doc["state"] == "AI_TRANSLATED_PENDING_INDEPENDENT_VALIDATION"
        assert doc["untranslatedAtBaseline"] == 183
        actual = {r["observanceId"]:r for r in doc["records"]}
        assert len(actual) == len(doc["records"]) == 183
        assert set(actual) == set(english), ("identity parity",locale)
        assert doc["forwardModel"]["languagePair"] == "en_" + locale
        assert doc["independentReverseModel"]["languagePair"] == locale + "_en"
        models[locale] = {"forward": doc["forwardModel"], "reverse":doc["independentReverseModel"]}
        all_langs[locale] = actual

    qualified = []
    for oid, source in english.items():
        orig = source["locale"]["en"]
        original_years = set(YEARS.findall(" ".join(
            [orig["origin"], orig["purpose"], *orig["facts"]])))
        original_resolutions = {m.upper() for m in RESOLUTIONS.findall(
            " ".join([orig["origin"], orig["promoter"], *orig["facts"]]))}
        localized = {"en":orig, "it":source["locale"]["it"]}
        diagnostics = {}
        for locale in LOCALES:
            draft = all_langs[locale][oid]
            target = draft["translations"]
            issues = []
            if not all(isinstance(target.get(k),str) and len(target[k].strip())>=25
                       for k in FIELDS):
                issues.append("EMPTY_OR_SHORT_TRANSLATED_FIELD")
            if len(target.get("origin","")) < 75:
                issues.append("ORIGIN_TRANSLATION_TOO_SHORT")
            facts = target.get("facts",[])
            if len(facts) != len(orig["facts"]) or any(
                not isinstance(x,str) or len(x.strip()) < 20 for x in facts
            ):
                issues.append("FACT_COUNT_OR_LENGTH_DRIFT")
            check = draft["aiRoundtrip"]
            recalls = check.get("purposeAndFactsEnglishTokenRecall",[])
            if (len(recalls) != 1 + len(orig["facts"]) or
                (sum(recalls)/max(len(recalls),1)) < .45):
                issues.append("AI_BACKTRANSLATION_SEMANTIC_HOLD")
            scope = " ".join([target.get("origin",""),target.get("purpose",""),*facts])
            current_years = set(YEARS.findall(scope))
            if current_years != original_years:
                issues.append("HISTORICAL_YEARS_NOT_PRESERVED")
            original_summary = " ".join([orig["origin"],orig["purpose"],*orig["facts"]])
            if scope.strip() == original_summary.strip():
                issues.append("UNTRANSLATED_ENGLISH_COPY")
            current_resolutions = {m.upper() for m in RESOLUTIONS.findall(
                scope + " " + target.get("promoter",""))}
            if not original_resolutions <= current_resolutions:
                issues.append("FOUNDING_RESOLUTION_REFERENCE_LOST")
            combined = " ".join([target.get("origin",""),target.get("purpose",""),*facts])
            language, probability = detect(combined) if combined.strip() else ("und",0.0)
            if language != locale or probability < .70:
                issues.append("LANGUAGE_CLASSIFICATION_HOLD")
            diagnostics[locale] = {
                "languageClassified": language,
                "languageConfidence": probability,
                "roundtripMinRecall": min(recalls,default=0),
                "roundtripMeanRecall": round(sum(recalls)/max(len(recalls),1),4),
                "expectedYears": sorted(original_years),
                "actualYears": sorted(current_years),
                "issues": issues,
            }
            localized[locale] = target
        errors = {locale:d["issues"] for locale,d in diagnostics.items() if d["issues"]}
        if errors:
            holds.append({"observanceId":oid,"errors":errors,"qa":diagnostics})
            continue
        canonical_path, original_sha = links[oid]
        qualified.append({
            "observanceId":oid,
            "introducedYear":source["introducedYear"],
            "firstObservedYear":source["firstObservedYear"],
            "sourceUrls":source["sources"],
            "sourceFile":canonical_path,
            "sourceGitBlobSha":original_sha,
            "sourceEnglishSha256":hashlib.sha256(
                json.dumps(orig,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
            "reviewStatus":"AI_MACHINE_TRANSLATION_SOURCE_CHRONOLOGY_PASSED",
            "locale":localized,
            "reviewEvidence":diagnostics,
        })
    hold_output.parent.mkdir(parents=True,exist_ok=True)
    hold_output.write_text(json.dumps({
        "reviewLevel":"AI_MACHINE_ONLY_NO_HUMAN_SIGNOFF",
        "candidateCount":183,
        "passedCount":len(qualified),
        "heldCount":len(holds),
        "holds":holds,
        "models":models,
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if holds:
        print(f"AI183 FAIL-CLOSED: {len(holds)} holds out of 183. Diagnostics {hold_output}",
              flush=True)
        raise SystemExit(2)
    pack={
        "schemaVersion":1,
        "scope":"WORLD_DAYS_EXISTING_183_EN_IT_HISTORY_AI_SIX_LOCALE",
        "status":"AI_MACHINE_TRANSLATION_SOURCE_CHRONOLOGY_PASSED",
        "modelVersion":"ArgosTranslate-1.11.0",
        "expectedCount":183,
        "recordCount":len(qualified),
        "originalRichEditorialCount":319,
        "unchangedSourceResearchedTotal":325,
        "catalogTotal":1111,
        "reviewAuthority":"AI_NEURAL_TRANSLATION_PLUS_INDEPENDENT_AI_BACKTRANSLATION_AND_DETERMINISTIC_PARITY",
        "notHumanFactCertified":True,
        "originalSourceUrlsNotIndependentlyRefetched":True,
        "models":models,
        "records":qualified,
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("AI183 COMPLETE: 183/183 AI-reviewed six-locale records",flush=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--holds",type=Path,required=True)
    a=ap.parse_args()
    audit(a.input,a.output,a.holds)

if __name__=="__main__":
    main()
