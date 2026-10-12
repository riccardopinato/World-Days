import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

final class UserPreferences {
  const UserPreferences({
    this.favoriteIds = const <String>{},
    this.recentIds = const <String>[],
    this.themeMode = ThemeMode.system,
    this.localeCode,
    this.marketCode = 'GLOBAL',
    this.dailyReminderEnabled = false,
    this.dailyReminderHour = 8,
    this.dailyReminderMinute = 0,
    this.weeklyDigestEnabled = false,
    this.favoriteReminderIds = const <String>{},
    this.followedCategories = const <String>{},
    this.streak = 0,
    this.lastOpenDate,
  });

  final Set<String> favoriteIds;
  final List<String> recentIds;
  final ThemeMode themeMode;
  final String? localeCode;
  final String marketCode;
  final bool dailyReminderEnabled;
  final int dailyReminderHour;
  final int dailyReminderMinute;
  final bool weeklyDigestEnabled;
  final Set<String> favoriteReminderIds;
  final Set<String> followedCategories;
  final int streak;
  final String? lastOpenDate;

  UserPreferences copyWith({
    Set<String>? favoriteIds,
    List<String>? recentIds,
    ThemeMode? themeMode,
    String? localeCode,
    bool clearLocale = false,
    String? marketCode,
    bool? dailyReminderEnabled,
    int? dailyReminderHour,
    int? dailyReminderMinute,
    bool? weeklyDigestEnabled,
    Set<String>? favoriteReminderIds,
    Set<String>? followedCategories,
    int? streak,
    String? lastOpenDate,
  }) =>
      UserPreferences(
        favoriteIds: favoriteIds ?? this.favoriteIds,
        recentIds: recentIds ?? this.recentIds,
        themeMode: themeMode ?? this.themeMode,
        localeCode: clearLocale ? null : (localeCode ?? this.localeCode),
        marketCode: marketCode ?? this.marketCode,
        dailyReminderEnabled:
            dailyReminderEnabled ?? this.dailyReminderEnabled,
        dailyReminderHour: dailyReminderHour ?? this.dailyReminderHour,
        dailyReminderMinute: dailyReminderMinute ?? this.dailyReminderMinute,
        weeklyDigestEnabled: weeklyDigestEnabled ?? this.weeklyDigestEnabled,
        favoriteReminderIds:
            favoriteReminderIds ?? this.favoriteReminderIds,
        followedCategories: followedCategories ?? this.followedCategories,
        streak: streak ?? this.streak,
        lastOpenDate: lastOpenDate ?? this.lastOpenDate,
      );

  Map<String, dynamic> toJson() => {
        'favoriteIds': favoriteIds.toList()..sort(),
        'recentIds': recentIds,
        'themeMode': themeMode.name,
        'localeCode': localeCode,
        'marketCode': marketCode,
        'dailyReminderEnabled': dailyReminderEnabled,
        'dailyReminderHour': dailyReminderHour,
        'dailyReminderMinute': dailyReminderMinute,
        'weeklyDigestEnabled': weeklyDigestEnabled,
        'favoriteReminderIds': favoriteReminderIds.toList()..sort(),
        'followedCategories': followedCategories.toList()..sort(),
        'streak': streak,
        'lastOpenDate': lastOpenDate,
      };

  factory UserPreferences.fromJson(Map<String, dynamic> json) {
    final theme = ThemeMode.values.firstWhere(
      (value) => value.name == json['themeMode'],
      orElse: () => ThemeMode.system,
    );
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
      dailyReminderEnabled: json['dailyReminderEnabled'] == true,
      dailyReminderHour: (json['dailyReminderHour'] as num?)?.toInt() ?? 8,
      dailyReminderMinute: (json['dailyReminderMinute'] as num?)?.toInt() ?? 0,
      weeklyDigestEnabled: json['weeklyDigestEnabled'] == true,
      favoriteReminderIds: ((json['favoriteReminderIds'] as List?) ?? const [])
          .map((e) => e.toString())
          .toSet(),
      followedCategories: ((json['followedCategories'] as List?) ?? const [])
          .map((e) => e.toString())
          .toSet(),
      streak: (json['streak'] as num?)?.toInt() ?? 0,
      lastOpenDate: json['lastOpenDate']?.toString(),
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
