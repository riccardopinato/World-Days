import 'dart:async';

import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/core/entitlements/billing_adapter.dart';
import 'package:world_days/core/entitlements/entitlement_models.dart';
import 'package:world_days/core/entitlements/entitlement_service.dart';
import 'package:world_days/core/entitlements/entitlement_store.dart';
import 'package:world_days/core/monetization/monetization_controller.dart';

class _MemoryStore implements EntitlementStore {
  _MemoryStore([this.value = const EntitlementSnapshot.free()]);

  EntitlementSnapshot value;

  @override
  Future<EntitlementSnapshot> load() async => value.asOfflineCache();

  @override
  Future<void> save(EntitlementSnapshot snapshot) async {
    value = snapshot;
  }
}

class _FakeBilling implements BillingAdapter {
  _FakeBilling({
    this.purchaseResult = const BillingResult(
      state: PurchaseFlowState.cancelled,
    ),
    this.restoreResult = const BillingResult(
      state: PurchaseFlowState.cancelled,
    ),
    this.available = true,
  });

  static const productId = 'world_days_remove_ads_lifetime';

  BillingResult purchaseResult;
  BillingResult restoreResult;
  bool available;
  final StreamController<BillingResult> _updates =
      StreamController<BillingResult>.broadcast();

  void emit(BillingResult result) => _updates.add(result);

  @override
  bool get supported => available;

  @override
  String get removeAdsProductId => productId;

  @override
  Stream<BillingResult> get updates => _updates.stream;

  @override
  Future<BillingProductInfo?> loadRemoveAdsProduct() async => available
      ? const BillingProductInfo(
          productId: productId,
          displayPrice: '€2.99',
        )
      : null;

  @override
  Future<BillingResult> purchaseRemoveAds() async => purchaseResult;

  @override
  Future<BillingResult> restoreRemoveAds() async => restoreResult;

  @override
  Future<void> dispose() async {
    await _updates.close();
  }
}

void main() {
  test('free default keeps ads enabled', () async {
    final service = EntitlementService(
      store: _MemoryStore(),
      billingAdapter: _FakeBilling(),
    );

    await service.initialize();

    expect(service.snapshot.plan, AppPlan.free);
    expect(service.limits.adsEnabled, isTrue);
    expect(service.flowState, PurchaseFlowState.ready);
  });

  test('cached lifetime entitlement survives offline as cache', () async {
    final store = _MemoryStore(
      EntitlementSnapshot(
        plan: AppPlan.lifetime,
        source: EntitlementSource.providerVerified,
        verifiedAt: DateTime.utc(2026, 10, 15),
      ),
    );
    final service = EntitlementService(
      store: store,
      billingAdapter: _FakeBilling(available: false),
    );

    await service.initialize();

    expect(service.snapshot.plan, AppPlan.lifetime);
    expect(service.snapshot.source, EntitlementSource.offlineCache);
    expect(service.removesAds, isTrue);
    expect(service.limits.adsEnabled, isFalse);
  });

  test('pending or cancelled purchase never grants entitlement', () async {
    final billing = _FakeBilling(
      purchaseResult: const BillingResult(
        state: PurchaseFlowState.pending,
        productId: _FakeBilling.productId,
        verified: false,
      ),
    );
    final service = EntitlementService(
      store: _MemoryStore(),
      billingAdapter: billing,
    );
    await service.initialize();

    expect(await service.purchaseRemoveAds(), PurchaseFlowState.pending);
    expect(service.removesAds, isFalse);

    billing.purchaseResult = const BillingResult(
      state: PurchaseFlowState.cancelled,
      productId: _FakeBilling.productId,
      verified: false,
    );
    expect(await service.purchaseRemoveAds(), PurchaseFlowState.cancelled);
    expect(service.removesAds, isFalse);
  });

  test('verified lifetime purchase grants and persists Remove Ads', () async {
    final store = _MemoryStore();
    final billing = _FakeBilling(
      purchaseResult: const BillingResult(
        state: PurchaseFlowState.purchased,
        productId: _FakeBilling.productId,
        verified: true,
      ),
    );
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
      clock: () => DateTime.utc(2026, 10, 15, 12),
    );
    await service.initialize();

    expect(await service.purchaseRemoveAds(), PurchaseFlowState.purchased);
    expect(service.snapshot.plan, AppPlan.lifetime);
    expect(service.snapshot.source, EntitlementSource.providerVerified);
    expect(service.removesAds, isTrue);
    expect(store.value.plan, AppPlan.lifetime);
  });

  test('verified asynchronous store update grants entitlement', () async {
    final store = _MemoryStore();
    final billing = _FakeBilling(
      purchaseResult: const BillingResult(
        state: PurchaseFlowState.purchasing,
        productId: _FakeBilling.productId,
      ),
    );
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
    );
    await service.initialize();

    expect(await service.purchaseRemoveAds(), PurchaseFlowState.purchasing);
    expect(service.removesAds, isFalse);

    billing.emit(
      const BillingResult(
        state: PurchaseFlowState.purchased,
        productId: _FakeBilling.productId,
        verified: true,
      ),
    );
    await Future<void>.delayed(Duration.zero);

    expect(service.removesAds, isTrue);
    expect(service.flowState, PurchaseFlowState.purchased);
  });

  test('restore requires verified expected product', () async {
    final store = _MemoryStore();
    final billing = _FakeBilling(
      restoreResult: const BillingResult(
        state: PurchaseFlowState.restored,
        productId: _FakeBilling.productId,
        verified: true,
      ),
    );
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
    );
    await service.initialize();

    expect(await service.restoreRemoveAds(), PurchaseFlowState.restored);
    expect(service.snapshot.plan, AppPlan.lifetime);
    expect(service.limits.adsEnabled, isFalse);
  });

  test('monetization boundary cannot request ads when suppressed', () {
    final monetization = MonetizationController();

    monetization.setAdsSuppressed(true);

    expect(monetization.adsSuppressed, isTrue);
    expect(monetization.canRequestAds, isFalse);
    monetization.dispose();
  });
}
