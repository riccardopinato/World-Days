# World Days — Active roadmap

Execution truth for the repository. Product scope remains governed by `docs/PRODUCT_BIBLE.txt`.

Audit baseline: `245f82148c1ca5ceee0977b82bf51a21b5b76a12`  
Full audit: `docs/AUDIT_2026-10-15_POST_PHASE_G.md`

## Current release state

World Days is technically healthy but **NOT Store Ready**.

Current automated evidence (Phase H merge candidate):
- Pull-request Development checks: analyze + **76 Flutter tests** + Web release PASS.
- The Android ARM64 step is conditional and skipped in PR validation; the post-merge `main` run remains the Android build gate.
- GitHub Pages deployment + hosted remote-content smoke PASS.
- Generated remote catalog: 296 records / 297 2026 occurrences.
- Hosted payload smoke: version `2026.10.14.1`, 501,993 bytes, SHA-256 `38e6ee66d3646c0c313ca7b4b8e395a79b2456ecfc5522cd25c948b0f624d8b7`.
- ARM64 internal release gate: ~24.1 MB.
- Phase B and G.1 implementation merge: `2a177fc00d6f6a5f041034e7c8e00f8cd651c0bb`.
- Permanent Android signing + production AdMob/UMP have prior physical evidence.

Important: the previous production/physical monetization evidence predates the current Phase-B/G.1 code. Final certification must use a new exact candidate artifact.

## Critical path to v1

Blocking sequence:

**C → E → F → I → J → K**

Phase D/H work can proceed in parallel where it does not destabilize the release candidate.

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

## Phase A — Consumer UX alignment — NEAR COMPLETE

Completed:
- [x] Around the World browsing does not mutate profile market.
- [x] Today primary hero is interactive and not duplicated immediately.
- [x] Up Next shows occurrence dates.
- [x] Calendar has weekday headers, Today jump and current-day affordance.
- [x] Catalog load failure exposes Retry.
- [x] Source-card provenance preserves verification metadata.

Open:
- [ ] Align Saved IA with Product Bible: either surface followed categories/reminder subscriptions in Saved or formally move that responsibility to Settings in product truth.
- [ ] Add an explicit Around-the-World empty state before market coverage expands.
- [ ] Replace the arbitrary Italy default for GLOBAL users with an explicit transient browse-market choice or another documented neutral rule.
- [ ] Final consumer copy/error-state sweep for content update, billing-unavailable and offline cases.

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

## Phase C — Editorial completion — BLOCKING

Current reviewed editorial coverage: **28 / 296 (~9.5%)**.

- [x] Extended editorial schema: hook, Why this date, Origin/history, quick facts, related observances.
- [x] Annual campaign themes consumed from year overrides.
- [ ] Complete original English editorial coverage for all launch records.
- [ ] Review primary/originator grounding and provenance for every reviewed article.
- [ ] Translate reviewed editorial content to IT/ES/FR/DE/PT.
- [ ] Replace generic editorial-coming-next states only when reviewed source-backed content exists.
- [ ] Re-run locale parity/editorial validators at 100% target coverage.

## Phase D — Today / Calendar / Discover / market completion

- [x] Today in 30 seconds for reviewed editorial entries.
- [x] Daily quiz / lightweight learning loop.
- [x] Tomorrow preview.
- [x] Calendar officiality/category/scope/country filters.
- [x] Upcoming 7 / 30 days.
- [x] Random discovery and themed collections.
- [ ] Decide whether day/week calendar modes add enough value for v1; otherwise remove that v1 expectation from Product Bible.
- [ ] Expand Around the World national coverage beyond the thin launch seed.
- [ ] Keep locale and market independent in every new flow.
- [ ] Add seasonal collection curation only after editorial coverage is sufficiently broad.

## Phase E — Remove Ads lifetime entitlement — BLOCKING

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
- [ ] Reassess client-only verification before any higher-value/account-bound monetization.

## Phase F — Retention physical QA — BLOCKING

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
- [ ] Extend accessibility automation beyond the current semantics/large-text smoke to explicit focus-order and touch-target assertions before final Phase J certification.
- [ ] Keep provider/plugin-specific Play billing behavior in the Phase E sandbox and Phase J exact-artifact gates rather than simulating store behavior in unit tests.

Evidence: `docs/PHASE_H_AUTOMATED_QA_EVIDENCE.md`.

## Phase I — Governance / product-truth / privacy alignment — BLOCKING

Completed:
- [x] Canonical Android ID is `com.riccardopinato.world_days`.
- [x] App Factory baseline aligned to `5f6b2489df2ac85fb85ccfea059983a090689de4`.
- [x] README, Android signing, AdMob docs and Golden reuse manifest reflect current subsystem state.
- [x] Post-Phase-G audit recorded.

Governance:
- [ ] Define release version-name / version-code policy.
- [ ] Define release tag/changelog/evidence convention.
- [ ] Protect `main` with required green checks / PR rules where repository permissions allow.
- [ ] Restrict Production Android Release to approved `main`/release-tag source identity.

Product-truth decisions:
- [ ] Decide **Android-first v1 + Web Preview** versus full Android+iOS v1.
- [ ] If Android-first is selected, move iOS production release to post-v1 in Product Bible.
- [ ] If iOS remains in v1, add production iOS AdMob ID, signing, App Store pipeline and physical QA.
- [ ] Resolve monetization scope mismatch: top banner only vs Product Bible inline/interstitial formats.
- [ ] Resolve analytics scope mismatch: explicitly defer v1 analytics or implement a privacy-reviewed measurement boundary.
- [ ] Resolve Saved IA mismatch from Phase A.

Privacy:
- [ ] Update public Privacy Policy for Play billing / purchase processing.
- [ ] Update policy for mobile GitHub Pages remote-content requests.
- [ ] Update `Last updated` date and redeploy.
- [ ] Freeze final privacy/Data Safety inputs only after analytics and platform scope decisions.

## Phase J — Exact-artifact regression / release certification — BLOCKING

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
