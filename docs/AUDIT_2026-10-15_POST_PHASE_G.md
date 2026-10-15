# World Days — Full repository audit after Phase G

Date: 2026-10-15  
Application baseline audited: `245f82148c1ca5ceee0977b82bf51a21b5b76a12`  
App Factory baseline: `5f6b2489df2ac85fb85ccfea059983a090689de4`

## 1. Audit verdict

World Days has a solid technical core and the post-Phase-G main branch is healthy:
- Development checks on main pass analyze, 41 Flutter tests, Web release and Android ARM64 build.
- GitHub Pages deployment succeeds and publishes the generated remote catalog pack.
- Current generated content pack: 296 canonical records / 297 2026 occurrences.
- ARM64 internal release gate is about 24.1 MB.
- AdMob/UMP and permanent Android signing have prior physical/production evidence.

The repository is **not Store Ready** yet. The remaining blockers are concentrated in editorial coverage, billing/store validation, physical retention QA, exact-artifact release certification, privacy/store metadata and governance.

The previous production-signed physical evidence predates the current Phase-G main SHA. It remains valid as subsystem evidence for the signing/AdMob integration, but it is not exact-artifact certification of the current app.

## 2. P0 — release blockers

### 2.1 Editorial coverage is still the largest product gap

Current reviewed editorial coverage is 28 / 296 records (~9.5%). The fallback behavior is safe, but most observances do not yet deliver the full Product Bible detail experience.

Required before v1 content-complete:
- original reviewed English editorial for launch records;
- primary/originator grounding review;
- derived IT/ES/FR/DE/PT packs;
- explicit unresolved/fallback state only where evidence is intentionally pending.

### 2.2 Remove Ads is implemented but not store-certified

The provider-neutral entitlement layer and `in_app_purchase` adapter exist, but the Play product has not been created/activated and sandbox evidence is missing.

A further release-risk was found in transaction finalization:
- entitlement is persisted before `completePurchase`;
- if `completePurchase` fails, the user keeps the entitlement, which is correct;
- however, on a later launch with a cached lifetime entitlement, `EntitlementService.initialize()` returns before the billing adapter is forced to attach to the Play purchase stream;
- there is no explicit durable retry path for a previously failed provider finalization.

Before certification, add an idempotent completion/acknowledgement recovery path and test it across process death/restart.

### 2.3 Native retention still lacks physical evidence

Notifications and the Android Home Screen Widget are implemented, but the exact-artifact physical checklist remains open:
- immediate and scheduled delivery;
- tap/deep link;
- reboot/update reconciliation;
- widget add/update/date rollover;
- widget tap/deep link.

### 2.4 Privacy policy is stale after the latest features

The public policy was last updated 2026-10-14. It currently does not describe:
- store billing / Remove Ads purchase processing;
- mobile remote-content requests to GitHub Pages.

The existing policy explicitly says it will be updated if a remote content service materially changes production data handling. Phase G now introduces that network path. The policy must be revised before store submission and Data Safety is finalized.

### 2.5 Current main has no exact current production candidate evidence

The current `main` SHA includes billing and Remote Content Pack v1 changes after the earlier production/physical validation.

Before Store Ready:
- generate a new production-signed APK + AAB from the final candidate;
- verify signer + artifact hashes;
- run physical and Play-internal regression against that exact source SHA.

## 3. P1 — technical/release hardening

### 3.1 Release workflows are not fully parity-aligned with Phase G

`dev-checks.yml` validates:
- content pack build/validation;
- native content-pack Android configuration.

The production and signed-QA workflows do not explicitly run the same Phase-G validation gates after platform generation.

Required:
- add `tool/validate_content_pack.py`;
- add `tool/validate_native_content_pack.py`;
- keep the exact release pipeline at least as strict as normal CI.

### 3.2 Production workflow should fail closed on release source identity

`android-production-release.yml` can be manually dispatched from a selectable Git ref and currently does not explicitly require `main` or an approved release tag.

