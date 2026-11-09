# World Days — certificazione delle 153 schede di ricerca (9 novembre 2026)

**Stato: controllo documentale progressivo, non pubblicazione.** Baseline App Factory Core `d4ed1185d36d419228fba6b57a979cde308bd321`; `main` World Days `9e312432b7fb46be1fc66437587d4cbe49033ad9` = **456** ricorrenze.

## Registro di certificazione completo e verificabile

| Stato documentale | Schede | Significato |
|---|---:|---|
| ALREADY_IN_MAIN_456 | **17** | Festività già presenti, stesso paese e commemorazione. Non duplicare. |
| IN_UNMERGED_PR_65 | **6** | Tre UNESCO e tre Giappone, test sorgente/Web PASS nella PR #65; non ancora su main, approvazione editoriale umana mancante. |
| PRIMARY_CALENDAR_2026_DATE_CONFIRMED | **34** | 12 Cambogia, 13 Sri Lanka, 6 Bangladesh, 3 Laos. Date e identità calendari 2026 verificate in fonti ufficiali; **non** prova di ricorrenza annuale multi-anno, unicità semantica o traduzioni. |
| PENDING_PRIMARY_SOURCE_IDENTITY_AND_RECURRENCE | **96** | Ricerca raccolta, ma fonte precisa, distinzione d'identità, anno e regola di ricorrenza non ancora interamente certificati. |
| **Totale** | **153** | Tutte le schede classificate, zero nuove pubblicate su main. |

La PR #65, se approvata e unita, porterebbe **462** ricorrenze distinte (285 GLOBAL + 177 NATIONAL); il divario verso 1.000 scenderebbe da **544** a **538**. Le altre **130** schede (34 con data 2026 ufficiale + 96 non ancora verificate in modo completo) non sono tutte necessariamente nuove: un titolo diverso non dimostra un'osservanza distinta.

La classificazione completa, voce per voce, viene generata da `tool/validate_research_certification_coverage.py` in `reports/research_certification_coverage.json` dopo aver ricostruito il catalogo reale e classificato i 153 record. La CI blocca un conteggio errato; conserva file di ricerca senza modificare runtime, APK o Play.

## Fonte primaria: 34 date del 2026 controllate

**Cambogia (12):** National Bank of Cambodia, https://www.nbc.gov.kh/english/news_and_events/official_holiday.php ; riscontro indipendente presso il Ministero dell'Economia e delle Finanze, https://mef.gov.kh/public-holiday-2026/. Khmer New Year (14–16 aprile), Pchum Ben (10–12 ottobre) e Bon Om Touk (23–25 novembre) sono **tre identità**, non otto giornate distinte. La data iniziale della festa nel 2026 è certificata, non la regola degli anni futuri.

**Sri Lanka (13):** Central Bank of Sri Lanka, https://www.cbsl.gov.lk/en/node/19362 . Dodici ricorrenze Poya nominalmente diverse più Capodanno singalese e tamil. `Adhi Poson` è una festività di mese intercalare presente nel 2026: non dichiararla evento fisso tutti gli anni. Le date dei pleniluni dipendono dal calendario ufficiale; niente ripetizione fittizia delle date del 2026.

**Bangladesh (6):** Bangladesh Bank, https://www.bb.org.bd/en/index.php/mediaroom/holiday e circolare ufficiale https://www.bb.org.bd/mediaroom/circulars/dos/nov162025dosl20e.pdf . `Chaitra Sankranti` riguarda specificamente i distretti di Rangamati, Khagrachari e Bandarban, **non** l'intero Bangladesh. `Language Martyrs' Day` è simultaneo e storicamente legato a International Mother Language Day: valutare con attenzione l'identità nazionale prima di creare un altro evento globale. `July Mass Uprising Day` compare ufficialmente il 5 agosto 2026, ma la presenza nel calendario non prova da sola il numero di anni di esistenza futura.

**Laos (3):** Consular Department / Lao Ministry of Foreign Affairs, https://laoevisa.gov.la/info . `Lao New Year` è una singola ricorrenza dal 14 al 16 aprile 2026. La fonte dice `Lao Women's Union Day`, ma non certifica *Founding Day* come denominazione ufficiale o anno di fondazione: correggere il titolo solo dopo un riscontro storico preciso. Festa nazionale 2 dicembre.

## Blocchi di qualità non aggirabili
1. Identità e alias cross-country: Capodanno lunare (Tet/Seollal/Chinese New Year), Buddha/Vesak, Holi/Diwali/Deepavali, Maha Bucha, festività civili nazionali e globali. Mantenere separati solo eventi istituzionalmente o culturalmente distinti e descritti senza duplicare la stessa identità per mercato.
2. Date lunari/astronomiche, calendario nepalese, Pasqua, festività regali e date regionali: implementare o verificare `LUNAR/AUTHORITY_DEFINED` con override **per anno**; non trattare `occurrence2026` come regola fissa fino al 2028.
3. Fonti: autorità governativa o originator, URL specifico, esatto rango di fonte, scope nazionale/regionale, istituzione `*` se non documentata.
4. Sei lingue EN/IT/ES/FR/DE/PT, contenuti storici, revisione editoriale qualificata distinti dalla sola ammissione dei metadati. Non inventare approvazioni.
5. Per ogni batch ammesso: controlli su **catalogo generato** (ID/alias/fonte), conteggi, integrazione runtime, regressione Flutter, Web Preview; PR e CI esatta HEAD prima di merge.
6. Solo Chat. APK/firma/Play sospesi, senza deploy di produzione.

**Obiettivo 1.000:** non ancora conseguito. Per certificare *tutte* le mancanti oltre alle candidate già inventariate, servirà raccogliere e verificare altre ricorrenze reali. Nessuna fonte esaminata giustifica dichiarare 544 giornate già certificate.
