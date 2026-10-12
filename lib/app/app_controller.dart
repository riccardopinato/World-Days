import 'package:flutter/material.dart';

import '../data/catalog_repository.dart';
import '../data/preferences_repository.dart';
import '../domain/observance.dart';
import '../domain/occurrence.dart';

final class AppController extends ChangeNotifier {
  AppController({
    CatalogRepository? catalogRepository,
    PreferencesRepository? preferencesRepository,
  })  : _catalogRepository = catalogRepository ?? const CatalogRepository(),
        _preferencesRepository = preferencesRepository ?? PreferencesRepository();

  final CatalogRepository _catalogRepository;
  final PreferencesRepository _preferencesRepository;

  CatalogSnapshot? catalog;
  UserPreferences preferences = const UserPreferences();
  Object? error;
  bool loading = true;

  Future<void> initialize() async {
    try {
      final values = await Future.wait([
        _catalogRepository.load(),
        _preferencesRepository.load(),
      ]);
      catalog = values[0] as CatalogSnapshot;
      preferences = values[1] as UserPreferences;
      await _updateStreak();
    } catch (e) {
      error = e;
    } finally {
      loading = false;
      notifyListeners();
    }
  }

  List<ObservanceOccurrence> occurrencesForYear(int year) {
    final value = catalog;
    if (value == null) return const [];
    return _catalogRepository.occurrencesForYear(year, value);
  }

  List<Observance> observancesForDate(DateTime date) {
    final value = catalog;
    if (value == null) return const [];
    final occurrences = occurrencesForYear(date.year);
    final result = <Observance>[];
    for (final occurrence in occurrences) {
      if (!occurrence.contains(date)) continue;
      final record = value.byId[occurrence.observanceId];
      if (record != null) result.add(record);
    }
    return result;
  }

  List<Observance> search(String query) {
    final value = catalog;
    if (value == null) return const [];
    final normalized = query.trim().toLowerCase();
    if (normalized.isEmpty) return value.records;
    return value.records
        .where(
          (item) =>
              item.title.toLowerCase().contains(normalized) ||
              item.aliases.any((alias) => alias.toLowerCase().contains(normalized)),
        )
        .toList(growable: false);
  }

  bool isFavorite(String id) => preferences.favoriteIds.contains(id);

  Future<void> toggleFavorite(String id) async {
    final next = {...preferences.favoriteIds};
    if (!next.add(id)) next.remove(id);
    preferences = preferences.copyWith(favoriteIds: next);
    notifyListeners();
    await _preferencesRepository.save(preferences);
  }

  Future<void> recordOpen(String id) async {
    final next = [id, ...preferences.recentIds.where((value) => value != id)].take(20).toList();
    preferences = preferences.copyWith(recentIds: next);
    notifyListeners();
    await _preferencesRepository.save(preferences);
  }

  Future<void> setThemeMode(ThemeMode mode) async {
    preferences = preferences.copyWith(themeMode: mode);
    notifyListeners();
    await _preferencesRepository.save(preferences);
  }

  Future<void> setLocale(String? code) async {
    preferences = code == null
        ? preferences.copyWith(clearLocale: true)
        : preferences.copyWith(localeCode: code);
    notifyListeners();
    await _preferencesRepository.save(preferences);
  }

  Future<void> _updateStreak() async {
    final now = DateTime.now();
    final today = _dateKey(now);
    final previous = preferences.lastOpenDate;
    if (previous == today) return;

    var streak = 1;
    if (previous != null) {
      final parsed = DateTime.tryParse(previous);
      if (parsed != null) {
        final yesterday = DateTime(now.year, now.month, now.day).subtract(const Duration(days: 1));
        if (_dateKey(parsed) == _dateKey(yesterday)) {
          streak = preferences.streak + 1;
        }
      }
    }

    preferences = preferences.copyWith(streak: streak, lastOpenDate: today);
    await _preferencesRepository.save(preferences);
  }

  static String _dateKey(DateTime date) =>
      '${date.year.toString().padLeft(4, '0')}-${date.month.toString().padLeft(2, '0')}-${date.day.toString().padLeft(2, '0')}';
}
