# World Days — Play Billing 9 dependency admission boundary

Date: 2026-11-03
Source baseline: `474fdc405217bf05ab28bd250b2e613c86e0506e`

The current source lock contains `in_app_purchase_android 0.5.5`,
which upgrades Google Play Billing 8.0.0 to 9.1.0.

Upstream verified notes:
- https://github.com/flutter/packages/blob/main/packages/in_app_purchase/in_app_purchase_android/CHANGELOG.md
- https://developer.android.com/google/play/billing/migrate-gpblv9

Upstream plugin 0.5.5 requires minSdk 23 or later (Flutter 3.47
requires at least 24). The plugin reports a blocked Play Store
as BILLING_UNAVAILABLE rather than ERROR; World Days surfaces
a generic unavailable state and does not grant lifetime access on error.

**Not a store certification.** Release gates still require:
- Official Play one-time product `world_days_remove_ads_lifetime`;
- internal-track Play-installed exact production AAB and license tester;
- successful purchase, pending, cancellation, purchase/restore and
  finalization after restart;
- no ad requests after entitlement and consent changes;
- Android signed artifact identity and Play signing fingerprints.

No dependency bump or downgrade is done in this hardening PR. The
source lock remains committed and reproducibility is enforced.
