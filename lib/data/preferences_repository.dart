import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

final class UserPreferences {
  const UserPreferences({
    this.favoriteIds = const <String>{},
    this.recentIds = const <String>[],
    this.themeMode = ThemeMode.system,
    this.localeCode,
    this.streak = 0,
    this.lastOpenDate,
  });

  final Set<String> favoriteIds;
  final List<String> recentIds;
  final ThemeMode themeMode;
  final String? localeCode;
  final int streak;
  final String? lastOpenDate;

  UserPreferences copyWith({
    Set<String>? favoriteIds,
    List<String>? recentIds,
    ThemeMode? themeMode,
    String? localeCode,
    bool clearLocale = false,
    int? streak,
    String? lastOpenDate,
  }) =>
      UserPreferences(
        favoriteIds: favoriteIds ?? this.favoriteIds,
        recentIds: recentIds ?? this.recentIds,
        themeMode: themeMode ?? this.themeMode,
        localeCode: clearLocale ? null : (localeCode ?? this.localeCode),
        streak: streak ?? this.streak,
        lastOpenDate: lastOpenDate ?? this.lastOpenDate,
      );

  Map<String, dynamic> toJson() => {
        'favoriteIds': favoriteIds.toList()..sort(),
        'recentIds': recentIds,
        'themeMode': themeMode.name,
        'localeCode': localeCode,
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
