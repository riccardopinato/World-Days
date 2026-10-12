#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "discovery" / "sources"
OUT = ROOT / "data" / "discovery" / "discovery_backlog.json"
REPORT = ROOT / "docs" / "DISCOVERY_DATA_REPORT.md"
CORE = ROOT / "assets" / "data" / "official_core.json"
OCC = ROOT / "assets" / "data" / "occurrences_2026.json"

MONTHS = {
    "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4,
    "maggio": 5, "giugno": 6, "luglio": 7, "agosto": 8,
    "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12,
}
GENERIC = re.compile(
    r"(?i)\b(giornata|giorno|giornate|mondiale|mondiali|internazionale|internazionali|"
    r"europea|europeo|nazionale|world|international|day|della|delle|degli|dei|del|di|"
    r"per|contro|alla|alle|al|agli|il|la|le|lo|l)\b"
)


def text_key(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace("’", "'")
    value = GENERIC.sub(" ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def raw_key(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def fixed_date_hint(label: str) -> str | None:
    value = raw_key(label)
    for month_name, month in MONTHS.items():
        if month_name not in value:
            continue
        match = re.search(r"\b(\d{1,2})\b", value)
        if not match:
            return None
        day = int(match.group(1))
        try:
            date(2026, month, day)
        except ValueError:
            return None
        return f"2026-{month:02d}-{day:02d}"
    match = re.fullmatch(r"(\d{2})-(\d{2})", label.strip())
    if match:
        month, day = map(int, match.groups())
        try:
            date(2026, month, day)
        except ValueError:
            return None
        return f"2026-{month:02d}-{day:02d}"
    return None


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_observations() -> list[dict]:
    observations: list[dict] = []
    for path in sorted(SOURCE_DIR.glob("*.json")):
        payload = load_json(path)
        observations.extend(payload.get("observations", []))
    return observations


def official_by_date() -> dict[str, list[str]]:
    occurrence = load_json(OCC)
    result: dict[str, list[str]] = defaultdict(list)
    for item in occurrence.get("occurrences", []):
        start = item.get("startDate")
        end = item.get("endDate")
        oid = item.get("observanceId")
        if not start or not end or not oid:
            continue
        cursor = date.fromisoformat(start)
        finish = date.fromisoformat(end)
        while cursor <= finish:
            if cursor.year == 2026:
                result[cursor.isoformat()].append(oid)
            cursor = date.fromordinal(cursor.toordinal() + 1)
    return result


def main() -> None:
    observations = load_observations()
    by_date = official_by_date()
    core = load_json(CORE)
    canonical_ids = {record["id"] for record in core.get("records", [])}

    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in observations:
        title = item.get("rawTitleIt", "")
        date_label = item.get("rawDateLabel", "")
        tkey = text_key(title)
        if not tkey:
            continue
        fixed = fixed_date_hint(date_label)
        dkey = fixed or raw_key(date_label)
        groups[(dkey, tkey)].append(item)

    candidates = []
    crosscheck_only_count = 0
    for index, ((dkey, tkey), items) in enumerate(sorted(groups.items()), start=1):
        fixed = fixed_date_hint(items[0]["rawDateLabel"])
        source_ids = sorted({i["sourceId"] for i in items})
        crosscheck_only = all(bool(i.get("crosscheckOnly")) for i in items)
        if crosscheck_only:
            crosscheck_only_count += 1
            continue
        possible = sorted(set(by_date.get(fixed, []))) if fixed else []
        possible = [value for value in possible if value in canonical_ids]
        review = [
            "verify originator/authority",
            "normalize canonical English title",
            "verify recurrence rule",
            "deduplicate aliases against canonical and discovery records",
            "classify officiality without upgrading from discovery evidence",
        ]
        if possible:
            review.insert(0, "review possible canonical collision on the same 2026 date")
        if fixed is None:
            review.insert(0, "resolve non-fixed or ambiguous date expression")
        candidates.append({
            "candidateId": f"discovery-{index:04d}",
            "rawDateLabels": sorted({i["rawDateLabel"] for i in items}),
            "fixedDateHint2026": fixed,
            "rawTitlesIt": sorted({i["rawTitleIt"] for i in items}),
            "normalizedTitleKey": tkey,
            "sources": [
                {
                    "sourceId": i["sourceId"],
                    "sourceUrl": i["sourceUrl"],
                    "sourceTier": i["sourceTier"],
                    "sourceKind": i["sourceKind"],
                }
                for i in sorted(items, key=lambda x: (x["sourceId"], x["rawTitleIt"]))
            ],
            "sourceCount": len(source_ids),
            "possibleCanonicalIds": possible,
            "status": "DISCOVERY_UNVERIFIED",
            "publishByDefault": False,
            "reviewNeeded": review,
        })

    candidates.sort(key=lambda x: (x["fixedDateHint2026"] or "9999", x["normalizedTitleKey"]))
    for i, item in enumerate(candidates, start=1):
        item["candidateId"] = f"discovery-{i:04d}"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schemaVersion": 2,
        "dataset": "world-days-discovery-backlog",
        "policy": {
            "publishByDefault": False,
            "officialityRule": "Discovery sources never upgrade officiality. Verify against the originator or a primary institutional source first.",
            "matchingRule": "possibleCanonicalIds are review hints based on date collision, never automatic merges.",
        },
        "observationCount": len(observations),
        "candidateCount": len(candidates),
        "crosscheckOnlyGroupCount": crosscheck_only_count,
        "items": candidates,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    source_counts = defaultdict(int)
    for item in observations:
        source_counts[item["sourceId"]] += 1
    multi_source = sum(1 for item in candidates if item["sourceCount"] >= 2)
    possible_collision = sum(1 for item in candidates if item["possibleCanonicalIds"])
    unresolved_date = sum(1 for item in candidates if item["fixedDateHint2026"] is None)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "# World Days — Discovery Data Report\n\n"
        "Generated by `tool/build_discovery.py`. Discovery data is not automatically publishable.\n\n"
        f"- Raw source observations: **{len(observations)}**\n"
        f"- Unified discovery candidates: **{len(candidates)}**\n"
        f"- Cross-check-only groups excluded from discovery backlog: **{crosscheck_only_count}**\n"
        f"- Candidates seen in 2+ sources: **{multi_source}**\n"
        f"- Candidates with same-date canonical collision hints: **{possible_collision}**\n"
        f"- Candidates with unresolved/movable date expressions: **{unresolved_date}**\n\n"
        "## Source observations\n\n"
        + "\n".join(f"- `{key}`: {value}" for key, value in sorted(source_counts.items()))
        + "\n\n## Publication rule\n\n"
        "Every candidate remains `DISCOVERY_UNVERIFIED` with `publishByDefault=false` until originator, recurrence, deduplication, and officiality are manually verified.\n",
        encoding="utf-8",
    )
    print(f"discovery: {len(observations)} observations -> {len(candidates)} candidates")


if __name__ == "__main__":
    main()
