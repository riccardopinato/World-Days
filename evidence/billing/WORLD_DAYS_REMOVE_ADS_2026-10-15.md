# World Days — Remove Ads billing evidence

Date: 2026-10-15

App Factory baseline:
`47c47f49a7b46812e3bd6f1231c3524f2b52b826`

Relevant Goldens:
- `GOLDEN_ENTITLEMENT_CONTRACT_FLUTTER_v1.txt` — COPY-READY provider-agnostic contract.
- `GOLDEN_PLAY_BILLING_LIFETIME_ENTITLEMENT_FLUTTER_v1_DRAFT.txt` — provider candidate, sandbox not verified.
- `GOLDEN_CODE_HYGIENE_v1.txt` — certified cleanup process.

Provider package:
- `in_app_purchase 3.3.1`.

Provider guidance checked:
- Flutter in_app_purchase package documentation, 2026-10-15.
- Google Play Billing integration documentation, 2026-10-15.

Implemented evidence:
- centralized entitlement service and ProductLimits;
- exact product mapping for `world_days_remove_ads_lifetime`;
- pending/cancel/error do not grant access;
- unverified/wrong-product PURCHASED/RESTORED fail closed;
- purchase stream attaches at billing startup, including cached-lifetime launches;
- durable pending-completion marker is written before provider finalization;
- failed `completePurchase` preserves entitlement and retry identity;
- next launch automatically reconciles previously unfinished provider state;
- matching provider redelivery finalizes and clears the marker;
- provider-reported already-complete state clears a matching stale marker;
- Remove Ads entitlement prevents new AdMob requests.

Automated regression scenarios:
- free default;
- billing unavailable;
- pending/cancel no grant;
- wrong product no grant;
- unverified terminal result no grant;
- verified lifetime grant;
- async purchase-stream grant;
- restore;
- offline cached lifetime;
- completion success;
- completion failure with durable marker;
- process-restart reconciliation and completion;
- stale-marker clear when provider no longer requires completion;
- entitled monetization request suppression.

Physical/store status:
- Play product catalog: NOT VERIFIED.
- Play Internal Testing purchase: NOT VERIFIED.
- Play sandbox pending/cancel: NOT VERIFIED.
- uninstall/reinstall restore: NOT VERIFIED.
- distribution acknowledgement evidence: NOT VERIFIED.

No provider/store physical gate is promoted to PASS by unit or CI evidence.
