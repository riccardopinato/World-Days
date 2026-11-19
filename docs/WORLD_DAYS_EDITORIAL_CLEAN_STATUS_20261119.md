# World Days — stato editoriale pulito al 19 novembre 2026

**Fonte operativa:** `main` @ `f6b70fc2298176c950d0cda9f0d6919c66267c13`. **Universo:** 1.111 ID canonici, senza conteggiare i duplicati fra wave, lingue e PR sorgente.

| Classe esclusiva per ID canonico | ID | Significato |
|---|---:|---|
| **COMPLETE_SIX_LOCALES_ON_MAIN** | **502** | Articolo editoriale integrato in tutte le lingue EN, IT, ES, FR, DE, PT |
| **ONLY_EN_IT_ON_MAIN** | **0** | Dossier storico soltanto bilingue, non ancora integrato come editoriale a sei lingue |
| **PENDING_EDITORIAL_SIX_LOCALES** | **609** | ID canonico del catalogo senza un articolo completo in tutte e sei le lingue |
| **TOTALE CANONICO** | **1.111** | 502 + 0 + 609 |

**Completezza editoriale: 45,18%.** La classe `PENDING` comprende la mancanza del racconto completo, non la mancanza di una scheda di calendario. Non confondere il totale con **626** ID privi di *dossier storico di origine*: quel numero usa una metrica distinta, poiché 17 articoli rich legacy non appartengono all'inventario dei 485 dossier storici preparati.

## Ricostruzione completa dei 502 articoli già integrati

- **56** editorials originali del prodotto.
- **173** articoli AI_CERTIFIED per Canada, Corea del Sud e Filippine (PR #133/#134).
- **90** articoli `AI_SOURCE_REVIEWED_SIX_LOCALE`: 82 Wave20 non già presenti nei 173, cinque originali CZ/SK/IT/FI/EE e tre recuperati da Canada/altre origini (PR #135 e successive importazioni).
- **183** dossier storici già esistenti, tradotti e ricontrollati nelle quattro lingue mancanti con modello IA (PR #138).
- 56 + 173 + 90 + 183 = **502 ID editoriali unici × 6 lingue**. **0** vecchi preview rimasti esclusivamente EN/IT.

Verifiche tecniche: `tool/validate_ai_183_translations.py` richiede i medesimi **502 ID unici** in ciascuno dei sei file `assets/data/editorial_*.json`, parità di ordinamento, nessun duplicato, corrispondenza con il catalogo 1.111 e zero preview storico-bilingui; `tool/publish_ai_183_translations.py` verifica i 183 ingressi esclusivi. La CI della PR #138 e il suo merge sono documentati in `ROADMAP.md`: [CI #43667518738](https://github.com/riccardopinato/World-Days/actions/runs/43667518738), [PR #138](https://github.com/riccardopinato/World-Days/pull/138). I sei JSON sono generati dalla pipeline e non vanno scambiati per sei sorgenti statiche indipendenti committate.

## Cosa NON sommare ai completati

- **Wave20 PR #118**: la coorte 100/100 è già inglobata; 18 sovrapposizioni con 173 AI_CERTIFIED, **82** importati in PR #135. La PR sorgente è stata chiusa come già sostituita, **senza merge ridondante**.
- **PR #120**: i suoi 173 testi preparati sono già stati recuperati dai merge editoriali successivi, non sono +173 nuovi. **Sette** candidature filippine con conflitti su identità/data/atto originario restano aperte come sottoinsieme del backlog, non sette storie già complete.
- **PR #119**: 46 righe di un indice canadese ≠ 46 nuovi ID. 31 riferimenti a storie sorgente + nove riferimenti Wave20 già presenti; sei dossier sono `RESEARCH_ONLY_NOT_CANONICAL_SIX_LOCALE_DRAFT` e **non** vanno importati con un ID inventato.
- **PR #122**: i cinque dossier nazionali sono già inclusi nei 90 pubblicati.
- **PR #128**: repin del ledger di otto sorgenti Wave20, non otto nuove storie.
- **PR #140 (Wave21)**: 100 ID congelati ma **zero** nuove storie editoriali redatte nella PR; sono una coorte di lavoro, non incremento dei 502.
- Le PR storiche o quelle di ricerca non sono una quarta categoria del conteggio: contano solo gli ID realmente raggiungibili come articolo sul `main` corrente.

## Procedura snella dai 609 in sospeso

In applicazione del Fast Track editoriale del Master App Factory Core (19/11/2026): produrre storie originali e le sei traduzioni con IA, ricontrollare date/fonti/accuratezza, traduzioni e duplicati, integrare in batch nel dataset ufficiale con CI GitHub, poi aggiornare le tre classi per **ID canonico**. Non richiedere revisori professionisti esterni o certificazioni editoriali artificiali per i normali contenuti descrittivi. Trattenere **solo** i record con errori concreti irrisolti e continuare con i restanti; non dichiarare merge/pubblicazione prima di avere prova della CI e del merge.

**Questo prospetto è una riconciliazione dello stato già integrato, non l'aggiunta di nuove storie in questa PR e non un rilascio nello Store.**
