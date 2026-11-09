import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/core/widgets/observance_card.dart';
import 'package:world_days/data/catalog_repository.dart';
import 'package:world_days/data/preferences_repository.dart';
import 'package:world_days/features/saved/saved_page.dart';

import '../support/world_days_test_support.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late CatalogSnapshot catalog;
  setUpAll(() async {
    // Load asset bundles outside testWidgets' fake-async zone.
    catalog = await const CatalogRepository().load();
  });

  testWidgets('Saved handles all bundled observances marked as favorites',
      (tester) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final favorites = {for (final item in catalog.records) item.id};
    final controller = await buildLoadedTestController(
      catalog: catalog,
      preferences: UserPreferences(favoriteIds: favorites),
    );
    addTearDown(controller.dispose);

    final stopwatch = Stopwatch()..start();
    await tester.pumpWidget(
      wrapTestApp(SavedPage(controller: controller)),
    );
    await tester.pump();
    stopwatch.stop();

    final listView = tester.widget<ListView>(find.byType(ListView).first);
    final declaredChildren = listView.childrenDelegate.estimatedChildCount ?? 0;
    final mountedCards = find.byType(ObservanceCard).evaluate().length;

    expect(catalog.records.length, greaterThanOrEqualTo(296));
    expect(controller.preferences.favoriteIds.length, catalog.records.length);
    expect(declaredChildren, greaterThanOrEqualTo(favorites.length * 2));
    expect(mountedCards, greaterThan(0));
    expect(tester.takeException(), isNull);

    // Explicitly widget-test CI wall time; NOT Android profile frame/GPU/RAM.
    final metrics = <String, Object>{
      'metric': 'flutter_widget_test_wall_clock_not_android_device',
      'viewport_logical_px': '390x844',
      'favorite_count': favorites.length,
      'declared_children': declaredChildren,
      'mounted_cards': mountedCards,
      'pump_wall_ms': stopwatch.elapsedMicroseconds / 1000,
    };
    debugPrint('WORLD_DAYS_SAVED_STRESS|${jsonEncode(metrics)}');
  }, timeout: const Timeout(Duration(seconds: 60)));
}
