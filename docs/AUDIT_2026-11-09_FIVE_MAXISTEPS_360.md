# World Days — Audit 360° completo dopo i cinque maxi-step

**Rapporto:** WD-AUD-2026-11-09-FIVE-STEP | **Data:** 9 novembre 2026 | **Ambito:** sorgenti, Product Bible, roadmap, test e GitHub Actions; dati runtime fisici e Play Console esplicitamente non disponibili.
**Factory baseline:** App-Factory-Core@2b3ae9e01764b7504980efca34f2543949dc7b89, CURRENT Master v27 / Golden Index v29 / Registry v2. Specifica: audit/MASTER_AUDIT_360_APP_FACTORY_v1.txt, inclusa addendum Flutter full checkout e due liste.
**Repo:** riccardopinato/World-Days | **base di questo rapporto:** main@2c85501adce13dcad88e20f04715d96658916c70 (dopo PR #55 e #56) | **Flutter SDK CI:** 3.47.3 | **versione sorgente:** 0.4.0+4. Il commit finale del presente rapporto può essere differente; non trasferire senza prova l'evidenza release/device.
**Fonti primarie locali:** [AGENTS](../AGENTS.md), [Product Bible](PRODUCT_BIBLE.txt), [Roadmap](../ROADMAP.md), [Editorial Policy](EDITORIAL_POLICY.md), [Physical QA](STEP_9_PHYSICAL_QA.md), [Profile runbook](SAVED_ANDROID_PROFILE_RUNBOOK_2026-11-09.md), [Release evidence](RELEASE_P0_EVIDENCE_MATRIX_2026-11-09.md).
**PR verificate:** [#53](https://github.com/riccardopinato/World-Days/pull/53) UI 390px, [#55](https://github.com/riccardopinato/World-Days/pull/55) dispositivo/profile/release-readiness, [#56](https://github.com/riccardopinato/World-Days/pull/56) Wave04 candidati sei lingue.
**CI pre-merge source:** #55 [run 42547952400](https://github.com/riccardopinato/World-Days/actions/runs/42547952400) SUCCESS; #56 [run 42547327148](https://github.com/riccardopinato/World-Days/actions/runs/42547327148) Development SUCCESS e [run 42547327160](https://github.com/riccardopinato/World-Days/actions/runs/42547327160) candidates SUCCESS. Al momento della redazione il nuovo main dopo #55 ha avviato [Development run 42548174013](https://github.com/riccardopinato/World-Days/actions/runs/42548174013) e [Web Preview 42548174005](https://github.com/riccardopinato/World-Days/actions/runs/42548174005); i risultati post-merge vanno letti separatamente prima di dichiarare il gate chiuso.

## A. Executive verdict

- World Days è un'app consumer Flutter Android-first, con Web Preview e sei lingue, centrata sulle ricorrenze internazionali verificabili.
- Il catalogo istituzionale e dei mercati contiene 296 osservanze. Le date/periodi, i nomi localizzati e i Verified Overview sono previsti su tutto il catalogo; i 296 record non sono equivalenti a 296 articoli storici approfonditi.
- Le **storie Rich Editorial revisionate e in uso sono 56/296**; 8 nuovi articoli completi per EN/IT/ES/FR/DE/PT sono stati archiviati in Wave04 come DRAFT/PENDING HUMAN, non pubblicati; **232/296** sono ancora senza una storia approfondita studiata.
- **Anni di istituzione già supportati da prove istituzionali: 35/296**; altri 8 proposti nella Wave04 e NON integrati; gli ignoti devono restare identificati con *.
- La correzione del dropdown Paese a 390px è integrata; nessuna regressione sorgente è stata rilevata sui test della PR #53, ma le interazioni native sul telefono richiedono collaudo.
- La schermata Saved contiene un ListView eager con 604 figli dichiarati per 296 preferiti; test CI mostra sei card montate. Non c'è prova di un problema di scroll su device.
- Test Flutter on-demand in modalità profile già scritti e parser fail-closed, ma **nessuna traccia FrameTiming fisica eseguita da questa chat**. Non ottimizzare ListView prematuramente.
- La pipeline di compilazione Android non equivale a un APK/AAB prodotto e firmato con identità release né a installazione da Play Store.
- Il P0 di pubblicazione resta **BLOCKED/NOT VERIFIED**: Play Billing sandbox, test prodotto lifetime, notifiche/widget reali, esatti APK/AAB firmati, store listing/Data Safety e app-ads.txt root.
- Il miglior rapporto rischio/valore è: chiudere release evidence su un unico source/artifact, preservare la versione già installata e lavorare sulle storie per batch indipendenti con revisione linguistica.
- NON introdurre un nuovo database, librerie mappe, AI generativa, nuove reti pubblicitarie o migrazioni massive per risolvere i blocchi attuali.
- NON marcare la Wave04 REVIEWED finché mancano conferma fonti, revisione del testo in inglese e revisione linguistica delle cinque traduzioni.

## B. Baseline, autorità, provenienza

| Strato | Valore | Evidence | Limite |
|---|---|---|---|
| Product scope | docs/PRODUCT_BIBLE.txt | SOURCE POLICY | Android v1, Web Preview, iOS post-v1 |
| Execution | ROADMAP.md, issue #43/#47/#54 | ROADMAP/ISSUE | vecchie righe storiche non sostituiscono lo stato attuale |
| Factory | Core@2b3ae9e, Master 27, Index 29 | CENTRAL BASELINE | vincola processo, non distribuisce app |
| Codice app | World-Days@2c85501 | GITHUB SOURCE | non APK installato |
| CI PR #55 | 42547952400 | CI EXACT-HEAD PR PASS | non signed-release |
| CI PR #56 | 42547327148 + 42547327160 | CI EXACT-HEAD PR PASS | draft non human-reviewed |
| 2 liste | benchmark catalogo PR #63 e test PR #53 | FLUTTER WIDGET TEST | non frame Android |
| Dispositivo/Play | nessuna traccia attuale | DEVICE_NOT_VERIFIED / PROVIDER_NOT_VERIFIED | non attribuire PASS |
| Privacy/Ads | policy e implementazione presenti, precedente evidenza fisica | SOURCE + HISTORICAL | prior evidence non certifica nuovo SHA |

## C. Scorecard qualitativa, senza numeri inventati

| Dimensione | Esito | Confidenza |
|---|---|---|
| Product scope e differenziazione | Buon perimetro, catalogo istituzionale e local-first | alta (docs + source) |
| Navigazione/UX | Implementata; overflow #52 corretto | alta sorgente / media runtime |
| Design/accessibilità | Design Material 3 e responsive; test su varie larghezze | media (widget test, screen reader fisico assente) |
| Localization | 6 UI/overview; Rich Editorial 56/296; Wave04 draft 8 | alta per conteggi, revisione Wave04 aperta |
| Integrità dati/catalogo | Seed versionato, provenienza e rollback pack | media-alta source; ripristino fisico N/D |
| Privacy/sicurezza | Offline-first, no login richiesto, confini Ads/UMP | media; verifica Play Data Safety aperta |
| Notifiche/widget | Source, fake tests e checklist | bassa su delivery reale, DEVICE_NOT_VERIFIED |
| Billing premium | Non-consumable code e failure tests | bassa Play purchase, PROVIDER_NOT_VERIFIED |
| Codice/architettura | Flutter separato per controller/services/repositories | media-alta CI |
| Performance Saved | 296 preferiti montati in widget test | N/D frame GPU, jank, memoria fisica |
| CI Web e ARM64 | PR green, test/localization/content pack | alta per SHA specificato |
| Android release firmata attuale | Non dimostrata | NOT VERIFIED |
| Store/monetizzazione reale | Non dimostrata | NOT VERIFIED |

## D. Inventario capability e stato verificabile

| Area / punto d'ingresso | Componente | Stato prodotto | Prova minima | Gap |
|---|---|---|---|---|
| Oggi | hero e osservanze correnti, prossimi eventi | IMPLEMENTATA IN SORGENTE | main + Flutter UI tests | device smoke |
| Calendario | mesi, date, filtri/ricorrenze | IMPLEMENTATA IN SORGENTE | test recurrence, civil day/DST | locale/timezone fisico |
| Scopri | categorie e collezioni, in-depth filter | IMPLEMENTATA IN SORGENTE | test discovery | UX ad ampio dataset |
| In giro per il mondo | selezione Paese transient, 7 mercati | IMPLEMENTATA IN SORGENTE | PR #53 + 36 layout cases | device 320/390px |
| Salvati | favorite, recents, categories, subscriptions | IMPLEMENTATA IN SORGENTE | PR #53 Saved stress 296 | frame/device #54 |
| Dettaglio | authority/source, date/period, *, related days | IMPLEMENTATA IN SORGENTE | generated records + validators | peer-review microcopy |
| Verified Overview | breve spiegazione di 296 record × 6 | IMPLEMENTATA / METADATA | generated catalog/l10n | non è Rich Editorial |
| Rich Editorial | 56 articoli × 6 | IMPLEMENTATA / REVIEWED | generators + validators | restanti 240 |
| Wave04 | 8 storie × 6, fonti e timeline | DRAFT/PENDING HUMAN | PR #56, CI candidate | NON IN APP |
| Notifiche | daily/weekly/favorite/category | IMPLEMENTATA SOURCE | source mocks/tests | fisico, reboot, delivery |
| Home Widget | Today, 45-day projection | IMPLEMENTATA SOURCE | Android native source/tests | launcher fisico |
| Share cards | local procedural imagery, social share | IMPLEMENTATA SOURCE | repository/tests | sharing device |
| Remote Content Pack | HTTPS hash, rollback, bundled fallback | IMPLEMENTATA SOURCE | validators and rollback tests | install/update device |
| Ads/UMP | banner gating e Privacy Choices | IMPLEMENTATA SOURCE | source tests + historical evidence | live/sandbox current SHA |
| Remove Ads | one-time lifetime entitlement | IMPLEMENTATA SOURCE | unit tests | Play product/purchase/restore |
| EN/IT/ES/FR/DE/PT | localization switching | IMPLEMENTATA SOURCE | build+locale validators | large font screen reader |
| CI/Web Preview | analyze, tests, Web build/deploy | IMPLEMENTATA/VERIFICATA SHA | runs | non garantisce Store |
| APK/AAB signing | manual signed pipelines, SHA manifest | IMPLEMENTATA SOURCE | workflow source | new exact-source artifact absent |
| Profile instrumentation | four favorites cohorts, engine frame timing parser | IMPLEMENTATA SOURCE | PR #55 tests/parser | DEVICE_NOT_VERIFIED |

## E. Audit schermate e journey

| Schermata | Journey osservabile da sorgente | Difetto/rischio | Verifica successiva |
|---|---|---|---|
| Today | apre dettaglio e favorite; dataset locale | notifiche / widget non certificati | tap/open/locale/restart dispositivo |
| Calendar | naviga date con recurrence | leap/DST gestiti da test; display device aperto | Android midnights/locale |
| Discover | selezioni, filtri, surprise me | review status distingue 56 rich vs fallback | smoke empty/out-of-scope |
| Around the World | transient country selector | overflow 12px corretto PR #53 | test telefono e screen reader |
| Saved | favorite, recents, followed, gestione | 604 child delegate a pieno catalogo, no proof jank | test on-device issue #54 |
| Detail | source, chronology, source-backed star fallback | Wave04 non deve comparire REVIEWED | six-language content QA |
| Settings | language/theme/reminders/purchase/privacy | provider state e permessi non validati su device | real UMP/Play/device |
| Share | share cards local | differenze Android FileProvider e intent | real Android sharing |

Il ciclo preferiti create/toggle → save → close/restart → filter → delete/untoggle è verificato solo nei percorsi coperti da sorgenti/test. Persistenza dopo reinstallazione/cambio telefono, import/export e dati reali sono **NON VERIFICATI**. Nessuna funzionalità di account o sync obbligatorio è richiesta nel v1: non proporla come gap.

## F. Universal entity lifecycle matrix

| Entità | Create/edit/delete/restore | Owner dati | Prova e rischio |
|---|---|---|---|
| Observance canonica | dataset immutabile versionato, non cancellabile dall'utente | asset seed/Content Pack | provenienza, checksum, rollback; non toccare schema senza gate |
| Editorial article | approvazione separata, rebuild versionato | data editorial/generator | 56 REVIEWED; 8 candidate non promosse |
| Favorites | toggle/reverse | local UserPreferences | CI widget; restart/update device N/D |
| Recents/streak | app-managed retention | local prefs | source tests; manual restart N/D |
| Followed categories/reminder prefs | settings/toggle | local prefs | unit test; Android channels N/D |
| Notifications scheduled | reconcile/update/cancel | native adapter | app/service source; exact delivery N/D |
| Home screen projection | generated daily snapshot | app widget service | source, device refresh N/D |
| Content update pack | download/stage/activate/rollback | ContentPackManager | CI test+SHA; real file storage N/D |
| Entitlement / Remove Ads | provider purchase, restore, pending | billing/store adapter | unit tests; Play license tester N/D |
| Personal accounts, multi-user data | NOT APPLICABLE to v1 | none | no forced identity or sync engine |

Delete/restore audit: removing a favorite must not delete canonical observance, editorial content or another user's data. Offline/content-pack rollback must not purge favorites. Device persistence and update paths need proof before claiming no loss.

## G. Issue register — evidence-based

| ID | Classe | Gravità | Finding | Evidenza / Status | Minimum gate |
|---|---|---|---|---|---|
| WD-AUD-001 | STORE BLOCKER | P0 | Play lifetime purchase, AAB, signing, actual QA | [#43](https://github.com/riccardopinato/World-Days/issues/43) OPEN / BLOCKED | verified Play-installed tests + artifacts |
| WD-AUD-002 | DEVICE GAP | P0 for release | notifications/widgets physical acceptance | [Phase F](STEP_9_PHYSICAL_QA.md) / NOT VERIFIED | exact APK + device records |
| WD-AUD-003 | UI BUG | P2 / FIXED SOURCE | 390px dropdown overflow | [#52](https://github.com/riccardopinato/World-Days/issues/52) CLOSED, PR #53 | physical small-screen smoke |
| WD-AUD-004 | PERFORMANCE UNKNOWN | P2 | full favorites may cause jank | [#54](https://github.com/riccardopinato/World-Days/issues/54) OPEN / NEEDS TEST | Android engine timings and memory |
| WD-AUD-005 | EDITORIAL COVERAGE | P1 content | 240/296 not reviewed rich | [#47](https://github.com/riccardopinato/World-Days/issues/47) OPEN | sources/translation/review per article |
| WD-AUD-006 | DRAFT HUMAN GATE | P1 content | 8 ×6 new prose not approved | [Wave04](EDITORIAL_WAVE04_CANDIDATES_2026-11-09.md) | source + six-language human review |
| WD-AUD-007 | STORE CONFIG | P0 release | root app-ads.txt and Play Data Safety not verified | [#43](https://github.com/riccardopinato/World-Days/issues/43) | live provider and owner evidence |
| WD-AUD-008 | DOC DRIFT | P2 | older README/roadmap numbers (28/41) and old release claims | initial docs read | keep new status appendix source-pinned |
| WD-AUD-009 | RELEASE ID | P0 gate | 0.4.0+4 may not exceed last Play-uploaded code | pubspec + #43 | owner confirms maximum Play versionCode |
| WD-AUD-010 | CONTEXTUAL PERFORMANCE | P3 | around-the-world list eager | 4 entries max per actual country | no refactor; revisit only with new country scale |
| WD-AUD-011 | SECURITY/RESTORE | P2 QA | device upgrade preserves favorites and entitlement | source only | same-signer N→N+1 test |
| WD-AUD-012 | BRAND/COMPETITION | P3 research | external site also uses "World Days" brand | public [world-days.com](https://world-days.com/) | trademark/market review if preparing launch; no infringement claim |

## H. Incongruenze Chat ↔ GitHub ↔ documenti ↔ release

- Passato: 28/296 o 41/296 Rich Editorial citati da README/vecchie sezioni ROADMAP. Presente: generator + Wave03 = **56/296**, Wave04 = 8 drafts separati. Nuova appendice di roadmap deve prevalere sui contatori storici.
- Passato: PR #53 richiedeva ancora gate Android post-merge. Verificato: sviluppo e ARM64 per main@6dd6916 SUCCESS; ogni successivo commit riapre il gate exact-source. 
- Un workflow di code-signing definito non prova un nuovo APK firmato; il binario ARM64 interno CI non equivale a Production Android Release.
- Il profilo CI 296 preferiti misura wall-time di Flutter test, non durata GPU frame. Il profilo on-device aggiunto non è stato eseguito.
- 8 nuovi testi scritti in sei lingue non sono 8 nuovi articoli REVIEWED: metadata e generator continuano a indicare 56 in runtime.
- L'indice Core/Golden v29 è attuale come processo. Le stringhe di bootstrap World Days v26.6 in AGENTS/Product Bible sono baseline storiche del progetto e NON riscrivono CURRENT.
- Proposta di iOS produzione o nuova AI locale non fa parte del v1 Android; nessun change autorizzato da questi maxi-step.

## I. Qualità, CI, release, test matrix

| Gate | Target/prova disponibile | Stato |
|---|---|---|
| Flutter static analyze | PR #55 Development run 42547952400 | PASS (source PR) |
| Flutter test/unit/widget | PR #55 e PR #56 Development checks | PASS (source PR) |
| Europe/Rome DST | PR Development checks | PASS (source PR) |
| Web release build | PR checks | PASS (source PR) |
| Editorial 8×6 draft validator | PR #56 run 42547327160 | PASS (draft shape/parity, not language approval) |
| Catalog 296/56/8/232 gap report | PR #56 workflow artifact | PASS (inventory only) |
| Native signed APK+AAB candidate | explicit manual production workflow | NOT VERIFIED |
| Actual billing purchase/cancel/restore | Play internal license tester | BLOCKED by Console/provider |
| Notification permission/reboot/delivery | physical Android exact APK | NOT VERIFIED |
| Launcher widget pin/tap/day change | physical Android | NOT VERIFIED |
| Saved frame P50/P95/P99+jank+RAM | physical Android clean fixture | DEVICE_NOT_VERIFIED |
| AppLab trusted production certification | manual exact artifact | NOT VERIFIED |
| Store listing/rollout | Play Console | NOT VERIFIED |

Never collapse CI green → device PASS → Store-ready. When running manual test, log source hash, artifact hash, signer, installed variant, device and observed result per scenario.

## J. App Factory, donor, Golden, capability re-use

- Reuse **existing** CI/release/source provenance patterns from Golden CI + Android Release + Web Deploy, still COPY-READY, not automatic consumer certification.
- Source-only testing vs runtime/physical validation follows AppLab CERTIFIED PROCESS while Release Reality Physical Validation Golden remains DRAFT, not falsely upgraded.
- Existing local-first content pack semantics and localization contracts are maintained; do not introduce alternative storage or duplicate billing, reminder or catalog owners.
- Flutter lexical scanner and World Days benchmark included in canonical Audit 360 addendum from Core PR #88; historic portfolio scan 13 Flutter repos / 1,467 Dart at 2026-11-09, 0 matches **only for specified legacy API patterns**. Six Cooking Anime accentColor cases were false positives; Anna background notification callback signature was correct.
- Wave04 research and FrameTiming summary scripts are **app-scoped QA/editorial candidates**, not globally certified Golden or new CAP. AppLab consumer/performance portability must be shown before promotion.
- No new app-to-app sync, shared account or cross-app data owner should be inferred for World Days.

## K. Competitor and differentiation — external public reference (9 November 2026)

| Reference | Observed differentiation / public features | Relevance |
|---|---|---|
| [National Today](https://nationaltoday.com/national-today-calendar/) | very broad calendar of national/popular dates | World Days can differentiate by authority/provenance tiers, not sheer count |
| [Checkiday](https://www.checkiday.com/updates.php) | mobile apps, notifications, RSS, calendar feeds | optional future export/subscription candidate, requires product decision |
| [National Day Calendar](https://nationaldaycalendar.com/) | editorial celebrations, recipes, quizzes and educational resources | richer original stories could support discovery; no copying |
| [World Days website](https://world-days.com/) | country-aware calendars and email reminders, shared generic name | compare international search/branding; not evidence of trademark violation |
| [National What Day? Play listing](https://play.google.com/store/apps/details?id=nationalwhatday.App) | offline daily app, reminders, widget, streaks | parity exists in source, but Store and device readiness differ |

Competitive claims are source/site descriptions, not usage metrics or independent market shares. Increased engagement or advertising revenue remains a hypothesis without privacy-compliant post-release data.

## L. Opportunity backlog — keep approval boundaries

**Already approved / actioned:** UI overflow fix; Flutter full checkout audit; Saved profile instrumentation; P0 release evidence preparation; eight Wave04 draft histories; retrospective audit.
**Approved but BLOCKED:** physical device QA including profile and notifications/widget; Play Billing licensed sandbox and Play-installed purchase; final signed APK/AAB and current Store evidence.
**Proposed only / not product-approved:** optional calendar subscriptions, wider national market coverage, enhanced topic discovery, further curated history waves with researched sources.
**Defer/do not do now:** convert every ListView.builder; copy 240 histories from the internet; invent year of introduction from a date rule; new accounts, cloud sync, subscriptions, embedded AI model, interstitial ads to artificially extend sessions.
**Simplification:** preserve one catalog source, one entitlement owner and one notification projection; avoid duplicate UI storage, oversized assets and conflicting provider workflows.

## M. Top 20 interventions, prioritized

| # | Intervention | Lane | Complexity | Reuse | Gate |
|---:|---|---|---|---|---|
| 1 | Confirm max Play-uploaded versionCode and package | P0 | S | medium | owner Console |
| 2 | Freeze final candidate exact source SHA | P0 | S | high | CI after source freeze |
| 3 | Execute production signing from main and verify APK/AAB hashes | P0 | M | high | secrets + manual release workflow |
| 4 | Play install internal-track AAB and non-consumable purchase/restore | P0 | M | medium | owner+license tester |
| 5 | Complete notification permission/delivery/reboot scenarios | P0 | M | high | phone/same artifact |
| 6 | Complete Home Widget date/locale/tap/pin scenarios | P0 | M | high | device/launcher |
| 7 | Confirm root app-ads.txt domain and AdMob crawler | P0 | S/M | medium | provider live proof |
| 8 | Complete Play Data Safety/privacy/content rating/support/screenshots | P0 | M | medium | owner console |
| 9 | Validate N→N+1 update without loss of favorites/settings | P0 | M | high | same permanent signing |
| 10 | Run Saved 0/50/150/296 on Android profile and collect traces | P2 | S/M | high | issue #54 |
| 11 | Separate RAM/CPU recordings from Flutter frame timing | P2 | M | high | Android profiler |
| 12 | Decide bounded Saved ListView.builder only after regression evidence | P2 | S/M | medium | before/after device |
| 13 | Human-verify 8 Wave04 source chronologies | P1 CONTENT | M | medium | review ledger |
| 14 | Qualified IT/ES/FR/DE/PT edits for Wave04 | P1 CONTENT | M | medium | parity + human |
| 15 | Promote only approved Wave04 rows into runtime new version | P1 CONTENT | M | medium | six-locale CI |
| 16 | Continue independent 232-record story research in batches | P1 CONTENT | L | high | primary-source provenance |
| 17 | Review remaining unknown-year establishment fields | P2 CONTENT | L | medium | never guess |
| 18 | Recheck detail UI at text scaling 2× and unknown-year fallback | P2 | S | high | widget/physical |
| 19 | Align README/roadmap counters and source-release evidence | P2 | S | high | SHA-specific docs |
| 20 | Re-run full Audit 360 after all source+device+Store gates | QA | M | high | compare exact deltas |

## N. Prossimi cinque maxi-step dopo questo ciclo

1. **P0 owner access and signed candidate:** finalize versionCode and materialize production signed APK/AAB from one exact main SHA, record source/signer/sha256. Do not publish to users.
2. **P0 physical native + billing:** perform same-artifact Android checklist, Play internal testing purchase lifecycle and root ad provider checks. Keep issue #43 OPEN until PASS recorded.
3. **P2 performance device:** execute 0/50/150/296 favorite profile, record actual frame budget, jank, RAM/CPU separate. Only then decide whether ListView.builder improves a material issue.
4. **P1 editorial:** review and promote the eight Wave04 draft stories individually, then continue primary-source research for remaining 232 IDs. No automatic promotion.
5. **QA and ecosystem reuse:** update this Audit 360 after real device/Store evidence, run new source scanner for updated SHA, compare coverage and validate no donor/Golden promotion without tests.

Dependencies: signed artifact requires final source freeze; physical purchase needs Console/internal Play track; benchmarks require clean Android device; editorial research can proceed independently but any promoted runtime content after signing demands re-certifying the new source/artifact.

## O. Decisioni necessarie dell'utente solo per gate esterni

- Accesso proprietario alla Play Console World Days, conferma massimo versionCode caricato e configurazione del prodotto non consumabile.
- Un dispositivo Android fisico *pulito o dedicato ai test*, senza rischio di sovrascrivere dati di app già installate.
- Qualifica/approvazione editoriale effettiva dei testi Wave04 nelle sei lingue. Non trasformare approvazione dei cinque maxi-step in attestazione di revisione linguistica dei 48 testi.
- Pubblicazione al pubblico non autorizzata da questa analisi; la scelta Store resta separata.

## P. Delta rispetto al precedente audit e agli ultimi cinque maxi-step

| Maxi-step richiesto | Delta reale | Evidence | Non verificato |
|---|---|---|---|
| 1 Saved profile | integration_test profile + host driver + fail-closed normalizer e runbook | PR #55, CI source PASS | phone FrameTiming / memory |
| 2 ListView conditional | nessuna modifica a Saved/Around rendering | source compare | beneficio reale builder |
| 3 release P0 | matrice di prove e handoff, workflow esistenti preservati | PR #55, issue #43 | signed final candidate/Play/device |
| 4 stories 296 | 8 nuove storie ×6 in draft, report per tutti i 296 | PR #56 | human approval; 232 not researched |
| 5 Full 360 | questo report, decision log, QA e catena P0 | branch audit docs | evidenza fisica da incorporare |

**Risolto:** dropdown Paese 390px. **Non risolto:** Play distribution, Native device QA, full rich editorial. **Decisione di non intervento:** no eager list rewrite without measurable jank.

## Q. Verdetto operativo finale

- **Se oggi si può fare una sola cosa:** sbloccare il pacchetto di evidenze per un APK/AAB realmente firmato dallo stesso source SHA e relativo Play internal test, preservando versionCode e signer.
- **Miglior quick win di codice già conseguito:** dropdown Paese accessibile su schermi compatti con test responsive e nessuna nuova dipendenza.
- **Intervento che evita più falsi bug:** tenere separati test widget CI e frame Android reali, e distinguerli da Store/provider PASS.
- **Funzione pronta nel codice ma non provata nella vita reale:** Remove Ads lifetime purchase/restore; in modo diverso notifiche e widget.
- **Gate oggettivo prossimo:** fonte main exact SHA + workflow production signed artifact e manifest → dispositivo Play licensed tester → proof.
- **Non fare:** dichiarare Store Ready, certificare 8 draft articoli, inventare 232 storie o refactor delle liste senza dispositivo.
- **Perimetro effettivo:** sorgente GitHub, documenti e CI ispezionati, competitori web di contesto; **nessuna installazione, misurazione frame fisica o acquisto Google Play** eseguiti.

## R. Audit additivo Flutter full-checkout e benchmark due liste

**Portfolio storico certificato come scansione sorgente, non runtime:** [App Factory PR #63](https://github.com/riccardopinato/Idee-app-Archivi-riferimenti/pull/63) scansionò 13 repo Flutter / 1.467 Dart; zero match API legacy nel solo subset implementato; gli indicatori REVIEW includevano falsi positivi classificati separatamente. Questo run è un **punto di confronto SHA-specifico**, non si è ripetuto su tutti i nuovi commit in questa analisi.

**World Days earlier two-list widget pump (Flutter 3.47.3 CI Linux):**

| Fixture | Saved median ms | Around the World median ms | Nota |
|---:|---:|---:|---|
| 10 | 71,043 | 39,846 | startup/warmup influisce |
| 50 | 55,101 | 35,731 | non monotonico |
| 150 | 48,502 | 33,681 | nessun device GPU |
| 300 | 47,447 | 35,048 | 612/604 declared list children |

**Current prior CI full-catalog Saved:** 296 favorite IDs, 604 ListView delegate children, 6 ObservanceCard mounted, **490,161 ms** one initial widget pump on CI Linux (not frame time, not Android). Earlier run data and raw samples: [App Factory PR #63](https://github.com/riccardopinato/Idee-app-Archivi-riferimenti/pull/63).

**Post five-step result:** [real-device profile driver](../integration_test/saved_device_profile_test.dart) and [Android runner guide](SAVED_ANDROID_PROFILE_RUNBOOK_2026-11-09.md) are in source. Source-only test parser detects fabricated/missing data. **No measured device output exists:** FrameTiming P95/P99, jank, memory and CPU are **NOT VERIFIED / NOT MEASURED**. The current World Days source SHA differs from the original benchmark SHA, and a source-only change to QA/documents cannot be called a new GPU benchmark.

**Next acceptance:** run test on clean physical phone and compare same corpus/hardware before and after a bounded change if needed. Any future audit uses the full source scanner at the *new exact SHA* and preserves all original 360 sections rather than replacing them with this addendum.

---

End of 2026-11-09 audit. User-authorized implementation and this follow-up audit are distinct work modes; this document does not authorize publishing, personal-data edits or bypassing human/provider gates.
