# Phase A/D — Consumer alignment evidence

Date: 2026-10-15
Repository: riccardopinato/World-Days
PR: #29 — phase-ad-consumer-alignment -> main
Factory baseline: 47c47f49a7b46812e3bd6f1231c3524f2b52b826 (Master v26.6 / Golden Index v18)

## Product decisions

The v1 consumer scope is intentionally bounded:

- Calendar v1 remains month + date detail + upcoming 7/30 days.
- Dedicated day/week modes are post-v1 candidates.
- Around the World keeps the verified IT/ES/FR/DE/PT/GB/US national seed for v1.
- Broader national coverage is post-v1 so Phase C editorial completion remains the content priority.
- Seasonal collection expansion is post-v1 and follows broader reviewed editorial coverage.
- Locale and market remain independent contracts.

## Phase A implementation

### Saved IA

Saved now surfaces the four product-truth concepts defined by the Product Bible:

- favorites;
- followed categories;
- reminder subscription summary;
- recently viewed.

Detailed reminder timing and permission controls remain in Settings. Saved links to Settings instead of creating a second retention-settings owner.

### Around the World

GLOBAL profiles no longer default silently to Italy.

The transient browse state is nullable until the user explicitly selects a country. Selecting a country does not mutate the profile market.

Two explicit states are rendered:

1. choose a country;
2. selected country has no verified national records yet.

### Consumer failure copy

Content-update failure copy now states that the current verified catalog remains available.

Billing-unavailable copy is recovery-oriented and does not imply purchase success, entitlement change or ad-state change.

All new UI copy is present in EN/IT/ES/FR/DE/PT.

## Code hygiene

A shared semantic-category presentation helper was introduced for Settings and Saved, avoiding a second duplicated UI label mapping.

Deliberately retained:

- category validation in preferences/controller, because those are domain/input guards rather than presentation mapping;
- detailed reminder controls in Settings, because Saved is a summary/discovery surface;
- the existing national seed, because adding unreviewed country records would violate source/provenance rules.

No dependency, asset, persistence schema or native capability change was introduced.

## Regression coverage

New widget coverage verifies:

- GLOBAL Around the World starts without a preselected country;
- selecting a transient country does not mutate profile market;
- a selected country with no test-fixture national records shows the explicit empty state;
- Saved surfaces followed categories and enabled reminder subscriptions;
- Saved can reach Settings for detailed reminder management.

Existing market-layer tests continue to verify locale/market independence.

## Automated validation

Development checks run #174 on functional head a768fbfda2855a3a47d7184f053b7ef050a2e885:

- dataset/content validators: PASS;
- localization generation: PASS;
- Flutter analyze: PASS;
- Flutter tests: 78/78 PASS;
- Web release build: PASS;
- Android ARM64 PR step: conditional / skipped by workflow design.

ROADMAP/evidence changes after that run are documentation-only. PR #29 still requires green CI on its final merge head before squash merge.

## Verdict

Phase A/D implementation is ready for merge once the final PR head is green.

This closes consumer IA/scope work only. It does not change the blocking release sequence C -> E -> F -> I -> J -> K.
