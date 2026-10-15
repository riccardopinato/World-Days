import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/core/notifications/reminder_plan.dart';
import 'package:world_days/core/retention/retention_target.dart';
import 'package:world_days/core/widget/world_days_home_widget_service.dart';
import 'package:world_days/data/preferences_repository.dart';
import 'package:world_days/domain/observance.dart';

const _authority = ObservanceAuthority(
  name: 'Test Authority',
  type: 'TEST',
  officiality: 'POPULAR',
);

const _planet = Observance(
  id: 'planet-day',
  title: 'Planet Day',
  periodKind: 'DAY',
  scope: 'GLOBAL',
  countries: [],
  regions: [],
  authority: _authority,
  sources: [],
  rules: [],
  aliases: [],
  categories: ['PLANET'],
  localizedTitles: {
    'it': 'Giornata del pianeta',
  },
  visualKey: 'planet',
);

const _health = Observance(
  id: 'health-day',
  title: 'Health Day',
  periodKind: 'DAY',
  scope: 'GLOBAL',
  countries: [],
  regions: [],
  authority: _authority,
  sources: [],
  rules: [],
  aliases: [],
  categories: ['HEALTH'],
  localizedTitles: {
    'it': 'Giornata della salute',
  },
  visualKey: 'health',
);

void main() {
  test('reminder preferences remain backward compatible and bounded', () {
    final preferences = ReminderPreferences.fromJson({
      'dailyEnabled': true,
      'dailyHour': 99,
      'dailyMinute': -8,
      'weeklyWeekday': 12,
      'favoriteEnabled': true,
      'followedVisualKeys': ['planet', 'health'],
    });

    expect(preferences.dailyEnabled, isTrue);
    expect(preferences.dailyHour, 23);
    expect(preferences.dailyMinute, 0);
    expect(preferences.weeklyWeekday, DateTime.sunday);
    expect(preferences.favoriteEnabled, isTrue);
    expect(preferences.followedCategories, {'PLANET', 'HEALTH'});

    final roundTrip = ReminderPreferences.fromJson(preferences.toJson());
    expect(roundTrip.toJson(), preferences.toJson());
  });

  test('retention target parses notification payloads and widget URIs', () {
    expect(
      RetentionTarget.fromPayload('tab:today')?.tab,
      RetentionTab.today,
    );
    expect(
      RetentionTarget.fromPayload('tab:calendar')?.tab,
      RetentionTab.calendar,
    );
    expect(
      RetentionTarget.fromPayload('observance:planet-day')?.observanceId,
      'planet-day',
    );
    expect(
      RetentionTarget.fromWidgetUri(
        Uri.parse('worlddays://observance/planet-day'),
      )?.observanceId,
      'planet-day',
    );
    expect(
      RetentionTarget.fromWidgetUri(
        Uri.parse('worlddays://today'),
      )?.tab,
      RetentionTab.today,
    );
    expect(RetentionTarget.fromPayload('unknown'), isNull);
  });

  test('reminder plan is finite, stable and localized', () {
    final now = DateTime(2026, 10, 14, 8);
    final settings = const ReminderPreferences(
      dailyEnabled: true,
      dailyHour: 9,
      dailyMinute: 0,
      weeklyEnabled: true,
      weeklyWeekday: DateTime.sunday,
      weeklyHour: 18,
      weeklyMinute: 0,
      favoriteEnabled: true,
      categoryEnabled: true,
      followedCategories: {'PLANET'},
    );

    List<Observance> recordsForDate(DateTime date) {
      if (date.year == 2026 && date.month == 10 && date.day == 15) {
        return const [_planet];
      }
      if (date.weekday == DateTime.monday) {
        return const [_planet];
      }
      if (date.year == 2026 && date.month == 10 && date.day == 16) {
        return const [_health];
      }
      return const [];
    }

    final plan = ReminderPlanBuilder.build(
      settings: settings,
      favoriteIds: const {'planet-day'},
      localeCode: 'it',
      observancesForDate: recordsForDate,
      now: now,
    );

    expect(plan.where((item) => item.stableId.startsWith('daily:')), hasLength(22));
    expect(plan.where((item) => item.stableId.startsWith('weekly:')), hasLength(6));
    expect(plan.where((item) => item.stableId.startsWith('favorite:')), hasLength(1));
    expect(plan.where((item) => item.stableId.startsWith('category:')), hasLength(10));
    expect(plan.length, 39);
    expect(plan.length, lessThan(50));
    expect(plan.map((item) => item.stableId).toSet(), hasLength(plan.length));
    expect(plan.every((item) => item.when.isAfter(now)), isTrue);
    final rollingFallback = plan.singleWhere(
      (item) => item.stableId == 'daily:rolling-fallback',
    );
    expect(rollingFallback.repeatDaily, isTrue);
    expect(rollingFallback.payload, 'tab:today');

    final favorite = plan.singleWhere(
      (item) => item.stableId.startsWith('favorite:'),
    );
    expect(favorite.title, 'Giornata del pianeta');
    expect(favorite.payload, 'observance:planet-day');
  });

  test('home widget projection carries localized offline schedule', () {
    final projection = WorldDaysWidgetProjection.build(
      localeCode: 'it',
      now: DateTime(2026, 10, 15, 12),
      days: 2,
      observancesForDate: (date) => date.day == 15
          ? const [_planet]
          : const [],
    );

    expect(projection.keys, ['2026-10-15', '2026-10-16']);
    expect(projection['2026-10-15']?['title'], 'Giornata del pianeta');
    expect(projection['2026-10-15']?['id'], 'planet-day');
    expect(
      projection['2026-10-16']?['title'],
      'Nessuna ricorrenza verificata',
    );
  });
}
