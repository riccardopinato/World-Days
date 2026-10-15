import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/core/monetization/monetization_controller.dart';
import 'package:world_days/core/monetization/monetization_platform_mobile.dart';

class _FakePlatform implements MonetizationPlatform {
  _FakePlatform({
    this.supported = true,
    this.canRequest = true,
    this.privacyRequired = false,
    this.formError,
    this.privacyError,
    this.updateError,
  });

  @override
  bool supported;
  bool canRequest;
  bool privacyRequired;
  String? formError;
  String? privacyError;
  Object? updateError;

  int updateCalls = 0;
  int formCalls = 0;
  int privacyStatusCalls = 0;
  int canRequestCalls = 0;
  int adsInitializeCalls = 0;
  int privacyFormCalls = 0;

  @override
  Future<void> requestConsentInfoUpdate() async {
    updateCalls++;
    final error = updateError;
    if (error != null) throw error;
  }

  @override
  Future<String?> loadAndShowConsentFormIfRequired() async {
    formCalls++;
    return formError;
  }

  @override
  Future<bool> privacyOptionsRequired() async {
    privacyStatusCalls++;
    return privacyRequired;
  }

  @override
  Future<bool> canRequestAds() async {
    canRequestCalls++;
    return canRequest;
  }

  @override
  Future<void> initializeAds() async {
    adsInitializeCalls++;
  }

  @override
  Future<String?> showPrivacyOptionsForm() async {
    privacyFormCalls++;
    return privacyError;
  }
}

void main() {
  test('eligible consent flow initializes Mobile Ads once', () async {
    final platform = _FakePlatform(
      canRequest: true,
      privacyRequired: true,
    );
    final controller = MonetizationController(platform: platform);

    await controller.initialize();

    expect(controller.initialized, isTrue);
    expect(controller.canRequestAds, isTrue);
    expect(controller.privacyOptionsRequired, isTrue);
    expect(platform.updateCalls, 1);
    expect(platform.formCalls, 1);
    expect(platform.adsInitializeCalls, 1);

    await controller.initialize();
    expect(platform.updateCalls, 1);
    expect(platform.adsInitializeCalls, 1);
  });

  test('suppressed entitlement makes zero consent and ad provider calls',
      () async {
    final platform = _FakePlatform();
    final controller = MonetizationController(platform: platform)
      ..setAdsSuppressed(true);

    await controller.initialize();

    expect(controller.initialized, isTrue);
    expect(controller.canRequestAds, isFalse);
    expect(platform.updateCalls, 0);
    expect(platform.formCalls, 0);
    expect(platform.canRequestCalls, 0);
    expect(platform.adsInitializeCalls, 0);
  });

  test('denied eligibility never initializes Mobile Ads', () async {
    final platform = _FakePlatform(canRequest: false);
    final controller = MonetizationController(platform: platform);

    await controller.initialize();

    expect(controller.canRequestAds, isFalse);
    expect(platform.adsInitializeCalls, 0);
  });

  test('consent update error fails closed when fallback eligibility fails',
      () async {
    final platform = _FakePlatform(
      updateError: StateError('network'),
      canRequest: false,
    );
    final controller = MonetizationController(platform: platform);

    await controller.initialize();

    expect(controller.initialized, isTrue);
    expect(controller.canRequestAds, isFalse);
    expect(controller.lastError, contains('ump_update'));
    expect(platform.adsInitializeCalls, 0);
  });

  test('privacy options refreshes ad eligibility after user choice', () async {
    final platform = _FakePlatform(
      canRequest: false,
      privacyRequired: true,
    );
    final controller = MonetizationController(platform: platform);
    await controller.initialize();

    platform
      ..canRequest = true
      ..privacyRequired = false;

    expect(await controller.showPrivacyOptions(), isTrue);

    expect(controller.canRequestAds, isTrue);
    expect(controller.privacyOptionsRequired, isFalse);
    expect(platform.privacyFormCalls, 1);
    expect(platform.adsInitializeCalls, 1);
  });

  test('privacy form error does not change eligibility optimistically',
      () async {
    final platform = _FakePlatform(
      canRequest: false,
      privacyRequired: true,
      privacyError: '7:form_error',
    );
    final controller = MonetizationController(platform: platform);
    await controller.initialize();

    expect(await controller.showPrivacyOptions(), isFalse);

    expect(controller.canRequestAds, isFalse);
    expect(controller.lastError, contains('ump_privacy_options'));
  });
}
