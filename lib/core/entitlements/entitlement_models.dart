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

class PendingPurchaseCompletion {
  const PendingPurchaseCompletion({
    required this.productId,
    required this.transactionId,
    required this.recordedAt,
  });

  final String productId;
  final String transactionId;
  final DateTime recordedAt;

  Map<String, dynamic> toJson() => {
        'productId': productId,
        'transactionId': transactionId,
        'recordedAt': recordedAt.toUtc().toIso8601String(),
      };

  factory PendingPurchaseCompletion.fromJson(Map<String, dynamic> json) {
    final productId = json['productId']?.toString().trim() ?? '';
    final transactionId = json['transactionId']?.toString().trim() ?? '';
    final recordedAt =
        DateTime.tryParse(json['recordedAt']?.toString() ?? '')?.toUtc();

    if (productId.isEmpty || transactionId.isEmpty || recordedAt == null) {
      throw const FormatException('invalid_pending_purchase_completion');
    }

    return PendingPurchaseCompletion(
      productId: productId,
      transactionId: transactionId,
      recordedAt: recordedAt,
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
    this.transactionId,
    this.verified = false,
    this.completionRequired = false,
    this.errorCode,
  });

  final PurchaseFlowState state;
  final String? productId;
  final String? transactionId;

  /// True only after the billing adapter has validated the store-reported
  /// state and mapped it to the expected product. This flag does not claim
  /// server-side receipt verification.
  final bool verified;

  /// True when the store reports that this transaction still requires
  /// provider finalization/acknowledgement after entitlement delivery.
  final bool completionRequired;
  final String? errorCode;

  bool grantsLifetime(String expectedProductId) =>
      verified &&
      productId == expectedProductId &&
      (state == PurchaseFlowState.purchased ||
          state == PurchaseFlowState.restored);
}
