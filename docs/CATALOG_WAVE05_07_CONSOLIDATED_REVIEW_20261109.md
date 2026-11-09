# World Days — lotto unico Wave05–07: 16 ricorrenze

## Decisione di consolidamento

Le precedenti PR #65 e #66 erano sviluppate in sequenza, seguite dalla #67. Per ridurre tre cicli di revisione, **l'intero lotto di 16 ricorrenze viene revisionato nella PR #67 su `main`**. I commit rimangono nella cronologia Git; la CI rigenera tutto il catalogo sul branch esatto. La ricerca distinta PR #64 resta in Draft e non è un prerequisito di merge.

**Catalogo proposto:** 456 → 472; 285 GLOBAL e 187 NATIONAL; gli stessi 28 Paesi. 16 nuovi record:
- 3 UNESCO: World Day of Romani Language (5 Nov), International Day against Illicit Trafficking in Cultural Property (14 Nov), International Day of Islamic Art (18 Nov).
- 3 Giappone: Coming of Age Day (2° lunedì di gennaio), Emperor's Birthday (23 Feb sotto il regime legale attuale), Shōwa Day (29 Apr).
- 7 Giappone: Greenery Day (4 May), Children's Day (5 May), Marine Day (3° lunedì di luglio), Mountain Day (11 Aug), Respect for the Aged Day (3° lunedì di settembre), Sports Day (2° lunedì di ottobre), Labor Thanksgiving Day (23 Nov).
- 3 India: Republic Day (26 Jan), Independence Day (15 Aug), Gandhi Jayanti (2 Oct).

## Verifiche tecniche e documentali

1. Fonti ufficiali di partenza UNESCO, Cabinet Office giapponese e India Post, collegate per record. Dove l'anno d'introduzione della festività non è documentato, mantenere `*`; non confondere anno evento storico con istituzione della festa.
2. Titoli EN/IT/ES/FR/DE/PT presenti in tutti i 16 nuovi record; il controllo strutturale non è una revisione linguistica qualificata.
3. Regole annuali 2026–2028 a data fissa o secondo/terzo lunedì; non includere date di sostituzione, equinozi con data non ancora annunciata o calendario lunare inventato.
4. Nuovi record rimangono `STUB`; 56 narrazioni storiche esistenti revisionate non sono alterate; nessuna nuova storia viene falsamente promossa a `REVIEWED`.
5. Un'unica suite CI deve superare generatore 472, validatori di tutte le Wave05–07, test Flutter, Europe/Rome, build Web. Tutti i 456 ID esistenti restano invariati.

## Check editoriale ancora aperto (non auto-approvato)

- [ ] Convalida terminologica/ortografica dei 16 titoli nelle 6 lingue
- [ ] Corretta identità nazionale versus internazionale (in particolare Children's Day, Gandhi Jayanti, non-violenza)
- [ ] Conferma dell'ambito nazionale, autorità e provenienza delle fonti
- [ ] Accettazione esplicita della pubblicazione metadata-only senza nuovi articoli lunghi
- [ ] Esito CI PASS e tutte le protezioni di branch su commit HEAD esatto

**Nessun merge senza i gate realmente richiesti**. Questo lotto non autorizza APK, Play, firma Android né deploy di produzione. La pubblicazione Web resta una decisione separata.

## Fonti canoniche

- https://www.unesco.org/es/days/romani-language
- https://www.unesco.org/en/days/against-illicit-trafficking
- https://www.unesco.org/en/days/islamic-art
- https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html
- https://www8.cao.go.jp/chosei/shukujitsu/gaiyou/kaku.html
- https://www.indiapost.gov.in/holidays-list
- https://www.ursc.gov.in/holidays.jsp
