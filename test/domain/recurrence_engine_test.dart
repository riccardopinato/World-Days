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
    const rule = OneOffRule(
      span: DateSpan(
        start: DateTime.utc(2026, 12, 31),
        end: DateTime.utc(2027, 1, 2),
      ),
    );
    expect(starts(2026, const [rule]), ['2026-12-31']);
    expect(starts(2027, const [rule]), ['2026-12-31']);
    expect(starts(2028, const [rule]), isEmpty);
    expect(
      RecurrenceEngine.resolve(year: 2028, rules: const [rule]).resolved,
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
