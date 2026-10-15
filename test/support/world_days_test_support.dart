import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:world_days/app/app_controller.dart';
import 'package:world_days/core/content_pack/content_pack_io.dart';
import 'package:world_days/core/content_pack/content_pack_manager.dart';
import 'package:world_days/core/content_pack/content_pack_models.dart';
import 'package:world_days/core/entitlements/billing_adapter.dart';
import 'package:world_days/core/entitlements/entitlement_models.dart';
import 'package:world_days/core/entitlements/entitlement_service.dart';
import 'package:world_days/core/entitlements/entitlement_store.dart';
import 'package:world_days/core/monetization/monetization_controller.dart';
import 'package:world_days/core/notifications/notification_gateway.dart';
import 'package:world_days/core/notifications/notification_health.dart';
import 'package:world_days/core/notifications/reminder_plan.dart';
import 'package:world_days/core/widget/home_widget_gateway.dart';
import 'package:world_days/data/catalog_repository.dart';
import 'package:world_days/data/preferences_repository.dart';
import 'package:world_days/domain/observance.dart';
import 'package:world_days/domain/occurrence.dart';
import 'package:world_days/l10n/app_localizations.dart';

const testAuthority = ObservanceAuthority(
  name: 'World Days Test Authority',
  type: 'TEST',
  officiality: 'OFFICIAL_INSTITUTIONAL',
);

const testSource = ObservanceSource(
  tier: 'D_ORIGINATOR',
  url: 'https://example.com/world-days-test',
  verifiedAt: '2026-10-15',
);

const testGlobalObservance = Observance(
  id: 'global-test-day',
  title: 'Global Test Day',
  periodKind: 'DAY',
  scope: 'GLOBAL',
  countries: [],
  regions: [],
  authority: testAuthority,
  sources: [testSource],
  rules: [],
  aliases: [],
  categories: ['LEARNING'],
  localizedTitles: {
    'it': 'Giornata globale di test',
  },
  visualKey: 'learning',
  editorialStatus: 'REVIEWED',
  lastVerifiedAt: '2026-10-15',
);

const testItalyObservance = Observance(
  id: 'italy-test-day',
  title: 'Italy Test Day',
  periodKind: 'DAY',
  scope: 'NATIONAL',
  countries: ['IT'],
  regions: [],
  authority: testAuthority,
  sources: [testSource],
  rules: [],
  aliases: [],
  categories: ['CULTURE'],
  localizedTitles: {
    'it': 'Giornata italiana di test',
  },
  visualKey: 'culture',
  editorialStatus: 'REVIEWED',
  lastVerifiedAt: '2026-10-15',
);

const testSpainObservance = Observance(
  id: 'spain-test-day',
  title: 'Spain Test Day',
  periodKind: 'DAY',
  scope: 'NATIONAL',
  countries: ['ES'],
  regions: [],
  authority: testAuthority,
  sources: [testSource],
  rules: [],
  aliases: [],
  categories: ['COMMUNITY'],
  visualKey: 'community',
  editorialStatus: 'REVIEWED',
  lastVerifiedAt: '2026-10-15',
);

CatalogSnapshot buildTestCatalog({
  DateTime? date,
}) {
  final day = date ?? DateTime(2026, 10, 15);
  const records = [
    testGlobalObservance,
    testItalyObservance,
    testSpainObservance,
  ];
  final occurrences = [
    for (final record in records)
      ObservanceOccurrence(
        observanceId: record.id,
        start: day,
        end: day,
      ),
  ];

  return CatalogSnapshot(
    records: records,
    byId: {for (final record in records) record.id: record},
    occurrences2026: occurrences,
    editorialByLocale: const {
      'en': {},
      'it': {},
      'es': {},
      'fr': {},
      'de': {},
      'pt': {},
    },
    yearOverrides: const [],
    datasetVersion: 'test-1',
  );
}

class MemoryEntitlementStore implements EntitlementStore {
  EntitlementSnapshot snapshot = const EntitlementSnapshot.free();
  PendingPurchaseCompletion? pending;

  @override
  Future<EntitlementSnapshot> load() async => snapshot;

  @override
  Future<void> save(EntitlementSnapshot value) async {
    snapshot = value;
  }

  @override
  Future<PendingPurchaseCompletion?> loadPendingCompletion() async => pending;

  @override
  Future<void> savePendingCompletion(
    PendingPurchaseCompletion value,
  ) async {
    pending = value;
  }

  @override
  Future<void> clearPendingCompletion({
    String? transactionId,
  }) async {
    if (transactionId != null &&
        pending != null &&
        pending!.transactionId != transactionId) {
      return;
    }
    pending = null;
  }
}

class UnsupportedContentTransport implements ContentPackTransport {
  const UnsupportedContentTransport();

  @override
  bool get supported => false;

  @override
  Future<String> getText(Uri uri) =>
      Future.error(UnsupportedError('test_transport_unsupported'));

  @override
  Future<List<int>> getBytes(
    Uri uri, {
    required int maxBytes,
  }) =>
      Future.error(UnsupportedError('test_transport_unsupported'));

  @override
  Future<void> close() async {}
}

class UnsupportedContentStorage implements ContentPackStorage {
  const UnsupportedContentStorage();

  @override
  bool get supported => false;

  @override
  Future<StoredContentPack?> readActive() async => null;

  @override
  Future<StoredContentPack?> readPrevious() async => null;

