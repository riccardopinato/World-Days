# World Days — avvio del primo lotto di 100 nuove storie

**Data:** 11 novembre 2026  
**Tipo:** backlog di ricerca documentata, **non** 100 storie pubblicate.

La pipeline `tool/editorial_origin_wave100.py` seleziona **esattamente 100 identità** presenti nel catalogo corrente, non già pubblicate come storie approfondite e non già incluse nelle quattro ricostruzioni originali. Priorità a 60 ricorrenze globali e 40 nazionali, con recupero automatico se un gruppo non raggiunge la quota.

## Cosa è già documentato per ogni candidato
- ID canonico, denominazione inglese e ambito (globale/nazionale);
- istituzione riportata nel catalogo, **senza confonderla con il fondatore**;
- anno ufficiale riportato nel catalogo, se disponibile, **non ricertificato automaticamente**;
- URL HTTPS e classe della fonte primaria/originatrice;
- lacune di ricerca e checklist per la storia;
- sei lingue di lavoro: IT, EN, ES, FR, DE, PT.

## Cosa resta da fare, singolarmente
Per ognuna delle 100 giornate: aprire e verificare la specifica fonte primaria; ricostruire l'origine e distinguere anno istitutivo da primo evento; documentare il motivo della data, promotore effettivo, finalità e 2–5 fatti circostanziati; redigere il racconto originale e tradurlo; eseguire revisione umana e test prima della pubblicazione.

**Non vengono inventati anni, promotori, curiosità o storie.** Un URL presente nel catalogo è un punto di partenza, non una certificazione autonoma della ricostruzione storica.

## Evidenza verificabile
- Output generato: `reports/editorial_origin_wave100.json`
- Validatore fail-closed: `tool/validate_editorial_origin_wave100.py`
- Artifact CI: `world-days-first-100-origin-dossiers`
- 100 dossier selezionati ≠ 100 nuovi articoli approvati.
- Nessuna modifica al catalogo di ricorrenze, APK, Play Store o rilascio pubblico.
