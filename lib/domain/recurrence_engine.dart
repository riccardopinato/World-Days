import 'golden_civil_date.dart' as golden;

enum RecurrenceKind {
  fixedDate,
  nthWeekday,
  firstMondayExceptFeb1Friday,
  weekdayOnOrAfter,
  lastWeekday,
  lastDayOfMonth,
  fixedRange,
  authorityDefined,
  lunar,
  oneOff,
}

final class DateSpan implements Comparable<DateSpan> {
  const DateSpan({required this.start, required this.end});

  final DateTime start;
  final DateTime end;

  bool contains(DateTime date) {
    final day = DateTime.utc(date.year, date.month, date.day);
    return !day.isBefore(start) && !day.isAfter(end);
  }

  @override
  int compareTo(DateSpan other) => start.compareTo(other.start);

  @override
  bool operator ==(Object other) =>
      other is DateSpan && other.start == start && other.end == end;

  @override
  int get hashCode => Object.hash(start, end);
}

sealed class RecurrenceRule {
  const RecurrenceRule(this.kind);
  final RecurrenceKind kind;
}

final class FixedDateRule extends RecurrenceRule {
  const FixedDateRule({required this.month, required this.day})
      : super(RecurrenceKind.fixedDate);
  final int month;
  final int day;
}

final class NthWeekdayRule extends RecurrenceRule {
  const NthWeekdayRule({
    required this.month,
    required this.weekday,
    required this.occurrence,
  })  : assert(occurrence >= 1 && occurrence <= 5),
        super(RecurrenceKind.nthWeekday);
  final int month;
  final int weekday;
  final int occurrence;
}

/// Irish St Brigid public-holiday rule: first Monday in February unless Feb 1 is Friday.
final class FirstMondayExceptFeb1FridayRule extends RecurrenceRule {
  const FirstMondayExceptFeb1FridayRule()
      : super(RecurrenceKind.firstMondayExceptFeb1Friday);
}

/// First ISO weekday on or after a fixed day of month (e.g. Iceland summer).
final class WeekdayOnOrAfterRule extends RecurrenceRule {
  const WeekdayOnOrAfterRule({
    required this.month,
    required this.day,
    required this.weekday,
  })  : assert(month >= 1 && month <= 12),
        assert(day >= 1 && day <= 24),
        assert(weekday >= 1 && weekday <= 7),
        super(RecurrenceKind.weekdayOnOrAfter);
  final int month;
  final int day;
  final int weekday;
}

final class LastWeekdayRule extends RecurrenceRule {
  const LastWeekdayRule({required this.month, required this.weekday})
      : super(RecurrenceKind.lastWeekday);
  final int month;
  final int weekday;
}

final class LastDayOfMonthRule extends RecurrenceRule {
  const LastDayOfMonthRule({required this.month})
      : super(RecurrenceKind.lastDayOfMonth);

  final int month;
}

final class FixedRangeRule extends RecurrenceRule {
  const FixedRangeRule({
    required this.startMonth,
    required this.startDay,
    required this.endMonth,
    required this.endDay,
  }) : super(RecurrenceKind.fixedRange);
  final int startMonth;
  final int startDay;
  final int endMonth;
  final int endDay;
}

final class AuthorityDefinedRule extends RecurrenceRule {
  const AuthorityDefinedRule({required this.overrides})
      : super(RecurrenceKind.authorityDefined);
  final Map<int, DateSpan> overrides;
}

final class LunarRule extends RecurrenceRule {
  const LunarRule({required this.overrides}) : super(RecurrenceKind.lunar);
  final Map<int, DateSpan> overrides;
}

final class OneOffRule extends RecurrenceRule {
  const OneOffRule({required this.span}) : super(RecurrenceKind.oneOff);

  final DateSpan span;
}

final class RecurrenceResolution {
  const RecurrenceResolution({required this.spans, required this.resolved});
  final List<DateSpan> spans;
  final bool resolved;
}

abstract final class RecurrenceEngine {
  static RecurrenceResolution resolve({
    required int year,
    required List<RecurrenceRule> rules,
  }) {
    final spans = <DateSpan>[];
    var resolved = true;

    for (final rule in rules) {
      if (rule is OneOffRule) {
        if (_overlapsYear(rule.span, year)) spans.add(rule.span);
        continue;
      }

      final span = _resolveOne(year, rule);
      if (span == null) {
        resolved = false;
      } else {
        spans.add(span);
      }
    }

    spans.sort();
    final seen = <String>{};
    final unique = <DateSpan>[];
    for (final span in spans) {
      final key =
          '${span.start.microsecondsSinceEpoch}:${span.end.microsecondsSinceEpoch}';
      if (seen.add(key)) unique.add(span);
    }

    return RecurrenceResolution(spans: unique, resolved: resolved);
  }

  static DateSpan? _resolveOne(int year, RecurrenceRule rule) {
    return switch (rule) {
      FixedDateRule r => _single(_checkedDate(year, r.month, r.day)),
      FirstMondayExceptFeb1FridayRule _ => _single(
          _irishBrigidHoliday(year),
        ),
      NthWeekdayRule r => _single(
          _nthWeekday(year, r.month, r.weekday, r.occurrence),
        ),
      WeekdayOnOrAfterRule r => _single(
          _weekdayOnOrAfter(year, r.month, r.day, r.weekday),
        ),
      LastWeekdayRule r => _single(
          _lastWeekday(year, r.month, r.weekday),
        ),
      LastDayOfMonthRule r => _single(
          DateTime.utc(year, r.month,
            golden.CivilDate.daysInMonth(year, r.month)),
        ),
      FixedRangeRule r => DateSpan(
          start: _checkedDate(year, r.startMonth, r.startDay),
          end: _checkedDate(
            r.endMonth < r.startMonth ? year + 1 : year,
            r.endMonth,
            r.endDay,
          ),
        ),
      AuthorityDefinedRule r => r.overrides[year],
      LunarRule r => r.overrides[year],
      OneOffRule _ => throw StateError('One-off rules are resolved separately'),
    };
  }

  static bool _overlapsYear(DateSpan span, int year) {
    final first = DateTime.utc(year, 1, 1);
    final last = DateTime.utc(year, 12, 31);
    return !span.end.isBefore(first) && !span.start.isAfter(last);
  }

  static DateTime _irishBrigidHoliday(int year) {
    final feb1 = _checkedDate(year, 2, 1);
    if (feb1.weekday == DateTime.friday) return feb1;
    final offset = (DateTime.monday - feb1.weekday + 7) % 7;
    return feb1.add(Duration(days: offset));
  }

  static DateTime _nthWeekday(
    int year, int month, int weekday, int occurrence,
  ) => golden.CivilRecurrence
      .nthWeekday(year, month, weekday, occurrence).toUtcDateTime();

  static DateTime _weekdayOnOrAfter(
    int year, int month, int day, int weekday,
  ) {
    final first = _checkedDate(year, month, day);
    final offset = (weekday - first.weekday + 7) % 7;
    return first.add(Duration(days: offset));
  }

  static DateTime _lastWeekday(int year, int month, int weekday) =>
      golden.CivilRecurrence.lastWeekday(year, month, weekday).toUtcDateTime();

  static DateTime _checkedDate(int year, int month, int day) =>
      golden.CivilDate(year, month, day).toUtcDateTime();

  static DateSpan _single(DateTime date) => DateSpan(start: date, end: date);
}
