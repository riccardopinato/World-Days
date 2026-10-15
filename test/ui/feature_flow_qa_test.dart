import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/data/preferences_repository.dart';
import 'package:world_days/features/calendar/calendar_page.dart';
import 'package:world_days/features/discover/around_the_world_page.dart';
import 'package:world_days/features/saved/saved_page.dart';
import 'package:world_days/features/settings/settings_page.dart';

import '../support/world_days_test_support.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Settings theme, reminder and widget actions remain interactive',
      (tester) async {
    final notifications = FakeNotificationGateway(permissionGranted: true);
    final widget = FakeHomeWidgetGateway(pinSupported: true);
    final controller = await buildLoadedTestController(
      notifications: notifications,
      widget: widget,
    );
    addTearDown(controller.dispose);

    await tester.pumpWidget(
      wrapTestApp(SettingsPage(controller: controller)),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.text('Dark'));
    await tester.pump();
    expect(controller.preferences.themeMode, ThemeMode.dark);

    await tester.scrollUntilVisible(
      find.text('Daily reminder'),
      250,
    );
    await tester.tap(find.text('Daily reminder'));
    await tester.pumpAndSettle();

    expect(controller.preferences.reminders.dailyEnabled, isTrue);
    expect(notifications.permissionCalls, 1);
    expect(notifications.reconcileCalls, greaterThanOrEqualTo(1));

    await tester.scrollUntilVisible(
      find.text('Add Today widget'),
      300,
    );
    await tester.tap(find.text('Add Today widget'));
    await tester.pumpAndSettle();

    expect(widget.syncCalls, greaterThanOrEqualTo(1));
    expect(widget.pinCalls, 1);
    expect(tester.takeException(), isNull);
  });

  testWidgets('Calendar filters national records without mutating profile market',
      (tester) async {
    final controller = await buildLoadedTestController(
      preferences: const UserPreferences(marketCode: 'IT'),
    );
    addTearDown(controller.dispose);

    await tester.pumpWidget(
      wrapTestApp(CalendarPage(controller: controller)),
    );
    await tester.pumpAndSettle();

    expect(find.text('Global Test Day'), findsOneWidget);
    await tester.scrollUntilVisible(
      find.text('Italy Test Day'),
      180,
      scrollable: find.byType(Scrollable).first,
    );
    expect(find.text('Italy Test Day'), findsOneWidget);
    expect(find.text('Spain Test Day'), findsNothing);

    await tester.tap(find.byTooltip('Calendar filters'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('National').last);
    await tester.pump();
    Navigator.of(tester.element(find.text('National').last)).pop();
    await tester.pumpAndSettle();

    expect(find.text('Global Test Day'), findsNothing);
    await tester.scrollUntilVisible(
      find.text('Italy Test Day'),
      180,
      scrollable: find.byType(Scrollable).first,
    );
    expect(find.text('Italy Test Day'), findsOneWidget);
    expect(controller.preferences.marketCode, 'IT');
    expect(tester.takeException(), isNull);
  });

  testWidgets('Around the World browsing is transient to profile market',
      (tester) async {
    final controller = await buildLoadedTestController(
      preferences: const UserPreferences(marketCode: 'IT'),
    );
    addTearDown(controller.dispose);

    await tester.pumpWidget(
      wrapTestApp(AroundTheWorldPage(controller: controller)),
    );
    await tester.pumpAndSettle();

    expect(find.text('Italy Test Day'), findsOneWidget);

    await tester.tap(find.byType(DropdownButtonFormField<String>));
    await tester.pumpAndSettle();
    await tester.tap(find.textContaining('Spain').last);
    await tester.pumpAndSettle();

    expect(find.text('Spain Test Day'), findsOneWidget);
    expect(find.text('Italy Test Day'), findsNothing);
    expect(controller.preferences.marketCode, 'IT');
  });

  testWidgets('Saved favorite opens detail without losing saved state',
      (tester) async {
    final controller = await buildLoadedTestController(
      preferences: const UserPreferences(
        favoriteIds: {'global-test-day'},
        recentIds: ['italy-test-day'],
      ),
    );
    addTearDown(controller.dispose);

    await tester.pumpWidget(
      wrapTestApp(SavedPage(controller: controller)),
    );
    await tester.pumpAndSettle();

    expect(find.text('Global Test Day'), findsOneWidget);
    expect(find.text('Italy Test Day'), findsOneWidget);

    await tester.tap(find.text('Global Test Day'));
    await tester.pumpAndSettle();

    expect(find.text('Global Test Day'), findsWidgets);
    expect(controller.isFavorite('global-test-day'), isTrue);
    expect(tester.takeException(), isNull);
  });

  testWidgets('Settings survives 360dp width with 200 percent text scale',
      (tester) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1;
    tester.platformDispatcher.textScaleFactorTestValue = 2;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);

    final controller = await buildLoadedTestController(
      notifications: FakeNotificationGateway(supported: false),
      widget: FakeHomeWidgetGateway(supported: false),
    );
    addTearDown(controller.dispose);

    await tester.pumpWidget(
      wrapTestApp(SettingsPage(controller: controller)),
    );
    await tester.pumpAndSettle();

    expect(find.text('Settings'), findsOneWidget);
    expect(find.text('Theme'), findsOneWidget);
    expect(tester.takeException(), isNull);

    final darkText = find.text('Dark');
    expect(darkText, findsOneWidget);
    final size = tester.getSize(darkText);
    expect(size.height, greaterThan(0));
  });
}
