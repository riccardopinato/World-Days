import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

final class ReminderPreferences {
  const ReminderPreferences({
    this.dailyEnabled = false,
    this.dailyHour = 9,
    this.dailyMinute = 0,
    this.weeklyEnabled = false,
    this.weeklyWeekday = DateTime.sunday,
    this.weeklyHour = 18,
    this.weeklyMinute = 0,
    this.favoriteEnabled = false,
    this.categoryEnabled = false,
    this.followedVisualKeys = const <String>{},
  });

  final bool dailyEnabled;
  final int dailyHour;
  final int dailyMinute;
  final bool weeklyEnabled;
  final int weeklyWeekday;
  final int weeklyHour;
  final int weeklyMinute;
  final bool favoriteEnabled;
  final bool categoryEnabled;
  final Set<String> followedVisualKeys;

  bool get anyEnabled =>
      dailyEnabled || weeklyEnabled || favoriteEnabled || categoryEnabled;

  ReminderPreferences copyWith({
    bool? dailyEnabled,
    int? dailyHour,
    int? dailyMinute,
    bool? weeklyEnabled,
    int? weeklyWeekday,
    int? weeklyHour,
    int? weeklyMinute,
    bool? favoriteEnabled,
    bool? categoryEnabled,
    Set<String>? followedVisualKeys,
  }) =>
      ReminderPreferences(
        dailyEnabled: dailyEnabled ?? this.dailyEnabled,
        dailyHour: dailyHour ?? this.dailyHour,
        dailyMinute: dailyMinute ?? this.dailyMinute,
        weeklyEnabled: weeklyEnabled ?? this.weeklyEnabled,
        weeklyWeekday: weeklyWeekday ?? this.weeklyWeekday,
        weeklyHour: weeklyHour ?? this.weeklyHour,
        weeklyMinute: weeklyMinute ?? this.weeklyMinute,
        favoriteEnabled: favoriteEnabled ?? this.favoriteEnabled,
        categoryEnabled: categoryEnabled ?? this.categoryEnabled,
        followedVisualKeys: followedVisualKeys ?? this.followedVisualKeys,
      );

  Map<String, dynamic> toJson() => {
        'dailyEnabled': dailyEnabled,
        'dailyHour': dailyHour,
        'dailyMinute': dailyMinute,
        'weeklyEnabled': weeklyEnabled,
        'weeklyWeekday': weeklyWeekday,
        'weeklyHour': weeklyHour,
        'weeklyMinute': weeklyMinute,
        'favoriteEnabled': favoriteEnabled,
        'categoryEnabled': categoryEnabled,
        'followedVisualKeys': followedVisualKeys.toList()..sort(),
      };

  factory ReminderPreferences.fromJson(Map<String, dynamic> json) =>
      ReminderPreferences(
        dailyEnabled: json['dailyEnabled'] == true,
        dailyHour: _boundedInt(json['dailyHour'], 9, 0, 23),
        dailyMinute: _boundedInt(json['dailyMinute'], 0, 0, 59),
        weeklyEnabled: json['weeklyEnabled'] == true,
        weeklyWeekday: _boundedInt(
          json['weeklyWeekday'],
          DateTime.sunday,
          DateTime.monday,
          DateTime.sunday,
        ),
        weeklyHour: _boundedInt(json['weeklyHour'], 18, 0, 23),
        weeklyMinute: _boundedInt(json['weeklyMinute'], 0, 0, 59),
        favoriteEnabled: json['favoriteEnabled'] == true,
        categoryEnabled: json['categoryEnabled'] == true,
        followedVisualKeys:
            ((json['followedVisualKeys'] as List?) ?? const [])
                .map((e) => e.toString())
                .toSet(),
      );

  static int _boundedInt(
    Object? value,
    int fallback,
    int min,
    int max,
  ) {
    final parsed = value is num ? value.toInt() : fallback;
    return parsed.clamp(min, max).toInt();
  }
}

final class UserPreferences {
  const UserPreferences({
    this.favoriteIds = const <String>{},
    this.recentIds = const <String>[],
    this.themeMode = ThemeMode.system,
    this.localeCode,
    this.marketCode = 'GLOBAL',
    this.streak = 0,
    this.lastOpenDate,
    this.reminders = const ReminderPreferences(),
  });

  final Set<String> favoriteIds;
  final List<String> recentIds;
  final ThemeMode themeMode;
  final String? localeCode;
  final String marketCode;
  final int streak;
  final String? lastOpenDate;
  final ReminderPreferences reminders;

  UserPreferences copyWith({
    Set<String>? favoriteIds,
    List<String>? recentIds,
    ThemeMode? themeMode,
    String? localeCode,
    bool clearLocale = false,
    String? marketCode,
    int? streak,
    String? lastOpenDate,
    ReminderPreferences? reminders,
  }) =>
      UserPreferences(
        favoriteIds: favoriteIds ?? this.favoriteIds,
        recentIds: recentIds ?? this.recentIds,
        themeMode: themeMode ?? this.themeMode,
        localeCode: clearLocale ? null : (localeCode ?? this.localeCode),
        marketCode: marketCode ?? this.marketCode,
        streak: streak ?? this.streak,
        lastOpenDate: lastOpenDate ?? this.lastOpenDate,
        reminders: reminders ?? this.reminders,
      );

  Map<String, dynamic> toJson() => {
        'favoriteIds': favoriteIds.toList()..sort(),
        'recentIds': recentIds,
        'themeMode': themeMode.name,
        'localeCode': localeCode,
        'marketCode': marketCode,
        'streak': streak,
        'lastOpenDate': lastOpenDate,
        'reminders': reminders.toJson(),
      };

  factory UserPreferences.fromJson(Map<String, dynamic> json) {
    final theme = ThemeMode.values.firstWhere(
      (value) => value.name == json['themeMode'],
      orElse: () => ThemeMode.system,
    );
    final reminderJson = json['reminders'];
    return UserPreferences(
      favoriteIds: ((json['favoriteIds'] as List?) ?? const [])
          .map((e) => e.toString())
          .toSet(),
      recentIds: ((json['recentIds'] as List?) ?? const [])
          .map((e) => e.toString())
          .toList(growable: false),
      themeMode: theme,
      localeCode: json['localeCode']?.toString(),
      marketCode: (json['marketCode']?.toString().toUpperCase() ?? 'GLOBAL'),
      streak: (json['streak'] as num?)?.toInt() ?? 0,
      lastOpenDate: json['lastOpenDate']?.toString(),
      reminders: reminderJson is Map
          ? ReminderPreferences.fromJson(
              Map<String, dynamic>.from(reminderJson),
            )
          : const ReminderPreferences(),
    );
  }
}

final class PreferencesRepository {
  static const _key = 'world_days_preferences_v1';

  Future<UserPreferences> load() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString(_key);
    if (raw == null || raw.isEmpty) return const UserPreferences();
    try {
      return UserPreferences.fromJson(
        Map<String, dynamic>.from(jsonDecode(raw) as Map),
      );
    } catch (_) {
      return const UserPreferences();
    }
  }

  Future<void> save(UserPreferences value) async {
    final prefs = await SharedPreferences.getInstance();
    final ok = await prefs.setString(_key, jsonEncode(value.toJson()));
    if (!ok) throw StateError('preferences_write_failed');
  }
}
