# World Days — catalogo ampio, Paesi + contesto editoriale (2026-11-09)

**Stato del lavoro:** nuova espansione dei contenuti e della ricerca; non è una certificazione APK/Play. **Priorità utente:** sospendere APK e certificazione Android/Google Play; sviluppare catalogo, storie e fonti. La milestone della PR è limitata al nuovo catalogo e alla navigazione Flutter, non alla pubblicazione Store.

## Problema risolto

La vecchia schermata Around the World mostrava **solo le giornate NATIONAL**: 14 schede su sette Paesi, pur esistendo nel catalogo **282 giornate GLOBAL** utilizzabili anche per un Paese selezionato. La vecchia lista eager non era progettata per mostrare centinaia di card. La nuova UX mostra **due sezioni chiaramente distinte**, con filtri *Tutte / Nazionali / Globali*, numeri espliciti e liste SliverList.builder a costruzione progressiva. Una giornata internazionale ONU non diventa una festa istituita dal governo italiano solo perché appare navigando l'Italia.

## Delta misurabile, versione 2026.11.09.1

| Fonte / livello | Prima | Ora | Delta |
|---|---:|---:|---:|
| Record GLOBAL canonici | 282 | 282 | 0 (preservati) |
| Record NATIONAL canonici | 14 | 57 | **+43** |
| Catalogo unico totale | 296 | **339** | **+43** |
| Titoli localizzati per ogni scheda | 6 | 6 | mantenuto EN/IT/ES/FR/DE/PT |
| Rich Editorial già revisionati | 56 | 56 | nessuna falsa promozione |
| Wave04 storie 6 lingue, bozza | 8 | 8 | non pubblicate |
| Country Wave01 EN+IT, bozza | 0 | 9 | 4 traduzioni + review da fare |
| Senza storia estesa già ricercata | 232 | **266** | 43 nuove schede, 9 bozze |
| Anni formali sostenuti da fonti primarie | 35 | **41** | +6, gli altri mostrano * |
| Record Paese + globali visibili navigando IT | 2 | **307** | 25 nazionali +282 globali |

### Copertura specifica per Paese

| Paese | Prima NATIONAL | Nuove schede | NATIONAL totali | Totali nella nuova vista con globali |
|---|---:|---:|---:|---:|
| IT | 2 | 23 | **25** | 307 |
| ES | 2 | 2 | **4** | 286 |
| FR | 2 | 7 | **9** | 291 |
| DE | 1 | 1 | **2** | 284 |
| PT | 2 | 2 | **4** | 286 |
| GB | 1 | 3 | **4** | 286 |
| US | 4 | 5 | **9** | 291 |
| **TOTAL** | **14** | **43** | **57** | globali condivise, NON moltiplicate nel catalogo |

I 282 record GLOBAL sono condivisi tra Paesi: **non sono 282×7 nuove date e non vanno contati più volte**.

## Fonti usate (e limiti)