  @override
  Future<void> activate(
    ContentPackManifest manifest,
    List<int> bytes,
  ) =>
      Future.error(UnsupportedError('test_storage_unsupported'));

  @override
  Future<bool> rollback() async => false;

  @override
  Future<void> close() async {}
}

ContentPackManager buildTestContentPackManager() => ContentPackManager(
      transport: const UnsupportedContentTransport(),
      storage: const UnsupportedContentStorage(),
      validator: (_) {},
    );

EntitlementService buildTestEntitlementService({
  MemoryEntitlementStore? store,
}) =>
    EntitlementService(
      store: store ?? MemoryEntitlementStore(),
      billingAdapter: const UnavailableBillingAdapter(),
    );

class FakeNotificationGateway implements NotificationGateway {
  FakeNotificationGateway({
    this.supported = true,
    this.permissionGranted = true,
  });

  @override
  bool supported;
  bool permissionGranted;
  int initializeCalls = 0;
  int permissionCalls = 0;
  int reconcileCalls = 0;
  int settingsCalls = 0;
  List<PlannedNotification> lastPlan = const [];

  final StreamController<String> _tapController =
      StreamController<String>.broadcast();
  String? initialPayload;

  void emitTap(String payload) => _tapController.add(payload);

  @override
  Stream<String> get notificationTapStream => _tapController.stream;

  @override
  String? takeInitialPayload() {
    final value = initialPayload;
    initialPayload = null;
    return value;
  }

  @override
  Future<void> initialize({bool force = false}) async {
    initializeCalls++;
  }

  @override
  Future<bool> requestPermissions() async {
    permissionCalls++;
    return permissionGranted;
  }

  @override
  Future<NotificationHealth> health() async => NotificationHealth(
        available: supported,
        notificationsEnabled: permissionGranted,
        exactAlarmsEnabled: false,
        reminderChannelEnabled: permissionGranted,
        pendingCount: lastPlan.length,
      );

  @override
  Future<void> openSystemSettings() async {
    settingsCalls++;
  }

  @override
  Future<void> reconcile(Iterable<PlannedNotification> plan) async {
    reconcileCalls++;
    lastPlan = plan.toList(growable: false);
  }

  @override
  Future<LocalNotificationDiagnostic> runLocalDiagnostic({
    required String immediateTitle,
    required String immediateBody,
    required String scheduledTitle,
    required String scheduledBody,
    Duration scheduledDelay = const Duration(seconds: 12),
  }) async =>
      LocalNotificationDiagnostic(
        permissionGranted: permissionGranted,
        immediateShown: permissionGranted,
        scheduledCreated: permissionGranted,
        scheduledDelaySeconds: scheduledDelay.inSeconds,
        health: await health(),
      );

  @override
  void dispose() {
    _tapController.close();
  }
}

class FakeHomeWidgetGateway implements HomeWidgetGateway {
  FakeHomeWidgetGateway({
    this.supported = true,
    this.pinSupported = true,
  });

  @override
  bool supported;
  bool pinSupported;
  int initializeCalls = 0;
  int syncCalls = 0;
  int pinCalls = 0;
  String? lastLocale;

  final StreamController<Uri> _clickController =
      StreamController<Uri>.broadcast();
  Uri? initialUri;

  void emitTap(Uri uri) => _clickController.add(uri);

  @override
  Stream<Uri> get clickStream => _clickController.stream;

  @override
  Future<Uri?> initialize() async {
    initializeCalls++;
    final value = initialUri;
    initialUri = null;
    return value;
  }

  @override
  Future<void> sync({
    required String localeCode,
    required WidgetObservancesForDate observancesForDate,
  }) async {
    syncCalls++;
    lastLocale = localeCode;
    observancesForDate(DateTime(2026, 10, 15));
  }

  @override
  Future<bool> isPinSupported() async => pinSupported;

  @override
  Future<bool> requestPin() async {
    pinCalls++;
    return pinSupported;
  }

  @override
  void dispose() {
    _clickController.close();
  }
}

Future<AppController> buildLoadedTestController({
  UserPreferences preferences = const UserPreferences(),
  FakeNotificationGateway? notifications,
  FakeHomeWidgetGateway? widget,
  CatalogSnapshot? catalog,
}) async {
  SharedPreferences.setMockInitialValues({
    'world_days_preferences_v1': jsonEncode(preferences.toJson()),
  });
  final controller = AppController(
    notificationService: notifications ?? FakeNotificationGateway(),
    homeWidgetService: widget ?? FakeHomeWidgetGateway(),
    entitlementService: buildTestEntitlementService(),
    contentPackManager: buildTestContentPackManager(),
    monetizationController: MonetizationController(),
  );
  controller.catalog = catalog ?? buildTestCatalog();
  controller.preferences = preferences;
  controller.loading = false;
  controller.error = null;
  return controller;
}

ThemeData testTheme() => ThemeData(
      useMaterial3: true,
      colorSchemeSeed: Colors.indigo,
    );


Widget wrapTestApp(
  Widget home, {
  Locale locale = const Locale('en'),
  ThemeMode themeMode = ThemeMode.light,
}) =>
    MaterialApp(
      locale: locale,
      theme: testTheme(),
      darkTheme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorSchemeSeed: Colors.indigo,
      ),
      themeMode: themeMode,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: AppLocalizations.supportedLocales,
      home: home,
    );
