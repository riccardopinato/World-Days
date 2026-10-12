#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "discovery" / "sources"
PARSER_VERSION = 1
USER_AGENT = "WorldDaysDatasetBot/0.1 (+https://github.com/riccardopinato/World-Days)"

MONTHS = (
    "gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|"
    "settembre|ottobre|novembre|dicembre"
)
DATE_TOKEN = re.compile(
    rf"(?i)(?:\b\d{{1,2}}(?:º|°|ª|o)?\b|\bprimo\b|\bprima\b|\bsecondo\b|\bseconda\b|"
    rf"\bterzo\b|\bterza\b|\bquarto\b|\bquarta\b|\bultimo\b|\bultima\b|\b{MONTHS}\b)"
)
CELEBRATION_TOKEN = re.compile(
    r"(?i)\b(giornata|giorno|giornate|settimana|mese|day|week|memoria|festa|anniversario)\b"
)
TRAILING_DATE = re.compile(
    rf"(?i)(?P<date>(?:il\s+)?(?:\d{{1,2}}(?:º|°|ª)?(?:\s*[/\-]\s*\d{{1,2}}(?:º|°|ª)?)?\s+"
    rf"(?:{MONTHS})|(?:primo|prima|secondo|seconda|terzo|terza|quarto|quarta|ultimo|ultima)\s+[^,.;]{{0,50}}))\s*$"
)


@dataclass(frozen=True)
class Source:
    source_id: str
    url: str
    tier: str
    kind: str
    crosscheck_only: bool = False


SOURCES = [
    Source("giornatemondiali", "https://www.giornatemondiali.it/", "C_DISCOVERY", "consumer_calendar"),
    Source("wikipedia_it", "https://it.wikipedia.org/wiki/Giornate,_anni_e_decenni_internazionali", "C_DISCOVERY", "reference_calendar"),
    Source("unric_it", "https://unric.org/it/calendario-giornate-internazionali/", "B_INSTITUTIONAL", "official_crosscheck", True),
    Source("rai_scuola", "https://www.raiscuola.rai.it/percorsi/giornate", "C_DISCOVERY", "editorial_calendar"),
    Source("pineta", "https://www.pinetanatureresort.it/blog/giornate-mondiali/", "C_DISCOVERY", "consumer_calendar"),
    Source("unesco_it", "https://www.unesco.it/it/temi-in-evidenza/comunicazione-e-informazione/giornate-internazionali-dellunesco/", "B_INSTITUTIONAL", "official_crosscheck", True),
    Source("coe_compass", "https://www.coe.int/it/web/compass/human-rights-calendar", "B_INSTITUTIONAL", "mixed_human_rights_calendar"),
]

FALLBACK_OBSERVATIONS = {
    "unric_it": [
        ("15 Luglio", "Giornata Mondiale delle Capacità dei Giovani"),
        ("18 Luglio", "Giornata Mondiale per Nelson Mandela"),
        ("20 Luglio", "Giornata Mondiale degli Scacchi"),
        ("25 Luglio", "Giornata Internazionale per il Benessere giudiziario"),
        ("30 Luglio", "Giornata Mondiale contro la Tratta di Esseri Umani"),
        ("30 Luglio", "Giornata Internazionale dell'Amicizia"),
        ("9 Agosto", "Giornata Internazionale dei Popoli Indigeni"),
        ("12 Agosto", "Giornata Internazionale della Gioventù"),
        ("19 Agosto", "Giornata Mondiale dell'Aiuto Umanitario"),
        ("27 Agosto", "Giornata Mondiale dei Laghi"),
        ("5 Settembre", "Giornata Internazionale della Carità"),
        ("7 Settembre", "Giornata Internazionale dell'Aria Pulita per Cieli Azzurri"),
        ("15 Settembre", "Giornata Internazionale della Democrazia"),
        ("21 Settembre", "Giornata Internazionale della Pace"),
        ("27 Settembre", "Giornata Mondiale del Turismo"),
    ],
    "unesco_it": [
        ("3 maggio", "Giornata Mondiale per la libertà di stampa"),
    ],
    "coe_compass": [
        ("27 gennaio", "Giorno della memoria dell'olocausto"),
        ("8 febbraio", "La giornata per internet sicuro"),
        ("12 febbraio", "La giornata con le mani nel sacco"),
        ("21 febbraio", "Giornata internazionale della lingua madre"),
        ("8 marzo", "Giornata internazionale della donna"),
        ("12 marzo", "Giornata mondiale contro la censura virtuale"),
        ("21 marzo", "Giornata mondiale della poesia"),
        ("21 marzo", "Giornata internazionale per l'eliminazione della discriminazione razziale"),
        ("22 marzo", "Giornata mondiale dell'acqua"),
        ("23 marzo", "Giornata mondiale della meteorologia"),
        ("24 marzo", "Giornata mondiale della tubercolosi"),
        ("2° martedi di aprile", "Giornata Europea dell'uguaglianza dei salari"),
        ("7 aprile", "Giornata mondiale della salute"),
        ("7 aprile", "Giornata Mondiale della Memoria in onore delle vittime del genocidio in Ruanda del 1994"),
        ("28 maggio", "Giornata europea del vicinato"),
        ("29 maggio", "Giornata internazionale dei corpi di pace delle Nazioni Unite"),
        ("31 maggio", "Giornata mondiale contro il tabacco"),
        ("4 giugno", "Giornata internazionale dei bambini vittime innocenti di aggressione"),
        ("5 giugno", "Giornata mondiale dell'ambiente"),
        ("12 giugno", "Giornata mondiale contro il lavoro infantile"),
        ("17 giugno", "Giornata mondiale contro la desertificazione e la siccità"),
        ("20 giugno", "Giornata mondiale dei rifugiati"),
        ("23 giugno", "Giornata delle Nazioni Unite per il servizio pubblico"),
        ("26 giugno", "Giornata internazionale contro l'abuso di droga e il traffico illecito"),
        ("26 giugno", "Giornata internazionale delle Nazioni Unite a sostegno delle vittime di tortura"),
        ("1° sabato di luglio", "Giornata internazionale delle cooperative"),
    ],
}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\xa0", " ")).strip(" \t\r\n-|–—")