| Ambito | Fonte istituzionale | Trattamento |
|---|---|---|
| Italia | [Presidenza del Consiglio — giornate celebrative](https://presidenza.governo.it/ufficio_cerimoniale/cerimoniale/giornate.html) | giornate civili non automaticamente festive; usa la data o il giorno della settimana previsto |
| Italia 21 marzo | [Legge 20/2017 — Gazzetta Ufficiale](https://www.gazzettaufficiale.it/atto/vediMenuHTML?atto.codiceRedazionale=17G00034&atto.dataPubblicazioneGazzetta=2017-03-10&tipoSerie=serie_generale&tipoVigenza=originario) | distinguere memoria collettiva e riconoscimento legislativo 2017 |
| Spagna | [Ley de Memoria Democrática 20/2022 — BOE](https://www.boe.es/eli/es/l/2022/10/19/20/con/20221020) | 31 ottobre articolo 7; 8 maggio articolo 8; entrambe 2022 |
| Francia | [Ministère des Armées — journées de mémoire](https://www.cheminsdememoire.gouv.fr/fr/le-devenir-des-journees-nationales), [Légifrance — mémoire de l'esclavage](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000692257/2017-10-25) | giornate di commemorazione; alcune date nazionali distinte dagli anniversari storici |
| Germania | [Bundesregierung — Tag des Grundgesetzes](https://www.bundesregierung.de/breg-de/aktuelles/tag-des-grundgesetzes-2349926) | 23 maggio è il giorno della Legge fondamentale del 1949; l'anno di origine del testo non è automaticamente l'anno di introduzione della commemorazione |
| Portogallo | [Diário da República — Dia da Liberdade](https://diariodarepublica.pt/dr/detalhe/decreto-lei/355-1983-439421), [Governo — Restauração](https://portugal.gov.pt/gc21/comunicacao/noticias/20161201-pm-1dezembro) | 25 aprile rivoluzione 1974 vs normative successive; 1 dicembre restaurazione 1640 |
| Regno Unito | [GOV.UK — Windrush 2018](https://www.gov.uk/government/news/annual-day-of-celebrations-for-the-windrush-generation), [flag days](https://www.gov.uk/guidance/designated-days-for-union-flag-flying), [Maritime Agency](https://insidemca.blog.gov.uk/2026/09/03/from-cadet-to-captain-a-merchant-navy-story/) | una nave e una commemorazione non equivalgono a tutta la storia della migrazione; domenica Remembrance è mobile |
| Stati Uniti | [OPM — federal holiday schedule](https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/), [National Archives — Juneteenth](https://www.archives.gov/news/topics/juneteenth) | in catalogo la **ricorrenza storica**, non il giorno sostitutivo del permesso lavorativo; Juneteenth federale dal 2021 |

Le fonti sono istituzionali, ma una fonte che prova data/titolo **non equivale a una storia lunga revisionata**. Un anno storico, un decreto che aggiorna l'osservanza e l'anno d'istituzione della giornata sono campi distinti. Quando il secondo non è provato, l'app mostra ***** e nessuna stima. Per i 43 nuovi record si applicano deduplicazione per ID, regole fisse/mobili e verifiche di titolo nelle sei lingue.

## Storie e approfondimenti, percorso controllato

Il nuovo [Country Wave01](../data/editorial/candidates/country_wave01_en_it_20261109.json) contiene **9 bozze originali EN/IT** con hook, spiegazione, origini, motivazione della data, fatti e suggerimenti, collegate a fonti primarie: memoria delle vittime delle mafie, unità italiana, Liberazione, memoria democratica spagnola, schiavitù in Francia, Windrush, Legge fondamentale tedesca, Dia da Liberdade portoghese, Juneteenth. Queste **non** sono pubblicate come articoli REVIEWED: mancano revisione editoriale/linguistica e quattro traduzioni (ES/FR/DE/PT). Il test `tool/validate_country_editorial_candidates.py` impedisce un'errata promozione nel runtime.

La precedente Wave04 mantiene 8 bozze complete in sei lingue: anche esse attendono la revisione umana. Il totale attuale **56 REVIEWED / 8 Wave04 DRAFT6 / 9 Country DRAFT2 / 266 non ricercati** è misurabile dal nuovo `tool/editorial_gap_manifest.py` a ogni build. Non associare monetizzazione e engagement a storie inventate: la qualità del testo resta il vincolo principale.

## Compatibilità e QA

- **Non cambiano:** 296 ID preesistenti, preferiti, recenti, impostazioni, login opzionale/no account, consenso pubblicitario, entitlement, notifiche/widget, servizi cloud.
- **Cambia:** dataset numerico v2026.11.09.1 con 339 record, occorrenze 2026 rigenerate e l'interfaccia di consultazione per i Paesi.
- **Regressioni obbligatorie:** `tool/build_dataset.py`, `tool/validate_dataset.py`, `tool/build_editorial.py`, `tool/validate_editorial.py`, sei locale editorial validators, `tool/validate_content_pack.py`, test Flutter calendario e filtri, 320/360/390/480 px con text scale 1/1,5/2. Testare nella CI `Development checks` del commit esatto.
- **Performance:** la crescita della lista nazionale+globale giustifica la conversione a `SliverList.builder` in questa schermata specifica. L'ottimizzazione della distinta lista Saved resta subordinata a profilo Android, senza attività su APK/Play.
- **Release:** nessun trigger manuale di signing, nessuna pubblicazione Android/Play. Workflow source/build esistenti non certificano Android fisico o Store. Blocchi #43 e #54 sospesi come richiesto.

## Roadmap di crescita (obiettivi, non conteggi certificati)

1. **ONDE 02–05:** portare ciascuno dei sette Paesi a un catalogo nazionale ben più sostanzioso, con fonti legislative e calendari civili ufficiali; aggiungere nuove regioni solo dopo aver definito l'owner dei codici Paese, senza moltiplicare falsamente giornate internazionali.
2. **Story Wave:** completare revisione dei 9 EN/IT e 8 sei-lingue, poi produrre contenuti ricchi *per piccoli batch verificabili*, mantenendo i 266 ancora privi di narrazione estesa in coda.
3. **Ampliamento globale:** confrontare periodicamente il catalogo unico con calendari ONU/UNESCO/OMS/UE e organismi originatori, verificando date aggiunte recentemente e deprecazioni con controllo delle fonti.
4. **Catalogo approfondito:** introdurre riquadri storia/origine/fatti correlati alle fonti senza immagini con testo incorporato, mantenendo gli attuali colori e fallback locale leggero.
5. **Maturità editoriale:** puntare a un catalogo **1.000+** di osservanze realmente distinte e provenienti da fonti classificate, con storia completa verificata progressivamente. L'obiettivo numerico NON prevale su correttezza, deduplicazione e titolo/lingue; non promettere 1.000 giornate tutte ONU.

**Decisione:** nuovi contenuti e QA Flutter attivi, **APK e certificazione Android/Google Play in sospeso** finché l'utente non li riattiva.
