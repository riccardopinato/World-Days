import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

class MonetizationController extends ChangeNotifier {
  bool _initialized = false;
  bool _canRequestAds = false;
  bool _privacyOptionsRequired = false;
  bool _mobileAdsInitialized = false;
  bool _adsSuppressed = false;
  String? _lastError;

  bool get supported =>
      defaultTargetPlatform == TargetPlatform.android ||
      defaultTargetPlatform == TargetPlatform.iOS;
  bool get initialized => _initialized;
  bool get canRequestAds => !_adsSuppressed && _canRequestAds;
  bool get adsSuppressed => _adsSuppressed;
  bool get privacyOptionsRequired => _privacyOptionsRequired;
  String? get lastError => _lastError;

  void setAdsSuppressed(bool value) {
    if (_adsSuppressed == value) return;
    _adsSuppressed = value;
    if (value) _canRequestAds = false;
    notifyListeners();
  }

  Future<void> initialize() async {
    if (_initialized || !supported) return;
    if (_adsSuppressed) {
      _initialized = true;
      _canRequestAds = false;
      notifyListeners();
      return;
    }
    _lastError = null;

    try {
      await _requestConsentInfoUpdate();
      await _refreshPrivacyOptionsRequirement();
      await _resolveAdEligibility();

      final formError = await _loadAndShowConsentFormIfRequired();
      if (formError != null) {
        _lastError =
            'ump_form:${formError.errorCode}:${formError.message}';
      }

      await _refreshPrivacyOptionsRequirement();
      await _resolveAdEligibility();
    } catch (error) {
      _lastError = 'ump_update:$error';
      try {
        await _refreshPrivacyOptionsRequirement();
        await _resolveAdEligibility();
      } catch (_) {
        _canRequestAds = false;
      }
    } finally {
      _initialized = true;
      notifyListeners();
    }
  }

  Future<bool> showPrivacyOptions() async {
    if (!supported) return false;
    final completer = Completer<FormError?>();
    try {
      await ConsentForm.showPrivacyOptionsForm((error) {
        if (!completer.isCompleted) completer.complete(error);
      });
      final error = await completer.future;
      if (error != null) {
        _lastError =
            'ump_privacy_options:${error.errorCode}:${error.message}';
        notifyListeners();
        return false;
      }
      await _refreshPrivacyOptionsRequirement();
      await _resolveAdEligibility();
      notifyListeners();
      return true;
    } catch (error) {
      _lastError = 'ump_privacy_options:$error';
      notifyListeners();
      return false;
    }
  }

  Future<void> _requestConsentInfoUpdate() {
    final completer = Completer<void>();
    ConsentInformation.instance.requestConsentInfoUpdate(
      ConsentRequestParameters(),
      () {
        if (!completer.isCompleted) completer.complete();
      },
      (error) {
        if (!completer.isCompleted) completer.completeError(error);
      },
    );
    return completer.future;
  }

  Future<FormError?> _loadAndShowConsentFormIfRequired() {
    final completer = Completer<FormError?>();
    ConsentForm.loadAndShowConsentFormIfRequired((error) {
      if (!completer.isCompleted) completer.complete(error);
    });
    return completer.future;
  }

  Future<void> _refreshPrivacyOptionsRequirement() async {
    final status = await ConsentInformation.instance
        .getPrivacyOptionsRequirementStatus();
    _privacyOptionsRequired =
        status == PrivacyOptionsRequirementStatus.required;
  }

  Future<void> _resolveAdEligibility() async {
    final allowed = await ConsentInformation.instance.canRequestAds();
    _canRequestAds = !_adsSuppressed && allowed;
    if (_canRequestAds && !_mobileAdsInitialized) {
      await MobileAds.instance.initialize();
      _mobileAdsInitialized = true;
    }
  }
}
