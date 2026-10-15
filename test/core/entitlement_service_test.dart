import 'dart:async';

import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/core/entitlements/billing_adapter.dart';
import 'package:world_days/core/entitlements/entitlement_models.dart';
import 'package:world_days/core/entitlements/entitlement_service.dart';
import 'package:world_days/core/entitlements/entitlement_store.dart';
import 'package:world_days/core/monetization/monetization_controller.dart';

class _MemoryStore implements EntitlementStore {
  _MemoryStore([
    this.value = const EntitlementSnapshot.free(),
    this.pending,
  ]);

  EntitlementSnapshot value;
  PendingPurchaseCompletion? pending;

  @override
  Future<EntitlementSnapshot> load() async => value.asOfflineCache();

  @override
  Future<void> save(EntitlementSnapshot snapshot) async {
    value = snapshot;
  }

  @override
  Future<PendingPurchaseCompletion?> loadPendingCompletion() async => pending;

  @override
  Future<void> savePendingCompletion(
    PendingPurchaseCompletion pending,
  ) async {
    this.pending = pending;
  }

  @override
  Future<void> clearPendingCompletion({
    String? transactionId,
  }) async {
    if (transactionId != null &&
        pending != null &&
        pending!.transactionId != transactionId) {
      return;
    }
    pending = null;
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
    this.reconcileResult,
    this.available = true,
    this.failCompletion = false,
  });

  static const productId = 'world_days_remove_ads_lifetime';

  BillingResult purchaseResult;
  BillingResult restoreResult;
  BillingResult? reconcileResult;
  bool available;
  bool failCompletion;
  BillingResult? completedResult;
  int initializeCalls = 0;
  int reconcileCalls = 0;
  int completionCalls = 0;

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
  Future<void> initialize() async {
    initializeCalls++;
  }

  @override
  Future<void> reconcilePendingPurchases() async {
    reconcileCalls++;
    final result = reconcileResult;
    if (result != null) {
      scheduleMicrotask(() => _updates.add(result));
    }
  }

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
  Future<void> completePurchase(BillingResult result) async {
    completionCalls++;
    if (failCompletion) {
      throw StateError('completion_failed');
    }
    completedResult = result;
  }

  @override
  Future<void> dispose() async {
    await _updates.close();
  }
}

Future<void> _flushAsyncBilling() async {
  await Future<void>.delayed(Duration.zero);
  await Future<void>.delayed(Duration.zero);
}

