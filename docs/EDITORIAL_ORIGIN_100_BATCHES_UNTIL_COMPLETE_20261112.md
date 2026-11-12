# World Days — completamento delle storie per blocchi di 100

**Avvio:** 12 novembre 2026. **Modalità:** solo Chat; dati e sorgenti canoniche su GitHub.

## Numeri all'avvio

- **1.111** ricorrenze canoniche su `main` al checkpoint.
- **4** storie di origine individualmente ricercate in IT/EN (ES/FR/DE/PT ancora bozze non certificate).
- **1.107** identità senza ricerca di origine certificata nel nuovo registro.
- **12 blocchi di lavoro**: undici da 100 e uno da 7, se la base resta a 1.111 e non vengono approvate altre storie.
- **56** storie editoriali precedenti `REVIEWED`, che non equivalgono automaticamente a 56 origini storiche indipendentemente ricertificate.

## Percorso operativo

`tool/editorial_origin_completion_waves.py` crea un report completo,
`reports/editorial_origin_completion/index.json` e i `batch_001.json` …
`batch_012.json`, usando esclusivamente gli ID effettivi del catalogo generato.

Il blocco 001 riutilizza i 100 dossier della Wave100 integrata via PR #93,
senza ricominciare o ricertificarli. I successivi raccolgono tutte le identità
restanti, incluse le bozze editoriali da finalizzare, quelle già pubblicate con
origine da ricertificare e i record nazionali con fonti a rischio da verificare.

Ogni blocco contiene non più di 100 ID, senza duplicati; se le ricorrenze
aumentano oltre 1.111, il generatore ricalcola il numero di blocchi.
Se una storia ottiene effettivamente una ricostruzione di origine certificata,
l'ID viene escluso dal backlog alla successiva generazione.

## Protocollo per rendere *finita* una storia

1. Controllare la specifica pagina/atto di fonte **primaria** e identità e data
   della ricorrenza. La presenza di una URL nel catalogo non basta.
2. Distinguere fatto storico commemorato, fondazione della giornata, prima
   osservanza e revisione successiva del calendario.
3. Documentare perché è stata scelta quella data; ente che ha deliberato,
   promotore effettivo **solo se provato**, scopo e 2–5 fatti verificabili.
4. Scrivere il racconto originale in inglese e italiano; tradurre ES/FR/DE/PT
   con verifica semantica e linguistica.
5. Collegare fonti puntuali, salvare lo stato bozza/revisione/approvazione;
   mai marcare come `REVIEWED` un semplice dossier o una traduzione non rivista.
6. Far passare validazioni Python, Flutter e Web, feedback revisori,
   branch protection e solo dopo integrare in `main` tramite PR.

## Protezioni e limiti

- **Blocchi generati** ≠ **storie redatte** ≠ **storie certificate** ≠ **storie pubblicate**.
- Se anno, promotore o spiegazione della data non sono dimostrati, restano `null`
  o `*`; niente prose storiche inventate né feste nazionali dedotte da
  EURES/DFAT/NCCA.
- I dati delle 56 storie legacy restano nel pack esistente fino a revisione,
  senza essere marcati automaticamente come origini ricertificate.
- Nessun APK, Google Play, deploy o esecuzione nativa di produzione.

## Evidenze e test

- Generatore: `tool/editorial_origin_completion_waves.py`
- Gate di copertura: `tool/validate_editorial_origin_completion_waves.py`
- Indice e singoli lotti: `reports/editorial_origin_completion/`
- Artifact GitHub Actions: `world-days-all-origin-waves-100`

Ogni esecuzione programmata recupera lo stato reale di `main` e non presume
che la coda del giorno precedente sia ancora invariata. Si procede sui
contenuti effettivamente verificabili anche se il prossimo blocco non può
essere completato in una sola esecuzione.
