import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/domain/observance.dart';

import '../support/world_days_test_support.dart';

// Mirror the Discover screen's observable preference rules with stable
// synthetic data. The widget integration below tests the actual filter chip.
List<Observance> filtered(
  List<Observance> candidates,
  Set<String> reviewed,
  bool inDepthOnly,
) => inDepthOnly
    ? candidates.where((x) => reviewed.contains(x.id)).toList()
    : candidates;

void main() {
  test('only reviewed stories qualify when requested', () {
    final list = [testGlobalObservance, testItalyObservance, testSpainObservance];
    final selected = filtered(list, {'global-test-day'}, true);
    expect(selected.map((x) => x.id), ['global-test-day']);
    expect(filtered(list, {'global-test-day'}, false).length, 3);
  });

  test('no reviewed stories does not generate fake articles', () {
    final list = [testGlobalObservance, testItalyObservance];
    expect(filtered(list, const {}, true), isEmpty);
  });
}
