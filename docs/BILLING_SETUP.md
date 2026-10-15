# World Days — Remove Ads billing setup

Status: provider adapter + durable completion-recovery implemented; Play catalog and sandbox evidence still required.

## Product contract

- Capability: lifetime Remove Ads.
- Product ID: `world_days_remove_ads_lifetime`.
- Product type: one-time, non-consumable purchase.
- Target reference price: EUR 2.99; storefront localization may vary.
- Core content remains free.
- Purchase/restore UI is shown only after the store resolves the product, or
  when an existing lifetime entitlement is already cached.

Runtime dependency:
- `in_app_purchase: 3.3.1` (official Flutter plugin, publisher flutter.dev).

## Google Play setup

Create the product under the World Days application in Play Console as a
one-time product.

Required configuration:
1. Product ID exactly `world_days_remove_ads_lifetime`.
2. Non-consumable / permanent entitlement semantics.
3. Active Buy purchase option.
4. Base/reference price targeting EUR 2.99, then review localized prices.
5. Publish/activate the product before sandbox validation.

Testing:
1. Add the tester account under Play Console license testing.
2. Make the same account eligible for the World Days internal test.
3. Upload the production-signed AAB to an internal testing release.
4. Install World Days from the Play internal-test link with that account.
5. Verify product price loads from Play rather than from app constants.
6. Exercise purchase, pending/cancel path, app restart, restore, and
   uninstall/reinstall restore.
7. Confirm entitled users make no AdMob banner request.

Google documents one-time products as the appropriate model for a single
charge that grants a durable premium capability. License testers can make test
purchases when the app/product is published to an eligible testing track.

## Runtime behavior

The app subscribes to the store purchase stream before starting a billing
flow.

State handling:
- pending: never grants Remove Ads;
- cancelled/error: never grants Remove Ads;
- purchased/restored: exact product ID and non-empty store verification data
  are required before the entitlement layer accepts the store-reported state;
- entitlement state is persisted before `completePurchase` finalizes a
  transaction;
- when provider finalization is required, a durable transaction marker is
  stored before `completePurchase`;
- if finalization fails, access is preserved and the marker survives process
  death;
- on a later launch the purchase stream is attached even for cached lifetime
  owners and provider reconciliation is triggered so an unfinished purchase
  can be re-delivered and finalized idempotently;
- a provider result showing no remaining completion requirement clears a
  matching stale marker;
- cached lifetime ownership suppresses AdMob before monetization initializes;
- restore is user initiated for normal recovery, while unfinished provider
  completion has its own automatic reconciliation path.

The Flutter `in_app_purchase` API requires completed purchases to be
finalized with `completePurchase` when `pendingCompletePurchase` is true.
Google Play requires acknowledgement after entitlement delivery; unacknowledged
non-consumable purchases can be automatically refunded after the provider
window. World Days therefore treats completion as a durable recoverable
operation rather than a best-effort one-shot callback.

Provider guidance re-verified 2026-10-15 against:
- https://pub.dev/packages/in_app_purchase
- https://developer.android.com/google/play/billing/integrate

## Verification boundary

The current v1 adapter performs client-side mapping of the store-reported
purchase status and verification payload to the expected product ID. The
internal `providerVerified` entitlement source means that this store state
has been accepted by the billing adapter; it does **not** claim server-side
receipt/token verification.

This is an explicit risk decision for the low-value Remove Ads entitlement.
If World Days later adds higher-value purchases, subscriptions, account-bound
entitlements, or meaningful fraud exposure, move verification to a trusted
backend before granting the durable capability.

## Release evidence still required

Do not mark Phase E certified until all of these are captured on the exact
release candidate:
- Play product resolves with localized price;
- test purchase succeeds;
- pending/cancel does not unlock;
- successful purchase removes the existing banner and prevents later ad
  requests;
- app restart preserves Remove Ads;
- restore succeeds after reinstall/cleared local state;
- purchase transaction is completed/acknowledged without repeated delivery;
- forced completion failure followed by process restart reconciles and
  completes the same transaction without revoking entitlement;
- production build remains signed by the pinned World Days certificate.
