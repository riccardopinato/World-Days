import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/core/monetization/banner_request_epoch.dart';

void main() {
  test('revocation invalidates an in-flight adaptive banner request', () {
    final gate = BannerRequestEpoch();
    final pending = gate.begin();
    expect(gate.isCurrent(pending), isTrue);
    gate.invalidate();
    expect(gate.isCurrent(pending), isFalse);
  });

  test('a newer request excludes callbacks from an old request', () {
    final gate = BannerRequestEpoch();
    final old = gate.begin();
    final current = gate.begin();
    expect(gate.isCurrent(old), isFalse);
    expect(gate.isCurrent(current), isTrue);
  });
}
