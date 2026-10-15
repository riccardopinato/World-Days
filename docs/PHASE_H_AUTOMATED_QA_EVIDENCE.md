# Phase H — Automated QA evidence

Date: 2026-10-15  
Repository: `riccardopinato/World-Days`  
PR: #28 — `phase-h-qa-refactor` → `main`  
Factory baseline: `47c47f49a7b46812e3bd6f1231c3524f2b52b826` (Master v26.6 / Golden Index v18)

## Scope

Phase H expands automated regression coverage and introduces testable boundaries without changing the product architecture or weakening release gates.

The acceptance rule remains: **green CI is required before merge, but green CI alone is not Store Ready certification**. Physical/store/provider checks remain in Phases E, F, I and J.

## Automated coverage added

### Maintained integration journey

`integration_test/app_smoke_test.dart` keeps the end-to-end product journey executable:

`launch → Today → detail → favorite → Saved → Calendar → Settings`

The integration harness uses deterministic local fakes for entitlement, remote-content transport/storage, notifications and Home Widget boundaries.

### AppController / retention

Coverage verifies:

- local-first initialization through injected boundaries;
- favorite persistence plus notification/widget reconciliation;
- permission-denied reminder behavior;
- deterministic notification and widget deep-link targets;
- widget pin projection ordering;
- global/national market visibility invariants.

### UI feature flows

Widget QA covers:

- Settings theme, reminders and widget actions;
- Calendar national-scope filtering without mutating profile market;
- Around-the-World transient browsing;
- Saved favorite → detail navigation;
- Settings at 360 dp / 200% text scale.

Navigation smoke additionally covers:

- all five mobile destinations;
- 360×800 mobile shell at 200% text scale;
- wide-shell NavigationRail switching;
- calendar day-cell button semantics.

### Monetization boundary

The UMP/Mobile Ads runtime is injectable. Tests verify:

- unsupported platforms perform no provider work;
- consent errors do not bypass eligibility;
- eligible consent initializes ads once;
- entitled users make zero consent/ad provider calls;
- denied consent never initializes ads;
- fallback errors fail closed;
- Privacy Choices refreshes eligibility;
- privacy-form failure is not treated optimistically.

### Entitlement lifecycle

Existing entitlement tests cover the Phase-H reliability boundary needed by UI/monetization QA:

- verified expected-product grants only;
- pending/cancel/unverified/wrong-product fail closed;
- durable pending-completion marker;
- failed provider completion survives restart;
- provider redelivery/finalization clears the durable marker;
- cached lifetime entitlement still attaches the store listener.

Real Play product resolution and purchase/restore behavior remain Phase E/J sandbox evidence.

### Content-pack filesystem

`FileContentPackStorage` tests cover:

- atomic active/previous tracking;
- rollback to last-known-good bytes;
- crash-safe fallback when the primary pointer is corrupt.

### Native-facing retention boundaries

Notification and Home Widget services now expose injectable gateways so AppController behavior can be tested without pretending platform delivery occurred. Physical delivery, reboot/update reconciliation and widget rendering remain Phase F/J device evidence.

## Accessibility / responsive finding closed

The final failing regression was:

`app shell survives small phone large text and exposes nav labels`

At 360×800 with 200% system text scaling, the overflow originated in `ObservanceHero`, not the compact navigation bar. The hero used a fixed large-text height increment that left 302 px of internal vertical space while the scaled content required roughly 408 px.

The fix makes hero height grow with the platform text scale instead of capping or overriding accessibility scaling.

Acceptance coverage keeps the 200% text-scale test intact.

## Warning review

No Phase-H blocking Flutter/Kotlin/dependency migration warning was found in the Development checks.

One generated branding warning remains:

`Icons with alpha channel are not allowed in the Apple App Store.`

This does not affect the Android/Web Phase-H gate. It must be resolved before App Store submission if Phase I keeps iOS in v1.

## CI acceptance

The merge head must satisfy the repository Development checks:

- dataset/editorial/content-pack validators;
- native scaffold validation;
- dependency-lock verification;
- branding/localization validation;
- Flutter analyze;
- **76 Flutter tests**;
- Web release build;
- Android ARM64 gate;
- APK artifact upload.

PR #28 must not be merged while this workflow is red.

## Residual work intentionally outside Phase H

- full focus-order and touch-target automation before Phase J certification;
- opportunistic split of oversized `AppController`, Settings and Calendar files when next touched;
- Play billing sandbox/provider evidence;
- exact-artifact notification/Home Widget physical QA;
- final exact-artifact accessibility/screen-reader regression.

## Verdict

**Phase H implementation: READY FOR MERGE only with green merge-head CI.**

This evidence does not certify World Days for store release.
