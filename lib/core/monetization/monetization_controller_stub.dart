import 'package:flutter/foundation.dart';

class MonetizationController extends ChangeNotifier {
  bool get supported => false;
  bool get canRequestAds => false;
  bool get privacyOptionsRequired => false;
  bool get initialized => true;
  String? get lastError => null;

  Future<void> initialize() async {}

  Future<bool> showPrivacyOptions() async => false;
}
