import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/data/preferences_repository.dart';

void main() {
  test('retention preferences round-trip without coupling locale and market', () {
    const original = UserPreferences(
      favoriteIds: {'world-water-day'},
      recentIds: ['world-water-day'],
      themeMode: ThemeMode.dark,
      localeCode: 'it',
      marketCode: 'US',
      dailyReminderEnabled: true,
      dailyReminderHour: 7,
      dailyReminderMinute: 45,
      weeklyDigestEnabled: true,
      favoriteReminderIds: {'world-water-day'},
      followedCategories: {'Health', 'Environment'},
      streak: 9,
      lastOpenDate: '2026-10-12',
    );

    final restored = UserPreferences.fromJson(original.toJson());

    expect(restored.localeCode, 'it');
    expect(restored.marketCode, 'US');
    expect(restored.dailyReminderEnabled, isTrue);
    expect(restored.dailyReminderHour, 7);
    expect(restored.dailyReminderMinute, 45);
    expect(restored.weeklyDigestEnabled, isTrue);
    expect(restored.favoriteReminderIds, {'world-water-day'});
    expect(restored.followedCategories, {'Health', 'Environment'});
    expect(restored.streak, 9);
  });

  test('legacy preference payload gets safe retention defaults', () {
    final restored = UserPreferences.fromJson({
      'favoriteIds': <String>[],
      'recentIds': <String>[],
      'themeMode': 'system',
      'localeCode': 'fr',
      'marketCode': 'FR',
    });

    expect(restored.dailyReminderEnabled, isFalse);
    expect(restored.dailyReminderHour, 8);
    expect(restored.dailyReminderMinute, 0);
    expect(restored.weeklyDigestEnabled, isFalse);
    expect(restored.favoriteReminderIds, isEmpty);
    expect(restored.followedCategories, isEmpty);
  });
}
