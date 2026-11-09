# World Days — certificazione sorgenti Wave05–10 (9 novembre 2026)

## La distinzione fondamentale

**Certificare la DATA del 2026 su un calendario governativo non equivale a certificare una nuova identità unica, la ricorrenza nel 2027–2028, le traduzioni o la pubblicazione nell'app.** Non usare conteggi di ricerca per aggiornare il catalogo runtime.

- App Factory Core baseline: `d4ed1185d36d419228fba6b57a979cde308bd321`, Master 27 / Golden Index 29.
- World Days `main` baseline: `9e312432b7fb46be1fc66437587d4cbe49033ad9` = **456** ricorrenze.
- PR #65 separata, metadata-only, CI PASS, 3 UNESCO + 3 Giappone, **462 solo se unita** (ancora non in main, umano/editoriale non approvato).
- Questo registro verifica **tutte le 153 schede** delle Wave05–10 con i criteri documentali realmente soddisfatti.

## Classificazione completa e verificabile

| Stato | Schede | Interpretazione esatta |
| --- | ---: | --- |
| `ALREADY_IN_MAIN_456` | **17** | Ricorrenze già presenti; non duplicarle |
| `IN_UNMERGED_PR_65` | **6** | Sei record tecnici testati in PR distinta, non in main |
| `PRIMARY_CALENDAR_2026_DATE_CONFIRMED` | **121** | Fonte istituzionale/di origine consultata e singola data o data iniziale **2026** controllata; tutte restano in research |
| `PENDING_PRIMARY_SOURCE_IDENTITY_AND_RECURRENCE` | **9** | Nepal: il registro ufficiale 2083 è disponibile come PDF nepalese, ma non è stata completata verifica indipendente delle conversioni e delle date |
| **Totale** | **153** | Nessuna ammissione extra dalla PR di ricerca |

**Contabilità residua:** le 121 candidate con calendario 2026 documentato NON sono tutte provate come nuove uniche e annuali. In `main` restano **456**: gap **544** verso 1.000. Se PR #65 viene approvata/unita: **462**, gap **538**. La ricerca disponibile non prova che esistano già 538 nuove ricorrenze pronte.

## Origini dei 121 riscontri nel 2026

| Paese | Voci | Fonte primaria |
| --- | ---: | --- |
| Canada CA | 22 | https://www.canada.ca/en/canadian-heritage/services/important-commemorative-days.html |
| Sudafrica ZA | 6 | https://www.gov.za/about-sa/public-holidays |
| Indonesia ID | 3 | https://www.setneg.go.id/baca/index/inilah_skb_3_menteri_libur_nasional_dan_cuti_bersama_2026 |
| Giappone JP | 9 | https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html |
| Thailandia TH | 13 | https://www.bot.or.th/en/financial-institutions-holiday.html |
| Singapore SG | 5 | https://www.mom.gov.sg/newsroom/press-releases/2025/0616-public-holidays-for-2026 |
| Vietnam VN | 4 | https://en.baochinhphu.vn/ministry-of-home-affairs-announces-2026-holiday-schedule-111251017163421877.htm |
| Cambogia KH | 12 | https://www.nbc.gov.kh/english/news_and_events/official_holiday.php ; https://mef.gov.kh/public-holiday-2026/ |
| Sri Lanka LK | 13 | https://www.cbsl.gov.lk/en/node/19362 |
| Bangladesh BD | 6 | https://www.bb.org.bd/en/index.php/mediaroom/holiday |
| Laos LA | 3 | https://laoevisa.gov.la/info |
| Filippine PH | 5 | https://elibrary.judiciary.gov.ph/thebookshelf/showdocs/7/99678 |
| India IN | 13 | https://cag.gov.in/en/pages/single/page-defence-new-delhi-holidaylist |
| Corea del Sud KR | 4 | https://www.bok.or.kr/eng/main/contents.do?menuNo=400373 |
| Malaysia MY | 3 | https://wbf.jknns.moh.gov.my/app/tetapanUtama |
| **Totale** | **121** | |

Il file `data/research/primary_2026_calendar_verified_20261109.json` contiene la matrice **voce per voce**, esatta data 2026, ambito e URL originale. È una certificazione circoscritta della fonte/occorrenza 2026.

