import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/data/catalog_repository.dart';
import 'package:world_days/domain/recurrence_engine.dart';

String iso(DateTime d) => '${d.year.toString().padLeft(4, '0')}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('Irish statutory St Brigid holiday observes Monday and Friday exception; cultural day unchanged', () async {
    final catalog = await const CatalogRepository().load();
    final public = catalog.byId['ie-w13-eures-st-brigid-s-day']!;
    final cultural = catalog.byId['ie-st-brigids-day']!;

    expect(public.countries, ['IE']);
    expect(public.introducedYear, 2023);
    expect(public.sources.first.url,
      'https://www.workplacerelations.ie/en/what_you_should_know/public-holidays/');
    expect(public.authority.officiality, 'OFFICIAL_INSTITUTIONAL');
    expect(public.rules.single, isA<AuthorityDefinedRule>());

    const dates = <int, String>{
      2026: '2026-02-02',
      2027: '2027-02-01',
      2028: '2028-02-07',
      2029: '2029-02-05',
      2030: '2030-02-01',
      2035: '2035-02-05',
    };
    for (final entry in dates.entries) {
      final observed = RecurrenceEngine.resolve(
        year: entry.key, rules: public.rules);
      expect(observed.resolved, isTrue);
      expect(observed.spans, hasLength(1));
      expect(iso(observed.spans.single.start), entry.value);
      final historical = RecurrenceEngine.resolve(
        year: entry.key, rules: cultural.rules);
      expect(historical.resolved, isTrue);
      expect(iso(historical.spans.single.start),
        '${entry.key}-02-01');
    }

    for (var year = 2023; year <= 2100; year++) {
      final result = RecurrenceEngine.resolve(year: year, rules: public.rules);
      expect(result.resolved, isTrue, reason: 'year $year');
      expect(result.spans, hasLength(1));
      final day = result.spans.single.start;
      final fridayFirst = DateTime.utc(year, 2, 1).weekday == DateTime.friday;
      expect(day.weekday, fridayFirst ? DateTime.friday : DateTime.monday,
        reason: 'year $year');
      expect(day.day, fridayFirst ? 1 : inInclusiveRange(1, 7),
        reason: 'year $year');
    }

    final beyond = RecurrenceEngine.resolve(year: 2101, rules: public.rules);
    expect(beyond.resolved, isFalse);
    expect(beyond.spans, isEmpty);
  });
}
