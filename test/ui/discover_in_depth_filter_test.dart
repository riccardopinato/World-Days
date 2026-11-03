import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/data/catalog_repository.dart';
import 'package:world_days/features/discover/discover_page.dart';
import 'package:world_days/l10n/app_localizations.dart';

import '../support/world_days_test_support.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late CatalogSnapshot snapshot;
  setUpAll(() async {
    snapshot = await const CatalogRepository().load();
  });

  testWidgets('Italian Discover filter shows only reviewed in-depth stories',
      (tester) async {
    final controller = await buildLoadedTestController(catalog: snapshot);
    addTearDown(controller.dispose);

    await tester.pumpWidget(
      wrapTestApp(
        DiscoverPage(controller: controller),
        locale: const Locale('it'),
      ),
    );
    await tester.pump(const Duration(milliseconds: 200));

    final chip = find.byKey(
      const ValueKey<String>('discover-in-depth-filter'),
    );
    expect(chip, findsOneWidget);
    expect(find.text('Storie approfondite'), findsOneWidget);
    expect(tester.widget<FilterChip>(chip).selected, isFalse);

    final candidates = controller.search('');
    final count = candidates
        .where((record) => snapshot.editorialById.containsKey(record.id))
        .length;
    final observances = AppLocalizations.of(tester.element(chip)).observances;

    await tester.ensureVisible(chip);
    await tester.tap(chip);
    await tester.pump(const Duration(milliseconds: 200));

    expect(tester.widget<FilterChip>(chip).selected, isTrue);
    expect(find.text('$count $observances'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
