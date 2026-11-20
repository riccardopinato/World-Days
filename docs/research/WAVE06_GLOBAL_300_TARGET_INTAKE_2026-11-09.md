# Wave06 — ricerca internazionale, target +300 ricorrenze distinte

**Non dichiarare 300 nuove giornate finché non sono state realmente raccolte, deduplicate e verificate.**

## Lotto realmente acquisito
- `data/research/wave06_japan_philippines_india_2026.json`: **38 record di ricerca** (JP 15, PH 10, IN 13), da fonti primarie.
- Japan: https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html (legge sulle festività e date 2026–27).
- Philippines: https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/7/99678 (Proclamation No. 1006, 2026); https://officialgazette.gov.ph/section/executive-issuances/proclamations/ per proclamazioni locali, da NON promuovere a ricorrenze annuali senza evidenza.
- India: https://cag.gov.in/en/pages/single/page-defence-new-delhi-holidaylist ; https://www.indiapost.gov.in/holidays-list (2026). Differenze tra uffici, stati, date di calendari religiosi: verificare caso per caso, non assegnare regola fissa.
- Controllo preliminare letterale contro i tre moduli Python `tool/build_dataset.py`, `tool/market_catalog.py`, `tool/market_expansion.py`: **Holi** compare già; 37 titoli non trovati letteralmente. Ciò NON certifica 37 identità nuove; restano market JSON e sinonimi.

## Principi di ammissione
1. Identità unica = ricorrenza, non semplice combinazione paese/data; un evento internazionale ripetuto in 30 paesi non vale 30 nuove giornate salvo reale distinta istituzione locale.
2. Non contare `substitute holiday`, `observed Monday`, giorni di chiusura uffici, ferie occasionali e proclamazioni valide solo nel 2026 come nuove ricorrenze annuali.
3. Se festività regionale, usare scope regionale e area corretta; non falsare `NATIONAL`.
4. Anno di istituzione non noto = `*`, mai l'anno dell'evento storico.
5. Date lunisolari, equinozi, Pasqua e giorni ordinali richiedono motore di ricorrenza e test su più anni.
6. Confrontare tutti i 456 record generati, `aliases`, traduzioni e mercati prima dell'ammissione.
7. Per l'integrazione: sei lingue, storie editoriali con fonte, QA e CI exact-head. APK e Play restano sospesi.

## Prossimi registri primari da esplorare (non ancora acquisiti)
- Europa: registri governativi di Austria, Svizzera, Belgio, Danimarca, Polonia, Grecia, Romania, Bulgaria, Croazia, Slovenia, Lituania, Lettonia, Estonia.
- Americhe: registri di Colombia, Cile, Perù, Argentina, Brasile, Messico, Costa Rica, Uruguay, Ecuador, Panama.
- Asia-Pacifico: Corea, Taiwan, Singapore, Malaysia, Thailandia, Vietnam, Indonesia, Nepal, Sri Lanka, Nuova Zelanda, Australia.
- Africa: Kenya, Ghana, Nigeria, Rwanda, Senegal, Marocco, Tunisia, Egitto, Sudafrica.
- Medio Oriente: Emirati Arabi Uniti, Arabia Saudita, Giordania, Israele, Turchia.
Questi sono **bacini di ricerca**, non giornate inventariate.

## Contabilità
Baseline `main`: 456. Wave05: 33 candidate research-only (3 UNESCO, 24 CA, 6 ZA). Wave06: 38 record research-only (15 JP, 10 PH, 13 IN). Totale lotti **71 schede di ricerca**, non 71 aggiunte uniche. Gap certificato a 1000: **544**. Il target utente +300 nuove richiede altri 300 record unici ammessi, non semplicemente 300 stringhe.