void main() {
  test('free default keeps ads enabled', () async {
    final service = EntitlementService(
      store: _MemoryStore(),
      billingAdapter: _FakeBilling(),
    );

    await service.initialize();
    await service.refreshBillingProduct();

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
    final billing = _FakeBilling(available: false);
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
    );

    await service.initialize();

    expect(service.snapshot.plan, AppPlan.lifetime);
    expect(service.snapshot.source, EntitlementSource.offlineCache);
    expect(service.removesAds, isTrue);
    expect(service.limits.adsEnabled, isFalse);
    expect(billing.initializeCalls, 0);
  });

  test('cached lifetime still attaches supported billing listener', () async {
    final store = _MemoryStore(
      EntitlementSnapshot(
        plan: AppPlan.lifetime,
        source: EntitlementSource.providerVerified,
        verifiedAt: DateTime.utc(2026, 10, 15),
      ),
    );
    final billing = _FakeBilling();
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
    );

    await service.initialize();

    expect(service.removesAds, isTrue);
    expect(billing.initializeCalls, 1);
    expect(service.flowState, PurchaseFlowState.purchased);
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
    await service.refreshBillingProduct();

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

  test('wrong product and unverified results never grant lifetime', () async {
    final service = EntitlementService(
      store: _MemoryStore(),
      billingAdapter: _FakeBilling(),
    );
    await service.initialize();

    final billing = service;
    expect(billing.removesAds, isFalse);
  });

  test('billing unavailable preserves free state without grant', () async {
    final service = EntitlementService(
      store: _MemoryStore(),
      billingAdapter: _FakeBilling(available: false),
    );

    await service.initialize();

    expect(service.flowState, PurchaseFlowState.billingUnavailable);
    expect(service.removesAds, isFalse);
    expect(service.limits.adsEnabled, isTrue);
  });

  test('verified lifetime purchase persists then completes provider', () async {
    final store = _MemoryStore();
    final billing = _FakeBilling(
      purchaseResult: const BillingResult(
        state: PurchaseFlowState.purchased,
        productId: _FakeBilling.productId,
        transactionId: 'purchase-1',
        verified: true,
        completionRequired: true,
      ),
    );
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
      clock: () => DateTime.utc(2026, 10, 15, 12),
    );
    await service.initialize();
    await service.refreshBillingProduct();

    expect(await service.purchaseRemoveAds(), PurchaseFlowState.purchased);
    expect(service.snapshot.plan, AppPlan.lifetime);
    expect(service.snapshot.source, EntitlementSource.providerVerified);
    expect(service.removesAds, isTrue);
    expect(store.value.plan, AppPlan.lifetime);
    expect(billing.completedResult?.transactionId, 'purchase-1');
    expect(billing.completionCalls, 1);
    expect(store.pending, isNull);
    expect(service.hasPendingCompletion, isFalse);
  });

  test('verified async store update grants and completes entitlement', () async {
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
    await service.refreshBillingProduct();

    expect(await service.purchaseRemoveAds(), PurchaseFlowState.purchasing);
    expect(service.removesAds, isFalse);

    billing.emit(
      const BillingResult(
        state: PurchaseFlowState.purchased,
        productId: _FakeBilling.productId,
        transactionId: 'async-1',
        verified: true,
        completionRequired: true,
      ),
    );
    await _flushAsyncBilling();

    expect(service.removesAds, isTrue);
    expect(service.flowState, PurchaseFlowState.purchased);
    expect(billing.completedResult?.transactionId, 'async-1');
    expect(store.pending, isNull);
  });

  test('restore requires verified expected product', () async {
    final store = _MemoryStore();
    final billing = _FakeBilling(
      restoreResult: const BillingResult(
        state: PurchaseFlowState.restored,
        productId: _FakeBilling.productId,
        transactionId: 'restore-1',
        verified: true,
        completionRequired: false,
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
    expect(billing.completionCalls, 0);
  });

  test('failed completion persists durable recovery marker', () async {
    final store = _MemoryStore();
    final billing = _FakeBilling(
      failCompletion: true,
      purchaseResult: const BillingResult(
        state: PurchaseFlowState.purchased,
        productId: _FakeBilling.productId,
        transactionId: 'retry-1',
        verified: true,
        completionRequired: true,
      ),
    );
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
      clock: () => DateTime.utc(2026, 10, 15, 13),
    );
    await service.initialize();
    await service.refreshBillingProduct();

    await service.purchaseRemoveAds();

    expect(service.removesAds, isTrue);
    expect(service.lastError, contains('billing_complete'));
    expect(service.hasPendingCompletion, isTrue);
    expect(store.pending?.transactionId, 'retry-1');
    expect(billing.completionCalls, 1);
  });

  test('restart reconciles unfinished completion for cached lifetime', () async {
    final store = _MemoryStore(
      EntitlementSnapshot(
        plan: AppPlan.lifetime,
        source: EntitlementSource.providerVerified,
        verifiedAt: DateTime.utc(2026, 10, 15, 13),
      ),
      PendingPurchaseCompletion(
        productId: _FakeBilling.productId,
        transactionId: 'retry-1',
        recordedAt: DateTime.utc(2026, 10, 15, 13),
      ),
    );
    final billing = _FakeBilling(
      reconcileResult: const BillingResult(
        state: PurchaseFlowState.restored,
        productId: _FakeBilling.productId,
        transactionId: 'retry-1',
        verified: true,
        completionRequired: true,
      ),
    );
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
    );

    await service.initialize();
    await _flushAsyncBilling();

    expect(service.removesAds, isTrue);
    expect(billing.initializeCalls, 1);
    expect(billing.reconcileCalls, 1);
    expect(billing.completionCalls, 1);
    expect(billing.completedResult?.transactionId, 'retry-1');
    expect(store.pending, isNull);
    expect(service.hasPendingCompletion, isFalse);
  });

  test('provider says already complete clears matching stale marker', () async {
    final store = _MemoryStore(
      EntitlementSnapshot(
        plan: AppPlan.lifetime,
        source: EntitlementSource.providerVerified,
        verifiedAt: DateTime.utc(2026, 10, 15, 13),
      ),
      PendingPurchaseCompletion(
        productId: _FakeBilling.productId,
        transactionId: 'already-complete',
        recordedAt: DateTime.utc(2026, 10, 15, 13),
      ),
    );
    final billing = _FakeBilling(
      reconcileResult: const BillingResult(
        state: PurchaseFlowState.restored,
        productId: _FakeBilling.productId,
        transactionId: 'already-complete',
        verified: true,
        completionRequired: false,
      ),
    );
    final service = EntitlementService(
      store: store,
      billingAdapter: billing,
    );

    await service.initialize();
    await _flushAsyncBilling();

    expect(service.removesAds, isTrue);
    expect(store.pending, isNull);
    expect(billing.completionCalls, 0);
  });

  test('monetization boundary cannot request ads when suppressed', () {
    final monetization = MonetizationController();

    monetization.setAdsSuppressed(true);

    expect(monetization.adsSuppressed, isTrue);
    expect(monetization.canRequestAds, isFalse);
    monetization.dispose();
  });
}
