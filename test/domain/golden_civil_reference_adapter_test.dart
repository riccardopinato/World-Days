import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/domain/golden_civil_date.dart' as golden;
import 'package:world_days/domain/recurrence_engine.dart';

void main() {
  test('consumer public API delegates the reference nth/last weekday for 3 years', () {
    for (final year in [2026, 2027, 2028]) {
      final first = RecurrenceEngine.resolve(
        year: year,
        rules: [const NthWeekdayRule(
          month: 7, weekday: DateTime.saturday, occurrence: 1)],
      ).spans.single.start;
      final expected = golden.CivilRecurrence
          .nthWeekday(year, 7, DateTime.saturday, 1).toUtcDateTime();
      expect(first, expected);

      final last = RecurrenceEngine.resolve(
        year: year,
        rules: [const LastWeekdayRule(
          month: 9, weekday: DateTime.thursday)],
      ).spans.single.start;
      expect(last, golden.CivilRecurrence
          .lastWeekday(year, 9, DateTime.thursday).toUtcDateTime());
    }
  });

  test('public API preserves leap-year last-day semantics', () {
    for (final year in [2027, 2028]) {
      final span = RecurrenceEngine.resolve(
        year: year, rules: [const LastDayOfMonthRule(month: 2)],
      ).spans.single;
      expect(span.start.day, golden.CivilDate.daysInMonth(year, 2));
      expect(span.end, span.start);
    }
  });

  test('consumer preserves unresolved lunar and one-off crossing year', () {
    final missing = RecurrenceEngine.resolve(
      year: 2027, rules: [const LunarRule(overrides: {})],
    );
    expect(missing.resolved, isFalse);
    final range = DateSpan(
      start: DateTime.utc(2026, 12, 31),
      end: DateTime.utc(2027, 1, 2),
    );
    final current = RecurrenceEngine.resolve(
      year: 2027, rules: [OneOffRule(span: range)],
    );
    expect(current.spans.single.start, DateTime.utc(2026, 12, 31));
  });

  test('invalid civil date is rejected before misleading occurrences', () {
    expect(() => RecurrenceEngine.resolve(
      year: 2027,
      rules: [const FixedDateRule(month: 2, day: 29)],
    ), throwsArgumentError);
  });
}
