import 'dart:async';

import 'package:flutter/foundation.dart';

import 'billing_adapter.dart';
import 'entitlement_models.dart';
import 'entitlement_store.dart';

class EntitlementService extends ChangeNotifier {
  EntitlementService({
    EntitlementStore? store,
    BillingAdapter? billingAdapter,
    DateTime Function()? clock,
  })  : _store = store ?? const SharedPreferencesEntitlementStore(),
        _billing = billingAdapter ?? const UnavailableBillingAdapter(),
        _clock = clock ?? DateTime.now;

  final EntitlementStore _store;
  final BillingAdapter _billing;
  final DateTime Function() _clock;
  StreamSubscription<BillingResult>? _billingSubscription;

  EntitlementSnapshot _snapshot = const EntitlementSnapshot.free();
  PurchaseFlowState _flowState = PurchaseFlowState.idle;
  BillingProductInfo? _product;
  String? _lastError;
  bool _initialized = false;

  EntitlementSnapshot get snapshot => _snapshot;
  ProductLimits get limits => ProductLimits.fromEntitlement(_snapshot);
  PurchaseFlowState get flowState => _flowState;
  BillingProductInfo? get product => _product;
  String? get lastError => _lastError;
  bool get initialized => _initialized;
  bool get billingSupported => _billing.supported;
  bool get removesAds => _snapshot.removesAds;

  Future<void> initialize() async {
    if (_initialized) return;
    _snapshot = await _store.load();
    _billingSubscription ??= _billing.updates.listen(
      (result) => unawaited(_applyBillingResult(result)),
      onError: (Object error) {
        _flowState = PurchaseFlowState.failed;
        _lastError = 'billing_update:$error';
        notifyListeners();
      },
    );
    _initialized = true;

    if (!_billing.supported) {
      _flowState = PurchaseFlowState.billingUnavailable;
      notifyListeners();
      return;
    }

    _flowState = PurchaseFlowState.loadingProduct;
    notifyListeners();

    try {
      _product = await _billing.loadRemoveAdsProduct();
      _flowState = _product == null
          ? PurchaseFlowState.billingUnavailable
          : PurchaseFlowState.ready;
      _lastError = _product == null ? 'remove_ads_product_unavailable' : null;
    } catch (error) {
      _flowState = PurchaseFlowState.failed;
      _lastError = 'billing_product_load:$error';
    }
    notifyListeners();
  }

  Future<PurchaseFlowState> purchaseRemoveAds() async {
    if (!_billing.supported || _product == null) {
      _flowState = PurchaseFlowState.billingUnavailable;
      notifyListeners();
      return _flowState;
    }

    _flowState = PurchaseFlowState.purchasing;
    _lastError = null;
    notifyListeners();

    try {
      final result = await _billing.purchaseRemoveAds();
      await _applyBillingResult(result);
    } catch (error) {
      _flowState = PurchaseFlowState.failed;
      _lastError = 'billing_purchase:$error';
      notifyListeners();
    }
    return _flowState;
  }

  Future<PurchaseFlowState> restoreRemoveAds() async {
    if (!_billing.supported) {
      _flowState = PurchaseFlowState.billingUnavailable;
      notifyListeners();
      return _flowState;
    }

    _flowState = PurchaseFlowState.restoring;
    _lastError = null;
    notifyListeners();

    try {
      final result = await _billing.restoreRemoveAds();
      await _applyBillingResult(result);
    } catch (error) {
      _flowState = PurchaseFlowState.failed;
      _lastError = 'billing_restore:$error';
      notifyListeners();
    }
    return _flowState;
  }

  Future<void> _applyBillingResult(BillingResult result) async {
    if (result.grantsLifetime(_billing.removeAdsProductId)) {
      final source = EntitlementSnapshot(
        plan: AppPlan.lifetime,
        source: EntitlementSource.providerVerified,
        verifiedAt: _clock().toUtc(),
      );
      await _store.save(source);
      _snapshot = source;
      _flowState = result.state;
      _lastError = null;
      notifyListeners();
      return;
    }

    _flowState = result.state;
    _lastError = result.errorCode;
    notifyListeners();
  }

  @override
  void dispose() {
    _billingSubscription?.cancel();
    unawaited(_billing.dispose());
    super.dispose();
  }
}
