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
      'CA': 32,
      'AU': 3,
      'BR': 3,
      'MX': 3,
      'IN': 2,
      'JP': 3,
      'CZ': 25,
      'SK': 29,
      'NO': 10,
      'FI': 20,
      'SE': 10,
      'PL': 18,
      'IE': 2,
      'NL': 2,
      'ZA': 6,
      'PH': 201,
      'NZ': 3,
      'SG': 2,
      'KR': 57,
      'AR': 8,
      'PE': 7,
      'MT': 8,
      'HR': 4,
      'CY': 4,
      'EE': 17,
      'LV': 5,
      'LT': 6,
      'IS': 3,
      'LU': 1,
      'CU': 1,
      'HT': 1,
      'SD': 1,
      'MM': 1,
      'NR': 1,
      'LK': 1,
      'GD': 1,
      'IR': 1,
      'RS': 1,
      'GM': 1,
      'LC': 1,
      'BN': 1,
      'GY': 1,
      'KW': 1,
      'DO': 1,
      'BG': 1,
      'GH': 1,
      'MU': 1,
      'TN': 1,
      'NA': 1,
      'PK': 1,
      'GR': 1,
      'BD': 1,
      'SN': 1,
      'ZW': 1,
      'TZ': 1,
      'SL': 1,
      'TG': 1,
      'MH': 1,
      'PY': 1,
      'CM': 1,
      'TL': 1,
      'YE': 1,
      'EC': 1,
      'ER': 1,
      'JO': 1,
      'GE': 1,
      'AZ': 1,
      'ET': 1,
      'WS': 1,
      'RU': 1,
      'SC': 1,
      'MZ': 1,
      'SI': 1,
      'MG': 1,
      'DJ': 1,
      'CD': 1,
      'BI': 1,
      'SO': 1,
      'BY': 1,
      'CV': 1,
      'RW': 1,
      'VE': 1,
      'KM': 1,
      'MW': 1,
      'SB': 1,
      'SS': 1,
      'BS': 1,
      'MN': 1,
      'KI': 1,
      'ST': 1,
      'ME': 1,
      'CO': 1,
      'BE': 1,
      'EG': 1,
      'LR': 1,
      'MV': 1,
      'MA': 1,
      'VU': 1,
      'BJ': 1,
      'CH': 1,
      'CK': 1,
      'BO': 1,
      'JM': 1,
      'CI': 1,
      'TD': 1,
      'CG': 1,
      'LI': 1,
      'GA': 1,
      'ID': 1,
      'AF': 1,
      'HU': 1,
      'UA': 1,
      'UY': 1,
      'MD': 1,
      'KG': 1,
      'MY': 1,
      'TT': 1,
      'UZ': 1,
      'VN': 1,
      'SM': 1,
      'SZ': 1,
      'AD': 1,
      'MK': 1,
      'KP': 1,
      'TJ': 1,
      'CR': 1,
      'SV': 1,
      'GT': 1,
      'HN': 1,
      'NI': 1,
      'PG': 1,
      'CL': 1,
      'KN': 1,
      'NP': 1,
      'AM': 1,
      'BZ': 1,
      'ML': 1,
      'SA': 1,
      'GW': 1,
      'TM': 1,
      'BW': 1,
      'CN': 1,
      'GN': 1,
      'NG': 1,
      'PW': 1,
      'TV': 1,
      'IQ': 1,
      'LS': 1,
      'UG': 1,
      'FJ': 1,
      'GQ': 1,
      'NU': 1,
      'ZM': 1,
      'KZ': 1,
      'AT': 1,
      'VC': 1,
      'TR': 1,
      'DZ': 1,
      'AG': 1,
      'DM': 1,
      'FM': 1,
      'PA': 1,
      'TO': 1,
      'KH': 1,
      'AO': 1,
      'OM': 1,
      'MC': 1,
      'LB': 1,
      'BA': 1,
      'SR': 1,
      'AL': 1,
      'MR': 1,
      'BB': 1,
      'CF': 1,
      'RO': 1,
      'LA': 1,
      'AE': 1,
      'TH': 1,
      'BF': 1,
      'KE': 1,
      'BH': 1,
      'BT': 1,
      'NE': 1,
      'QA': 1,
      'LY': 1,
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
    for (final country in <String>['IT', 'ES', 'FR', 'DE', 'PT', 'GB', 'US', 'CA', 'AU', 'BR', 'MX', 'IN', 'JP', 'CZ', 'SK', 'NO', 'FI', 'SE', 'PL', 'IE', 'NL', 'ZA', 'PH', 'NZ', 'SG', 'KR', 'AR', 'PE', 'MT', 'HR', 'CY', 'EE', 'LV', 'LT', 'IS', 'LU', 'CU', 'HT', 'SD', 'MM', 'NR', 'LK', 'GD', 'IR', 'RS', 'GM', 'LC', 'BN', 'GY', 'KW', 'DO', 'BG', 'GH', 'MU', 'TN', 'NA', 'PK', 'GR', 'BD', 'SN', 'ZW', 'TZ', 'SL', 'TG', 'MH', 'PY', 'CM', 'TL', 'YE', 'EC', 'ER', 'JO', 'GE', 'AZ', 'ET', 'WS', 'RU', 'SC', 'MZ', 'SI', 'MG', 'DJ', 'CD', 'BI', 'SO', 'BY', 'CV', 'RW', 'VE', 'KM', 'MW', 'SB', 'SS', 'BS', 'MN', 'KI', 'ST', 'ME', 'CO', 'BE', 'EG', 'LR', 'MV', 'MA', 'VU', 'BJ', 'CH', 'CK', 'BO', 'JM', 'CI', 'TD', 'CG', 'LI', 'GA', 'ID', 'AF', 'HU', 'UA', 'UY', 'MD', 'KG', 'MY', 'TT', 'UZ', 'VN', 'SM', 'SZ', 'AD', 'MK', 'KP', 'TJ', 'CR', 'SV', 'GT', 'HN', 'NI', 'PG', 'CL', 'KN', 'NP', 'AM', 'BZ', 'ML', 'SA', 'GW', 'TM', 'BW', 'CN', 'GN', 'NG', 'PW', 'TV', 'IQ', 'LS', 'UG', 'FJ', 'GQ', 'NU', 'ZM', 'KZ', 'AT', 'VC', 'TR', 'DZ', 'AG', 'DM', 'FM', 'PA', 'TO', 'KH', 'AO', 'OM', 'MC', 'LB', 'BA', 'SR', 'AL', 'MR', 'BB', 'CF', 'RO', 'LA', 'AE', 'TH', 'BF', 'KE', 'BH', 'BT', 'NE', 'QA', 'LY']) {
      final national = controller.recordsForMarket(country);
      final all = controller.recordsForMarket(country, includeGlobal: true);
      expect(all.length, national.length + global.length, reason: country);
      expect(all.map((x) => x.id).toSet().length, all.length);
      expect(all.where((x) => x.scope == 'NATIONAL').length, national.length);
    }
    expect(controller.catalog!.records.length, 1111);
    // initialize() may have an unawaited remote update probe; do not dispose
    // this controller during the current test zone while that probe runs.
  });

  test('every market dropdown option can be persisted, unsupported code rejected', () async {
    final controller = await _controller();
    for (final code in <String>['CA', 'CZ', 'NL', 'MT', 'HR', 'CY', 'EE', 'LV', 'LT', 'IS', 'LU']) {
      await controller.setMarket(code);
      expect(controller.preferences.marketCode, code);
      expect(controller.recordsForMarket(code), isNotEmpty);
    }
    await expectLater(controller.setMarket('XX'), throwsArgumentError);
    // Remote-content pack and native device certification are separate gates.
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
