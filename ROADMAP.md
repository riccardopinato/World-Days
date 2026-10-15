# World Days — Active roadmap

Execution truth for the repository. Product scope remains governed by `docs/PRODUCT_BIBLE.txt`.

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
- exact-artifact physical notification/deep-link/widget QA remains required.

### Step 10.1 — AdMob / UMP / permanent Android release identity ✅
Completed and physically validated on Android:
- permanent signing identity and production signer verification;
- production APK + AAB workflow;
- UMP consent appears on clean state;
- deny-consent path verified;
- Privacy Choices reopens and allows changing the decision;
- production adaptive banner loads;
- public Privacy Policy published.

## Post-audit completion roadmap — 2026-10-15

The app is NOT Store Ready until the gates below are closed.

### Phase A — Functional UX fixes — IN PROGRESS
- [x] Around the World browsing no longer mutates the user's profile market.
- [x] Today primary hero is interactive and no longer immediately duplicated.
- [x] Up Next shows occurrence dates.
- [x] Calendar adds weekday headers, Today jump and current-day affordance.
- [x] Catalog load failure exposes a retry path.
- [x] Improve source-card provenance UX and preserve verification metadata.
- [ ] Finish remaining consumer error/empty states.

### Phase B — Data/runtime structural fixes — IN PROGRESS
- [x] Cache yearly occurrences and date indexes instead of recomputing per calendar cell.
- [x] Include previous-year carry-over ranges when indexing a year.
- [x] Introduce deterministic primary-observance ranking.
- [x] Separate semantic categories from `visualKey`.
- [x] Migrate category reminders from visual keys to semantic categories with legacy preference migration.
- [x] Expose all visual collections and complete officiality filters in Discover.
- [x] Align runtime recurrence support with LAST_DAY_OF_MONTH and ONE_OFF.
- [x] Align the data contract with the actual recurrence representation.
- [x] Represent unresolved authority/lunar dates explicitly in future-year UI instead of silently disappearing.

### Phase C — Editorial completion — BLOCKING
Current reviewed editorial coverage: 28 / 296.
- [x] Extend editorial schema to include hook, Why this date, Origin/history, quick facts and related observances; annual campaign themes are consumed from year overrides.
- [ ] Complete original English editorial coverage for all launch records.
- [ ] Review primary-source grounding and provenance.
- [ ] Translate reviewed editorial content to IT/ES/FR/DE/PT.
- [ ] Replace generic placeholders with explicit fallback states only where evidence is intentionally pending.

### Phase D — Today / Calendar / Discover completion
- [x] Today in 30 seconds for reviewed editorial entries.
- [x] Daily quiz / lightweight learning loop.
- [x] Tomorrow preview.
- [x] Calendar officiality/category/scope/country filters.
- [x] Upcoming 7 / 30 days views.
- [ ] Decide whether day/week modes add enough value for v1.
- [ ] Expand Around the World national coverage beyond the current thin seed.
- [ ] Keep locale and market independent in every flow.

### Phase E — Remove Ads lifetime entitlement — BLOCKING
- [x] Provider-agnostic entitlement contract, persistent lifetime cache and centralized ProductLimits.
- [ ] One-time Remove Ads store adapter/product.
- [ ] Restore/reconcile entitlement against the configured store.
- [ ] Sandbox billing QA.
- [x] Entitled users suppress the ad request itself, not merely hide the banner.
- [x] Settings purchase/status UX is wired to the entitlement boundary and activates when billing is configured.

### Phase F — Retention physical QA — BLOCKING
- [ ] Immediate notification on exact production candidate.
- [ ] Scheduled notification.
- [ ] Notification tap/deep link.
- [ ] Reboot/app-update reconciliation.
- [ ] Home Widget add/update/date rollover.
- [ ] Widget tap/deep link.
- [x] Add a rolling generic daily fallback after the 21-day tailored reminder horizon.

### Phase G — Remote Content Pack v1 — BLOCKING BEFORE LONG-TERM CONTENT OPERATIONS
- [ ] Bundled catalog remains immutable fallback.
- [ ] Versioned remote manifest.
- [ ] Checksum/integrity verification.
- [ ] Staged download and validation.
- [ ] Atomic activation.
- [ ] Rollback to last-known-good.
- [ ] Annual campaign/theme override channel.
- [ ] Offline/network-failure tests.

### Phase H — Code hygiene / QA expansion
- [x] Remove obsolete `synthetic-package` l10n option.
- [x] Split notification diagnostics from the main consumer Settings surface.
- [x] Preserve source verification metadata in the runtime model.
- [ ] Expand AppController / Settings / Calendar / Around-the-World tests.
- [ ] Add monetization state tests where platform boundaries permit.
- [ ] Add maintained integration smoke test.
- [ ] Review dependency warnings for Flutter/Kotlin plugin migration.
- [x] Allow users to choose the weekly reminder weekday.

### Phase I — Governance / identity alignment — IN PROGRESS
- [x] Canonical Android application ID fixed to `com.riccardopinato.world_days` in product truth.
- [x] Repository Factory baseline aligned to `5f6b2489df2ac85fb85ccfea059983a090689de4`.
- [ ] Update README, signing/AdMob docs and Golden reuse manifest to the post-production state.
- [ ] Establish release versioning policy.
- [ ] Protect `main` with required green checks/ruleset before store release.

### Phase J — Exact-artifact regression / certification
- [ ] Generate release candidate APK + AAB.
- [ ] Verify signer SHA-256 and artifact hashes.
- [ ] Full offline/navigation/search/favorites/share/localization regression.
- [ ] Accessibility and large-text regression.
- [ ] Upgrade/install-in-place check.
- [ ] Final CERTIFIED / NOT CERTIFIED evidence bundle.

### Phase K — Store readiness — FINAL ONLY
Do not start until Phases C, E, F and J are closed.
- [ ] app-ads.txt.
- [ ] Play Console app setup.
- [ ] Data Safety.
- [ ] Store listing/localizations.
- [ ] Screenshots/feature graphic/icon verification.
- [ ] Production rollout plan.

## Release policy

A green CI build is necessary but not sufficient. World Days is publishable only after the exact candidate artifact satisfies the physical and evidence gates above.
