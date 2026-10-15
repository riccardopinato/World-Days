import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:world_days/app/app_controller.dart';
import 'package:world_days/app/world_days_app.dart';
import 'package:world_days/core/content_pack/content_pack_io.dart';
import 'package:world_days/core/content_pack/content_pack_manager.dart';
import 'package:world_days/core/content_pack/content_pack_models.dart';
import 'package:world_days/core/entitlements/billing_adapter.dart';
import 'package:world_days/core/entitlements/entitlement_models.dart';
import 'package:world_days/core/entitlements/entitlement_service.dart';
import 'package:world_days/core/entitlements/entitlement_store.dart';
import 'package:world_days/core/notifications/notification_gateway.dart';
import 'package:world_days/core/notifications/notification_health.dart';
import 'package:world_days/core/notifications/reminder_plan.dart';
import 'package:world_days/core/widget/home_widget_gateway.dart';
import 'package:world_days/domain/observance.dart';

class _MemoryEntitlementStore implements EntitlementStore {
  EntitlementSnapshot value = const EntitlementSnapshot.free();
  PendingPurchaseCompletion? pending;

  @override
  Future<EntitlementSnapshot> load() async => value;

  @override
  Future<void> save(EntitlementSnapshot snapshot) async {
    value = snapshot;
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
  Future<void> clearPendingCompletion({String? transactionId}) async {
    if (transactionId == null ||
        pending == null ||
        pending!.transactionId == transactionId) {
      pending = null;
    }
  }
}

class _UnsupportedTransport implements ContentPackTransport {
  const _UnsupportedTransport();

  @override
  bool get supported => false;

  @override
  Future<String> getText(Uri uri) =>
      Future.error(UnsupportedError('integration_test_transport'));

  @override
  Future<List<int>> getBytes(Uri uri, {required int maxBytes}) =>
      Future.error(UnsupportedError('integration_test_transport'));

  @override
  Future<void> close() async {}
}

class _UnsupportedStorage implements ContentPackStorage {
  const _UnsupportedStorage();

  @override
  bool get supported => false;

  @override
  Future<StoredContentPack?> readActive() async => null;

  @override
  Future<StoredContentPack?> readPrevious() async => null;

  @override
  Future<void> activate(ContentPackManifest manifest, List<int> bytes) =>
      Future.error(UnsupportedError('integration_test_storage'));

  @override
  Future<bool> rollback() async => false;

  @override
  Future<void> close() async {}
}

class _NoopNotifications implements NotificationGateway {
  final StreamController<String> _controller =
      StreamController<String>.broadcast();

  @override
  bool get supported => false;

  @override
  Stream<String> get notificationTapStream => _controller.stream;

  @override
  String? takeInitialPayload() => null;

  @override
  Future<void> initialize({bool force = false}) async {}

  @override
  Future<bool> requestPermissions() async => false;

  @override
  Future<NotificationHealth> health() async => const NotificationHealth(
        available: false,
        notificationsEnabled: false,
        exactAlarmsEnabled: false,
        reminderChannelEnabled: false,
        pendingCount: 0,
      );

  @override
  Future<void> openSystemSettings() async {}

  @override
  Future<void> reconcile(Iterable<PlannedNotification> plan) async {}

  @override
  Future<LocalNotificationDiagnostic> runLocalDiagnostic({
    required String immediateTitle,
    required String immediateBody,
    required String scheduledTitle,
    required String scheduledBody,
    Duration scheduledDelay = const Duration(seconds: 12),
  }) async =>
      LocalNotificationDiagnostic(
        permissionGranted: false,
        immediateShown: false,
        scheduledCreated: false,
        scheduledDelaySeconds: scheduledDelay.inSeconds,
        health: await health(),
      );

  @override
  void dispose() {
    _controller.close();
  }
}

class _NoopWidget implements HomeWidgetGateway {
  final StreamController<Uri> _controller = StreamController<Uri>.broadcast();

  @override
  bool get supported => false;

  @override
  Stream<Uri> get clickStream => _controller.stream;

  @override
  Future<Uri?> initialize() async => null;

  @override
  Future<void> sync({
    required String localeCode,
    required List<Observance> Function(DateTime date) observancesForDate,
  }) async {}

  @override
  Future<bool> isPinSupported() async => false;

  @override
  Future<bool> requestPin() async => false;

  @override
  void dispose() {
    _controller.close();
  }
}

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets(
    'launch -> Today -> detail -> favorite -> Saved -> Calendar -> Settings',
    (tester) async {
      SharedPreferences.setMockInitialValues({});

      final controller = AppController(
        notificationService: _NoopNotifications(),
        homeWidgetService: _NoopWidget(),
        entitlementService: EntitlementService(
          store: _MemoryEntitlementStore(),
          billingAdapter: const UnavailableBillingAdapter(),
        ),
        contentPackManager: ContentPackManager(
          transport: const _UnsupportedTransport(),
          storage: const _UnsupportedStorage(),
          validator: (_) {},
        ),
      );
      addTearDown(controller.dispose);

      await controller.initialize();
      await controller.setLocale('en');

      final today = controller.observancesForDate(DateTime.now());
      expect(today, isNotEmpty);
      final record = today.first;

      await tester.pumpWidget(WorldDaysApp(controller: controller));
      await tester.pumpAndSettle();

      expect(find.text('Today'), findsWidgets);
      expect(find.text(record.title), findsWidgets);

      await tester.tap(find.text(record.title).first);
      await tester.pumpAndSettle();

      expect(find.text(record.title), findsWidgets);
      await tester.tap(find.byTooltip('Add to favorites'));
      await tester.pumpAndSettle();
      expect(controller.isFavorite(record.id), isTrue);

      Navigator.of(tester.element(find.text(record.title).first)).pop();
      await tester.pumpAndSettle();

      await tester.tap(find.text('Saved').last);
      await tester.pumpAndSettle();
      expect(find.text(record.title), findsOneWidget);

      await tester.tap(find.text('Calendar').last);
      await tester.pumpAndSettle();
      expect(find.text('Calendar'), findsWidgets);

      await tester.tap(find.text('Settings').last);
      await tester.pumpAndSettle();
      expect(find.text('Settings'), findsWidgets);
      expect(tester.takeException(), isNull);
    },
  );
}
