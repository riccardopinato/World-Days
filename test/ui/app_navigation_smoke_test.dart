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

  testWidgets('primary navigation has deterministic focus order and safe tap targets',
      (tester) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final controller = await buildLoadedTestController();
    addTearDown(controller.dispose);

    await tester.pumpWidget(WorldDaysApp(controller: controller));
    await tester.pumpAndSettle();

    const expected = ['Today', 'Calendar', 'Discover', 'Saved', 'Settings'];
    final group = tester.widget<FocusTraversalGroup>(
      find.byKey(
        const ValueKey<String>('primary-navigation-focus-group'),
      ),
    );
    expect(group.policy, isA<WidgetOrderTraversalPolicy>());

    final bar = tester.widget<NavigationBar>(find.byType(NavigationBar));
    expect(
      bar.destinations
          .cast<NavigationDestination>()
          .map((destination) => destination.label)
          .toList(growable: false),
      expected,
    );

    for (final label in expected) {
      await tester.tap(find.text(label).last);
      await tester.pumpAndSettle();
      expect(
        tester,
        meetsGuideline(androidTapTargetGuideline),
        reason: 'Android tap target guideline on $label',
      );
      expect(
        tester,
        meetsGuideline(labeledTapTargetGuideline),
        reason: 'Labeled tap target guideline on $label',
      );
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

    expect(find.byType(NavigationBar), findsNothing);
    final compactGroup = tester.widget<FocusTraversalGroup>(
      find.byKey(
        const ValueKey<String>('primary-navigation-focus-group'),
      ),
    );
    expect(compactGroup.policy, isA<WidgetOrderTraversalPolicy>());
    final tooltips = tester
        .widgetList<Tooltip>(
          find.descendant(
            of: find.byKey(
              const ValueKey<String>('primary-navigation-focus-group'),
            ),
            matching: find.byType(Tooltip),
          ),
        )
        .map((tooltip) => tooltip.message)
        .toList(growable: false);
    expect(tooltips, ['Today', 'Calendar', 'Discover', 'Saved', 'Settings']);
    final largeTextException = tester.takeException();
    if (largeTextException != null) {
      debugDumpRenderTree();
    }
    expect(largeTextException, isNull);
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
    final railGroup = tester.widget<FocusTraversalGroup>(
      find.byKey(
        const ValueKey<String>('primary-navigation-focus-group'),
      ),
    );
    expect(railGroup.policy, isA<WidgetOrderTraversalPolicy>());
    final rail = tester.widget<NavigationRail>(find.byType(NavigationRail));
    expect(
      rail.destinations
          .map((destination) => (destination.label as Text).data)
          .toList(growable: false),
      ['Today', 'Calendar', 'Discover', 'Saved', 'Settings'],
    );
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
    expect(semantics.flagsCollection.isButton, isTrue);
  });
}
