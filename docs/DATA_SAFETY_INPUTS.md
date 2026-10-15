# World Days — Privacy / Data Safety engineering inputs

Freeze date: 2026-10-15
Scope: Android-first v1 + Flutter Web Preview
Source-of-truth purpose: engineering input for final Play Console declarations and privacy review. This file is not legal advice and does not replace provider disclosures or the final Play Console questionnaire.

## 1. First-party account / backend model

- No mandatory account or login.
- No World Days user-account backend in v1.
- Core preferences, favorites, recents, streak/reminder state and entitlement cache are local-first.
- No separate first-party analytics SDK/event pipeline in v1.
- No proprietary remote push service in v1.

## 2. Local application data

Stored locally as needed for product behavior:
- language / theme / country-market preferences;
- favorites and recently viewed observances;
- streak / lightweight local learning state;
- notification/reminder preferences and subscriptions;
- home-widget projection/state required by the Android widget;
- lifetime Remove Ads entitlement state and verification timestamp;
- when store completion is unfinished: product ID, transaction ID and recorded timestamp for safe retry.

World Days does not store payment-card details.

## 3. Google Mobile Ads / UMP

Production Android v1 uses:
- Google Mobile Ads;
- Google User Messaging Platform (UMP);
- one anchored adaptive banner placement only.

No inline adaptive or interstitial placement is enabled in v1 product scope.

Provider disclosures must be rechecked when completing Play Data Safety. Current engineering assumption is that Google SDKs can process network/device identifiers, product interaction and diagnostic/advertising measurement data depending on consent, configuration, region and provider behavior.

World Days must not claim those provider-side fields as first-party local-only data.

## 4. Google Play Billing

V1 can offer the one-time lifetime product:
- `world_days_remove_ads_lifetime`.

Google Play handles store account/payment authorization and store-side transaction processing.

The app can receive:
- product metadata / localized display price;
- purchase status;
- product ID;
- purchase/transaction identifier;
- verification data exposed by the store SDK;
- whether provider finalization is still required.

The app persists only the entitlement snapshot plus the minimal pending-completion record described above.

No server-side receipt-verification backend is part of v1.

## 5. Remote catalog updates / GitHub Pages

Bundled data remains the offline fallback.

Supported mobile builds can request:
- the public World Days GitHub Pages content manifest;
- a versioned public catalog payload.

Requests are HTTPS GET-style catalog update traffic. World Days does not attach favorites, recents, reminder preferences, entitlement state or profile settings to those content requests.

GitHub can receive ordinary request/network metadata under GitHub's own policies.

## 6. Web Preview

The Web Preview:
- is hosted on GitHub Pages;
- does not initialize/request AdMob;
- can expose normal GitHub-hosted web request metadata to GitHub;
- is a product preview, not proof of Android ads/billing/native behavior.

## 7. Device/native features

Android v1 uses:
- local notifications;
- boot/app-update reconciliation for local scheduled state;
- Android home-screen widget;
- system share UI for user-initiated share cards.

No v1 capability requires:
- precise location;
- contacts;
- microphone;
- camera;
- user file upload to a World Days backend.

## 8. Audience

World Days is a general-audience informational app and is not designed specifically for children.

Final Play Console target-audience/ads declarations must be kept consistent with the actual AdMob/UMP age-treatment configuration used for the release candidate.

## 9. Final Play Console freeze checklist

Before Phase J/K certification:
- recheck current Google Mobile Ads SDK Data Safety disclosure;
- recheck current Google Play Billing/provider disclosure where applicable;
- confirm exact production dependency lock;
- confirm no analytics SDK was added;
- confirm no new permissions/network services were added;
- confirm Privacy Policy matches the exact release candidate;
- map the above facts into Play Data Safety without guessing provider-side collection;
- record the submitted declaration snapshot/evidence.

Any new analytics, account backend, push provider, ad format or data collection reopens this privacy/Data Safety freeze.
