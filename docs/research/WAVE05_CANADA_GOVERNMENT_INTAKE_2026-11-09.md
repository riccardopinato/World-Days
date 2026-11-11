# Wave05 — Canada government observances intake

**Status: RESEARCH_ONLY. Runtime stays 456.** Research JSON: `data/research/wave05_canada_official_calendar_20261109.json` (12 candidates, source links and legal-tier classifications). None is approved as an additional unique observance.

Primary register: https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days.html (Canadian Heritage, updated June 2026). It mixes official commemorative dates, awareness days and observances of different legal status. Do **not** label all items statutory holidays or UN days.

Independent higher-specificity sources:
- National Day of Remembrance for Victims of Air Disasters (8 Jan): https://laws.justice.gc.ca/eng/regulations/SI-2021-2/page-1.html (statutory instrument SI/2021-2).
- National Day of Remembrance of the Québec City Mosque Attack (29 Jan): https://laws-lois.justice.gc.ca/eng/regulations/SI-2021-17/page-1.html (SI/2021-17).
- Sir John A. Macdonald Day (11 Jan): https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days/sir-john-macdonald-day.html (2002 Act).
- British Home Child Day (28 Sep): https://www.ourcommons.ca/members/en/guy-lauzon(25516)/motions/8853980 (House motion adopted 2018, **not** a statutory proclamation).
- Persons Day (18 Oct): https://women-gender-equality.canada.ca/en/commemorations-celebrations/womens-history-month/persons-day.html (1929 is the historical case, **not** a verified establishment year).
- National Day of Remembrance and Action on Violence Against Women (6 Dec): https://www.canada.ca/en/women-gender-equality/commemorations-celebrations/16-days/national-day-remembrance.html (1989 is the tragedy year, **not** the designation year).

### Preliminary overlap check
Searched literal English names against `tool/build_dataset.py`, `tool/market_catalog.py` and `tool/market_expansion.py`; **0 exact literal matches among these 12**. This is not sufficient to prove unique IDs: the 174 market entries include JSON packs and alternate canonical titles. The new intake has no six-locale titles, editorial histories, generated assets or CI integration.

### Next admission gate
1. Compare all 12 against generated `official_core.json` canonical IDs, aliases and semantic equivalents; drop any duplicate, including different names for the same event.
2. Check source-defined legal classification and fixed/moving recurrence for 2026–2028.
3. Prepare six-locale titles, editorial source citations, appropriate introduced-year `*` where no verified establishment evidence.
4. Add selected records through the market source layer, preserve ID stability and all existing 456.
5. Run exact-head dataset, Flutter and country UI tests. Keep APK/Play paused.

### Progress
456 existing + 3 UNESCO research candidates + 12 Canada research candidates (**15 candidate records, 0 admitted**). The gap to 1000 is still **544**. Prioritize Canada national calendar and additional government registers; avoid generic cultural dates as national statutory days.
