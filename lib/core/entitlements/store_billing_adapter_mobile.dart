import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:in_app_purchase/in_app_purchase.dart';

import 'billing_adapter.dart';
import 'entitlement_models.dart';

BillingAdapter createStoreBillingAdapter() => InAppPurchaseBillingAdapter();

class InAppPurchaseBillingAdapter implements BillingAdapter {
  InAppPurchaseBillingAdapter({
    InAppPurchase? store,
    String? productId,
  })  : _store = store,
        _productId = productId ??
            const String.fromEnvironment(
              'WORLD_DAYS_REMOVE_ADS_PRODUCT_ID',
              defaultValue: 'world_days_remove_ads_lifetime',
            );

  InAppPurchase? _store;
  InAppPurchase get _storeClient => _store ??= InAppPurchase.instance;
  final String _productId;
  final StreamController<BillingResult> _updates =
      StreamController<BillingResult>.broadcast();
  final Map<String, PurchaseDetails> _awaitingCompletion = {};

  StreamSubscription<List<PurchaseDetails>>? _purchaseSubscription;
  ProductDetails? _product;
  bool _storeAvailable = false;
  bool _disposed = false;

  @override
  bool get supported =>
      defaultTargetPlatform == TargetPlatform.android ||
      defaultTargetPlatform == TargetPlatform.iOS;

  @override
  String get removeAdsProductId => _productId;

  @override
  Stream<BillingResult> get updates => _updates.stream;

  Future<void> _ensurePurchaseListener() async {
    if (_purchaseSubscription != null || !supported || _disposed) return;
    _purchaseSubscription = _storeClient.purchaseStream.listen(
      (items) => unawaited(_handlePurchases(items)),
      onError: (Object error) {
        if (_disposed) return;
        _updates.add(
          BillingResult(
            state: PurchaseFlowState.failed,
            productId: _productId,
            errorCode: 'purchase_stream:$error',
          ),
        );
      },
    );
  }

  @override
  Future<BillingProductInfo?> loadRemoveAdsProduct() async {
    if (!supported || _disposed) return null;

    try {
      _storeAvailable = await _storeClient.isAvailable();
      if (!_storeAvailable) return null;

      await _ensurePurchaseListener();
      final response = await _storeClient.queryProductDetails({_productId});
      if (response.error != null ||
          response.notFoundIDs.contains(_productId)) {
        return null;
      }

      ProductDetails? match;
      for (final product in response.productDetails) {
        if (product.id == _productId) {
          match = product;
          break;
        }
      }
      if (match == null) return null;

      _product = match;
      return BillingProductInfo(
        productId: match.id,
        displayPrice: match.price,
        title: match.title,
      );
    } catch (_) {
      _storeAvailable = false;
      return null;
    }
  }

  @override
  Future<BillingResult> purchaseRemoveAds() async {
    if (!supported || _disposed) {
      return const BillingResult(
        state: PurchaseFlowState.billingUnavailable,
        errorCode: 'billing_platform_unsupported',
      );
    }

    final product = _product ?? (await _loadProductDetails());
    if (!_storeAvailable || product == null) {
      return BillingResult(
        state: PurchaseFlowState.billingUnavailable,
        productId: _productId,
        errorCode: 'remove_ads_product_unavailable',
      );
    }

    await _ensurePurchaseListener();
    try {
      final started = await _storeClient.buyNonConsumable(
        purchaseParam: PurchaseParam(productDetails: product),
      );
      return BillingResult(
        state:
            started ? PurchaseFlowState.purchasing : PurchaseFlowState.failed,
        productId: _productId,
        errorCode: started ? null : 'purchase_not_started',
      );
    } catch (error) {
      return BillingResult(
        state: PurchaseFlowState.failed,
        productId: _productId,
        errorCode: 'purchase_start:$error',
      );
    }
  }

  @override
  Future<BillingResult> restoreRemoveAds() async {
    if (!supported || _disposed) {
      return const BillingResult(
        state: PurchaseFlowState.billingUnavailable,
        errorCode: 'billing_platform_unsupported',
      );
    }

    try {
      _storeAvailable = await _storeClient.isAvailable();
      if (!_storeAvailable) {
        return BillingResult(
          state: PurchaseFlowState.billingUnavailable,
          productId: _productId,
          errorCode: 'store_unavailable',
        );
      }
      await _ensurePurchaseListener();
      await _storeClient.restorePurchases();
      return BillingResult(
        state: PurchaseFlowState.ready,
        productId: _productId,
        errorCode: 'restore_completed_without_match',
      );
    } catch (error) {
      return BillingResult(
        state: PurchaseFlowState.failed,
        productId: _productId,
        errorCode: 'restore_start:$error',
      );
    }
  }

  Future<ProductDetails?> _loadProductDetails() async {
    final info = await loadRemoveAdsProduct();
    return info == null ? null : _product;
  }

  Future<void> _handlePurchases(List<PurchaseDetails> purchases) async {
    for (final purchase in purchases) {
      if (_disposed || purchase.productID != _productId) continue;

      switch (purchase.status) {
        case PurchaseStatus.pending:
          _updates.add(
            BillingResult(
              state: PurchaseFlowState.pending,
              productId: _productId,
              transactionId: purchase.purchaseID,
            ),
          );
          break;
        case PurchaseStatus.canceled:
          _updates.add(
            BillingResult(
              state: PurchaseFlowState.cancelled,
              productId: _productId,
              transactionId: purchase.purchaseID,
              errorCode: 'purchase_cancelled',
            ),
          );
          break;
        case PurchaseStatus.error:
          _updates.add(
            BillingResult(
              state: PurchaseFlowState.failed,
              productId: _productId,
              transactionId: purchase.purchaseID,
              errorCode: purchase.error?.code ?? 'purchase_error',
            ),
          );
          break;
        case PurchaseStatus.purchased:
        case PurchaseStatus.restored:
          final localData =
              purchase.verificationData.localVerificationData.trim();
          final serverData =
              purchase.verificationData.serverVerificationData.trim();
          if (localData.isEmpty && serverData.isEmpty) {
            _updates.add(
              BillingResult(
                state: PurchaseFlowState.failed,
                productId: _productId,
                transactionId: purchase.purchaseID,
                errorCode: 'purchase_verification_data_missing',
              ),
            );
            break;
          }

          final transactionId = purchase.purchaseID ??
              '${purchase.productID}:${purchase.transactionDate ?? 'unknown'}';
          if (purchase.pendingCompletePurchase) {
            _awaitingCompletion[transactionId] = purchase;
          }
          _updates.add(
            BillingResult(
              state: purchase.status == PurchaseStatus.restored
                  ? PurchaseFlowState.restored
                  : PurchaseFlowState.purchased,
              productId: _productId,
              transactionId: transactionId,
              verified: true,
            ),
          );
          break;
      }
    }
  }

  @override
  Future<void> completePurchase(BillingResult result) async {
    final transactionId = result.transactionId;
    if (transactionId == null) return;
    final purchase = _awaitingCompletion[transactionId];
    if (purchase == null || !purchase.pendingCompletePurchase) return;
    await _storeClient.completePurchase(purchase);
    _awaitingCompletion.remove(transactionId);
  }

  @override
  Future<void> dispose() async {
    if (_disposed) return;
    _disposed = true;
    await _purchaseSubscription?.cancel();
    _purchaseSubscription = null;
    _awaitingCompletion.clear();
    await _updates.close();
  }
}
