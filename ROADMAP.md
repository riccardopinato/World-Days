# World Days — Active roadmap

## Existing stories: registry and publication gate (12 November 2026)

- [x] Wave12 PR #108 records International Day of Nowruz with original 2010 UN resolution, 21 March first-year observance, and separation from earlier cultural tradition. **64/1,111** source-linked records after CI and merge, **1,047** pending; **154** distinct source-linked drafts left in PRs #109–#114. Human six-language approval not claimed.

- [x] Wave11 PR #107: World Day for Glaciers (21 March), UN adoption 2022 and primary UN event evidence for the first 2025 celebration. Source-linked origins **63/1,111** on successful merge; remaining **1,048**. Specific legislative date rationale remains unknown; six-locale signoff not claimed.
- [x] Candidate registry updated to **155 unique IT/EN story drafts** across PR #108–#114, each distinct from already integrated source research.


- [x] Wave10 PR #106: research UNESCO International Day for Digital Learning, 19 March, designation 2023 and first UNESCO edition in 2024, while leaving undocumented choice of the date unasserted. After green merge **62/1,111** researched origins, **1,049** pending; no six-language approval.
- [x] Pending source-draft register reduced to **156 unique stories** in 8 open PRs (#107–#114), without duplicates or publishing a source draft as a reviewed runtime article.


- [x] Wave09 PR #105: add source-linked histories for International Day of Women Judges (UN adoption 2021, first commemoration 2022) and International Day to Combat Islamophobia (UN adoption 2022, first commemorative event 2023), with original UN evidence for inaugural observances. Source-linked total **61/1,111** after green merge; **1,050** still lack individual source research.
- [x] Update pending PR registry to **157 distinct IT/EN draft origins** from PR #106–#114 (9 open PRs); research drafts are not qualified human-reviewed rich articles and remain gated out of Flutter runtime.


- [x] Wave08 PR #104: add independently sourced International Day for Disarmament and Non-Proliferation Awareness (5 March) with original 2022 General Assembly decision A/RES/77/51, six draft sponsors documented, first annual observance 2023, calendar-day choice not attributed without evidence. Source-linked total **59/1,111** upon successful merge; remaining **1,052**. Rich editorial six-language approval still false.
- [x] Reconcile the Wave08 review finding by updating README and ROADMAP to 59 source-linked origins and **159 pending IT/EN drafts** in 10 open PRs (#105–#114), rather than reporting outdated 55/1,056 coverage.


- [x] Wave07 PR #103: account for the source-researched 6 February FGM observance, with unknown early-history facts kept unasserted. Source-research total upon green merge: **58/1,111**; remaining **1,053**. Runtime six-locale approval remains false.
- [x] Update the unique pending story register to **160 IDs in 11 PRs (#104–#114)**, with cross-check that none is already integrated on main.


- [x] Merge PR #102 with 2 source-linked IT/EN histories (seagrass and wildlife); main source-research count becomes **57/1,111**, pending **1,054** at this snapshot. This is not equivalent to 57 human-reviewed six-language articles.
- [x] Register the **161 distinct IT/EN historical drafts** already present in open PR #103–#114 with canonical IDs, exact source batch paths, source commits, and review-status flags in `data/editorial/registry/pending_origin_story_prs_20261112.json`.
- [x] Require explicit `runtimeRichEditorialApproved` in the generated origin ledger and Flutter detail panel; no approval is inferred from a verified source URL, CI check, or the presence of the text in a wave batch. Unapproved histories retain the fallback panel.
- [ ] Reconcile source and first-observance review findings in PR #104, #111, #112 and #114; repeat exact-head CI after fixes.
- [ ] Secure qualified factual/linguistic review EN/IT/ES/FR/DE/PT and publication approval before any runtime rich-origin promotion. The 56 existing legacy reviewed editorial entries remain separate.
- [ ] Recheck current main and regenerate the origin report after each further successful merge; update this 2026-11-12 checkpoint rather than treating the snapshot as a live counter.
- [ ] Continue with the first outstanding canonical IDs in batches of at most 100, never mistake the archived draft corpus for approved content.
- [x] Disable the existing `Deploy Web Preview` push-to-main trigger; use manual `workflow_dispatch` only. Note that PR #102 caused the previous automatic deployment run 43277603486 before this safety change.
- [ ] No further APK, Play, deploy, or store promotion in this phase.


## Prime 9 origini certificate da fonti specifiche tra 100 bozze (12 novembre 2026)

- [x] Analizzare singolarmente nove ricorrenze della PR #100 tramite fonti istitutive originali ONU, UNESCO e CIPSH; redigere nuova storia d'origine IT/EN con anno, prima osservanza quando provata, scelta della data, promotore e quattro fatti.
- [x] Correggere l'errore documentale World Logic Day: la risoluzione UNESCO è **40 C/38**, non 40 C/39.
- [x] Creare `origin_stories_wave05_20261112.json` e riferimenti cronologici; collegare il validatore `validate_editorial_origin_wave05_20261112.py` alla CI.
- [x] Mantenere tutti i 100 testi iniziali nell'archivio: l'eventuale storia verificata è un successore autonomo del draft; non pubblicare automaticamente i 91 non verificati.
- [ ] Superare i gate exact-head Flutter, Web, Python e review per integrare il branch.
- [ ] Proseguire la ricerca per le altre 91 bozze del lotto da 100 e poi con la coda residua.
- [ ] Tradurre e revisionare ES/FR/DE/PT e ottenere review editoriale/fattuale qualificata; non dichiarare tale passaggio già svolto.

**Conteggio condizionato a CI/merge:** 55/1.111 origini IT/EN source-researched, 1.056 senza revisione individuale; 100 bozze narrative archiviate, nove promosse con successore documentato. Registro: `docs/EDITORIAL_FIRST_NINE_OF_100_FACT_REVIEW_20261112.md`.

## Primo lotto da 100 racconti originali IT/EN (12 novembre 2026)

- [x] Scrivere 100 testi narrativi unici, non dossier vuoti, con italiano e inglese, fonti istituzionali e numero di risoluzione riferito alla data.
- [x] Conservare identità e date del catalogo, non riutilizzare i 46 ID delle origini ricercate, bloccare i segnaposto tecnici e associare stato bozza a tutti i testi.
- [x] Pubblicare il testo consultabile in `docs/WORLD_DAYS_100_ORIGINAL_STORIES_DRAFT_20261112.md` e i dati strutturati in `data/editorial/candidates/origin_100_original_bilingual_drafts_20261112.json`.
- [x] Aggiungere validatore CI `tool/validate_origin_100_original_drafts_20261112.py`, con guardrail di *non promozione* nel layer offline.
- [ ] Per ognuna delle 100 bozze verificare l'atto istitutivo originario, anno di adozione, persona o Paese proponente (se noto), motivo della data e curiosità specifiche. La sola presenza nella lista ONU/UNESCO non è sufficiente.
- [ ] Ampliare i testi in stile narrativo lungo, effettuare revisione fattuale, scrivere ES/FR/DE/PT e revisionare tutte le lingue prima della promozione.
- [ ] Continuare per gruppi da 100 fino a coprire gli ID rimanenti.

**Verità del checkpoint:** 100 bozze IT/EN redatte, ma **0 nuove origini di questo lotto dichiarate certificate**. I 46 approfondimenti storici IT/EN già integrati su main restano distinti; 1.065 identità richiedono ancora ricerca individuale. Nessun APK/Play/deploy.

## Wave04 — 14 storie ONU/UNESCO dal lotto istituzionale precedente (12 novembre 2026)

- [x] Recuperare 14 testi di origine individualmente ricercati nel precedente file `un_primary_2026_11_03_02.json` senza moltiplicare o sostituire i 1.111 ID canonici.
- [x] Completare l'approfondimento IT/EN per ogni storia con fondazione, data storica, promotore o ente adottante dimostrato, finalità e fatti verificabili; mantenere sconosciute le circostanze non documentate.
- [x] Aggiungere il batch append-only `origin_stories_wave04_20261112.json` e un gate Python di corrispondenza al precedente registro di fonti, anni, testi e status delle quattro lingue aggiuntive.
- [ ] Verificare CI completa sul commit esatto; integrare soltanto dopo gate/review verdi.
- [ ] Revisionare con competenza editoriale e linguistica ES/FR/DE/PT prima di dichiarare le storie certificate in sei lingue.
- [ ] Proseguire in lotti fino al completamento, ricercando origini singole per le restanti 1.065 ricorrenze su 1.111, con priorità alle fonti istituzionali specifiche.

**Checkpoint atteso dopo merge, a catalogo invariato:** 46 origini documentate IT/EN, 1.065 da completare; coda automatica 11 blocchi (10×100+65), 79 anni documentati già presenti. Le 56 storie editoriali legacy sono un conteggio distinto. Nessun APK/Play/produzione.

## Wave03 — 15 storie storiche ONU/UNESCO già documentate, ora mostrate nell'app (12 novembre 2026)

- [x] Riutilizzare le 15 schede fonte-ricercate in `data/editorial/batches/un_primary_2026_11_03_03.json` senza riscrivere o inventare cronologie; ricomporle in testi IT/EN per il pannello offline delle origini.
- [x] Distinguere autorità istitutive, proposte documentate, anniversari commemorati e prime celebrazioni solo dove dimostrabili.
- [x] Integrare un nuovo batch append-only `origin_stories_wave03_20261112.json` nel generatore esistente, con validazione CI sui 15 ID, provenienza, cronologia e testi IT/EN.
- [ ] Completare review editoriale qualificata e traduzioni ES/FR/DE/PT, senza promuovere automaticamente draft.
- [ ] Continuare per blocchi massimi da 100 sulle ricorrenze rimanenti, incluse le verifiche delle fonti nazionali e dei 56 articoli legacy.

**Dopo merge e validazione:** 32 origini IT/EN documentate su 1.111, ancora 1.079; i 56 precedenti articoli runtime sono separati dalla nuova ricertificazione di origine. Nessun nuovo ID canonico.

## Wave02 — otto nuove storie di origine con fonti primarie (12 novembre 2026)

- [x] Collegare `origin_stories_wave02_20261112.json` come batch append-only di 8 origini documentate da ONU, UNESCO, OMS, Ramsar e fonti istituzionali originarie.
- [x] Scrivere testi originali IT/EN con motivo della data (quando provato), istituzione, ente promotore documentato, primo evento e curiosità tracciabili; segnalare esplicitamente ciò che non è provato.
- [x] Aggiungere gate Python per anni, URL istituzionali, dati già presenti nelle bozze Wave04 e assenza di attribuzioni arbitrarie; collegarlo alla CI.
- [ ] Verificare i risultati CI Python, Flutter e Web sull'ultimo commit e le eventuali review prima del merge.
- [ ] Svolgere revisione editoriale/linguistica qualificata delle lingue ES/FR/DE/PT: la loro presenza come bozze non costituisce certificazione.
- [ ] Continuare sul primo blocco da 100 con nuovi racconti verificabili, senza saltare o riaprire ID già completati.

**Conteggio atteso dopo CI e merge, a catalogo invariato:** 17/1.111 origini individualmente ricercate, 1.094 da approfondire, 56 vecchi articoli editoriali distinti.

## Primo lotto: 5 nuove storie UNESCO con fonti individuali (12 novembre 2026)

- [x] Ricercare con pagine UNESCO e IMU cinque identità non ancora trattate nel nuovo ledger: traffico illecito di beni culturali (14 novembre), arte islamica (18 novembre), matematica (14 marzo), donne nel multilateralismo (25 gennaio) e ingegneria sostenibile (4 marzo).
- [x] Redigere per ognuna testi originali IT/EN: origine e istituzione, promotore distinto dall'ente che ha proclamato, scopo e tre fatti circostanziati; ragioni della data sconosciute restano dichiarate non documentate.
- [x] Collegare file di lotto `data/editorial/batches/origin_stories_wave01_20261112.json` al generatore del registro offline e alle code 100-ID; test fonte/anno/struttura.
- [ ] Revisione editoriale e linguistica indipendente; completamento e verifica delle traduzioni ES/FR/DE/PT. Non equiparare bozza a pubblicazione editoriale plurilingue certificata.
- [ ] Continuare il blocco 001 fino a 100 nuove origini storiche verificate, poi procedere al blocco successivo.

**Checkpoint dopo questa integrazione (da confermare su CI):** 9 origini individualmente ricercate su 1.111; 1.102 ancora senza nuovo audit d'origine; 56 precedenti articoli REVIEWED restano una classificazione separata. La coda si rigenera da main, non conserva conteggi fissi.

## Programma storie: lotti consecutivi da 100 (12 novembre 2026)

- [x] Predisporre la suddivisione riproducibile di **tutte** le origini da ricercare: 1.107 ID in 12 lotti (11 × 100 + 7), senza duplicazioni, mentre il catalogo resta a 1.111.
- [x] Riusare il primo lotto Wave100 (#93), completare i lotti successivi e certificare in CI gli ID, la copertura, la provenienza e lo stato delle bozze, senza fingere che i dossier siano racconti finiti.
- [ ] Per ciascun lotto produrre effettivamente racconti individuali verificati in fonte primaria, anno fondazione se documentato, ragione data, promotore provato, contesto e curiosità.
- [ ] Integrare testi originali e traduzioni EN/IT/ES/FR/DE/PT dopo revisione fattuale, editoriale e linguistica.
- [ ] Aggiornare automaticamente i lotti rimasti man mano che gli approfondimenti diventano effettivamente certificati; nuove ricorrenze si aggiungono senza tetto massimo.

Protocollo: [EDITORIAL_ORIGIN_100_BATCHES_UNTIL_COMPLETE_20261112.md](docs/EDITORIAL_ORIGIN_100_BATCHES_UNTIL_COMPLETE_20261112.md).
**Avanzamento di ricerca iniziale:** 4 origini ricercate; 1.107 ancora da verificare individualmente. I 56 articoli legacy non vengono conteggiati come 56 nuove certificazioni di origine.

## Source-backed origin stories — implemented for 4/1,111, remaining 1,107 (11 November 2026)

- [x] Add a per-ID offline research ledger and visible source-bound IT/EN origin, adopter/proposer (where known), why and contextual facts for four World Days; native localization beyond IT/EN remains pending.
- [x] Preserve 56 previously reviewed English rich-editorial records as distinct from four additionally source-audited origin narratives; do not claim the remaining 1,107 have been researched.
- [x] Build and validate the origin-index asset in development, dependency and platform bootstrap paths so Web and future Android compilation do not omit it.
- [ ] Independently research origins and historical contexts for the remaining 1,107 canonical records; check dates, individual national law and cultural/institutional classification, especially EURES/DFAT/NCCA.
- [ ] Extend source-reviewed IT/EN prose and later independently reviewed ES/FR/DE/PT. Never invent a historical proposer, year or holiday status. Continue expansion beyond 1,111 as source evidence supports.
- [ ] Deploy only after CI, reviewer approval, and corrected origin/recurrence quality gates.


## Certification and editorial continuation — 2026-11-11

- [x] Prepare Ireland St Brigid statutory holiday correction against [WRC public-holiday guidance](https://www.workplacerelations.ie/en/what_you_should_know/public-holidays/): annual exceptions 2023–2100 and separate traditional 1 February record; **CI pending** until confirmed on the new PR head.
- [x] Stage two distinct source-grounded English origin narratives for editorial review without increasing the runtime REVIEWED count prematurely.
- [ ] Confirm exact-head Python validation, Flutter tests and Web release CI; reconcile main's actual Git commit to the 1,111-record generated dataset.
- [ ] Review national legal dates and institutional index records (DFAT, EURES, NCCA), correct provenance/recurrence errors, and distinguish official public holidays from cultural anniversaries.
- [ ] Build 1,111-entry editorial gap registry (source/why/creator/year/context), verify evidence per record, publish source-grounded stories in batches, and localize translations with review gates. Do not fabricate unknown details.
- [ ] Never auto-upgrade English fallback STUB articles into REVIEWED or treat minimum 1,111 as maximum.


## Wave10 — complete next +100 identity threshold (11 November 2026)

- [x] Version 100 source-index records: 50 Korean government commemorations, 50 Philippine National Commission cultural anniversaries
- [x] Exclude known Korean Children's Day and National Memorial Day IDs from double counting
- [x] Keep country/authority/source, original Korean terms, date-rule semantics and nonstatutory cultural classification
- [x] Add exact 711-ID catalog validator, 2026–2029 recurring date tests, locale fallback disclosure, market/UI expectation updates
- [ ] Pass CI and review original institutional source date/identity matches, particularly Philippine cultural anniversary descriptions
- [ ] Merge protected PR after exact-head successful checks and substantive review
- [ ] After approved merge, target 1,000 will require **289 additional distinct identities**
- [ ] Native title translations for 100 Wave10 records, and separately 100+ previous Wave09/wave08 editorial debts, are not yet complete
- [ ] Long-form editorial remains a separate research-and-translation pipeline

No APK, native physical QA or Play publishing.


## Wave09 — 73 verified-source national record admissions; 100-item canonical growth

- [x] Source 73 national civic/memorial/flag days from six first-party government or institution-maintained registers.
- [x] Stage 23 Slovak, 18 Czech, 13 Polish, 9 Swedish, 5 Norwegian and 5 Finnish identities; no cross-wave ID/title collisions.
- [x] Add deterministic 2026–2029 date validation; support Finnish Midsummer's weekday-on/after June 20 and third Sunday of May.
- [x] Add officiality/source tier distinction: Finnish University Almanac Office originator records versus government statutory observances.
- [x] Extend all Python and Flutter market-count, dataset and content-pack gates; preserve 27 already merged Canadian records.
- [ ] Exact-head CI, review correction and protected PR merge to reach **611** canonical identities.
- [ ] **Mandatory translation debt**: 73 EN fallbacks in five non-English title locales; source English is not certified native translation.
- [ ] Complete source-reviewed long-form stories and authoritative introduction years separately from new ID admission.
- [ ] After Wave09 merge **389 additional distinct records** remain for target 1,000. Next work must be a **100-source-verified-record batch**, not several 7–30 entry batches.

No APK, signing, Android physical QA, billing or Play publishing.


## Wave08 — Canada 27 actual canonical admissions; parallel discovery batch 100

- [x] Build separate 27-entry Canadian Heritage national civic catalog packet, six title locales and supported annual dates
- [x] Add 27 new non-overlapping canonical identities with `introducedYear=null`, preserving all previous stable IDs
- [x] Update market count, analytics expectations and full Python/Flutter/Web CI gates
- [ ] Review source authority and exact-head CI; merge source-only catalog PR after gate success
- [ ] Target after merge **538 canonical records**, **462 additional identities required** for 1,000
- [ ] Independently deduplicate separate 100-row institutional-index intake (Canada and Camden) before any future canonical promotion
- [ ] Follow 100-record admission batches once primary source identity, rule, rights and locale are complete

No Android APK, signing, device work or Play rollout.


## Wave07 — 32 national institutional observances / five new markets (10 November 2026)

- [x] Prepare five separately sourced national authority lists: Estonia, Latvia, Lithuania, Iceland, Luxembourg.
- [x] Add 32 unique nationally scoped identifiers and their fixed or `NTH_WEEKDAY` recurrence rules; no EURES index-only auto-admission.
- [x] Add six title locales, new market labels/options, 2026–2028 recurrence validation, generated data and 320px browse tests.
- [ ] Run and pass protected PR exact-head CI and review comments.
- [ ] Merge and confirm **511** canonical observances (**289 GLOBAL + 222 NATIONAL**) across **36 markets**.
- [ ] Rich history and professional locale review remains separate; **56** preexisting source-reviewed stories preserved.
- [ ] Following Wave07 merge, target 1,000 needs **489** more distinct and source-qualified records.
- [ ] Continue 50–100 entry multi-country governmental batches, automated reconciliation and source-based acceptance.

No APK, Android signing, physical certification or Play release.


## Wave06 — three new institutionally sourced national markets (10 November 2026)

- [x] Research 2026 competent-authority calendars for Malta, Croatia and Cyprus.
- [x] Add 16 distinct national source records with fixed recurring dates and verified authority links.
- [x] Integrate country options, six display locales and stable offline ID generation.
- [x] Add dedicated dataset, date, provenance and Flutter 320px browse regression tests.
- [ ] Obtain exact-head CI and review feedback; do not infer a green check from successful source commits.
- [ ] Merge protected-main PR; confirm catalog version `2026.11.10.2`, **479 IDs**, **31 market options** and unchanged reviewed editorial histories.
- [ ] Expand additional national calendars in larger evidence-backed waves; 1,000 still requires **521 further unique canonical identities** if this PR lands.
- [ ] Qualified translations and full editorial stories are independent acceptance gates.

Owner's Android APK / signing / device / Play pause still applies.


## Institutional Wave05 — 7 global records (10 November 2026; source PR)

- [x] Document official UNESCO and WHO observances and detect the World TB Day alias without duplicating it.
- [x] Propose seven canonical source-backed entries with fixed-date rules, six display-title locales and five evidence-backed founding years; preserve two unknown years.
- [x] Add dedicated source/date/no-rich-editorial regression and development-workflow check.
- [ ] Pass exact-commit CI and Flutter/Web checks; review missing user-facing provenance and no duplicate identities.
- [ ] Review translations with qualified locale checks and keep original long-form narratives unapproved until reviewed.
- [ ] Merge through guarded PR, verify generated catalog revision `2026.11.10.1` on main, and then validate Web Preview content delivery.
- [ ] Continue 30–50 record institutional batches with independent author/date/recurrence/ID review; do not conflate batch candidates with published records.

**Proposed catalog after merge:** 463 unique (289 global + 174 national). Rich Editorial remains **56 reviewed**. No APK, Android signing, billing, Play or production rollout in this task.


## Content-first Wave04 — 83 sourced days / 15 new markets (9 November 2026)

[Source-level catalog, 83 individual records and provenance](docs/CATALOG_WAVE04_15_COUNTRIES_2026-11-09.md). Approved content-first implementation **adds 83 unique national/civic and institutionally recognized events**, making **456 unique observances (282 GLOBAL, 174 NATIONAL) across 28 country choices**. Retains all 373 canonical IDs and original colors/UX; published content revision `2026.11.09.4` after exact-source CI. New annual rules include last Monday of August (Philippines), last Saturday in August (Finnish Nature Day), fourth Monday in October (New Zealand Labour Day), along with statutorily fixed commemorations. The cultural St Brigid date remains 1 February, distinct from Ireland's conditional Monday employment holiday.

**Authority separation:** government holiday calendars are `OFFICIAL_INSTITUTIONAL` and university catalogued Finnish customary flag days are `RECOGNIZED_INSTITUTIONAL` with originator evidence. Never multiply a shared GLOBAL entry into a country-specific official claim. **Only one new formal introduction year is proven**, giving 65/456, unknown 391 marked `*`.

**Editorial:** 56 runtime reviewed, 25 complete six-locale drafts **awaiting human editorial and native-language review**, 375 with no researched full narrative. The Wave04 national titles and source summaries are NOT human-approved stories.

**Next five maxi-steps:** (1) validate exact-head 456-record catalog, 28-market six-locale and responsive tests, original ID retention and source-tier consistency; (2) continue primary-government-source expansion in batches 50–100 with regional/source country research, aiming first at 600, then 800, then 1,000+ without duplicated international dates; (3) review the 25 drafted six-locale histories with qualified human signoff and promote per-article only when approved; (4) produce new source-backed in-depth history batches for the growing uncovered set; (5) rerun additive Audit 360 on exact-source Flutter code and country/global browsing.

**Owner exclusions still active:** APK, production signing, Play Console, Android physical certification and Google Play distribution ON HOLD. Open #43/#54 are not considered completed; source-only CI and Web Preview can run. No Store-ready claim.

## Content-first milestone 03 — six new markets and 25 six-locale story candidates (9 November 2026)

**Source:** [Wave03 13-country expansion](docs/COUNTRY_WAVE03_SIX_NEW_MARKETS_2026-11-09.md) and [25-story review dossier](docs/EDITORIAL_25_SIX_LOCALE_DRAFT_QA_2026-11-09.md).

**Catalog:** from 354 to **373 distinct** records: 282 GLOBAL (unchanged), **91 NATIONAL** (+19), 13 countries (+6: CA 5, AU 3, BR 3, MX 3, IN 2, JP 3); EN/IT/ES/FR/DE/PT titles, original IDs and local-first behavior preserved. **64 documented formal institution years**, 309 unknown `*`. Versioned pack **2026.11.09.3**. Mexico shifted workday dates and Japan substitute holidays must not be confused with canonical dates.

**Historical stories:** 56 in runtime REVIEWED; all **25 candidates have six-locale texts** (the 8 older global candidates + 17 country drafts translated into ES/FR/DE/PT) with provenance, origin, significance, facts and participation suggestions. This meets structural completion of the translations, **not qualified human editorial/linguistic approval**. Source-specific chronology and translation parity CI controls prohibit accidental runtime promotion. **292 days still lack fully researched long-form stories**.

**Next 5 maxi-steps:** (1) exact-head CI Flutter data tests, 13-country UI at 320/390px, six locales, content-pack integrity; (2) qualified source/linguistic human review of 25 six-locale candidate stories and controlled per-story promotion; (3) additional country expansion and stable source-ledger by region/officiality, progressively toward 1,000+ distinct days; (4) structured long-form editorial expansion across remaining 292 days, maintaining date/source/year provenance; (5) additive Audit 360 + cross-application Flutter scanner/performance regression after every content milestone.

**User exclusions persist:** APK, signing, physical Android/Play testing and Google Play Console publication SUSPENDED. Do not reopen issues #43/#54 as active release work; the existing source CI may run without authorizing a mobile release.

## Content-first progress — Country Wave02, 9 November 2026

[Research, dates, provenance and history status](docs/CATALOG_GROWTH_COUNTRY_WAVE02_2026-11-09.md). Second content batch proposes **15 source-supported national days** beyond the 339 baseline, giving **354 unique events = 282 GLOBAL + 72 NATIONAL**. New market totals: IT 25, ES **8**, FR 9, DE **4**, PT **9**, GB **8**, US 9; no duplicated UN days and no replacement of approved IDs. Versioned bundled content: **2026.11.09.2**. Ten new establishment years are source-backed, increasing the total from 41 to **51**, without inferring unknown dates.

**Stories:** 56 reviewed and currently served; eight older Wave04 six-language candidates, nine older Wave01 EN/IT candidates, **eight new Wave02 EN/IT** candidate histories (25 drafts total, none counted as reviewed), **273** remaining without a researched long story. Wave02 drafts include original origins, date context and actions but require human fact verification + four additional language translations before approval.

**Next content-first order:** (1) exact-head CI + editorial gap run + source audit, (2) more primary-source dates for undercovered ES/DE/PT/GB and carefully admitted additional countries, (3) independent content review and six-language completion for 25 queued stories, (4) structured origin/quick facts/related-day UI with current design, (5) catalog-scale list/performance regression and incremental audit.

**Explicit pause remains in force:** NO APK, signed release, Play Console or native Android certification. Keep #43 and #54 paused/open. Source-only Flutter CI and Web Preview can run. New dates must not be mislabeled as national holidays, and an unknown introduced year stays `*`. This update supersedes older numeric snapshots for factual status while preserving them in historical roadmap sections.

## Content-first priority — 9 November 2026 (owner-approved)

**APK generation, Android physical certification, Play Console/Google Play and Store publication: ON HOLD.** Issues #43 and #54 are preserved, not closed. Continue Flutter source QA, data validation, richer stories, authority/source review and country discovery.

[Catalog Growth Wave01](docs/CATALOG_GROWTH_COUNTRY_STORIES_2026-11-09.md) introduces **43 sourced national/civic records**, preserving existing 296 IDs and producing **339 unique records: 282 GLOBAL / 57 NATIONAL**. Seven country views display each country's official/national layer separately from 282 shared world observances; the latter are not counted as new national announcements. Counts: IT 25, ES 4, FR 9, DE 2, PT 4, GB 4, US 9; combined browse totals range 284–307. UI uses lazy slivers, not 300 eager cards.

**Editorial coverage is not promoted by this expansion:** 56 reviewed rich stories; 8 Wave04 six-language drafts pending human approval; 9 new Country Wave01 EN+IT historical drafts requiring four additional languages and review; 266 records without researched full narrative. Source-backed formal years = 41; otherwise * remains. This is distinct from the 339 available six-locale metadata overviews.

**Next content-first five maxi-steps:** (1) complete exact-head CI/locale and calendar regression for 339; (2) expand low-coverage national markets ES/DE/PT/GB with individual official sources, no guessed dates; (3) research and human-review 8+9 queued histories in EN/IT/ES/FR/DE/PT; (4) extend global/region/originator coverage, de-duplicate and enrich history/info in batches of 20–30; (5) run full additive Audit 360 Flutter source scan + both lists after growth. Long-term 1,000+ distinct sourced events is a **target, not an established count**.

**Acceptance:** new primary-source ID/date/country/authority and six titles; deterministic recurrence 2026–2028; no overlabeling GLOBAL as NATIONAL; source-backed year or *; preserved preferences/content-pack rollback; reviewed narrative is promoted only after independent editorial and native-language checks; existing color system and light offline fallback retained. No native APK/Play gate is resumed without explicit user request.

## Execution update — 9 November 2026, five maxi-steps and full Audit 360

[Full source-bound Audit 360](docs/AUDIT_2026-11-09_FIVE_MAXISTEPS_360.md) supersedes earlier coverage counters **only for their factual statuses**; earlier roadmap sections are retained as historical execution records. Factory baseline used: App-Factory-Core@2b3ae9e, Master v27 / Golden Index v29.

| Workstream | Verified implementation or preparation | Unclosed acceptance |
|---|---|---|
| Saved physical performance (issue #54) | [PR #55](https://github.com/riccardopinato/World-Days/pull/55) includes clean-device Flutter profile mode for 0/50/150/296 favorites, raw FrameTiming driver, fail-closed report parser and device instructions | **DEVICE_NOT_VERIFIED**; no measured GPU/jank/RAM on phone |
| List architecture | Existing Saved/Around the World rendering unchanged: no physical regression proves a need for ListView.builder | optimization **CONDITIONAL**, not preapproved |
| Release P0 (issue #43) | Source/release-readiness matrix and existing signed APK+AAB workflow reviewed; native source gates pass on relevant PR SHAs | **BLOCKED** Google Play Console sandbox, owner-managed versionCode, manual signed production candidate, notifications, widget, Device/Play/App Ads |
| 296 histories (issue #47) | 296 canonical titles/verified overview metadata; **56 REVIEWED** rich articles in six locales; **8 NEW DRAFT** historical articles in six locales [PR #56](https://github.com/riccardopinato/World-Days/pull/56) | 8 drafts require human editorial+translation review, **232** entries still lacking researched rich articles; 8 proposal years are NOT visible in app |
| Full Audit 360 | 2026-11-09 comprehensive [report](docs/AUDIT_2026-11-09_FIVE_MAXISTEPS_360.md) with issue matrix, release evidence, lifetime purchase gate and cross-app audit addendum | runtime Store/devices NOT VERIFIED; next audit after physical acceptance |

Actual source state after the implementation merges: main@2c85501adce13dcad88e20f04715d96658916c70 before this audit-only documentation PR. The Flutter 3.47.3 on-PR gates are PASS: [QA PR #55 run 42547952400](https://github.com/riccardopinato/World-Days/actions/runs/42547952400); [editorial PR #56 source run 42547327148](https://github.com/riccardopinato/World-Days/actions/runs/42547327148) and [candidate validator 42547327160](https://github.com/riccardopinato/World-Days/actions/runs/42547327160). Every main SHA needs its **own** post-merge evidence.

**Critical path remains release E → F → J → K (issue #43)**. No automatic Play publish, no payment product activation, no fabricated device evidence; a verified signed APK/AAB requires an explicit owner/manual production workflow and one immutable signer/source/artifact manifest.

Execution truth for the repository. Product scope remains governed by `docs/PRODUCT_BIBLE.txt`.

Audit baseline (historical): `245f82148c1ca5ceee0977b82bf51a21b5b76a12`  
Full historical audit: `docs/AUDIT_2026-10-15_POST_PHASE_G.md`

## Execution refresh — 2026-11-03, post-PR #44

**Source stabilization integrated, NOT STORE CERTIFIED.**

- [PR #44](https://github.com/riccardopinato/World-Days/pull/44) was
  squash-merged through the active protected-main ruleset. The exact
  stabilization commit is `7c67f553b371d5b5e7a1d04b629d8ef7aa3a6dbe`
  and the source version remains `0.4.0+4`.
- The previous separate PRs #39–#42 were closed as superseded, not
  independently merged again.
- [Main branch protection #37](https://github.com/riccardopinato/World-Days/issues/37)
  has been **verified active and closed**: ruleset #26445843 targets the
  default `main` branch, requires PR with resolved conversations,
  up-to-date `validate` checks, blocks force-push/deletion and has
  no bypass.
- The integrated candidate's [Development checks #41630766103](https://github.com/riccardopinato/World-Days/actions/runs/41630766103)
  passed **104 Flutter + 9 Europe/Rome DST** tests, Flutter analyze and
  Web release; [Android admission #41630765848](https://github.com/riccardopinato/World-Days/actions/runs/41630765848)
  passed strict pre/post-scaffold dependency lock and ARM64 compile.
- Post-merge main [Development checks #41637425080](https://github.com/riccardopinato/World-Days/actions/runs/41637425080)
  and [Deploy Web Preview #41637424946](https://github.com/riccardopinato/World-Days/actions/runs/41637424946)
  are the **separate authoritative post-merge gates**. Always inspect
  their final conclusions and artifacts; a PR's green check cannot
  be substituted for post-merge source certification.

**Critical path remains Phase E → F → J → K**, tracked in
[release issue #43](https://github.com/riccardopinato/World-Days/issues/43):
Play Billing sandbox, exact-source signed APK/AAB, Android physical
notifications/widget/UX QA, AdMob domain-root app-ads.txt and official
Play Console declarations. None is closed by internal non-production
ARM64 build evidence.

The older October evidence below remains **historical**. Do not use
it as exact-head Store release certification.

## Editorial detail next wave — proposed 2026-11-03

- [ ] For all 296 canonical records: show verified date/period, authority,
      geography, establishment year when sourced (otherwise `*`), and source links
      in the original lightly tinted facts card.
- [ ] Expand source-reviewed historical narrative in **all six locales**.
      Pilot adds Africa Industrialization Day and enriches World Water Day;
      the remaining 267 still require individual primary-source and human
      editorial review, not generic AI-generated historical claims.
- [ ] Validate Rich Editorial and localized fallback, unknown years and
      large-text layout across mobile/Web on an exact GitHub CI head.

## Current release state

World Days is technically healthy but **NOT Store Ready**.

Current automated evidence:
- Phase I merge `44720a125db88386180f31951f9cf167c555b8a4` was the October baseline at `0.4.0+4`; superseded as main SHA by the November 3 Golden CivilDate integration.
- Post-merge Development checks #212: validators + analyze + **80 Flutter tests** + Web release + Android ARM64 build/upload PASS.
- The Android ARM64 step is conditional and skipped in PR validation; post-merge `main` remains the Android build gate.
- GitHub Pages deployment + hosted remote-content smoke PASS.
- Generated remote catalog: 296 records / 297 2026 occurrences.
- Hosted payload smoke: version `2026.10.14.1`, 501,993 bytes, SHA-256 `38e6ee66d3646c0c313ca7b4b8e395a79b2456ecfc5522cd25c948b0f624d8b7`.
- ARM64 internal release gate: ~24.1 MB.
- Phase C implementation merge: `446d1d5edb2a4cd52a773808f3a59d9f4a072bcf`.
- Permanent Android signing + production AdMob/UMP have prior physical evidence.

Important: the previous production/physical monetization evidence predates the current Phase-B/G.1 code. Final certification must use a new exact candidate artifact.

## Critical path to v1

Blocking sequence:

**E → F → J → K**

Phase A/B/C/D/G/H implementation scope is closed. Phase I repository implementation is also closed; its remaining repository-admin/live-URL evidence items run in parallel and must be truthful before final store release.

---

## Completed foundation

Steps 1–8.2 established the Flutter/CI baseline, canonical catalog, multilingual titles, market layer, visual system and share cards.

### Step 9 — Retention / native layer

Implementation complete:
- timezone-aware inexact local scheduling with stable IDs;
- daily/weekly/favorite/category reminder plans;
- notification diagnostics and deterministic reconciliation;
- notification tap + Home Widget deep links;
- Android XML/RemoteViews widget with offline projection;
- generated Android/iOS native setup and CI validation.

Open release evidence:
- exact-artifact physical notification/deep-link/widget QA remains required in Phase F.

### Step 10.1 — AdMob / UMP / permanent Android release identity ✅

Completed and physically validated on Android:
- permanent signing identity and production signer verification;
- production APK + AAB workflow;
- UMP consent on clean state;
- deny-consent path;
- Privacy Choices/revocation;
- production adaptive banner serving;
- public Privacy Policy.

The integration remains valid, but current-main exact-artifact certification is reopened by later code changes and belongs to Phase J.

---

## Phase A — Consumer UX alignment ✅

Completed:
- [x] Around the World browsing does not mutate profile market.
- [x] Today primary hero is interactive and not duplicated immediately.
- [x] Up Next shows occurrence dates.
- [x] Calendar has weekday headers, Today jump and current-day affordance.
- [x] Catalog load failure exposes Retry.
- [x] Source-card provenance preserves verification metadata.

- [x] Saved now surfaces followed categories and reminder subscription state while detailed reminder controls remain in Settings.
- [x] Around the World has explicit choose-country and no-verified-country-content empty states.
- [x] GLOBAL users no longer inherit an arbitrary Italy browse default; country browsing is explicit and transient.
- [x] Consumer failure copy for content updates and billing preserves current-state truth and recovery.

## Phase B — Data/runtime acceptance ✅

Completed:
- [x] Cache yearly occurrences and date indexes.
- [x] Include previous-year carry-over ranges.
- [x] Deterministic primary-observance ranking.
- [x] Semantic categories separated from `visualKey`.
- [x] Legacy visual-key reminder migration to semantic categories.
- [x] Visual collections and officiality filters.
- [x] Runtime/data-contract support for LAST_DAY_OF_MONTH and ONE_OFF.
- [x] Explicit unresolved authority/lunar future dates.
- [x] Runtime source verification metadata preserved.

Audit-required hardening:
- [x] Full-catalog occurrence acceptance for **2026, 2027 and 2028**, not only representative recurrence vectors.
- [x] `validate_dataset.py` requires at least one source for every publishable record.
- [x] Non-empty observance/source verification metadata is enforced in CI and runtime catalog decoding.
- [x] No-duplicate occurrence invariant covers observance/date/rule across generated years.
- [x] Cross-year range acceptance has explicit regression coverage.
- [x] 2026 generated occurrence output is cross-checked against the runtime recurrence engine.

## Phase C — Content understanding / editorial completion ✅

V1 coverage is intentionally two-tier and provenance-safe:

- **Verified Overview:** 296 / 296 launch records × EN/IT/ES/FR/DE/PT.
- **Rich Editorial:** 28 / 296 curated records, preserved as the reviewed long-form layer.

Completed:
- [x] Extended Rich Editorial schema: hook, Why this date, Origin/history, quick facts, related observances.
- [x] Annual campaign themes consumed from year overrides.
- [x] Every launch record has a concise Verified Overview derived only from canonical verified metadata.
- [x] Verified Overview copy is centralized in ARB localization resources and never relabeled as REVIEWED editorial.
- [x] Every reviewed Rich Editorial article is gated by canonical authority/source provenance with a strong primary/institutional/originator source.
- [x] Existing reviewed Rich Editorial content has EN/IT/ES/FR/DE/PT locale parity.
- [x] Generic “editorial coming next” placeholders are removed from consumer detail flows.
- [x] Full-catalog six-locale coverage is regression-tested.

Post-v1 content program:
- [ ] Expand Rich Editorial beyond the current 28 reviewed records only after source review.
- [ ] Add richer Why-this-date/origin/facts/actions where canonical sources support those claims.

## Phase D — Today / Calendar / Discover / market completion ✅

- [x] Today in 30 seconds for reviewed editorial entries.
- [x] Daily quiz / lightweight learning loop.
- [x] Tomorrow preview.
- [x] Calendar officiality/category/scope/country filters.
- [x] Upcoming 7 / 30 days.
- [x] Random discovery and themed collections.
- [x] v1 Calendar scope frozen to month + date detail + upcoming 7/30; dedicated day/week modes moved post-v1.
- [x] v1 Around-the-World scope frozen to the verified IT/ES/FR/DE/PT/GB/US seed; broader national coverage moved post-v1 so Phase C remains the content priority.
- [x] Locale and market remain independent, including transient Around-the-World browsing.
- [x] Seasonal collection expansion explicitly deferred post-v1 until editorial coverage is broader.

## Phase E — Remove Ads lifetime entitlement — EXTERNAL PLAY GATE

Implemented:
- [x] Provider-agnostic entitlement contract.
- [x] Persistent lifetime cache and centralized ProductLimits.
- [x] Official Flutter `in_app_purchase` adapter.
- [x] Purchase stream / restore / pending / cancel / error handling.
- [x] Entitled users suppress the ad request itself.
- [x] Settings purchase/status UX is connected to the entitlement boundary.

Store work:
- [ ] Create and activate Play one-time product `world_days_remove_ads_lifetime`.
- [ ] Review localized pricing around target EUR 2.99.
- [ ] Upload production-signed AAB to Play internal testing.
- [ ] Add license/internal tester configuration.

Audit blocker — provider finalization:
- [x] Durable/idempotent `completePurchase` recovery after completion failure or process restart.
- [x] Cached lifetime entitlement still attaches the store listener and does not prevent unfinished-transaction reconciliation.
- [x] Durable pending-completion marker is persisted before provider finalization and cleared only after successful/confirmed completion.
- [x] Automated tests cover failed completion → restart → provider redelivery → completed transaction.
- [x] Unverified/wrong-product terminal store results fail closed instead of surfacing a false purchase-success state.

Sandbox evidence:
- [ ] Product resolves with Play-localized price.
- [ ] Successful test purchase unlocks Remove Ads.
- [ ] Pending/cancel/error never unlock.
- [ ] Existing banner disappears and later ad requests are suppressed.
- [ ] Restart preserves entitlement.
- [ ] Reinstall/clear-local-state restore succeeds.
- [ ] Purchase is completed/acknowledged without repeat delivery.

Risk boundary:
- [x] Client-only store-state verification is explicitly bounded to the low-value v1 Remove Ads entitlement; any higher-value, subscription or account-bound monetization must reopen trusted-backend verification.

## Phase F — Retention physical QA — BLOCKING

Preparation now implemented:
- [x] Signed QA and Production lanes bind artifacts to the committed `pubspec.yaml` version identity.
- [x] Both signed lanes emit a machine-readable artifact manifest with source SHA, workflow run, version, signer and APK/AAB SHA-256/size.
- [x] Physical checklist requires hash verification before testing and forbids transferring PASS evidence to rebuilt bytes.
- [x] Compact large-text navigation has explicit focus order and automated >=48dp touch-target assertions.

Run on the exact release candidate:

- [ ] Notification permission-denied behavior.
- [ ] Immediate diagnostic notification.
- [ ] Scheduled diagnostic notification.
- [ ] Daily/favorite/category notification delivery.
- [ ] Notification tap/deep link.
- [ ] Channel-disabled diagnostic.
- [ ] Reboot reconciliation.
- [ ] N → N+1 app-update reconciliation.
- [ ] Home Widget add/pin.
- [ ] Widget current content.
- [ ] Widget date rollover.
- [ ] Widget locale/market refresh.
- [ ] Widget tap/deep link.
- [x] Rolling generic daily fallback beyond the tailored 21-day horizon.

Evidence must record source SHA, APK SHA-256, device and Android version.

## Phase G — Remote Content Pack v1 ✅

Core implementation complete:
- [x] Immutable bundled fallback.
- [x] Versioned manifest on GitHub Pages.
- [x] HTTPS, expected byte size and SHA-256 verification.
- [x] Full World Days catalog/domain validation before activation.
- [x] Versioned staged storage.
- [x] Crash-resilient active/previous pointer.
- [x] Rollback to previous verified content.
- [x] Bundled fallback after invalid stored state.
- [x] Annual campaign/theme and authoritative date overrides.
- [x] Settings check/install/status UX.
- [x] Offline/network/checksum/corrupt-active tests.
- [x] Web explicitly remains bundled-only.

### Phase G.1 — Remote content hardening ✅

Audit findings:
- [x] Runtime `payloadUrl` is pinned to `riccardopinato.github.io/World-Days/content/` with a constrained immutable filename shape.
- [x] Payload download is streamed through a hard byte cap before materialization.
- [x] Bounded stream overflow has direct automated coverage.
- [x] `validate_content_pack.py` added to Signed Android QA.
- [x] `validate_content_pack.py` added to Production Android Release.
- [x] `validate_native_content_pack.py` added to Signed Android QA.
- [x] `validate_native_content_pack.py` added to Production Android Release.
- [x] Post-Pages-deploy smoke gate checks hosted manifest/payload propagation, size and SHA-256 agreement.
- [x] Signed-manifest cryptography remains a future escalation only if the hosting/threat model changes.

## Phase H — Code hygiene / automated QA expansion ✅

Completed:
- [x] Obsolete synthetic-package l10n option removed.
- [x] Notification diagnostics split from consumer Settings.
- [x] Source verification metadata preserved.
- [x] Weekly reminder weekday is user-selectable.
- [x] Maintained `integration_test` journey: launch → Today → detail → favorite → Saved → Calendar → Settings.
- [x] AppController tests use injected entitlement/content/notification/widget boundaries.
- [x] Settings interaction/widget actions have widget-test coverage.
- [x] Calendar filter/navigation behavior has regression coverage.
- [x] Around-the-World browsing is regression-tested as transient to profile market.
- [x] Saved → detail navigation and favorite persistence have regression coverage.
- [x] Monetization controller is tested behind a fake UMP/Mobile Ads platform boundary.
- [x] Entitlement recovery covers failed finalization, restart/redelivery and durable completion markers.
- [x] Filesystem content-pack storage has active/previous, rollback and corrupt-pointer recovery tests.
- [x] Notification/widget retention adapters are injectable and deterministic controller behavior is covered.
- [x] Responsive/accessibility smoke covers 360×800 at 200% text scale, wide NavigationRail switching and calendar button semantics.
- [x] Large-text overflow in `ObservanceHero` fixed without capping the platform text scale.
- [x] Flutter/Kotlin/dependency warning sweep found no Phase-H blocker; the generated iOS launcher-icon alpha warning remains a Phase-I/store-scope concern if iOS stays in v1.
- [x] Pull-request Development checks pass analyze + 76 Flutter tests + Web release; Android ARM64 remains the conditional post-merge `main` gate.

Deferred / bounded follow-up:
- [ ] Split oversized orchestration/UI files only when next touched: `AppController`, Settings and Calendar first.
- [x] Extend accessibility automation with explicit compact-navigation focus order and >=48dp touch-target assertions; screen-reader/contrast remain physical Phase J checks.
- [ ] Keep provider/plugin-specific Play billing behavior in the Phase E sandbox and Phase J exact-artifact gates rather than simulating store behavior in unit tests.

Evidence: `docs/PHASE_H_AUTOMATED_QA_EVIDENCE.md`.

## Phase I — Governance / product-truth / privacy alignment — IMPLEMENTATION COMPLETE / ADMIN + DEPLOY EVIDENCE GATES

Completed:
- [x] Canonical Android ID is `com.riccardopinato.world_days`.
- [x] App Factory baseline aligned to `47c47f49a7b46812e3bd6f1231c3524f2b52b826` (Master v26.6 / Golden Index v18).
- [x] README, Android signing, AdMob docs and Golden reuse manifest reflect current subsystem state.
- [x] Post-Phase-G audit recorded.

Governance:
- [x] Release version-name/version-code policy defined; committed `pubspec.yaml` is the production source of truth.
- [x] Release tag/changelog/evidence convention defined in `docs/RELEASE_GOVERNANCE.md` and `CHANGELOG.md`.
- [ ] USER-ACTION: protect `main` with required PR/green-check rules. Connected GitHub integration has no Admin permission (branch-protection endpoint returns 403).
- [x] Production Android Release fails closed unless dispatched from `main`; artifact version identity is source-bound rather than run-number-bound.

Product-truth decisions:
- [x] V1 production scope frozen to **Android-first + Flutter Web Preview**.
- [x] iOS production/App Store release moved post-v1 in Product Bible.
- [x] No iOS production signing/AdMob/App Store pipeline is claimed for v1.
- [x] V1 monetization frozen to the safe top anchored adaptive banner + lifetime Remove Ads; inline/interstitial formats moved post-v1.
- [x] First-party analytics/event pipeline explicitly deferred post-v1.
- [x] Saved IA aligned in Phase A: favorites, followed categories, reminder subscriptions and recents.

Privacy:
- [x] Privacy Policy source updated for Google Play Billing / purchase processing and minimal local entitlement/finalization state.
- [x] Privacy Policy source updated for mobile GitHub Pages remote-content requests.
- [x] Privacy Policy `Last updated` set to 15 October 2026.
- [x] Privacy/Data Safety engineering inputs frozen in `docs/DATA_SAFETY_INPUTS.md` after Android-first / no-analytics decisions.
- [x] POST-MERGE DEPLOY: GitHub Pages deployment completed successfully after Phase I merge.
- [ ] POST-MERGE LIVE URL: independently verify the canonical privacy URL serves the 15 October 2026 text; current external fetch tooling cannot reach that Pages URL.

## Phase J — Exact-artifact regression / release certification — BLOCKING

Release-prep automation:
- [x] Production workflow emits `production-artifact-manifest.json` binding source SHA, workflow run, versionName/versionCode, signer and exact APK/AAB hashes.
- [x] Release-governance validation prevents regression to workflow-run-number versionCode in both production and signed-QA lanes.
- [x] Release-evidence writer has deterministic Python tests in Development checks.

Release candidate:
- [ ] Freeze source SHA after blocking phases are closed.
- [ ] Generate production APK + AAB from the approved source.
- [ ] Verify permanent direct-APK signer SHA-256.
- [ ] Capture APK/AAB SHA-256.
- [ ] Verify production workflow source identity.
- [ ] Run N → N+1 update-in-place using two permanent-signature builds.

Play identity:
- [ ] Configure/confirm Play App Signing.
- [ ] Record upload certificate fingerprint.
- [ ] Record Play app-signing certificate fingerprint.
- [ ] Confirm expected distinction from direct-distribution signing where applicable.

Regression:
- [ ] Full offline startup/navigation.
- [ ] Today/Calendar/Discover/Saved/Settings.
- [ ] Search/filter/market/localization.
- [ ] Favorites/recents/streak.
- [ ] Share cards.
- [ ] Remote content update/rollback/offline fallback.
- [ ] AdMob consent/banner/Privacy Choices.
- [ ] Remove Ads Play sandbox.
- [ ] Retention physical QA.
- [ ] Accessibility/large-text/screen-reader/focus regression.
- [ ] Upgrade/install-in-place regression.
- [ ] Crash-free smoke over repeated cold/warm launches.

Evidence:
- [ ] Build final Evidence Bundle.
- [ ] Verdict: **CERTIFIED / NOT CERTIFIED / BLOCKED**.

## Phase K — Store readiness — FINAL ONLY

Do not start final submission until C, E, F, I and J are closed.

Developer website / app-ads:
- [ ] Choose final developer website hostname.
- [ ] Publish the exact AdMob-provided `app-ads.txt` snippet at **hostname root**.
- [ ] Do not rely only on `/World-Days/app-ads.txt`; AdMob resolves the store developer-site hostname and checks `/app-ads.txt`.
- [ ] Link the same developer website in Play listing.
- [ ] Verify AdMob crawler status after publication.

Play Console:
- [ ] App setup / package association.
- [ ] Internal test release and billing evidence.
- [ ] Data Safety aligned to final SDK/network set.
- [ ] Content rating / target audience / ads declarations.
- [ ] Store listing EN canonical + planned localizations.
- [ ] Screenshots.
- [ ] Feature graphic.
- [ ] Icon verification.
- [ ] Privacy Policy URL.
- [ ] Support/developer website.
- [ ] Production rollout/staged rollout plan.

If iOS remains in v1:
- [ ] Add equivalent App Store Connect readiness track before final certification.

---

## Post-v1 candidates

- Broader national/regional market coverage.
- iOS production release if v1 becomes Android-first.
- Analytics/KPI pipeline if intentionally deferred from v1.
- Inline adaptive ads / conservative completion-point interstitials if intentionally deferred.
- Additional seasonal collections.
- Optional signed content manifests only if threat model requires them.

## Release policy

Green CI is necessary but not sufficient.

World Days is publishable only when the **same exact candidate** satisfies:
1. automated gates,
2. store/provider sandbox gates,
3. physical-device gates,
4. signer/artifact identity evidence,
5. privacy/store metadata consistency,
6. final Evidence Bundle verdict.


## Source-reviewed stories: batch 01 — pending PR (2026-11-03)

- [ ] Add and validate source chronology for Education 2018, Environment
  1972, Oceans 2008 and Wildlife 2013, preserving distinctions between
  UN proclamation, date origin and first observance.
- [ ] Review multilingual wording across EN, IT, ES, FR, DE, PT;
  30/296 detailed histories after merging this batch; remaining 266.
- [ ] Pass full current CI and source checks, merge through protected
  main, then verify Web/Android and update issue #47.
- [ ] Continue further batches of source-audited stories until 296/296,
  not generic machine-generated filler.


## Editorial + discovery implementation — 2026-11-03 (PR pending)

- Source-backed research batch 02 proposes 11 additional histories
  and 14 first-party founding-year citations; expected coverage
  **41/296 stories, 20/296 establishment years** after acceptance.
- Every one of the 296 detail pages gains a deterministic
  “Related observances” continuation section, prioritizing topic
  relevance and source-reviewed articles, without new tracking or
  extra advertising slots. Every user-initiated navigation is voluntary.
- No unsourced date/year is added. **255 stories and 276 years**
  are still incomplete and remain issue #47 work.
- After CI: protected-main review/merge, remote Web content smoke,
  strict-lock Android ARM64 compilation, device accessibility QA and
  retention measurement only with privacy-compliant analytics.


## Wave 03 — research and localization acceptance gate (2026-11-03)

- [ ] Accept 15 new factual historical narratives in six languages,
  each with a distinct institutional source and dated timeline.
- [ ] Pass dedicated `tool/validate_editorial_wave03.py`, full
  catalog/translation validation, all Flutter tests, Rome DST and Web.
- [ ] Merge only via protected main; verify current source SHA's Web
  content pack and ARM64 Android artifact independently.
- [ ] Continue remaining **240/296** sourced histories and
  **261/296** unverified establishment years through issue #47.