def key_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().replace("’", "'")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def looks_like_date(value: str) -> bool:
    v = clean(value)
    if len(v) > 120 or not DATE_TOKEN.search(v):
        return False
    return bool(re.search(rf"(?i)\b({MONTHS})\b", v) or re.search(r"\b\d{1,2}[º°ª]?\b", v))


def looks_like_title(value: str) -> bool:
    v = clean(value)
    return 5 <= len(v) <= 240 and bool(CELEBRATION_TOKEN.search(v))


def normalize_link_title(value: str) -> tuple[str, str] | None:
    text = clean(value)
    if not looks_like_title(text):
        return None
    match = TRAILING_DATE.search(text)
    if not match:
        return None
    date_label = clean(match.group("date"))
    title = clean(text[: match.start()])
    title = re.sub(
        r"(?i)^(?:rai scuola|da newton|medicina e salute|educazione civica|percorso(?:\s+\w+)?|"
        r"speciale|scienze|storia|filosofia|tecnologia|teatro e danza|storia dell'arte|"
        r"scienze sociali|scienze motorie|fisica|diritto|economia e finanza|webdoc|articolo|lancio|laboratorio)\s+",
        "",
        title,
    )
    title = re.sub(r"(?i)^(?:articolo|percorso|lancio|laboratorio)\s+", "", title)
    title = clean(title)
    if not looks_like_title(title):
        return None
    return date_label, title


def observation(source: Source, date_label: str, title: str, extraction: str) -> dict:
    return {
        "sourceId": source.source_id,
        "sourceUrl": source.url,
        "sourceTier": source.tier,
        "sourceKind": source.kind,
        "crosscheckOnly": source.crosscheck_only,
        "rawDateLabel": clean(date_label),
        "rawTitleIt": clean(title),
        "extraction": extraction,
    }


def extract_tables(soup: BeautifulSoup, source: Source) -> list[dict]:
    out: list[dict] = []
    for row in soup.find_all("tr"):
        cells = [clean(cell.get_text(" ", strip=True)) for cell in row.find_all(["th", "td"])]
        cells = [cell for cell in cells if cell]
        if len(cells) < 2:
            continue
        date_idx = next((i for i, cell in enumerate(cells) if looks_like_date(cell)), None)
        if date_idx is None:
            continue
        title_idx = next(
            (i for i, cell in enumerate(cells) if i != date_idx and looks_like_title(cell)),
            None,
        )
        if title_idx is None:
            continue
        out.append(observation(source, cells[date_idx], cells[title_idx], "table"))
    return out


def extract_links(soup: BeautifulSoup, source: Source) -> list[dict]:
    out: list[dict] = []
    for anchor in soup.find_all("a"):
        parsed = normalize_link_title(anchor.get_text(" ", strip=True))
        if parsed is None:
            continue
        date_label, title = parsed
        out.append(observation(source, date_label, title, "link"))
    return out


def deduplicate(items: list[dict]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []
    for item in items:
        key = (key_text(item["rawDateLabel"]), key_text(item["rawTitleIt"]))
        if not key[0] or not key[1] or key in seen:
            continue
        seen.add(key)
        out.append(item)
    out.sort(key=lambda x: (key_text(x["rawDateLabel"]), key_text(x["rawTitleIt"])))
    return out


def _fallback_items(source: Source) -> list[dict]:
    return [
        observation(source, date_label, title, "fallback_web_verified_2026-10-12")
        for date_label, title in FALLBACK_OBSERVATIONS.get(source.source_id, [])
    ]


def fetch(source: Source) -> dict:
    http_status = None
    fetch_error = None
    items: list[dict] = []
    try:
        response = requests.get(
            source.url,
            timeout=30,
            headers={"User-Agent": USER_AGENT, "Accept-Language": "it,en;q=0.8"},
        )
        http_status = response.status_code
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = deduplicate(extract_tables(soup, source) + extract_links(soup, source))
    except requests.RequestException as exc:
        fetch_error = f"{type(exc).__name__}: {exc}"

    if not items:
        items = deduplicate(_fallback_items(source))

    return {
        "schemaVersion": 1,
        "parserVersion": PARSER_VERSION,
        "source": {
            "id": source.source_id,
            "url": source.url,
            "tier": source.tier,
            "kind": source.kind,
            "crosscheckOnly": source.crosscheck_only,
        },
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "httpStatus": http_status,
        "fetchError": fetch_error,
        "usedFallback": bool(items and any(i["extraction"].startswith("fallback_") for i in items)),
        "observationCount": len(items),
        "observations": items,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary = []
    for source in SOURCES:
        payload = fetch(source)
        path = OUT / f"{source.source_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary.append({"sourceId": source.source_id, "count": payload["observationCount"]})
        print(f"{source.source_id}: {payload['observationCount']} observations")
    (OUT.parent / "snapshot_summary.json").write_text(
        json.dumps({"schemaVersion": 1, "sources": summary}, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
