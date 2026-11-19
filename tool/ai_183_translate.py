#!/usr/bin/env python3
"""World Days: source-pinned 183-story AI translation candidate generator.

Run only for source-researched origin histories not already represented by one
of the 319 rich editorial entries. The CPU inference models are external
build-time tools; NO model is packaged in Flutter. Output is a DRAFT until
independent AI roundtrip/review and all product validators pass.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BATCHES = ROOT / "data/editorial/batches"
LOCALES = ("es", "fr", "de", "pt")
FIELDS = ("heading", "origin", "promoter", "purpose")
YEARS = re.compile(r"\b(?:18|19|20)\d{2}\b")

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def source_inventory():
    files = [BATCHES / "origin_stories_primary_20261111.json"]
    # Historical 183-story inventory is frozen at Wave20; Wave21+ are drafts.
    files += sorted(p for p in BATCHES.glob("origin_stories_wave*.json")
                    if re.fullmatch(r"origin_stories_wave(?:0[1-9]|1[0-9]|20)_\d{8}\.json", p.name))
    assert len(files) == 21, ("unexpected source files", len(files))
    all_records = {}
    for path in files:
        batch = load(path)
        assert batch["status"] == "SOURCE_CHECKED_EDITORIAL_NOT_1111_ALL_COMPLETE", path
        assert batch["count"] == len(batch["records"])
        for item in batch["records"]:
            oid = item["observanceId"]
            assert oid not in all_records, ("duplicate", oid)
            assert {"en", "it"} <= set(item["locale"])
            assert item["sources"] and all(
                urlsplit(u).scheme == "https" and urlsplit(u).netloc
                for u in item["sources"]
            )
            for language in ("en", "it"):
                text = item["locale"][language]
                assert all(isinstance(text[k], str) and text[k].strip()
                           for k in FIELDS), (oid, language)
                assert 2 <= len(text["facts"]) <= 5
            all_records[oid] = item
    assert len(all_records) == 325, len(all_records)
    rich = load(ROOT / "assets/data/editorial_en.json")
    ids = {r["observanceId"] for r in rich["entries"]}
    assert len(ids) == rich["entryCount"] == 319, "Must generate 319 baseline before translation"
    pending = {oid: r for oid, r in all_records.items() if oid not in ids}
    assert len(pending) == 183, (len(pending), "strict inventory mismatch")
    return dict(sorted(pending.items()))

def get_model(from_code, to_code):
    import argostranslate.package as package
    import argostranslate.translate as translate
    available = package.get_available_packages()
    models = [p for p in available if p.from_code == from_code and p.to_code == to_code]
    if not models:
        raise SystemExit(f"No installed-or-downloadable Argos model: {from_code}->{to_code}")
    model = max(models, key=lambda p: p.package_version)
    path = model.download()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    package.install_from_path(path)
    languages = translate.get_installed_languages()
    source = next(x for x in languages if x.code == from_code)
    target = next(x for x in languages if x.code == to_code)
    return source.get_translation(target), {
        "engine": "ArgosTranslate-OpenNMT-CTranslate2",
        "languagePair": from_code + "_" + to_code,
        "packageVersion": model.package_version,
        "modelSha256": digest,
    }

def key_tokens(s):
    return set(re.findall(r"[a-z]{3,}", s.lower())) - {
        "the","and","for","with","that","are","this","its","from","their",
        "has","was","were","had","about","into","those","which","have","but",
        "then","over","also","while","would","year","day","days"
    }

def roundtrip_overlap(src, english_return):
    a, b = key_tokens(src), key_tokens(english_return)
    return round(len(a & b) / max(1, len(a)), 4)

def translate_locale(locale, destination):
    if locale not in LOCALES:
        raise SystemExit("Target must be one of es/fr/de/pt")
    inventory = source_inventory()
    import argostranslate.package as package
    package.update_package_index()
    forward, model = get_model("en", locale)
    backward, reverse = get_model(locale, "en")
    translated = []
    for i, (oid, row) in enumerate(inventory.items(), 1):
        original = row["locale"]["en"]
        target = {field: forward.translate(original[field]) for field in FIELDS}
        target["facts"] = [forward.translate(f) for f in original["facts"]]
        # A second independent AI inference pass checks the translation via
        # target->English backtranslation. Chronology/identity checks are
        # enforced again by the offline assembler before publication.
        probes = [original["purpose"], *original["facts"]]
        translations = [target["purpose"], *target["facts"]]
        roundtrips = [backward.translate(t) for t in translations]
        scores = [roundtrip_overlap(s, t) for s,t in zip(probes, roundtrips)]
        src_years = set(YEARS.findall(" ".join(
            [original["origin"], original["purpose"], *original["facts"]])))
        dst_years = set(YEARS.findall(" ".join(
            [target["origin"], target["purpose"], *target["facts"]])))
        translated.append({
            "observanceId": oid,
            "locale": locale,
            "translations": target,
            "aiRoundtrip": {
                "purposeAndFactsEnglishTokenRecall": scores,
                "minimumRecall": min(scores),
                "sourceYears": sorted(src_years),
                "translatedYears": sorted(dst_years),
            }
        })
        if i % 10 == 0 or i == len(inventory):
            print(f"AI183 {locale}: {i}/{len(inventory)}", flush=True)
    payload = {
        "schemaVersion": 1,
        "state": "AI_TRANSLATED_PENDING_INDEPENDENT_VALIDATION",
        "catalogTotal": 1111,
        "untranslatedAtBaseline": len(inventory),
        "locale": locale,
        "forwardModel": model,
        "independentReverseModel": reverse,
        "records": translated,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(f"AI183 generated {locale}: {len(translated)} candidates -> {destination}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--locale", required=True, choices=LOCALES)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    translate_locale(args.locale, args.output)

if __name__ == "__main__":
    main()
