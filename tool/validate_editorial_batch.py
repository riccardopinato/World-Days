#!/usr/bin/env python3
"""Source provenance and six-locale editorial QA for the current research batch."""
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
batch = json.loads((ROOT / "data/editorial/batches/un_primary_2026_11_03_02.json").read_text(encoding="utf-8"))
LOCALES = {"en", "it", "es", "fr", "de", "pt"}
ALLOWED_HOSTS = {
    "www.un.org", "un.org", "www.unesco.org", "digitallibrary.un.org",
    "mandates.un.org",
}
assert batch["batchId"] == "UN-PRIMARY-2026-11-03-02"
assert batch["datasetVersion"] == "2026.11.03.3"
assert batch["reviewedAt"] == "2026-11-03"
rows = batch["entries"]
evidence = batch["establishment"]
assert len(rows) == 14 and len(evidence) == 14
ids = [item["id"] for item in rows]
assert len(ids) == len(set(ids))
sources = {item["id"]: item for item in evidence}
assert set(ids) == set(sources)

new_articles = {
    "international-mother-language-day",
    "international-day-of-happiness",
    "world-autism-awareness-day",
    "international-day-of-families",
    "international-youth-day",
    "international-day-of-democracy",
    "international-day-of-older-persons",
    "international-day-of-persons-with-disabilities",
    "international-volunteer-day-for-economic-and-social-development",
    "international-anti-corruption-day",
    "international-literacy-day",
}
assert len(new_articles) == 11

for row in rows:
    id = row["id"]
    assert set(row["translations"]) == LOCALES, (id, "missing locale")
    record = sources[id]
    assert isinstance(record["year"], int) and 1900 <= record["year"] <= 2026
    url = record["source"]
    parsed = urlsplit(url)
    assert parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS
    assert not parsed.username and not parsed.password
    assert parsed.path not in ("", "/"), (id, "nonspecific source")
    english = row["translations"]["en"]
    for locale, copy in row["translations"].items():
        assert copy["hook"] and len(copy["hook"]) >= 22, (id, locale, "hook")
        assert len(copy["origin"]) >= 145, (id, locale, "origin")
        assert len(copy["whyThisDate"]) >= 44, (id, locale, "date story")
        assert copy["origin"] != english["origin"] or locale == "en", (
            id, locale, "untranslated origin",
        )
        if id in new_articles:
            assert len(copy["summary"]) >= 90, (id, locale, "summary")
            assert len(copy["whyItMatters"]) >= 100, (id, locale, "why")
            actions = copy["waysToTakePart"]
            assert len(actions) == 2 and all(len(a) >= 35 for a in actions)
        assert str(record["year"]) in copy["origin"], (id, locale, "year omitted")
    if id == "international-day-of-peace":
        for item in row["translations"].values():
            assert "1981" in item["origin"] and "2001" in item["origin"]
    if id == "human-rights-day":
        for item in row["translations"].values():
            assert "1948" in item["origin"] and "1950" in item["origin"]
    if id == "international-mother-language-day":
        for item in row["translations"].values():
            assert "1952" in item["origin"] and "1999" in item["origin"]

print(f"source batch ok: {len(rows)} histories x 6 locales; 14 source-backed years")
