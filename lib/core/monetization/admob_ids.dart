import 'package:flutter/foundation.dart';

class AdMobIds {
  AdMobIds._();

  static const _production = bool.fromEnvironment(
    'WORLD_DAYS_ADS_PRODUCTION',
    defaultValue: false,
  );

  static const _androidProductionBanner =
      String.fromEnvironment('ADMOB_ANDROID_BANNER_ID');
  static const _iosProductionBanner =
      String.fromEnvironment('ADMOB_IOS_BANNER_ID');

  static const androidTestBanner =
      'ca-app-pub-3940256099942544/9214589741';
  static const iosTestBanner =
      'ca-app-pub-3940256099942544/2435281174';

  static bool get production => _production;

  static String? banner() {
    if (kIsWeb) return null;
    return switch (defaultTargetPlatform) {
      TargetPlatform.android => _production
          ? _validatedProductionId(_androidProductionBanner)
          : androidTestBanner,
      TargetPlatform.iOS => _production
          ? _validatedProductionId(_iosProductionBanner)
          : iosTestBanner,
      _ => null,
    };
  }

  static String _validatedProductionId(String value) {
    final trimmed = value.trim();
    if (!RegExp(r'^ca-app-pub-\d{16}/\d{10}$').hasMatch(trimmed)) {
      throw StateError('invalid_or_missing_production_banner_id');
    }
    if (trimmed.startsWith('ca-app-pub-3940256099942544/')) {
      throw StateError('production_banner_uses_google_test_id');
    }
    return trimmed;
  }
}
