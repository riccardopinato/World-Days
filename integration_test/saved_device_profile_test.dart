// ON-DEMAND DEVICE TEST ONLY. Never installed over user-owned production data.
// Run via flutter drive --profile on a clean, disposable Android test device.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'package:world_days/data/catalog_repository.dart';
import 'package:world_days/data/preferences_repository.dart';
import 'package:world_days/features/saved/saved_page.dart';

import '../test/support/world_days_test_support.dart';

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  // Let the actual Android scheduler drive frame timing during flings.
  // The default test policy may suppress frames and bias measurements.
  binding.framePolicy = LiveTestWidgetsFlutterBindingFramePolicy.fullyLive;

  late CatalogSnapshot snapshot;
  setUpAll(() async {
    // No production network, no user records. Bundled, verified offline pack.
    snapshot = await const CatalogRepository().load();
    expect(snapshot.records.length, greaterThanOrEqualTo(296));
  });

  for (final count in <int>[0, 50, 150, 296]) {
    testWidgets('Saved device profile: $count offline favorites', (tester) async {
      final ids = <String>{
        for (final record in snapshot.records.take(count)) record.id,
      };
      final controller = await buildLoadedTestController(
        catalog: snapshot,
        preferences: UserPreferences(favoriteIds: ids),
      );
      addTearDown(controller.dispose);

      await tester.pumpWidget(
        wrapTestApp(SavedPage(controller: controller)),
      );
      await tester.pumpAndSettle(const Duration(milliseconds: 16));
      expect(tester.takeException(), isNull);
      expect(controller.preferences.favoriteIds.length, count);

      final scrollable = find.byType(Scrollable).first;
      // Warmup (excluded from FrameTiming capture).
      if (count > 0) {
        await tester.fling(scrollable, const Offset(0, -450), 1300);
        await tester.pumpAndSettle(const Duration(milliseconds: 16));
      }

      // Flutter engine frame timings on-device. The integration driver
      // exports reportData to a host JSON; no fabricated FPS claims.
      await binding.watchPerformance(() async {
        for (var repeat = 0; repeat < 5; repeat++) {
          await tester.fling(
            scrollable,
            Offset(0, repeat.isEven ? -650 : 650),
            1650,
          );
          await tester.pumpAndSettle(const Duration(milliseconds: 16));
        }
      }, reportKey: 'saved_scroll_$count' '_favorites');

      expect(tester.takeException(), isNull);
    }, timeout: const Timeout(Duration(minutes: 5)));
  }
}