### Precisazioni anti-errore importanti

1. **Nepal (9):** Ministero dell'Interno `https://moha.gov.np/en/page/government-and-public-holidays-in-2083` pubblica il calendario B.S. 2083 tramite PDF da 8,22 MB. La verifica diretta del PDF/conversione gregoriana non è stata completata: non attribuire per analogia una data 2026 né un ambito nazionale alle festività regionali Gai Jatra/Indra Jatra/Jitiya. Nove voci restano in stato PENDING. La disponibilità del PDF non implica che sia stato letto o certificato.
2. **Sudafrica Family Day:** 6 aprile 2026 / 29 marzo 2027 sono date riportate nel calendario ufficiale; la regola è Easter Monday. Per il 2028 si calcola il 17 aprile, da convalidare sul calendario pubblicato dall'autorità. Non usare il 6 aprile come giorno fisso annuale; possibile alias di Easter Monday mondiale da valutare prima di creare una nuova identità.
3. **Sri Lanka:** Adhi Poson 2026 è intercalare, non ricorrenza che debba comparire in modo invariato ogni anno. Ogni Poya dipende dal calendario lunare locale.
4. **Bangladesh:** Chaitra Sankranti è limitata ai tre distretti collinari nominati nel calendario della Bangladesh Bank; Language Martyrs Day condivide data e storia con International Mother Language Day ma ha origine nazionale specifica.
5. **Laos:** il registro ministeriale dice `Lao Women's Union Day`, non prova che `Founding Day` sia la denominazione legale. Lao New Year 14–16 aprile è una sola festa.
6. **Filippine:** Proclamation 1006 comprende alcune giornate speciali valide nel **2026**: la presenza non prova una ricorrenza annuale permanente (ad esempio All Souls' Day come giorno aggiuntivo). Non duplicare i giorni di ferie.
7. **Giappone:** l'equinozio è dichiarato ufficialmente ogni anno, non una data gregoriana fissa. Giorni sostitutivi esclusi.
8. **Thailandia:** 31 maggio è Visakha Bucha nel 2026, mentre 1 giugno è giorno sostitutivo; il 5 dicembre è la commemorazione, non il sostitutivo del 7 dicembre. Il calendario è degli istituti finanziari, non prova uniformità per tutti i lavoratori.
9. **Singapore, India, Corea, Vietnam:** Seollal, Tết, Capodanno cinese, Eid, Vesak, Buddha Purnima, Deepavali e festività analoghe non si moltiplicano automaticamente per Paese; il catalogo richiede una decisione semantica sulle celebrazioni locali.
10. **Malaysia:** l'anniversario ufficiale del sovrano va riesaminato annualmente. Le date sono quelle pubblicate per il 2026, non un contratto perpetuo.

## Gate obbligatori prima di ammettere altre identità

- Confrontare alias, paese, scope, istituzione e storia con tutti i 456 record generati e con le 6 identità in PR #65.
- Confirmare regola annuale e date per 2026, 2027, 2028, o mantenere un `AUTHORITY_DEFINED` annuale senza inventare occorrenze.
- Introdurre anno soltanto con fonte primaria adeguata; altrimenti `*`.
- Scrivere tutti i sei titoli EN/IT/ES/FR/DE/PT ed eventuale articolo storico; QA linguistico/editoriale qualificato resta un gate separato, non auto-approvato.
- PR contenuto a batch limitato, CI exact-head generator + Flutter analyze/test/Web. Non merge PR di ricerca come se fosse un catalogo pubblicabile.
- Sospensione APK, firma, Android e Google Play invariata.

## Evidenza CI

Il job `Research candidates — generated catalog semantic overlap audit` esegue:

1. `tool/build_dataset.py` + `tool/validate_dataset.py`: 456 identità su main.
2. `tool/audit_research_candidates.py`: 153 candidati contro ID, alias, 6 lingue.
3. `tool/validate_research_overlap_decisions.py`: 17 già esistenti, 3 falsi positivi.
4. `tool/validate_research_certification_coverage.py`: 153 identificati univocamente in 4 livelli e verifica URL+data 2026. Produce `reports/research_certification_coverage.json` come artifact.

**CI PASS del registro non certifica storia, unicità di 121 candidati, anno di istituzione o release su dispositivo.**
