import 'dart:async';

import 'package:flutter/material.dart';

import '../core/content_pack/content_pack_manager.dart';
import '../core/content_pack/content_pack_models.dart';
import '../core/content_pack/content_pack_runtime.dart';
import '../core/entitlements/entitlement_models.dart';
import '../core/entitlements/entitlement_service.dart';
import '../core/monetization/monetization_controller.dart';
import '../core/notifications/notification_gateway.dart';
import '../core/notifications/notification_health.dart';
import '../core/notifications/notification_service.dart';
import '../core/notifications/reminder_plan.dart';
import '../core/retention/retention_target.dart';
import '../core/widget/home_widget_gateway.dart';
import '../core/widget/world_days_home_widget_service.dart';
import '../data/catalog_repository.dart';
import '../data/preferences_repository.dart';
import '../domain/observance.dart';
import '../domain/occurrence.dart';

final class AppController extends ChangeNotifier {
  AppController({
    CatalogRepository? catalogRepository,
    PreferencesRepository? preferencesRepository,
    NotificationGateway? notificationService,
    HomeWidgetGateway? homeWidgetService,
    MonetizationController? monetizationController,
    EntitlementService? entitlementService,
    ContentPackManager? contentPackManager,
  })  : monetization = monetizationController ?? MonetizationController(),
        entitlements = entitlementService ?? EntitlementService(),
        contentPacks = contentPackManager ??
            createContentPackManager(
              validator: CatalogRepository.validateContentPackPayload,
            ),
        _catalogRepository = catalogRepository ?? const CatalogRepository(),
        _preferencesRepository =
            preferencesRepository ?? PreferencesRepository(),
        _notificationService =
            notificationService ?? NotificationService.instance,
        _homeWidgetService =
            homeWidgetService ?? WorldDaysHomeWidgetService.instance;

  final MonetizationController monetization;
  final EntitlementService entitlements;
  final ContentPackManager contentPacks;
  final CatalogRepository _catalogRepository;
  final PreferencesRepository _preferencesRepository;
  final NotificationGateway _notificationService;
  final HomeWidgetGateway _homeWidgetService;

  StreamSubscription<String>? _notificationTapSubscription;
  StreamSubscription<Uri>? _widgetTapSubscription;
  RetentionTarget? _pendingRetentionTarget;

  final Map<int, List<ObservanceOccurrence>> _occurrencesByYear = {};
  final Map<int, Map<String, List<ObservanceOccurrence>>> _occurrenceIndexByYear = {};
  final Map<int, List<Observance>> _unresolvedByYear = {};

  CatalogSnapshot? catalog;
  UserPreferences preferences = const UserPreferences();
  Object? error;
  bool loading = true;

  bool get nativeNotificationsAvailable => _notificationService.supported;
  bool get androidWidgetAvailable => _homeWidgetService.supported;

  Future<void> initialize() async {
    loading = true;
    error = null;

    if (!_entitlementListenerAttached) {
      entitlements.addListener(_onEntitlementChanged);
      _entitlementListenerAttached = true;
    }
    if (!_contentPackListenerAttached) {
      contentPacks.addListener(_onContentPackChanged);
      _contentPackListenerAttached = true;
    }

    try {
      await contentPacks.initialize();
    } catch (_) {
      // Remote content is optional. Bundled assets remain the source fallback.
    }

    try {
      await entitlements.initialize();
      monetization.setAdsSuppressed(entitlements.removesAds);
    } catch (_) {
      // Entitlement bootstrap must not block local-first core startup.
    }

    try {
      final values = await Future.wait([
        _catalogRepository.load(contentPack: contentPacks.activePayload),
        _preferencesRepository.load(),
      ]);
      final loadedCatalog = values[0] as CatalogSnapshot;
      _replaceCatalog(loadedCatalog);
      if (contentPacks.activePayload == null) {
        contentPacks.setBundledVersion(loadedCatalog.datasetVersion);
      }
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
    }

    loading = false;
    notifyListeners();

    if (error == null && contentPacks.supported) {
      unawaited(contentPacks.checkForUpdate());
    }
  }

  Future<bool> checkContentUpdates() => contentPacks.checkForUpdate();

  Future<bool> installContentUpdate() async {
    final installed = await contentPacks.installAvailableUpdate();
    if (!installed) return false;

    try {
      final next = await _catalogRepository.load(
        contentPack: contentPacks.activePayload,
      );
      _replaceCatalog(next);
      await _reconcileNativeRetention();
      notifyListeners();
      return true;
    } catch (_) {
      await contentPacks.rollback();
      try {
        final recovered = await _catalogRepository.load(
          contentPack: contentPacks.activePayload,
        );
        _replaceCatalog(recovered);
      } catch (_) {
        final bundled = await _catalogRepository.load();
        _replaceCatalog(bundled);
        contentPacks.setBundledVersion(bundled.datasetVersion);
      }
      await _reconcileNativeRetention();
      notifyListeners();
      return false;
    }
  }

  ContentPackStatus get contentPackStatus => contentPacks.status;

  void _replaceCatalog(CatalogSnapshot next) {
    catalog = next;
    _occurrencesByYear.clear();
    _occurrenceIndexByYear.clear();
    _unresolvedByYear.clear();
  }

  Future<void> reload() async {
    loading = true;
    error = null;
    notifyListeners();
    await initialize();
  }

  List<ObservanceOccurrence> occurrencesForYear(int year) {
    final value = catalog;
    if (value == null) return const [];
    return _occurrencesByYear.putIfAbsent(
      year,
      () => _catalogRepository.occurrencesForYear(year, value),
    );
  }

