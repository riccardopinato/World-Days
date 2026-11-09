# World Days — FAST SOURCE GATE v1 (9 novembre 2026)

## Obiettivo
Passare dal controllo manuale di singole pagine a un **processo per lotti da 20–40 ricorrenze** con risultati verificabili in GitHub Actions. Questo è un acceleratore della ricerca, **non un permesso di pubblicare automaticamente dati non verificati**.

## Regola dei cinque siti

**Cinque siti concordi NON equivalgono sempre a cinque fonti indipendenti.** Bisogna riconoscere la stessa origine documentale (atto, decreto, ministero, dataset originario) e contare **una sola origine** anche quando è riprodotta da molti domini.

Per la **data/periodo nel 2026**:

| Evidenza | Decisione automatica |
|---|---|
| Una fonte primaria dell'organizzatore o dell'autorità competente, con voce/date effettivamente lette | `DATE_2026_CONFIRMED_BY_ORIGINATOR` |
| Due o più fonti primarie che riprendono lo stesso decreto | Una sola origine; resta confermata la data perché esiste una fonte primaria verificata |
| Tre o più pubblicazioni realmente indipendenti e affidabili, senza atto/sito dell'organizzatore | `DATE_2026_SECONDARY_CONSENSUS_REVIEW`; verificare la fonte primaria prima di assegnare ufficialità |
| Cinque siti aggregatori che copiano lo stesso calendario | **Una** origine, `DATE_2026_INSUFFICIENT_PRIMARY_EVIDENCE` |
| Anche una fonte affidabile con data discordante | `CONFLICT_NEEDS_REVIEW`: bloccare |
| Link alla fonte senza data/voce effettivamente consultata | Evidenza incompleta: non contare come ispezione documentale |

Per **identità, ambito, ufficialità, regola annuale, anno di introduzione, alias e traduzioni** sono necessari gate separati. La sola concordanza delle date del 2026 non autorizza la stessa data nel 2027/2028 e non converte automaticamente una festività nazionale in una giornata mondiale.

## Primo batch eseguito

`data/research/source_consensus_attestations_20261109.json` contiene **17 schede**, 12 Cambogia e 5 Singapore. Per ogni voce: stringa evento pubblicata, data, URL, publisher, documento originario, classificazione della fonte e giorno di consultazione.

Risorse verificate:
- https://www.nbc.gov.kh/english/news_and_events/official_holiday.php
- https://lrc.gov.kh/en/annual-holiday-calendar-2026/
- https://www.mom.gov.sg/newsroom/press-releases/2025/0616-public-holidays-for-2026
- https://data.gov.sg/datasets?resultId=d_149b61ad0a22f61c09dc80f2df5bbec8&sort=updatedAt

Le due pagine cambogiane usano il medesimo registro delle festività nazionali 2026 e vanno raggruppate come **un'origine**; il portale open data di Singapore ripubblica il calendario MOM e va contato con **la stessa origine**. La verifica del decreto non prova l'unicità della ricorrenza; la festa del Capodanno cinese, ad esempio, può avere già un'identità condivisa nel catalogo.

`tool/score_source_consensus.py` produce `reports/research_date_consensus_2026.json` e controlla le voci contro il registro preesistente delle 121 evidenze 2026, senza aggiungere record al runtime. `tool/test_source_consensus.py` copre copie dello stesso decreto, conflitti, assenza di fonte primaria, cinque siti affidabili realmente indipendenti, URL malformati e assenza di voce verificata.

## Prossima sequenza accelerata

1. **Ricerca in blocco:** per le **104 candidate** con riscontro 2026 non già duplicate né incluse nella PR #67, ripartire dalle **42** a verifica più semplice a data/rule più semplice, lanciando gruppi di 20–40 (non micro-PR da 3). Risolvere poi le **62** con rischi semantici o calendari mobili; 9 Nepal restano in attesa della lettura del PDF ministeriale B.S. 2083.
2. **Data gate:** acquisire fonte originaria e 2026 date per tutte le voci di un calendario in una singola lettura; ulteriori fonti indipendenti soltanto per conflitti o ambiguità. Non fare 5 ricerche quando un ministero competente pubblica l'intera tabella.
3. **Identity gate:** confrontare Paese, ID, alias, significato e data nel catalogo completo (già 24 duplicati identificati). Lo stesso giorno e lo stesso Paese da soli sono un *segnale*, non dimostrano coincidenza semantica.
4. **Annual rule gate:** per FIXED_DATE verificare normativa e continuità; per lunari/astronomiche usare override ufficiali anno per anno, non dedurre date 2027/2028 per analogia.
5. **Batch source PR:** integrare 20–40 ID distinti alla volta con sei titoli localizzati, fonti e CI integrata. Consolidare le 16 giornate delle PR precedenti in una sola PR #67 verso main prima dei nuovi lotti. L'approvazione editoriale qualificata resta indipendente dai test automatici.

## Coda automatica pronta

`tool/plan_bulk_research_batches.py` produce `reports/research_fast_batches.json` dai report GitHub di deduplicazione e controllo delle date: **42 candidate in due lotti** (`FAST-01` da 30 e `FAST-02` da 12), raggruppate per Paese per verificare un registro governativo per volta. I **16 record già nella PR #67** non vengono inclusi. Ogni scheda contiene il link ufficiale, l'eventuale riscontro diretto dell'estratto e i gate mancanti. Questi lotti sono pacchetti di lavoro, **non 42 identità già certificate per il runtime**.

## Stato e protezioni

- `main`: 456; PR consolidata #67: 472 *proposti*, non ancora uniti; 24 duplicati già scoperti, 16 in PR #67, 104 ulteriori candidate 2026 (42 coda rapida, 62 complessa), 9 Nepal incomplete.
- Nessun accesso di terze parti o AI può produrre false attestazioni. Il solo URL e il numero di siti non attestano che una specifica riga del calendario sia stata verificata.
- Vietato promuovere automaticamente record di sola ricerca a `OFFICIAL_*`, `REVIEWED` o runtime: fonte originaria e controllo semantico effettivi sono obbligatori.
- Solo Chat; nessuna automazione programmata; APK, firma, Play e deploy produzione sospesi.
