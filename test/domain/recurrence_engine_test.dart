import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/domain/recurrence_engine.dart';

String iso(DateTime value) =>
    '${value.year.toString().padLeft(4, '0')}-${value.month.toString().padLeft(2, '0')}-${value.day.toString().padLeft(2, '0')}';

List<String> starts(int year, List<RecurrenceRule> rules) =>
    RecurrenceEngine.resolve(year: year, rules: rules)
        .spans
        .map((span) => iso(span.start))
        .toList(growable: false);

void main() {
  test('Iceland First Day of Summer is Thursday April 19–25, not always fourth Thursday', () {
    const rule = WeekdayOnOrAfterRule(
      month: 4,
      day: 19,
      weekday: DateTime.thursday,
    );
    expect(starts(2026, const [rule]), ['2026-04-23']);
    expect(starts(2027, const [rule]), ['2027-04-22']);
    expect(starts(2028, const [rule]), ['2028-04-20']);
    expect(starts(2029, const [rule]), ['2029-04-19']);
  });

  test('Irish 2023 St Brigid public holiday moves and has Friday exception', () {
    const rule = FirstMondayExceptFeb1FridayRule();
    final dates = <int, String>{
      2026: '2026-02-02',
      2027: '2027-02-01',
      2028: '2028-02-07',
      2029: '2029-02-05',
      2030: '2030-02-01',
      2031: '2031-02-03',
    };
    for (final entry in dates.entries) {
      expect(starts(entry.key, const [rule]), [entry.value],
          reason: 'Irish primary holiday rule for ${entry.key}');
    }
    // The separate traditional commemoration remains fixed on 1 February.
    expect(starts(2028, const [FixedDateRule(month: 2, day: 1)]),
        ['2028-02-01']);
  });

  test('International Day of Cooperatives = first Saturday of July', () {
    const rule = NthWeekdayRule(
      month: 7,
      weekday: DateTime.saturday,
      occurrence: 1,
    );
    expect(starts(2026, const [rule]), ['2026-07-04']);
    expect(starts(2027, const [rule]), ['2027-07-03']);
    expect(starts(2028, const [rule]), ['2028-07-01']);
  });

  test('World Habitat Day = first Monday of October', () {
    const rule = NthWeekdayRule(
      month: 10,
      weekday: DateTime.monday,
      occurrence: 1,
    );
    expect(starts(2026, const [rule]), ['2026-10-05']);
    expect(starts(2027, const [rule]), ['2027-10-04']);
    expect(starts(2028, const [rule]), ['2028-10-02']);
  });

  test('World Maritime Day = last Thursday of September', () {
    const rule = LastWeekdayRule(month: 9, weekday: DateTime.thursday);
    expect(starts(2026, const [rule]), ['2026-09-24']);
    expect(starts(2027, const [rule]), ['2027-09-30']);
    expect(starts(2028, const [rule]), ['2028-09-28']);
  });

  test('Last day of month resolves leap years correctly', () {
    const rule = LastDayOfMonthRule(month: 2);
    expect(starts(2027, const [rule]), ['2027-02-28']);
    expect(starts(2028, const [rule]), ['2028-02-29']);
  });

  test('One-off rules resolve only for overlapping years', () {
    final rule = OneOffRule(
      span: DateSpan(
        start: DateTime.utc(2026, 12, 31),
        end: DateTime.utc(2027, 1, 2),
      ),
    );
    expect(starts(2026, [rule]), ['2026-12-31']);
    expect(starts(2027, [rule]), ['2026-12-31']);
    expect(starts(2028, [rule]), isEmpty);
    expect(
      RecurrenceEngine.resolve(year: 2028, rules: [rule]).resolved,
      isTrue,
    );
  });

  test('Lunar rule remains unresolved without a trusted yearly override', () {
    const rule = LunarRule(overrides: {});
    final result = RecurrenceEngine.resolve(year: 2027, rules: const [rule]);
    expect(result.resolved, isFalse);
    expect(result.spans, isEmpty);
  });
}