  List<Observance> unresolvedObservancesForYear(int year) {
    final value = catalog;
    if (value == null) return const [];
    return _unresolvedByYear.putIfAbsent(
      year,
      () => _catalogRepository.unresolvedForYear(year, value),
    );
  }

  List<Observance> observancesForDate(
    DateTime date, {
    String? marketCode,
  }) {
    final value = catalog;
    if (value == null) return const [];
    final occurrences =
        _occurrenceIndexForYear(date.year)[_dateKey(date)] ?? const [];
    final result = <Observance>[];
    for (final occurrence in occurrences) {
      final record = value.byId[occurrence.observanceId];
      if (record != null && isVisibleForMarket(record, marketCode)) {
        result.add(record);
      }
    }
    result.sort(_compareObservances);
    return result;
  }

  Map<String, List<ObservanceOccurrence>> _occurrenceIndexForYear(int year) {
    return _occurrenceIndexByYear.putIfAbsent(year, () {
      final index = <String, List<ObservanceOccurrence>>{};
      final yearStart = DateTime(year, 1, 1);
      final yearEnd = DateTime(year, 12, 31);
      final candidates = <ObservanceOccurrence>[
        ...occurrencesForYear(year - 1),
        ...occurrencesForYear(year),
      ];

      for (final occurrence in candidates) {
        var start = DateTime(
          occurrence.start.year,
          occurrence.start.month,
          occurrence.start.day,
        );
        var end = DateTime(
          occurrence.end.year,
          occurrence.end.month,
          occurrence.end.day,
        );
        if (end.isBefore(yearStart) || start.isAfter(yearEnd)) continue;
        if (start.isBefore(yearStart)) start = yearStart;
        if (end.isAfter(yearEnd)) end = yearEnd;

        for (var cursor = start;
            !cursor.isAfter(end);
            cursor = cursor.add(const Duration(days: 1))) {
          index.putIfAbsent(_dateKey(cursor), () => []).add(occurrence);
        }
      }
      return index;
    });
  }

  int _compareObservances(Observance a, Observance b) {
    final score = _observancePriority(b).compareTo(_observancePriority(a));
    if (score != 0) return score;
    return a.title.compareTo(b.title);
  }

  int _observancePriority(Observance record) {
    var score = switch (record.authority.officiality) {
      'OFFICIAL_UN' => 600,
      'OFFICIAL_UN_AGENCY' => 560,
      'OFFICIAL_UNESCO' => 550,
      'OFFICIAL_WHO' => 550,
      'OFFICIAL_INSTITUTIONAL' => 450,
      'RECOGNIZED_NGO' => 300,
      'POPULAR' => 200,
      _ => 100,
    };
    if (record.scope == 'GLOBAL') score += 20;
    if (record.periodKind == 'DAY') score += 10;
    if (catalog?.editorialByLocale['en']?.containsKey(record.id) ?? false) {
      score += 5;
    }
    return score;
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

  bool _monetizationListenerAttached = false;
  bool _entitlementListenerAttached = false;
  bool _contentPackListenerAttached = false;

  bool get removeAdsEntitled => entitlements.removesAds;
  ProductLimits get productLimits => entitlements.limits;
  PurchaseFlowState get purchaseFlowState => entitlements.flowState;
  BillingProductInfo? get removeAdsProduct => entitlements.product;

  Future<PurchaseFlowState> purchaseRemoveAds() =>
      entitlements.purchaseRemoveAds();

  Future<PurchaseFlowState> restoreRemoveAds() =>
      entitlements.restoreRemoveAds();

  Future<void> initializeMonetization() async {
    if (!_monetizationListenerAttached) {
      monetization.addListener(_onMonetizationChanged);
      _monetizationListenerAttached = true;
    }
    await monetization.initialize();
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

  Future<void> setWeeklyReminderWeekday(int weekday) async {
    if (weekday < DateTime.monday || weekday > DateTime.sunday) {
      throw ArgumentError.value(weekday, 'weekday', 'Unsupported weekday');
    }
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(
        weeklyWeekday: weekday,
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

  Future<void> toggleFollowedCategory(String key) async {
    const allowed = {
      'PLANET',
      'HEALTH',
      'PEOPLE',
      'LEARNING',
      'CULTURE',
      'FOOD',
      'FUTURE',
      'COMMUNITY',
    };
    final normalized = key.trim().toUpperCase();
    if (!allowed.contains(normalized)) {
      throw ArgumentError.value(key, 'key', 'Unsupported semantic category');
    }
    final next = {...preferences.reminders.followedCategories};
    if (!next.add(normalized)) next.remove(normalized);
    preferences = preferences.copyWith(
      reminders: preferences.reminders.copyWith(followedCategories: next),
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

  void _onEntitlementChanged() {
    monetization.setAdsSuppressed(entitlements.removesAds);
    if (!loading) notifyListeners();
  }

  void _onContentPackChanged() {
    if (!loading) notifyListeners();
  }

  @override
  void dispose() {
    _notificationTapSubscription?.cancel();
    _widgetTapSubscription?.cancel();
    if (_monetizationListenerAttached) {
      monetization.removeListener(_onMonetizationChanged);
    }
    if (_entitlementListenerAttached) {
      entitlements.removeListener(_onEntitlementChanged);
    }
    if (_contentPackListenerAttached) {
      contentPacks.removeListener(_onContentPackChanged);
    }
    contentPacks.dispose();
    entitlements.dispose();
    monetization.dispose();
    super.dispose();
  }
}
