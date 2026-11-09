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

  testWidgets('Italy shows 25 national + 285 global, separated and lazily built',
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

    expect(find.text('All · 310'), findsOneWidget);
    expect(find.text('National · 25'), findsOneWidget);
    expect(find.text('Global · 285'), findsOneWidget);
    // The second sliver is below the viewport and should not be mounted yet.
    expect(find.byType(SliverList), findsOneWidget);
    expect(find.byType(ObservanceCard).evaluate().length, lessThan(30));
    expect(tester.takeException(), isNull);

    await tester.tap(find.text('Global · 285'));
    await tester.pumpAndSettle();
    expect(find.text('Global · 285'), findsOneWidget);
    expect(find.byType(SliverList), findsOneWidget);
    expect(controller.preferences.marketCode, 'IT');
    expect(tester.takeException(), isNull);
  });

  // Country selector and lazy list must accept all six newly admitted markets.
  const markets = <(String, int, String)>[
    ('CA', 25, 'fr'),
    ('AU', 3, 'en'),
    ('BR', 3, 'pt'),
    ('MX', 3, 'es'),
    ('IN', 5, 'de'),
    ('JP', 13, 'it'),
    ('BD', 2, 'it'),
    ('ID', 2, 'en'),
    ('KH', 3, 'fr'),
    ('MY', 2, 'de'),
    ('VN', 2, 'pt'),
    ('LA', 1, 'es'),
  ];
  // Source-verified Wave04: all fifteen new countries must remain selectable.
  const wave04Markets = <(String, int, String)>[
    ('CZ', 7, 'it'),
    ('SK', 6, 'es'),
    ('NO', 5, 'fr'),
    ('FI', 15, 'de'),
    ('SE', 1, 'pt'),
    ('PL', 5, 'en'),
    ('IE', 2, 'it'),
    ('NL', 2, 'es'),
    ('ZA', 6, 'fr'),
    ('PH', 7, 'de'),
    ('NZ', 3, 'pt'),
    ('SG', 2, 'en'),
    ('KR', 7, 'it'),
    ('AR', 8, 'es'),
    ('PE', 7, 'fr'),
  ];
  for (final market in wave04Markets) {
    testWidgets('Wave04 ${market.$1}: national/global 320px without overflow',
        (tester) async {
      tester.view.physicalSize = const Size(320, 844);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      final controller = await buildLoadedTestController(
        catalog: catalog,
        preferences: UserPreferences(marketCode: market.$1),
      );
      addTearDown(controller.dispose);
      await tester.pumpWidget(
        wrapTestApp(
          AroundTheWorldPage(controller: controller),
          locale: Locale(market.$3),
        ),
      );
      await tester.pumpAndSettle();
      expect(controller.recordsForMarket(market.$1), hasLength(market.$2));
      expect(find.byType(ChoiceChip), findsNWidgets(3));
      expect(find.byType(ObservanceCard).evaluate().length, lessThan(30));
      expect(tester.takeException(), isNull);
    });
  }

  for (final market in markets) {
    testWidgets('Wave03 ${market.$1} is browseable in ${market.$3} at 320px',
        (tester) async {
      tester.view.physicalSize = const Size(320, 844);
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      final controller = await buildLoadedTestController(
        catalog: catalog,
        preferences: UserPreferences(marketCode: market.$1),
      );
      addTearDown(controller.dispose);
      await tester.pumpWidget(
        wrapTestApp(
          AroundTheWorldPage(controller: controller),
          locale: Locale(market.$3),
        ),
      );
      await tester.pumpAndSettle();
      expect(controller.recordsForMarket(market.$1), hasLength(market.$2));
      expect(find.byType(ChoiceChip), findsNWidgets(3));
      expect(find.byType(ObservanceCard).evaluate().length, lessThan(30));
      expect(controller.preferences.marketCode, market.$1);
      expect(tester.takeException(), isNull);
    });
  }

  test('national source is not conflated with world scope', () async {
    final national = catalog.records.where((r) => r.scope == 'NATIONAL').toList();
    final global = catalog.records.where((r) => r.scope == 'GLOBAL').toList();
    expect(catalog.records.length, 504);
    expect(national.length, 219);
    expect(global.length, 285);
    expect(national.every((r) => r.countries.length == 1), isTrue);
    expect(global.every((r) => r.countries.isEmpty), isTrue);
    expect(catalog.byId.containsKey('italian-mafia-victims-remembrance-day'), isTrue);
    expect(catalog.byId.containsKey('spain-democratic-memory-victims-day'), isTrue);
  });
}
