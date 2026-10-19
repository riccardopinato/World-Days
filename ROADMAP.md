# World Days — Active roadmap

Execution truth for the repository. Product scope remains governed by `docs/PRODUCT_BIBLE.txt`.

Audit baseline: `245f82148c1ca5ceee0977b82bf51a21b5b76a12`  
Full audit: `docs/AUDIT_2026-10-15_POST_PHASE_G.md`

## Current release state

World Days is technically healthy but **NOT Store Ready**.

Current automated evidence:
- Phase I merge `44720a125db88386180f31951f9cf167c555b8a4` is the current `main` baseline at `0.4.0+4`.
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
