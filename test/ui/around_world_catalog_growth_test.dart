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

  testWidgets('Italy shows 25 national + 289 global, separated and lazily built',
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

    expect(find.text('All · 314'), findsOneWidget);
    expect(find.text('National · 25'), findsOneWidget);
    expect(find.text('Global · 289'), findsOneWidget);
    // The second sliver is below the viewport and should not be mounted yet.
    expect(find.byType(SliverList), findsOneWidget);
    expect(find.byType(ObservanceCard).evaluate().length, lessThan(30));
    expect(tester.takeException(), isNull);

    await tester.tap(find.text('Global · 289'));
    await tester.pumpAndSettle();
    expect(find.text('Global · 289'), findsOneWidget);
    expect(find.byType(SliverList), findsOneWidget);
    expect(controller.preferences.marketCode, 'IT');
    expect(tester.takeException(), isNull);
  });

  // Country selector and lazy list must accept all six newly admitted markets.
  const markets = <(String, int, String)>[
    ('CA', 32, 'fr'),
    ('AU', 3, 'en'),
    ('BR', 3, 'pt'),
    ('MX', 3, 'es'),
    ('IN', 2, 'de'),
    ('JP', 3, 'it'),
  ];
  // Source-verified Wave04: all fifteen new countries must remain selectable.
  const wave04Markets = <(String, int, String)>[
    ('CZ', 25, 'it'),
    ('SK', 29, 'es'),
    ('NO', 10, 'fr'),
    ('FI', 20, 'de'),
    ('SE', 10, 'pt'),
    ('PL', 18, 'en'),
    ('IE', 2, 'it'),
    ('NL', 2, 'es'),
    ('ZA', 6, 'fr'),
    ('PH', 201, 'de'),
    ('NZ', 3, 'pt'),
    ('SG', 2, 'en'),
    ('KR', 57, 'it'),
    ('AR', 8, 'es'),
    ('PE', 7, 'fr'),
  ];
  // Wave06: source-approved national market admissions must render with locale fallback.
  const wave06Markets = <(String, int, String)>[
    ('MT', 8, 'it'),
    ('HR', 4, 'de'),
    ('CY', 4, 'fr'),
  ];
  for (final market in wave06Markets) {
    testWidgets('Wave06 ${market.$1}: available in ${market.$3} at 320px',
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

  const wave07Markets = <(String, int, String)>[
    ('EE', 17, 'it'),
    ('LV', 5, 'es'),
    ('LT', 6, 'fr'),
    ('IS', 3, 'de'),
    ('LU', 1, 'pt'),
  ];
  for (final market in wave07Markets) {
    testWidgets('Wave07 ${market.$1} locale ${market.$3} 320px browse',
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
    expect(catalog.records.length, 1111);
    expect(national.length, 822);
    expect(global.length, 289);
    expect(national.every((r) => r.countries.length == 1), isTrue);
    expect(global.every((r) => r.countries.isEmpty), isTrue);
    expect(catalog.byId.containsKey('italian-mafia-victims-remembrance-day'), isTrue);
    expect(catalog.byId.containsKey('spain-democratic-memory-victims-day'), isTrue);
  });
}
