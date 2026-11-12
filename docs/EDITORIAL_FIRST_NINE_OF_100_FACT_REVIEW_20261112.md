# World Days — prime nove origini verificate dalle 100 bozze IT/EN

**Data verifica:** 12 novembre 2026  
**Baseline:** `main@b1cb098671ad918dd2994c1599727a1a4b4d4863`  
**Stato:** 9 racconti di origine con verifica documentale individuale e testi IT/EN, **non** revisione editoriale/linguistica umana in sei lingue.

La ricerca recupera nove bozze dal lotto originale da 100 e ne redige la ricostruzione storica vera e propria: anno di istituzione, eventuale prima celebrazione, motivo documentato della data, soggetto deliberante e proponente se identificabile, contesto e quattro fatti. Ogni storia viene integrata nel layer offline `origin_stories_wave*.json` solo dopo i gate Python e CI.

| ID | Data | Istituzione formale | Prima osservanza documentata / stimata | Ragione storica della data / promotore | Fonti primarie |
| --- | --- | ---: | --- | --- | --- |
| world-logic-day | 14 gennaio | 2019 | 2019 (CIPSH: 2020 seconda giornata) | Nascita di Alfred Tarski e morte di Kurt Gödel; proclamazione UNESCO con CIPSH. **Correzione 40 C/38** | [UNESCO](https://www.unesco.org/en/days/world-logic), [CIPSH](https://wld.cipsh.international/background.html), [Risoluzioni UNESCO 2019](https://unesdoc.unesco.org/ark:/48223/pf0000372579) |
| world-day-for-african-and-afrodescendant-culture | 24 gennaio | 2019 | Non accertata | Carta per il Rinascimento culturale africano adottata dall'Unione Africana nel 2006 | [UNESCO](https://www.unesco.org/en/days/african-culture) |
| international-day-of-peaceful-coexistence | 28 gennaio | 2025 | 2026 (primo calendario successivo) | Giorno designato dall'ONU: non identificato un anniversario precedente | [ONU](https://www.un.org/en/observances/peaceful-coexistence-day), [A/RES/79/269](https://mandates.un.org/mandate/A/RES/79/269) |
| international-day-of-human-fraternity | 4 febbraio | 2020 | 2021 | Firma del documento ad Abu Dhabi nel 2019 da parte di papa Francesco e Ahmad al-Tayyib | [ONU](https://www.un.org/en/observances/human-fraternity) |
| world-pulses-day | 10 febbraio | 2018 | 2019 | Proposta del Burkina Faso dopo l'Anno internazionale dei legumi 2016 | [ONU background](https://www.un.org/en/node/226413), [UNGA 2018](https://www.un.org/en/ga/73/resolutions.shtml) |
| international-day-of-the-arabian-leopard | 10 febbraio | 2023 | Non accertata | Data decisa dalla risoluzione, ragione commemorativa non dimostrata | [A/RES/77/295](https://mandates.un.org/mandate/A/RES/77/295) |
| international-day-of-women-and-girls-in-science | 11 febbraio | 2015 | 2016 | Data designata dall'ONU; coordinamento RASIT, UNESCO e UN Women | [A/RES/70/212](https://mandates.un.org/mandate/A/RES/70/212), [ONU](https://www.un.org/en/observances/women-and-girls-in-science-day) |
| international-day-for-the-prevention-of-violent-extremism-as-and-when-conducive-to-terrorism | 12 febbraio | 2022 | 2023 (prima data dopo la risoluzione) | Nessun anniversario della data provato dalla risoluzione | [A/RES/77/243](https://mandates.un.org/mandate/A/RES/77/243) |
| global-tourism-resilience-day | 17 febbraio | 2023 | 2023 | Proposta della Giamaica e altri Stati, nel contesto della ripresa turistica | [A/RES/77/269](https://mandates.un.org/mandate/A/RES/77/269), [bozza e proponenti](https://digitallibrary.un.org/record/3999604) |

## Correzioni e controlli
- Corretto `tool/build_dataset.py`: World Logic Day = **UNESCO 40 C/Resolution 38**, non 39, come risulta dai verbali ufficiali. Allineati anche il JSON del lotto da 100 e il libretto Markdown.
- Aggiunti nove anni fondativi con fonti specifiche, distinti dalle date del primo evento (se ignoto, `null`).
- Il lotto originario di **100 bozze** resta un archivio di narrazioni scritte: le nove storie ricercate hanno record successori separati; le altre 91 **non** vengono promosse automaticamente.
- Le nuove origini **non** vengono spacciate per storie approvate in ES/FR/DE/PT; mantenuti EN/IT e fallback.
- Fonte consultata ≠ revisione umana indipendente. Eventuali review editoriali esterne sono ancora da completare.

**Copertura attesa dopo CI e merge:** 55 origini storico-istitutive con testi IT/EN su 1.111 ricorrenze; 1.056 identità ancora senza questo livello di approfondimento; 91 bozze originarie del lotto da 100 ancora da verificare individualmente. Conteggi subordinati alla rigenerazione del catalogo e ai test.
