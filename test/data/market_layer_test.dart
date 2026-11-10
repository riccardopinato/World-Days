import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:world_days/app/app_controller.dart';

Future<AppController> _controller() async {
  SharedPreferences.setMockInitialValues({});
  final controller = AppController();
  await controller.initialize();
  return controller;
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('launch markets expose only their national layer', () async {
    final controller = await _controller();

    final expected = <String, int>{
      'IT': 25,
      'ES': 8,
      'FR': 9,
      'DE': 4,
      'PT': 9,
      'GB': 8,
      'US': 9,
      'CA': 5,
      'AU': 3,
      'BR': 3,
      'MX': 3,
      'IN': 2,
      'JP': 3,
      'CZ': 7,
      'SK': 6,
      'NO': 5,
      'FI': 15,
      'SE': 1,
      'PL': 5,
      'IE': 2,
      'NL': 2,
      'ZA': 6,
      'PH': 7,
      'NZ': 3,
      'SG': 2,
      'KR': 7,
      'AR': 8,
      'PE': 7,
      'MT': 8,
      'HR': 4,
      'CY': 4,
    };

    for (final entry in expected.entries) {
      final records = controller.recordsForMarket(entry.key);
      expect(records, hasLength(entry.value), reason: entry.key);
      expect(
        records.every(
          (record) =>
              record.scope == 'NATIONAL' &&
              record.countries.length == 1 &&
              record.countries.single == entry.key,
        ),
        isTrue,
        reason: entry.key,
      );
    }
  });

  test('each country also has the shared global layer without false national authority', () async {
    final controller = await _controller();
    final global = controller.recordsForMarket('GLOBAL', includeGlobal: true);
    expect(global, hasLength(289));
    expect(global.every((item) => item.scope == 'GLOBAL'), isTrue);
    for (final country in <String>['IT', 'ES', 'FR', 'DE', 'PT', 'GB', 'US', 'CA', 'AU', 'BR', 'MX', 'IN', 'JP', 'CZ', 'SK', 'NO', 'FI', 'SE', 'PL', 'IE', 'NL', 'ZA', 'PH', 'NZ', 'SG', 'KR', 'AR', 'PE', 'MT', 'HR', 'CY']) {
      final national = controller.recordsForMarket(country);
      final all = controller.recordsForMarket(country, includeGlobal: true);
      expect(all.length, national.length + global.length, reason: country);
      expect(all.map((x) => x.id).toSet().length, all.length);
      expect(all.where((x) => x.scope == 'NATIONAL').length, national.length);
    }
    expect(controller.catalog!.records.length, 479);
    // initialize() may have an unawaited remote update probe; do not dispose
    // this controller during the current test zone while that probe runs.
  });

  test('market and locale preferences remain independent', () async {
    final controller = await _controller();

    await controller.setLocale('it');
    await controller.setMarket('US');

    expect(controller.preferences.localeCode, 'it');
    expect(controller.preferences.marketCode, 'US');

    final mlk = controller.catalog!.byId['martin-luther-king-jr-day']!;
    final italy = controller.catalog!.byId['italian-republic-day']!;
    final global = controller.catalog!.byId['world-braille-day']!;

    expect(controller.isVisibleForMarket(mlk), isTrue);
    expect(controller.isVisibleForMarket(italy), isFalse);
    expect(controller.isVisibleForMarket(global), isTrue);

    await controller.setMarket('IT');

    expect(controller.preferences.localeCode, 'it');
    expect(controller.preferences.marketCode, 'IT');
    expect(controller.isVisibleForMarket(mlk), isFalse);
    expect(controller.isVisibleForMarket(italy), isTrue);
    expect(controller.isVisibleForMarket(global), isTrue);
  });

  test('global market hides national records from normal discovery', () async {
    final controller = await _controller();

    expect(controller.preferences.marketCode, 'GLOBAL');
    expect(controller.search('Martin Luther King'), isEmpty);
    expect(controller.search('World Braille Day'), isNotEmpty);

    await controller.setMarket('US');

    expect(
      controller.search('Martin Luther King').map((item) => item.id),
      contains('martin-luther-king-jr-day'),
    );
  });
}
