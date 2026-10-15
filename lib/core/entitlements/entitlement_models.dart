enum AppPlan { free, premium, lifetime }

enum EntitlementSource {
  localDefault,
  providerVerified,
  offlineCache,
  qaOverride,
  unknown,
}

class EntitlementSnapshot {
  const EntitlementSnapshot({
    required this.plan,
    required this.source,
    required this.verifiedAt,
  });

  const EntitlementSnapshot.free()
      : plan = AppPlan.free,
        source = EntitlementSource.localDefault,
        verifiedAt = null;

  final AppPlan plan;
  final EntitlementSource source;
  final DateTime? verifiedAt;

  bool get removesAds => plan == AppPlan.premium || plan == AppPlan.lifetime;

  EntitlementSnapshot asOfflineCache() => EntitlementSnapshot(
        plan: plan,
        source: plan == AppPlan.free
            ? EntitlementSource.localDefault
            : EntitlementSource.offlineCache,
        verifiedAt: verifiedAt,
      );

  Map<String, dynamic> toJson() => {
        'plan': plan.name,
        'source': source.name,
        'verifiedAt': verifiedAt?.toUtc().toIso8601String(),
      };

  factory EntitlementSnapshot.fromJson(Map<String, dynamic> json) {
    final plan = AppPlan.values.firstWhere(
      (value) => value.name == json['plan'],
      orElse: () => AppPlan.free,
    );
    final source = EntitlementSource.values.firstWhere(
      (value) => value.name == json['source'],
      orElse: () => EntitlementSource.unknown,
    );
    return EntitlementSnapshot(
      plan: plan,
      source: source,
      verifiedAt: DateTime.tryParse(json['verifiedAt']?.toString() ?? ''),
    );
  }
}

class ProductLimits {
  const ProductLimits({required this.adsEnabled});

  final bool adsEnabled;

  factory ProductLimits.fromEntitlement(EntitlementSnapshot snapshot) =>
      ProductLimits(adsEnabled: !snapshot.removesAds);
}

enum PurchaseFlowState {
  idle,
  loadingProduct,
  ready,
  purchasing,
  restoring,
  pending,
  purchased,
  restored,
  cancelled,
  failed,
  billingUnavailable,
}

class BillingProductInfo {
  const BillingProductInfo({
    required this.productId,
    required this.displayPrice,
    this.title,
  });

  final String productId;
  final String displayPrice;
  final String? title;
}

class BillingResult {
  const BillingResult({
    required this.state,
    this.productId,
    this.verified = false,
    this.errorCode,
  });

  final PurchaseFlowState state;
  final String? productId;

  /// True only after the billing adapter has validated provider state and
  /// mapped the transaction to the expected product.
  final bool verified;
  final String? errorCode;

  bool grantsLifetime(String expectedProductId) =>
      verified &&
      productId == expectedProductId &&
      (state == PurchaseFlowState.purchased ||
          state == PurchaseFlowState.restored);
}
