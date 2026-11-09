#!/usr/bin/env python3
"""Wave05 content admission gate: catalog identities, provenance and real 2026-28 dates.

Independent of rich editorial approval and mobile release. Needs build_dataset.py first.
"""
import json
from datetime import date, timedelta
from pathlib import Path
from market_wave05 import EXPECTED, load_wave05_japan, occurrence

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "assets/data/official_core.json").read_text(encoding="utf-8"))
occurrences = json.loads((ROOT / "assets/data/occurrences_2026.json").read_text(encoding="utf-8"))
records = catalog["records"]
by_id = {r["id"]: r for r in records}
assert len(records) == len(by_id) == 492
assert catalog["datasetVersion"] == "2026.11.09.8"
assert len([r for r in records if r["scope"] == "GLOBAL"]) == 285
assert len([r for r in records if r["scope"] == "NATIONAL"]) == 207

expected = {
    "world-day-of-romani-language": ("GLOBAL", "", "2026-11-05", 2015,
        "https://www.unesco.org/es/days/romani-language"),
    "international-day-against-illicit-trafficking-in-cultural-property":
        ("GLOBAL", "", "2026-11-14", 2019,
            "https://www.unesco.org/en/days/against-illicit-trafficking"),
    "international-day-of-islamic-art": ("GLOBAL", "", "2026-11-18", 2019,
        "https://www.unesco.org/en/days/islamic-art"),
    "japan-coming-of-age-day": ("NATIONAL", "JP", "2026-01-12", 1948,
        "https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku.html"),
    "japan-emperors-birthday": ("NATIONAL", "JP", "2026-02-23", None, None),
    "japan-showa-day": ("NATIONAL", "JP", "2026-04-29", 2007,
        "https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku.html"),
}
locs = {"en", "it", "es", "fr", "de", "pt"}
for ident, (scope, country, when, year, evidence_url) in expected.items():
    r = by_id[ident]
    assert r["scope"] == scope and r["countries"] == ([country] if country else [])
    assert r.get("introducedYear") == year
    assert r.get("introducedYearSource") == evidence_url
    assert r["editorialStatus"] == "STUB", ident
    assert set(r["localizedTitles"]) == locs
    assert all(r["localizedTitles"][l].strip() for l in locs)
    assert r["localizedTitles"]["en"] == r["canonicalTitleEn"]
    assert all(s["url"].startswith("https://") for s in r["sources"])
    assert any(s["tier"] == "A_PRIMARY" for s in r["sources"])
    if scope == "GLOBAL":
        assert r["authority"]["name"] == "UNESCO"
        assert r["authority"]["officiality"] == "OFFICIAL_UNESCO"
    else:
        assert r["authority"]["type"] == "GOVERNMENT"
        assert r["authority"]["officiality"] == "OFFICIAL_INSTITUTIONAL"
    generated = [o for o in occurrences["occurrences"] if o["observanceId"] == ident]
    assert len(generated) == 1 and generated[0]["startDate"] == when, ident
    rule = r["recurrenceRules"][0]
    if rule["kind"] == "FIXED_DATE":
        assert [date(year, rule["month"], rule["day"]).isoformat() for year in (2026, 2027, 2028)] == [
            when, when.replace("2026", "2027"), when.replace("2026", "2028")
        ], ident

japan = load_wave05_japan()
assert set(x["id"] for x in japan) == set(EXPECTED)
assert len([r for r in records if r["countries"] == ["JP"]]) == 13

assert all(x["observanceId"] in by_id for x in occurrences["occurrences"])
assert len(occurrences["dateIndex"]) == 365
print("WAVE05 ADMISSION QA PASS: 456 retained + 3 UNESCO + 3 Japan + 7 Japan Wave06 + 3 India Wave07 = 492; "
      "six locales, official sources, identity, date rules. "
      "Long-form human editorial and mobile release NOT certified.")
