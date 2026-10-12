import 'package:flutter/material.dart';

import '../core/retention/home_widget_service.dart';
import '../core/retention/notification_service.dart';
import '../data/catalog_repository.dart';
import '../data/preferences_repository.dart';
import '../domain/observance.dart';
import '../domain/occurrence.dart';

final class AppController extends ChangeNotifier {
  AppController({
    CatalogRepository? catalogRepository,
    PreferencesRepository? preferencesRepository,
    NotificationService? notificationService,
    HomeWidgetService? homeWidgetService,
  })  : _catalogRepository = catalogRepository ?? const CatalogRepository(),
        _preferencesRepository = preferencesRepository ?? PreferencesRepository(),
        _notificationService = notificationService ?? NotificationService(),
        _homeWidgetService = homeWidgetService ?? const HomeWidgetService();

  final CatalogRepository _catalogRepository;
  final PreferencesRepository _preferencesRepository;
  final NotificationService _notificationService;
  final HomeWidgetService _homeWidgetService;

  CatalogSnapshot? catalog;
  UserPreferences preferences = const UserPreferences();
  Object? error;
  bool loading = true;
  String? _notificationTargetId;

  Future<void> initialize() async {
    try {
      final values = await Future.wait([
        _catalogRepository.load(),
        _preferencesRepository.load(),
      ]);
      catalog = values[0] as CatalogSnapshot;
      preferences = values[1] as UserPreferences;
      final launchPayload = await _notificationService.initialize(
        onPayload: _handleNotificationPayload,
      );
      if (launchPayload != null) _handleNotificationPayload(launchPayload);
      await _updateStreak();
      await refreshRetentionSchedule();
      await syncHomeWidget();
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
      if (record != null && isVisibleForMarket(record)) result.add(record);
    }
    return result;
  }

  bool isVisibleForMarket(Observance record, [String? marketCode]) {
    final market = (marketCode ?? preferences.marketCode).toUpperCase();
    if (record.scope == 'GLOBAL') return true;
    if (market == 'GLOBAL') return false;
    return record.countries.contains(market);
  }

  List<Observance> recordsForMarket(
    String marketCode, {
    bool includeGlobal = false,
  }) {
    final value = catalog;
    if (value == null) return const [];
    final market = marketCode.toUpperCase();
    return value.records.where((record) {
      if (record.scope == 'GLOBAL') return includeGlobal;
      return record.countries.contains(market);
    }).toList(growable: false);
  }

  List<Observance> search(String query) {
    final value = catalog;
    if (value == null) return const [];
    final normalized = query.trim().toLowerCase();
    return value.records.where((item) {
      if (!isVisibleForMarket(item)) return false;
      if (normalized.isEmpty) return true;
      return item.title.toLowerCase().contains(normalized) ||
          item.aliases.any((alias) => alias.toLowerCase().contains(normalized));
    }).toList(growable: false);
  }


  String? takeNotificationTarget() {
    final value = _notificationTargetId;
    _notificationTargetId = null;
    return value;
  }

  List<String> availableCategories() {
    final value = catalog;
    if (value == null) return const [];
    final categories = <String>{};
    for (final record in value.records) {
      if (!isVisibleForMarket(record)) continue;
      categories.addAll(record.categories);
    }
    final result = categories.toList()..sort();
    return result;
  }

  Future<bool> setDailyReminder(bool enabled) async {
    if (enabled && !await _notificationService.requestPermission()) {
      return false;
    }
    preferences = preferences.copyWith(dailyReminderEnabled: enabled);
    notifyListeners();
    await _preferencesRepository.save(preferences);
    await refreshRetentionSchedule();
    return true;
  }

  Future<void> setDailyReminderTime(TimeOfDay time) async {
    preferences = preferences.copyWith(
      dailyReminderHour: time.hour,
      dailyReminderMinute: time.minute,
    );
    notifyListeners();
    await _preferencesRepository.save(preferences);
    await refreshRetentionSchedule();
  }

  Future<bool> setWeeklyDigest(bool enabled) async {
    if (enabled && !await _notificationService.requestPermission()) {
      return false;
    }
    preferences = preferences.copyWith(weeklyDigestEnabled: enabled);
    notifyListeners();
    await _preferencesRepository.save(preferences);
    await refreshRetentionSchedule();
    return true;
  }

  bool hasFavoriteReminder(String id) =>
      preferences.favoriteReminderIds.contains(id);

  Future<bool> toggleFavoriteReminder(String id) async {
    final next = {...preferences.favoriteReminderIds};
    final enabling = next.add(id);
    if (!enabling) {
      next.remove(id);
    } else if (!await _notificationService.requestPermission()) {
      return false;
    }
    preferences = preferences.copyWith(favoriteReminderIds: next);
    notifyListeners();
    await _preferencesRepository.save(preferences);
    await refreshRetentionSchedule();
    return true;
  }

  bool followsCategory(String category) =>
      preferences.followedCategories.contains(category);

  Future<bool> toggleCategoryFollow(String category) async {
    final next = {...preferences.followedCategories};
    final enabling = next.add(category);
    if (!enabling) {
      next.remove(category);
    } else if (!await _notificationService.requestPermission()) {
      return false;
    }
    preferences = preferences.copyWith(followedCategories: next);
    notifyListeners();
    await _preferencesRepository.save(preferences);
    await refreshRetentionSchedule();
    return true;
  }

