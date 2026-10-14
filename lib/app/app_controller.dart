import 'dart:async';

import 'package:flutter/material.dart';

import '../core/monetization/monetization_controller.dart';
import '../core/notifications/notification_health.dart';
import '../core/notifications/notification_service.dart';
import '../core/notifications/reminder_plan.dart';
import '../core/retention/retention_target.dart';
import '../core/widget/world_days_home_widget_service.dart';
import '../data/catalog_repository.dart';
import '../data/preferences_repository.dart';
import '../domain/observance.dart';
import '../domain/occurrence.dart';

final class AppController extends ChangeNotifier {
  AppController({
    CatalogRepository? catalogRepository,
    PreferencesRepository? preferencesRepository,
    NotificationService? notificationService,
    WorldDaysHomeWidgetService? homeWidgetService,
    MonetizationController? monetizationController,
  })  : monetization = monetizationController ?? MonetizationController(),
        _catalogRepository = catalogRepository ?? const CatalogRepository(),
        _preferencesRepository =
            preferencesRepository ?? PreferencesRepository(),
        _notificationService =
            notificationService ?? NotificationService.instance,
        _homeWidgetService =
            homeWidgetService ?? WorldDaysHomeWidgetService.instance;

  final MonetizationController monetization;
  final CatalogRepository _catalogRepository;
  final PreferencesRepository _preferencesRepository;
  final NotificationService _notificationService;
  final WorldDaysHomeWidgetService _homeWidgetService;

  StreamSubscription<String>? _notificationTapSubscription;
  StreamSubscription<Uri>? _widgetTapSubscription;
  RetentionTarget? _pendingRetentionTarget;

  CatalogSnapshot? catalog;
  UserPreferences preferences = const UserPreferences();
  Object? error;
  bool loading = true;

