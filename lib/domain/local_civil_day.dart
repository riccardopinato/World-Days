import 'golden_civil_date.dart';

/// Local date-only arithmetic: an elapsed 24 hours is not always a civil day.
abstract final class LocalCivilDay {
  static DateTime start(DateTime value) =>
      DateTime(value.year, value.month, value.day);

  /// Move by calendar days, preserving midnight across 23h/25h DST days.
  static DateTime add(DateTime value, int days) =>
      DateTime(value.year, value.month, value.day + days);

  static DateTime nextMidnight(DateTime now) => add(now, 1);

  static DateTime at(DateTime day, int hour, int minute) =>
      DateTime(day.year, day.month, day.day, hour, minute);

  static String key(DateTime value) =>
      CivilDate.fromDateTime(value).toString();
}
