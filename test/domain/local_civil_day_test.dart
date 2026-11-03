import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/domain/local_civil_day.dart';

void main() {
  test('calendar-day arithmetic handles DST, new year and leap day', () {
    for (final pair in [
      (DateTime(2026, 3, 28), '2026-03-29'),
      (DateTime(2026, 3, 29), '2026-03-30'),
      (DateTime(2026, 10, 24), '2026-10-25'),
      (DateTime(2026, 10, 25), '2026-10-26'),
      (DateTime(2026, 12, 31), '2027-01-01'),
      (DateTime(2028, 2, 28), '2028-02-29'),
      (DateTime(2028, 2, 29), '2028-03-01'),
    ]) {
      expect(LocalCivilDay.key(LocalCivilDay.add(pair.$1, 1)), pair.$2);
    }
    expect(LocalCivilDay.key(LocalCivilDay.add(DateTime(2026, 1, 1), -1)),
        '2025-12-31');
  });

  test('next midnight is 23h or 25h away across Rome DST', () {
    for (final day in [DateTime(2026, 3, 29), DateTime(2026, 10, 25)]) {
      final next = LocalCivilDay.nextMidnight(day);
      expect(next.hour, 0);
      expect(LocalCivilDay.key(next),
          LocalCivilDay.key(LocalCivilDay.add(day, 1)));
    }
    if (Platform.environment['TZ'] == 'Europe/Rome') {
      final spring = DateTime(2026, 3, 29);
      final autumn = DateTime(2026, 10, 25);
      expect(LocalCivilDay.nextMidnight(spring).difference(spring),
          const Duration(hours: 23));
      expect(LocalCivilDay.nextMidnight(autumn).difference(autumn),
          const Duration(hours: 25));
      expect(LocalCivilDay.key(autumn.add(const Duration(days: 1))),
          '2026-10-25');
    }
  });

  test('reminder wall-clock hour stays stable across transitions', () {
    for (final date in [
      DateTime(2026, 3, 28), DateTime(2026, 3, 29),
      DateTime(2026, 3, 30), DateTime(2026, 10, 24),
      DateTime(2026, 10, 25), DateTime(2026, 10, 26),
    ]) {
      final atNine = LocalCivilDay.at(date, 9, 15);
      expect((atNine.hour, atNine.minute), (9, 15));
      expect(LocalCivilDay.key(atNine), LocalCivilDay.key(date));
    }
  });
}