Before store release, enforce one documented release source rule:
- final `main` SHA, or
- immutable signed/reviewed release tag.

Record source SHA in evidence, as already done, and reject unintended refs.

### 3.3 Remote Content Pack runtime needs two security/robustness hardening items

The core Phase G architecture is correct, but two boundaries are weaker than the documentation wording:

1. Runtime manifest validation requires HTTPS but does not restrict the payload hostname/path. CI validates `riccardopinato.github.io/World-Days/content/`, while the app would accept a manifest pointing at another HTTPS host.

2. `http.Client.get()` buffers the full payload before the post-download size verification. The 5 MiB manifest cap therefore does not strictly cap bytes read into memory from a misbehaving/compromised origin.

Before final certification:
- enforce the expected content origin/path at runtime;
- use a streamed response or hard byte cutoff so actual downloaded bytes are bounded.

These are hardening issues, not evidence of current content corruption.

### 3.4 Dataset contract is stronger than the automated acceptance gate

The Product Bible requires occurrence-generation coverage across at least 2026, 2027 and 2028. Current tests exercise representative recurrence rules in those years, but do not run full-catalog acceptance over all three years.

Also, `validate_dataset.py` does not currently assert for every publishable record:
- at least one source exists;
- `lastVerifiedAt` is present/non-empty.

Add full-catalog 2026/2027/2028 generation/invariant tests and enforce the remaining data-contract invariants in CI.

### 3.5 Automated coverage is still narrow relative to product surface

Current suite: 41 Flutter tests across domain/data/retention/entitlement/content-pack/basic UI.

Still missing:
- maintained `integration_test` smoke path;
- Settings interaction coverage;
- Calendar interaction/filter coverage;
- Around-the-World state coverage;
- Saved/detail navigation coverage;
- monetization controller state coverage with a fake boundary;
- billing adapter lifecycle/finalization-retry coverage;
- filesystem content-pack storage tests;
- notification/widget adapter tests where deterministic fakes are possible.

### 3.6 Main is not protected

The current GitHub branch metadata reports `main` as unprotected. This conflicts with the intended stable-main/release-gate discipline.

Before release:
- require green Development checks for merges;
- require PR flow;
- prevent accidental force/direct release-critical pushes where repository permissions allow.

### 3.7 Release versioning is still undefined

`pubspec.yaml` is currently `0.3.0+3`; production workflows override build number with the Actions run number.

Define:
- version-name policy;
- version-code policy;
- release tag convention;
- changelog/release evidence convention.

## 4. Product-truth mismatches to resolve explicitly

### 4.1 Android vs iOS v1 scope

Product Bible lists Android, iOS and Web Preview. Current release/readiness work is Android-centric:
- Android production signing exists;
- Play billing setup is planned;
- Store roadmap is Play-specific;
- iOS production AdMob identity/signing/App Store pipeline/physical QA are not present.

Choose one before certification:
- **recommended:** Android-first v1 + Web Preview, with iOS explicitly moved post-v1 in Product Bible; or
- keep iOS in v1 and add the full iOS production/store lane.

### 4.2 Monetization format scope

Product Bible lists:
- top/anchored adaptive banner;
- inline adaptive placements;
- conservative interstitial after natural completion.

Runtime currently ships only the dedicated top adaptive banner.

Before release, either:
- formally scope v1 to the top banner only; or
- implement inline/interstitial with frequency caps, consent gating and physical QA.

Do not leave product truth claiming formats that the app does not implement.

### 4.3 Analytics / KPI scope

Product Bible defines an event/KPI contract, but there is no first-party analytics implementation in `lib/` and the Privacy Policy currently says no separate first-party analytics backend is enabled.

Before store metadata is frozen:
- explicitly defer analytics from v1 and update Product Bible/KPI wording; or
- implement a privacy-reviewed analytics boundary and then update policy/Data Safety.

For a first release, deferring analytics is the lower-risk path.

### 4.4 Saved information architecture

Product Bible says Saved contains favorites, followed categories, reminder subscriptions and recently viewed items.

