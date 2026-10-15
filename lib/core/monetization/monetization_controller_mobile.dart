import 'package:flutter/foundation.dart';

import 'monetization_platform_mobile.dart';

class MonetizationController extends ChangeNotifier {
  MonetizationController({
    MonetizationPlatform? platform,
  }) : _platform = platform ?? const GoogleMonetizationPlatform();

  final MonetizationPlatform _platform;

  bool _initialized = false;
  bool _canRequestAds = false;
  bool _privacyOptionsRequired = false;
  bool _mobileAdsInitialized = false;
  bool _adsSuppressed = false;
  String? _lastError;

  bool get supported => _platform.supported;
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
      await _platform.requestConsentInfoUpdate();
      await _refreshPrivacyOptionsRequirement();
      await _resolveAdEligibility();

      final formError = await _platform.loadAndShowConsentFormIfRequired();
      if (formError != null) {
        _lastError = 'ump_form:$formError';
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
    try {
      final error = await _platform.showPrivacyOptionsForm();
      if (error != null) {
        _lastError = 'ump_privacy_options:$error';
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

  Future<void> _refreshPrivacyOptionsRequirement() async {
    _privacyOptionsRequired = await _platform.privacyOptionsRequired();
  }

  Future<void> _resolveAdEligibility() async {
    final allowed = await _platform.canRequestAds();
    _canRequestAds = !_adsSuppressed && allowed;
    if (_canRequestAds && !_mobileAdsInitialized) {
      await _platform.initializeAds();
      _mobileAdsInitialized = true;
    }
  }
}
