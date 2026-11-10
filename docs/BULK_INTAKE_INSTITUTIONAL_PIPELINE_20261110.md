# World Days — Pipeline massiva per giornate istituzionali v1

**Baseline App Factory:** `App-Factory-Core@2953e9b50f5f43fbd5a1702cb41785a4235592a5` (Master v27, Golden Index v29).
**Baseline World Days:** `main@9e312432b7fb46be1fc66437587d4cbe49033ad9`, 456 record. Il branch padre #73 propone 511 record (292 globali + 219 nazionali) ma non è ancora unito. Questa PR **non aggiunge nuove giornate**: automatizza il processo per le prossime ondate da 30–50, senza superare approvazioni editoriali o rilasci.

## Procedura per i prossimi lotti

1. Ricerca su registri ufficiali **ONU, UNESCO, OMS, FAO, ILO, UNICEF, UNHCR e governi**. Estrarre in un solo passaggio il calendario dell'istituzione. Il solo link non dimostra la lettura della singola giornata: conservare nome ed estratto puntuale della data.
2. Preparare un file JSON conforme a `data/intake/institutional_batch_template.json` con `batchId`, `count` e fino a **50 record**. Ogni riga contiene ID, Paese/ambito, sei titoli localizzati, regola annuale e le date 2026–2028, attestazioni con `originId` per identificare documenti ripubblicati, fonte primaria e stato editoriale.
3. **Un solo comando di verifica:** `python3 tool/bulk_intake.py --input data/intake/<lotto>.json --report reports/<lotto>-review.json`. Produce un rapporto machine-readable per tutti i record e indica i motivi dei blocchi. L'origine ufficiale serve a certificare la data/istituzione, non l'intera identità.
4. Un record può passare ad **ammissione** soltanto con fonte istituzionale verificata, regola pluriennale corretta, nessun duplicato di ID/titolo/alias, sei titoli, Paese supportato, decisione semantica e **approvazione editoriale qualificata realmente registrata** con reviewer e URL dell'evidenza. Il tool non compila né inventa questo campo.
5. Quando TUTTI i record del file hanno gate verdi, eseguire esplicitamente `python3 tool/bulk_intake.py --input data/intake/<lotto>.json --emit-approved`. Il file viene generato in `data/market/bulk_approved/` senza sovrascrivere un lotto approvato precedente.
6. Una nuova PR contenuti include i file del lotto e il rapporto. Il generatore `tool/build_dataset.py` carica **automaticamente** tutti i nuovi file approvati, sia GLOBAL sia NATIONAL, con le sei traduzioni. Il contratto `tool/catalog_source_contract.py` ricalcola le quantità e la versione senza modificare a mano sei validatori e i test Flutter. **CI exact-head** obbligatoria: catalogo, date, Flutter analyze/test, Europe/Rome e build Web; nessun APK o deploy automatico.

## Perché cinque siti uguali non bastano

- Pagine che riprendono lo stesso comunicato/decreto e hanno lo stesso `originId`: **una sola fonte documentale**.
- Una fonte direttamente dell'istituzione competente, con **voce e data effettivamente verificate**, è sufficiente come prova della data per l'anno 2026.
- Anche una fonte con data discordante blocca automaticamente il record; la concordanza di cinque siti secondari non prevale sul conflitto.
- `FIXED_DATE`, `NTH_WEEKDAY` e `LAST_WEEKDAY` sono supportati per ricorrenze annuali dimostrate. Date lunari, astronomiche, intercalari, sostituzioni festive e casi specifici dell'anno richiedono **un altro gate**; il sistema li blocca anziché inventare il 2027/2028.
- Il nome di una giornata in un elenco ONU può già esistere in app con un altro alias: rimane necessaria la decisione di unicità semantica, oltre al confronto automatico degli ID e titoli.
- **Un link HTTPS e un excerpt nel JSON sono attestazioni registrate, non una nuova consultazione in rete del tool Python.** Il ricercatore/revisore deve aver realmente controllato la fonte primaria. Il controllo dei domini riusa host primari del catalogo esistente; un nuovo host istituzionale non verificato viene bloccato.

## Test che NON vanno aggiornati per ogni lotto

`data/catalog_source_contract.json` rappresenta la base congelata a 456 record e le singole fonti incrementalmente approvate (Wave05–09 e 10 ID globali istituzionali). Il contratto aggrega le aggiunte in modo indipendente dal contenuto runtime:
- `tool/catalog_source_contract.py` confronta il totale **dichiarato dalle sorgenti** con quello **generato** e preserva gli ID incrementali.
- `tool/validate_dataset.py` e `tool/market_coverage.py` non confrontano più `511` scritto manualmente, ma l'output del contratto.
- I validatori Wave05–10 conservano le **date, le identità e le verifiche specifiche**, ma non hanno più totali generali statici.
- `tool/build_dataset.py`, `tool/build_editorial.py` e `tool/build_editorial_locales.py` condividono una versione calcolata a partire dalla base e dal numero di nuovi lotti approvati.
- I test Dart sul mercato globale e i widget mantengono i **minimi storici da preservare**, ricavando i totali correnti dal catalogo realmente caricato.
- `tool/test_bulk_intake.py` contiene casi completamente **sintetici**: 50 record, cinque siti che copiano un documento, fonte contraddittoria, alias già presente, paese non supportato, anni non coerenti, lingua incompleta e approvazione mancante. Non sono giornate reali.

## Stato di certificazione

- `RESEARCH_ONLY_BLOCKED`: record ricercato ma non ammissibile, con motivazioni individuali.
- `ELIGIBLE`: i controlli strutturali/attestazioni e la revisione dichiarata nel file sono completi; non sostituisce la verifica umana effettiva.
- `HUMAN_EDITORIAL_APPROVED_AND_SOURCE_VERIFIED`: ammesso in file source-only esplicitamente dopo validazione, pronto per PR e test. **Non implica `REVIEWED` della storia lunga.**
- `MERGED`: soltanto dopo CI exact-head, approvazioni richieste e merge effettivo.
- `RELEASED`: soltanto dopo deployment verificato. Sospesi APK, Android, Google Play e deploy pubblico.

**Nessuna automazione schedulata**, nessun uso di Work. Tutte le operazioni restano in Chat e i lotti non vengono messi in produzione autonomamente.

## Files

- `tool/bulk_intake.py` — prova per record, deduplicazione e rapporto
- `data/intake/institutional_batch_template.json` — modello vuoto, nessuna falsa giornata
- `data/market/bulk_approved/` — importi con gate realmente approvati
- `tool/bulk_approved.py` — trasforma le righe ammesse in record per il generatore
- `data/catalog_source_contract.json` e `tool/catalog_source_contract.py` — conteggi e versione autonomi
- `tool/test_bulk_intake.py` — test avversariali
- `.github/workflows/bulk-intake-source-gate.yml` — verifica veloce di source
- `.github/workflows/dev-checks.yml` — suite completa per il ramo Flutter/Web