Current Saved page contains favorites + recently viewed. Followed categories/reminder controls live in Settings.

Resolve by either:
- surfacing followed categories/reminder subscriptions in Saved; or
- updating Product Bible to make Settings the canonical home for those controls.

## 5. Store-readiness findings

### 5.1 app-ads.txt requires a root developer-site location

Google AdMob derives the app-ads.txt lookup from the developer website hostname in the store listing and checks the hostname root, e.g. `https://example.com/app-ads.txt`.

The current GitHub Pages project path is `https://riccardopinato.github.io/World-Days/`. Publishing only `/World-Days/app-ads.txt` would not satisfy a crawler looking for `https://riccardopinato.github.io/app-ads.txt`.

Before Play launch:
- choose the final developer website hostname;
- publish the exact AdMob-provided app-ads.txt snippet at that hostname root;
- link the same developer website from the store listing;
- verify AdMob crawler status after publication.

Official reference:
https://support.google.com/admob/answer/9363762

### 5.2 Play App Signing identity must be captured separately

Before Play distribution, document the Play App Signing configuration and distinguish:
- upload certificate;
- Play app-signing certificate;
- existing direct-APK permanent certificate.

The final evidence bundle should record the relevant fingerprints for both direct QA and Play-distributed artifacts.

Official reference:
https://support.google.com/googleplay/android-developer/answer/9842756

### 5.3 Data Safety must reflect the final exact SDK/network set

Final Data Safety/privacy review must include at least:
- Google Mobile Ads + UMP;
- Play billing / one-time product;
- local notifications/widget behavior;
- GitHub Pages remote content requests;
- no account backend;
- analytics decision.

## 6. Maintainability / P2 findings

- `AppController`, Settings and Calendar are now large orchestration/UI units. They remain analyzable and tested, but future feature work should split focused services/view sections before they become migration bottlenecks.
- Around the World starts on Italy when the profile market is GLOBAL. This is deterministic but arbitrary for a global consumer app; consider a neutral/transient browse-market state.
- Market coverage is intentionally thin and remains a content-expansion task.
- Accessibility has basic semantics/large-text tests, but final certification still needs screen-reader/focus/contrast/touch-target physical QA.

## 7. What is already strong and should not be reworked

No redesign is recommended for:
- canonical-vs-editorial data separation;
- semantic categories vs visual keys;
- recurrence engine approach;
- local-first bundled fallback;
- content-pack checksum/staging/rollback architecture;
- UMP consent gating;
- ad-request suppression for Remove Ads;
- permanent Android signing identity;
- CI/Web Preview baseline;
- source-provenance model.

The next work should close release evidence and content completeness, not replace the architecture.

## 8. Recommended critical path

1. Data-contract hardening + release-workflow parity.
2. Billing finalization recovery.
3. Complete editorial coverage.
4. Create Play Remove Ads product and run internal-track sandbox QA.
5. Retention physical QA.
6. Resolve Android-first vs iOS v1, analytics and ad-format scope.
7. Update Privacy Policy + Data Safety inputs.
8. Establish versioning + main protection.
9. Produce exact final candidate and run full regression.
10. Configure developer website/app-ads.txt + Play Console release assets.
11. Final Evidence Bundle and CERTIFIED / NOT CERTIFIED verdict.


## 9. Phase B + G.1 remediation — 2026-10-15

The following audit findings were closed by PR #25:
- full-catalog recurrence acceptance now exercises 2026, 2027 and 2028;
- runtime/CI enforce source presence and verification metadata;
- generated occurrence uniqueness and cross-year ranges have explicit gates;
- content payload URLs are pinned to the approved GitHub Pages origin/path;
- payload transfer is streamed through a hard manifest-sized byte cap;
- signed QA and production release workflows run content-pack/native-content validation;
- GitHub Pages deployment now performs a public manifest/payload propagation + checksum smoke check.

These items are therefore no longer on the critical path. Remaining v1 blockers start with Phase C, E, F and I/J in `ROADMAP.md`.