  Future<void> refreshRetentionSchedule() async {
    final value = catalog;
    if (value == null) return;

    final now = DateTime.now();
    final requests = <ReminderRequest>[];
    final ids = <int>{};

    void add(ReminderRequest request) {
      if (ids.add(request.id) && requests.length < 120) {
        requests.add(request);
      }
    }

    if (preferences.dailyReminderEnabled) {
      for (var offset = 0; offset < 31; offset++) {
        final date = DateTime(now.year, now.month, now.day)
            .add(Duration(days: offset));
        final when = DateTime(
          date.year,
          date.month,
          date.day,
          preferences.dailyReminderHour,
          preferences.dailyReminderMinute,
        );
        if (!when.isAfter(now)) continue;
        final records = observancesForDate(date);
        if (records.isEmpty) continue;
        final primary = records.first;
        final extra = records.length - 1;
        add(
          ReminderRequest(
            id: _stableReminderId('daily:${_dateKey(date)}'),
            title: primary.title,
            body: extra > 0
                ? 'Today on World Days · +$extra more'
                : 'Today on World Days',
            when: when,
            payload: 'observance:${primary.id}',
          ),
        );
      }
    }

    if (preferences.weeklyDigestEnabled) {
      var monday = DateTime(now.year, now.month, now.day);
      monday = monday.add(Duration(days: (DateTime.monday - monday.weekday) % 7));
      if (!monday.isAfter(now)) {
        monday = monday.add(const Duration(days: 7));
      }
      for (var week = 0; week < 8; week++) {
        final start = monday.add(Duration(days: week * 7));
        final when = start.subtract(const Duration(days: 1)).copyWith(
              hour: 18,
              minute: 0,
            );
        final seen = <String>{};
        final upcoming = <Observance>[];
        for (var day = 0; day < 7; day++) {
          for (final record
              in observancesForDate(start.add(Duration(days: day)))) {
            if (seen.add(record.id)) upcoming.add(record);
          }
        }
        if (upcoming.isEmpty || !when.isAfter(now)) continue;
        final preview = upcoming.take(2).map((item) => item.title).join(' · ');
        add(
          ReminderRequest(
            id: _stableReminderId('weekly:${_dateKey(start)}'),
            title: 'Your World Days week',
            body: upcoming.length > 2
                ? '$preview · +${upcoming.length - 2} more'
                : preview,
            when: when,
            payload: 'today',
          ),
        );
      }
    }

    final horizon = now.add(const Duration(days: 180));
    final years = {now.year, horizon.year};
    for (final year in years) {
      for (final occurrence in occurrencesForYear(year)) {
        if (occurrence.start.isBefore(now) || occurrence.start.isAfter(horizon)) {
          continue;
        }
        final record = value.byId[occurrence.observanceId];
        if (record == null || !isVisibleForMarket(record)) continue;

        final favoriteMatch =
            preferences.favoriteReminderIds.contains(record.id);
        final categoryMatch = record.categories.any(
          preferences.followedCategories.contains,
        );
        if (!favoriteMatch && !categoryMatch) continue;

        final when = DateTime(
          occurrence.start.year,
          occurrence.start.month,
          occurrence.start.day,
          18,
        ).subtract(const Duration(days: 1));
        if (!when.isAfter(now)) continue;
        final reason = favoriteMatch ? 'favorite' : 'category';
        add(
          ReminderRequest(
            id: _stableReminderId(
              '$reason:${record.id}:${_dateKey(occurrence.start)}',
            ),
            title: 'Tomorrow: ${record.title}',
            body: favoriteMatch
                ? 'A saved World Day is coming up.'
                : 'A followed category has a World Day tomorrow.',
            when: when,
            payload: 'observance:${record.id}',
          ),
        );
      }
    }

    requests.sort((a, b) => a.when.compareTo(b.when));
    await _notificationService.replaceSchedule(requests);
  }

  Future<void> syncHomeWidget() async {
    final now = DateTime.now();
    final days = <HomeWidgetDay>[];
    for (var offset = 0; offset < 14; offset++) {
      final date = DateTime(now.year, now.month, now.day)
          .add(Duration(days: offset));
      days.add(
        HomeWidgetDay(
          date: date,
          observances: observancesForDate(date),
        ),
      );
    }
    await _homeWidgetService.sync(days);
  }

  void _handleNotificationPayload(String payload) {
    if (!payload.startsWith('observance:')) return;
    final id = payload.substring('observance:'.length);
    if (id.isEmpty || catalog?.byId[id] == null) return;
    _notificationTargetId = id;
    notifyListeners();
  }

  static int _stableReminderId(String value) {
    var hash = 0x811c9dc5;
    for (final unit in value.codeUnits) {
      hash ^= unit;
      hash = (hash * 0x01000193) & 0x7fffffff;
    }
    return hash;
  }

  bool isFavorite(String id) => preferences.favoriteIds.contains(id);

  Future<void> toggleFavorite(String id) async {
    final next = {...preferences.favoriteIds};
    final added = next.add(id);
    if (!added) next.remove(id);

    var reminderIds = preferences.favoriteReminderIds;
    if (!added && reminderIds.contains(id)) {
      reminderIds = {...reminderIds}..remove(id);
    }

    preferences = preferences.copyWith(
      favoriteIds: next,
      favoriteReminderIds: reminderIds,
    );
    notifyListeners();
    await _preferencesRepository.save(preferences);
    if (!added) await refreshRetentionSchedule();
  }

  Future<void> recordOpen(String id) async {
    final next =
        [id, ...preferences.recentIds.where((value) => value != id)]
            .take(20)
            .toList();
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

  Future<void> setMarket(String code) async {
    final normalized = code.toUpperCase();
    const allowed = {'GLOBAL', 'IT', 'ES', 'FR', 'DE', 'PT', 'GB', 'US'};
    if (!allowed.contains(normalized)) {
      throw ArgumentError.value(code, 'code', 'Unsupported market');
    }
    preferences = preferences.copyWith(marketCode: normalized);
    notifyListeners();
    await _preferencesRepository.save(preferences);
    await refreshRetentionSchedule();
    await syncHomeWidget();
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
