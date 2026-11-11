# Wave05 — Dedup audit corretto (2026-11-09)

Baseline: `main@9e312432b7fb46be1fc66437587d4cbe49033ad9` = **456 ricorrenze** (282 globali + 174 nazionali).

## Esito delle 22 candidate iniziali

- **18** già presenti nel generatore globale con lo stesso titolo canonico. Include `International Day of the World's Indigenous Women and Girls`: nel sorgente la chiamata `fixed("...")` usa virgolette doppie e il primo grep l'aveva omessa.
- **1** già presente con denominazione estesa: `World AMR Awareness Week` = `World Antimicrobial Resistance Awareness Week`.
- **3** candidate residue UNESCO, **non integrate** e ancora soggette a confronto completo con i 456 record generati.

| Candidate | Ricorrenza | Fonte istituzionale | Stato |
|---|---|---|---|
| World Day of Romani Language | 5 novembre | https://www.unesco.org/en/days/list | RESEARCH_ONLY |
| International Day against Illicit Trafficking in Cultural Property | 14 novembre | https://www.unesco.org/en/days/against-illicit-trafficking | RESEARCH_ONLY |
| International Day of Islamic Art | 18 novembre | https://www.unesco.org/en/days/islamic-art | RESEARCH_ONLY |

Il pack storico `data/research/wave05_four_official_candidates_20261109.json` contiene ora **3 record** (`recordCount=3`), non quattro. Il nome file è mantenuto per stabilità della PR, non esprime il conteggio attuale.

## QA e limiti

- `tool/check_wave05_candidates.py`: verifica sintattica AST dei titoli Python, lettura delle sorgenti JSON di mercato, collisioni di slug e presenza delle sei lingue; non esegue dedup semantico completo su output generato.
- `.github/workflows/wave05-research-check.yml`: workflow PR dedicato, da verificare su exact HEAD; **nessun PASS dichiarato senza esecuzione**.
- Le traduzioni sono bozze non revisionate da madrelingua.
- Le fonti e gli anni di proclamazione non equivalgono automaticamente all'anno di prima celebrazione.
- Per l'ONU AI Day il 31 agosto è osservato dal 2027; per WHO World Prematurity Day il 15 novembre vale dal 2026. Non inserire dati falsi per anni precedenti.
- Nessuna modifica ai 456 record runtime, ai generatori di asset, ad APK, Play o pubblicazione.

## Gate prima dell'ammissione

1. Eseguire script CI e correggere eventuali errori.
2. Confrontare titoli, ID e alias contro **l'output completo** di 456 record, non solo contro i sorgenti.
3. Verificare le tre pagine ufficiali, ricorrenze e anno di introduzione con prova primaria.
4. Integrare localizzazioni EN/IT/ES/FR/DE/PT e test di ricorrenza 2026–2028 in una **PR contenuti separata**.
5. Mergiare soltanto con gate exact-head verdi e nessun conflitto.

Obiettivo: >=1000 identità uniche. **544** mancanti, invariati in questa PR di sola ricerca.
