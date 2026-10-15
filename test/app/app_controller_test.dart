import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:world_days/app/app_controller.dart';
import 'package:world_days/core/retention/retention_target.dart';
import 'package:world_days/data/preferences_repository.dart';

import '../support/world_days_test_support.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('controller initializes local-first core with injected retention fakes',
      () async {
    SharedPreferences.setMockInitialValues({});
    final notifications = FakeNotificationGateway();
    final widget = FakeHomeWidgetGateway();
    final controller = AppController(
      notificationService: notifications,
      homeWidgetService: widget,
      entitlementService: buildTestEntitlementService(),
      contentPackManager: buildTestContentPackManager(),
    );
    addTearDown(controller.dispose);

    await controller.initialize();

    expect(controller.loading, isFalse);
    expect(controller.error, isNull);
    expect(controller.catalog, isNotNull);
    expect(controller.catalog!.records.length, greaterThanOrEqualTo(296));
    expect(notifications.initializeCalls, 1);
    expect(notifications.reconcileCalls, greaterThanOrEqualTo(1));
    expect(widget.initializeCalls, 1);
    expect(widget.syncCalls, greaterThanOrEqualTo(1));
  });

  test('favorite mutation persists and reconciles retention projection',
      () async {
    final notifications = FakeNotificationGateway();
    final widget = FakeHomeWidgetGateway();
    final controller = await buildLoadedTestController(
      notifications: notifications,
      widget: widget,
      preferences: const UserPreferences(
        reminders: ReminderPreferences(
          favoriteEnabled: true,
        ),
      ),
    );
    addTearDown(controller.dispose);

    await controller.toggleFavorite(testGlobalObservance.id);

    expect(controller.isFavorite(testGlobalObservance.id), isTrue);
    expect(notifications.reconcileCalls, 1);
    expect(widget.syncCalls, 1);

    final raw = (await SharedPreferences.getInstance())
        .getString('world_days_preferences_v1');
    expect(raw, isNotNull);
    final decoded = jsonDecode(raw!) as Map<String, dynamic>;
    expect(
      (decoded['favoriteIds'] as List).contains(testGlobalObservance.id),
      isTrue,
    );
  });

  test('permission denial leaves reminder disabled and avoids reconciliation',
      () async {
    final notifications = FakeNotificationGateway(permissionGranted: false);
    final widget = FakeHomeWidgetGateway();
    final controller = await buildLoadedTestController(
      notifications: notifications,
      widget: widget,
    );
    addTearDown(controller.dispose);

    final enabled = await controller.setDailyReminderEnabled(true);

    expect(enabled, isFalse);
    expect(controller.preferences.reminders.dailyEnabled, isFalse);
    expect(notifications.permissionCalls, 1);
    expect(notifications.reconcileCalls, 0);
    expect(widget.syncCalls, 0);
  });

  test('notification and widget taps map to deterministic retention targets',
      () async {
    SharedPreferences.setMockInitialValues({});
    final notifications = FakeNotificationGateway()
      ..initialPayload = 'tab:calendar';
    final widget = FakeHomeWidgetGateway()
      ..initialUri = Uri.parse('worlddays://observance/italy-test-day');
    final controller = AppController(
      notificationService: notifications,
      homeWidgetService: widget,
      entitlementService: buildTestEntitlementService(),
      contentPackManager: buildTestContentPackManager(),
    );
    addTearDown(controller.dispose);

    await controller.initialize();

    final initial = controller.takeRetentionTarget();
    expect(initial?.observanceId, testItalyObservance.id);

    notifications.emitTap('tab:today');
    await Future<void>.delayed(Duration.zero);
    expect(controller.takeRetentionTarget()?.tab, RetentionTab.today);

    widget.emitTap(Uri.parse('worlddays://today'));
    await Future<void>.delayed(Duration.zero);
    expect(controller.takeRetentionTarget()?.tab, RetentionTab.today);
  });

  test('home-widget pin request syncs projection before requesting pin',
      () async {
    final notifications = FakeNotificationGateway();
    final widget = FakeHomeWidgetGateway(pinSupported: true);
    final controller = await buildLoadedTestController(
      notifications: notifications,
      widget: widget,
    );
    addTearDown(controller.dispose);

    final result = await controller.requestHomeWidgetPin();

    expect(result, isTrue);
    expect(widget.syncCalls, 1);
    expect(widget.pinCalls, 1);
  });

  test('market visibility keeps global and national scopes deterministic',
      () async {
    final controller = await buildLoadedTestController(
      preferences: const UserPreferences(marketCode: 'IT'),
    );
    addTearDown(controller.dispose);

    expect(controller.isVisibleForMarket(testGlobalObservance), isTrue);
    expect(controller.isVisibleForMarket(testItalyObservance), isTrue);
    expect(controller.isVisibleForMarket(testSpainObservance), isFalse);

    await controller.setMarket('GLOBAL');

    expect(controller.isVisibleForMarket(testGlobalObservance), isTrue);
    expect(controller.isVisibleForMarket(testItalyObservance), isFalse);
  });
}
