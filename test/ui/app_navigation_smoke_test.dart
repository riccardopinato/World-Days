import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/app/world_days_app.dart';

import '../support/world_days_test_support.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('phone shell navigates all five destinations without exceptions',
      (tester) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final controller = await buildLoadedTestController();
    addTearDown(controller.dispose);

    await tester.pumpWidget(WorldDaysApp(controller: controller));
    await tester.pumpAndSettle();

    for (final label in ['Today', 'Calendar', 'Discover', 'Saved', 'Settings']) {
      await tester.tap(find.text(label).last);
      await tester.pumpAndSettle();
      expect(find.text(label), findsWidgets);
      expect(tester.takeException(), isNull);
    }
  });

  testWidgets('app shell survives small phone large text and exposes nav labels',
      (tester) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1;
    tester.platformDispatcher.textScaleFactorTestValue = 2;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);

    final controller = await buildLoadedTestController();
    addTearDown(controller.dispose);

    await tester.pumpWidget(WorldDaysApp(controller: controller));
    await tester.pumpAndSettle();

    expect(find.byType(NavigationBar), findsOneWidget);
    for (final label in ['Today', 'Calendar', 'Discover', 'Saved', 'Settings']) {
      expect(find.text(label), findsWidgets);
    }
    expect(tester.takeException(), isNull);
  });

  testWidgets('wide shell switches to NavigationRail', (tester) async {
    tester.view.physicalSize = const Size(1200, 900);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final controller = await buildLoadedTestController();
    addTearDown(controller.dispose);

    await tester.pumpWidget(WorldDaysApp(controller: controller));
    await tester.pumpAndSettle();

    expect(find.byType(NavigationRail), findsOneWidget);
    expect(find.byType(NavigationBar), findsNothing);
    expect(tester.takeException(), isNull);
  });

  testWidgets('calendar day cells expose button semantics', (tester) async {
    final controller = await buildLoadedTestController();
    addTearDown(controller.dispose);

    await tester.pumpWidget(WorldDaysApp(controller: controller));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Calendar').last);
    await tester.pumpAndSettle();

    final todayLabel = DateTime.now().day.toString();
    final semantics = tester.getSemantics(find.text(todayLabel).first);
    expect(semantics.hasFlag(SemanticsFlag.isButton), isTrue);
  });
}
