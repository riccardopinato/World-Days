import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:google_mobile_ads/google_mobile_ads.dart';

abstract interface class MonetizationPlatform {
  bool get supported;

  Future<void> requestConsentInfoUpdate();

  Future<String?> loadAndShowConsentFormIfRequired();

  Future<bool> privacyOptionsRequired();

  Future<bool> canRequestAds();

  Future<void> initializeAds();

  Future<String?> showPrivacyOptionsForm();
}

class GoogleMonetizationPlatform implements MonetizationPlatform {
  const GoogleMonetizationPlatform();

  @override
  bool get supported =>
      defaultTargetPlatform == TargetPlatform.android ||
      defaultTargetPlatform == TargetPlatform.iOS;

  @override
  Future<void> requestConsentInfoUpdate() {
    final completer = Completer<void>();
    ConsentInformation.instance.requestConsentInfoUpdate(
      ConsentRequestParameters(),
      () {
        if (!completer.isCompleted) completer.complete();
      },
      (error) {
        if (!completer.isCompleted) {
          completer.completeError(
            StateError('ump_update:${error.errorCode}:${error.message}'),
          );
        }
      },
    );
    return completer.future;
  }

  @override
  Future<String?> loadAndShowConsentFormIfRequired() {
    final completer = Completer<String?>();
    ConsentForm.loadAndShowConsentFormIfRequired((error) {
      if (!completer.isCompleted) {
        completer.complete(
          error == null
              ? null
              : '${error.errorCode}:${error.message}',
        );
      }
    });
    return completer.future;
  }

  @override
  Future<bool> privacyOptionsRequired() async {
    final status = await ConsentInformation.instance
        .getPrivacyOptionsRequirementStatus();
    return status == PrivacyOptionsRequirementStatus.required;
  }

  @override
  Future<bool> canRequestAds() =>
      ConsentInformation.instance.canRequestAds();

  @override
  Future<void> initializeAds() async {
    await MobileAds.instance.initialize();
  }

  @override
  Future<String?> showPrivacyOptionsForm() async {
    final completer = Completer<String?>();
    await ConsentForm.showPrivacyOptionsForm((error) {
      if (!completer.isCompleted) {
        completer.complete(
          error == null
              ? null
              : '${error.errorCode}:${error.message}',
        );
      }
    });
    return completer.future;
  }
}
