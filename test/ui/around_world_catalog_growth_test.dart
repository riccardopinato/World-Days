import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/core/widgets/observance_card.dart';
import 'package:world_days/data/catalog_repository.dart';
import 'package:world_days/data/preferences_repository.dart';
import 'package:world_days/features/discover/around_the_world_page.dart';

import '../support/world_days_test_support.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late CatalogSnapshot catalog;

  setUpAll(() async {
    catalog = await const CatalogRepository().load();
  });

  testWidgets('Italy shows 25 national + 282 global, separated and lazily built',
      (tester) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final controller = await buildLoadedTestController(
      catalog: catalog,
      preferences: const UserPreferences(marketCode: 'IT'),
    );
    addTearDown(controller.dispose);

    await tester.pumpWidget(
      wrapTestApp(AroundTheWorldPage(controller: controller)),
    );
    await tester.pumpAndSettle();

    expect(find.text('All · 307'), findsOneWidget);
    expect(find.text('National · 25'), findsOneWidget);
    expect(find.text('Global · 282'), findsOneWidget);
    expect(find.byType(SliverList), findsNWidgets(2));
    expect(find.byType(ObservanceCard).evaluate().length, lessThan(30));
    expect(tester.takeException(), isNull);

    await tester.tap(find.text('Global · 282'));
    await tester.pumpAndSettle();
    expect(find.text('Global · 282'), findsOneWidget);
    expect(find.byType(SliverList), findsOneWidget);
    expect(controller.preferences.marketCode, 'IT');
    expect(tester.takeException(), isNull);
  });

  test('national source is not conflated with world scope', () async {
    final national = catalog.records.where((r) => r.scope == 'NATIONAL').toList();
    final global = catalog.records.where((r) => r.scope == 'GLOBAL').toList();
    expect(catalog.records.length, 339);
    expect(national.length, 57);
    expect(global.length, 282);
    expect(national.every((r) => r.countries.length == 1), isTrue);
    expect(global.every((r) => r.countries.isEmpty), isTrue);
    expect(catalog.byId.containsKey('italian-mafia-victims-remembrance-day'), isTrue);
    expect(catalog.byId.containsKey('spain-democratic-memory-victims-day'), isTrue);
  });
}