  bool get nativeNotificationsAvailable => _notificationService.supported;
  bool get androidWidgetAvailable => _homeWidgetService.supported;

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
    }

    if (error == null) {
      try {
        await _initializeNativeRetention();
      } catch (_) {
        // Native retention is a projection. It must never block core startup.
      }
      monetization.addListener(_onMonetizationChanged);
      unawaited(monetization.initialize());
    }

    loading = false;
    notifyListeners();
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
      return item.searchableTitles.any(
            (title) => title.toLowerCase().contains(normalized),
          ) ||
          item.aliases.any(
            (alias) => alias.toLowerCase().contains(normalized),
          );
    }).toList(growable: false);
  }

  bool isFavorite(String id) => preferences.favoriteIds.contains(id);

  Future<void> toggleFavorite(String id) async {
    final next = {...preferences.favoriteIds};
    if (!next.add(id)) next.remove(id);
    preferences = preferences.copyWith(favoriteIds: next);
    notifyListeners();
    await _savePreferencesAndReconcile();
  }

  Future<void> recordOpen(String id) async {
    final next = [
      id,
      ...preferences.recentIds.where((value) => value != id),
    ].take(20).toList();
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
    await _savePreferencesAndReconcile();
  }

  Future<void> setMarket(String code) async {
    final normalized = code.toUpperCase();
    const allowed = {'GLOBAL', 'IT', 'ES', 'FR', 'DE', 'PT', 'GB', 'US'};
    if (!allowed.contains(normalized)) {
      throw ArgumentError.value(code, 'code', 'Unsupported market');
    }
    preferences = preferences.copyWith(marketCode: normalized);
    notifyListeners();
    await _savePreferencesAndReconcile();
  }

  Future<bool> requestNotificationPermission() async {
    final granted = await _notificationService.requestPermissions();
    if (granted) await _reconcileNativeRetention();
    notifyListeners();
    return granted;
  }

  Future<NotificationHealth> notificationHealth() =>
      _notificationService.health();

  Future<void> openNotificationSettings() =>
      _notificationService.openSystemSettings();

  Future<LocalNotificationDiagnostic> runNotificationDiagnostic() async {
    final copy = _diagnosticCopy(_effectiveLocaleCode);
    return _notificationService.runLocalDiagnostic(
      immediateTitle: copy.$1,
      immediateBody: copy.$2,
      scheduledTitle: copy.$3,
      scheduledBody: copy.$4,
    );
  }

  Future<bool> setDailyReminderEnabled(bool enabled) async {
    if (enabled && !await _notificationService.requestPermissions()) {
      return false;
    }
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(dailyEnabled: enabled),
    );
    notifyListeners();
    await _savePreferencesAndReconcile();
    return true;
  }

  Future<bool> setWeeklyReminderEnabled(bool enabled) async {
    if (enabled && !await _notificationService.requestPermissions()) {
      return false;
    }
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(weeklyEnabled: enabled),
    );
    notifyListeners();
    await _savePreferencesAndReconcile();
    return true;
  }

  Future<bool> setFavoriteReminderEnabled(bool enabled) async {
    if (enabled && !await _notificationService.requestPermissions()) {
      return false;
    }
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(favoriteEnabled: enabled),
    );
    notifyListeners();
    await _savePreferencesAndReconcile();
    return true;
  }

  Future<bool> setCategoryReminderEnabled(bool enabled) async {
    if (enabled && !await _notificationService.requestPermissions()) {
      return false;
    }
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(categoryEnabled: enabled),
    );
    notifyListeners();
    await _savePreferencesAndReconcile();
    return true;
  }

  Future<void> setDailyReminderTime(TimeOfDay time) async {
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(
        dailyHour: time.hour,
        dailyMinute: time.minute,
      ),
    );
    notifyListeners();
    await _savePreferencesAndReconcile();
  }

  Future<void> setWeeklyReminderTime(TimeOfDay time) async {
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(
        weeklyHour: time.hour,
        weeklyMinute: time.minute,
      ),
    );
    notifyListeners();
    await _savePreferencesAndReconcile();
  }

  Future<void> toggleFollowedVisualKey(String key) async {
    const allowed = {
      'planet',
      'health',
      'people',
      'learning',
      'culture',
      'food',
      'future',
      'community',
    };
    if (!allowed.contains(key)) {
      throw ArgumentError.value(key, 'key', 'Unsupported visual category');
    }
    final next = {...preferences.reminders.followedVisualKeys};
    if (!next.add(key)) next.remove(key);
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(followedVisualKeys: next),
    );
    notifyListeners();
    await _savePreferencesAndReconcile();
  }

  Future<bool> isHomeWidgetPinSupported() =>
      _homeWidgetService.isPinSupported();

  Future<bool> requestHomeWidgetPin() async {
    await _syncHomeWidget();
    return _homeWidgetService.requestPin();
  }

  RetentionTarget? takeRetentionTarget() {
    final target = _pendingRetentionTarget;
    _pendingRetentionTarget = null;
    return target;
  }

  Future<void> _initializeNativeRetention() async {
    _notificationTapSubscription ??=
        _notificationService.notificationTapStream.listen(_handlePayload);
    await _notificationService.initialize();
    _handlePayload(_notificationService.takeInitialPayload());

    _widgetTapSubscription ??=
        _homeWidgetService.clickStream.listen(_handleWidgetUri);
    final initialWidgetUri = await _homeWidgetService.initialize();
    _handleWidgetUri(initialWidgetUri);

    await _reconcileNativeRetention();
  }

  Future<void> _savePreferencesAndReconcile() async {
    await _preferencesRepository.save(preferences);
    await _reconcileNativeRetention();
  }

  Future<void> _reconcileNativeRetention() async {
    if (catalog == null) return;
    final plan = ReminderPlanBuilder.build(
      settings: preferences.reminders,
      favoriteIds: preferences.favoriteIds,
      localeCode: _effectiveLocaleCode,
      observancesForDate: observancesForDate,
    );
    await _notificationService.reconcile(plan);
    await _syncHomeWidget();
  }

  Future<void> _syncHomeWidget() async {
    await _homeWidgetService.sync(
      localeCode: _effectiveLocaleCode,
      observancesForDate: observancesForDate,
    );
  }

  void _handlePayload(String? payload) {
    final target = RetentionTarget.fromPayload(payload);
    if (target == null) return;
    _pendingRetentionTarget = target;
    if (!loading) notifyListeners();
  }

  void _handleWidgetUri(Uri? uri) {
    final target = RetentionTarget.fromWidgetUri(uri);
    if (target == null) return;
    _pendingRetentionTarget = target;
    if (!loading) notifyListeners();
  }

  String get _effectiveLocaleCode =>
      preferences.localeCode ??
      WidgetsBinding.instance.platformDispatcher.locale.languageCode;

  Future<void> _updateStreak() async {
    final now = DateTime.now();
    final today = _dateKey(now);
    final previous = preferences.lastOpenDate;
    if (previous == today) return;

    var streak = 1;
    if (previous != null) {
      final parsed = DateTime.tryParse(previous);
      if (parsed != null) {
        final yesterday = DateTime(now.year, now.month, now.day)
            .subtract(const Duration(days: 1));
        if (_dateKey(parsed) == _dateKey(yesterday)) {
          streak = preferences.streak + 1;
        }
      }
    }

    preferences = preferences.copyWith(streak: streak, lastOpenDate: today);
    await _preferencesRepository.save(preferences);
  }

  static (String, String, String, String) _diagnosticCopy(String locale) =>
      switch (locale.toLowerCase().split(RegExp('[-_]')).first) {
        'it' => (
            'Test notifiche',
            'La notifica immediata funziona.',
            'Test promemoria programmato',
            'La notifica programmata funziona.',
          ),
        'es' => (
            'Prueba de notificaciones',
            'La notificación inmediata funciona.',
            'Prueba de recordatorio programado',
            'La notificación programada funciona.',
          ),
        'fr' => (
            'Test des notifications',
            'La notification immédiate fonctionne.',
            'Test du rappel programmé',
            'La notification programmée fonctionne.',
          ),
        'de' => (
            'Benachrichtigungstest',
            'Die sofortige Benachrichtigung funktioniert.',
            'Test der geplanten Erinnerung',
            'Die geplante Benachrichtigung funktioniert.',
          ),
        'pt' => (
            'Teste de notificações',
            'A notificação imediata funciona.',
            'Teste do lembrete agendado',
            'A notificação agendada funciona.',
          ),
        _ => (
            'Notification test',
            'The immediate notification works.',
            'Scheduled reminder test',
            'The scheduled notification works.',
          ),
      };

  static String _dateKey(DateTime date) =>
      '${date.year.toString().padLeft(4, '0')}-'
      '${date.month.toString().padLeft(2, '0')}-'
      '${date.day.toString().padLeft(2, '0')}';

  void _onMonetizationChanged() {
    if (!loading) notifyListeners();
  }

  @override
  void dispose() {
    _notificationTapSubscription?.cancel();
    _widgetTapSubscription?.cancel();
    monetization.removeListener(_onMonetizationChanged);
    monetization.dispose();
    super.dispose();
  }
}
