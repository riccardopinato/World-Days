import 'entitlement_models.dart';

abstract interface class BillingAdapter {
  bool get supported;

  String get removeAdsProductId;

  /// Provider purchase updates. A purchase or restore call can return before a
  /// store transaction reaches its final state; the verified terminal state
  /// arrives through this stream.
  Stream<BillingResult> get updates;

  /// Attaches provider listeners during app startup even when an entitlement
  /// is already cached, so unfinished transactions can be redelivered.
  Future<void> initialize();

  /// Requests provider reconciliation for an unfinished transaction recorded
  /// by the entitlement layer. Implementations must be idempotent.
  Future<void> reconcilePendingPurchases();

  Future<BillingProductInfo?> loadRemoveAdsProduct();

  Future<BillingResult> purchaseRemoveAds();

  Future<BillingResult> restoreRemoveAds();

  /// Finalizes a provider transaction only after the entitlement layer has
  /// persisted/delivered the verified capability.
  Future<void> completePurchase(BillingResult result);

  Future<void> dispose();
}

class UnavailableBillingAdapter implements BillingAdapter {
  const UnavailableBillingAdapter({
    this.productId = 'world_days_remove_ads_lifetime',
  });

  final String productId;

  @override
  bool get supported => false;

  @override
  String get removeAdsProductId => productId;

  @override
  Stream<BillingResult> get updates => const Stream<BillingResult>.empty();

  @override
  Future<void> initialize() async {}

  @override
  Future<void> reconcilePendingPurchases() async {}

  @override
  Future<BillingProductInfo?> loadRemoveAdsProduct() async => null;

  @override
  Future<BillingResult> purchaseRemoveAds() async => const BillingResult(
        state: PurchaseFlowState.billingUnavailable,
        errorCode: 'billing_unavailable',
      );

  @override
  Future<BillingResult> restoreRemoveAds() async => const BillingResult(
        state: PurchaseFlowState.billingUnavailable,
        errorCode: 'billing_unavailable',
      );

  @override
  Future<void> completePurchase(BillingResult result) async {}

  @override
  Future<void> dispose() async {}
}
