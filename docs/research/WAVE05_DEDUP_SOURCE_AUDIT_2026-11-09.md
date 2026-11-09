# Wave05 — Deduplicazione rigorosa e quattro nuove candidate (09/11/2026)

**BASE:** `main@9e312432b7fb46be1fc66437587d4cbe49033ad9` = 456 ID (282 GLOBAL / 174 NATIONAL).
**GATE:** RESEARCH ONLY; **0** nuove ricorrenze pubblicate. Non confondere le candidate con la copertura dell'app.

## Risultato della prima deduplicazione

Sulle 22 voci della ricerca preliminare, il confronto con le chiamate canoniche `fixed/rng/nth/lastwd/...` di `tool/build_dataset.py` mostra:
- **17 corrispondenze testuali dirette** già implementate: voci #1, #3–#12, #16–#21.
- **1 corrispondenza semantica/alias**: #22 «World AMR Awareness Week» = `World Antimicrobial Resistance Awareness Week` già nel generatore. NON aggiungere come nuova identità.
- **4 candidate non presenti con il medesimo titolo nel generatore globale**: #2, #13, #14, #15. Richiedono verifica di `market_expansion`, alias e pack finale prima dell'ammissione. Non chiamarle ancora «4 nuove giornate integrate».

### Quattro schede candidate con fonti individuali

| Ricorrenza | Data annuale | Origine e status | Anno di proclamazione documentabile | Fonte primaria | Stato |
|---|---|---|---|---|---|
| International Day of the World's Indigenous Women and Girls | 5 settembre | ONU, Assemblea Generale, A/RES/80/10 | 2025 | https://www.un.org/en/observances/indigenous-women-day | Global candidate; duplicate check partial |
| World Day of Romani Language | 5 novembre | UNESCO, Conferenza Generale 38a | 2015 | https://www.unesco.org/es/days/romani-language | Global candidate; duplicate check partial |
| International Day against Illicit Trafficking in Cultural Property | 14 novembre | UNESCO, Conferenza Generale 40a | 2019 | https://www.unesco.org/en/days/against-illicit-trafficking | Global candidate; duplicate check partial |
| International Day of Islamic Art | 18 novembre | UNESCO, Conferenza Generale 40a | 2019 | https://www.unesco.org/en/days/islamic-art | Global candidate; duplicate check partial |

**Nota cronologica:** «anno di proclamazione» non implica automaticamente prima celebrazione. Il campo `introducedYear` del catalogo va compilato solo dopo avere verificato l'esatto significato richiesto dallo schema.

### Revisione dati esistenti: due date importanti

- `International Day of Safe, Secure and Trustworthy Artificial Intelligence` esiste già. A/RES/80/302 proclama **31 agosto** con osservanza **a partire dal 2027**: https://mandates.un.org/mandate/A/RES/80/302. Evitare una falsa celebrazione 2026.
- `World Prematurity Day` esiste già. L'OMS indica **15 novembre dal 2026**, in precedenza 17 novembre: https://www.who.int/campaigns/world-prematurity-day/2026. Verificare e correggere eventuali record/test di anni precedenti, senza introdurre una seconda giornata.

## Coverage math on exact source

| Stage | Global current | National current | Totale nel runtime | Candidati unici ammissibili adesso |
|---|---:|---:|---:|---:|
| HEAD main | 282 | 174 | **456** | 0 |
| Research after screening | 282 | 174 | **456** | **4 da verificare**, non aggiunte |
| If all 4 pass admission | 286 | 174 | **460** | Condizionale, non attuale |

Restano almeno **544** nuove identità fino a 1000. Le fonti ONU/UNESCO/OMS da sole non sono sufficienti a sostenere l'espansione: le 18 già presenti tra 22 candidate mostrano l'alto tasso di sovrapposizione. Priorità successiva: registri statali / commemorazioni regionali con perimetro geografico chiaro e classificazione diversa dagli eventi mondiali.

## Release-gate per implementazione successiva

1. Estrarre **tutti** i 456 ID generati, inclusi `market_catalog` e `market_expansion` e controllare titolo/alias/regole/autorità (non basta grep).
2. Eseguire match letterali e semantici per le 4 candidate, poi creare ID canonici solo se indipendenti.
3. Tradurre EN/IT/ES/FR/DE/PT, con `overview` e provenance; mantenere flag editoriale separato per storie lunghe.
4. Verificare recurrence 2026–2028, condizioni 2027 per AI, e vecchia data OMS per gli anni passati.
5. Eseguire CI esatta su branch e solo allora una PR contenuti separata (non dichiarare PASS qui).

Nessuna modifica a APK, Play, signing, billing, advertising, dati utente o runtime.
