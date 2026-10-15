import 'package:flutter/foundation.dart';

class MonetizationController extends ChangeNotifier {
  bool _adsSuppressed = false;

  bool get supported => false;
  bool get canRequestAds => false;
  bool get adsSuppressed => _adsSuppressed;
  bool get privacyOptionsRequired => false;
  bool get initialized => true;
  String? get lastError => null;

  void setAdsSuppressed(bool value) {
    if (_adsSuppressed == value) return;
    _adsSuppressed = value;
    notifyListeners();
  }

  Future<void> initialize() async {}

  Future<bool> showPrivacyOptions() async => false;
}
