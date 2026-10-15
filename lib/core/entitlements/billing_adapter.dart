import 'entitlement_models.dart';

abstract interface class BillingAdapter {
  bool get supported;

  String get removeAdsProductId;

  Future<BillingProductInfo?> loadRemoveAdsProduct();

  Future<BillingResult> purchaseRemoveAds();

  Future<BillingResult> restoreRemoveAds();

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
  Future<void> dispose() async {}
}
