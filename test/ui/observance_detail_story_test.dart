import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/data/catalog_repository.dart';
import 'package:world_days/features/detail/observance_detail_page.dart';

import '../support/world_days_test_support.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Africa detail shows source-backed 1989 and original Italian story',
      (tester) async {
    final snapshot = await const CatalogRepository().load();
    final record = snapshot.byId['africa-industrialization-day']!;
    final controller = await buildLoadedTestController(catalog: snapshot);
    addTearDown(controller.dispose);

    await tester.pumpWidget(
      wrapTestApp(
        ObservanceDetailPage(observance: record, controller: controller),
        locale: const Locale('it'),
      ),
    );
    await tester.pumpAndSettle();

    final facts = find.byKey(
      const ValueKey<String>('detail-facts-card'),
    );
    expect(facts, findsOneWidget);
    expect(tester.widget<Card>(facts).color, isNull,
        reason: 'Existing lavender theme/card surface must be unchanged');
    expect(find.text('In breve'), findsOneWidget);
    expect(find.text('1989'), findsOneWidget);
    expect(find.textContaining('novembre'), findsWidgets);
    expect(tester.takeException(), isNull);

    await tester.scrollUntilVisible(
      find.textContaining('E se una parte'),
      220,
      scrollable: find.byType(Scrollable).last,
    );
    expect(find.textContaining('E se una parte'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('unknown establishment is shown as *, never invented',
      (tester) async {
    final snapshot = await const CatalogRepository().load();
    final record = snapshot.byId['world-habitat-day']!;
    final controller = await buildLoadedTestController(catalog: snapshot);
    addTearDown(controller.dispose);

    await tester.pumpWidget(wrapTestApp(
      ObservanceDetailPage(observance: record, controller: controller),
      locale: const Locale('it'),
    ));
    await tester.pumpAndSettle();

    expect(find.text('In breve'), findsOneWidget);
    expect(find.text('*'), findsOneWidget);
    expect(find.textContaining("L'anno di istituzione"), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('facts card survives small phone and 200 percent text scale',
      (tester) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1;
    tester.platformDispatcher.textScaleFactorTestValue = 2;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);

    final snapshot = await const CatalogRepository().load();
    final record = snapshot.byId['africa-industrialization-day']!;
    final controller = await buildLoadedTestController(catalog: snapshot);
    addTearDown(controller.dispose);

    await tester.pumpWidget(wrapTestApp(
      ObservanceDetailPage(observance: record, controller: controller),
      locale: const Locale('it'),
    ));
    await tester.pumpAndSettle();

    expect(find.byKey(const ValueKey<String>('detail-facts-card')),
        findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
