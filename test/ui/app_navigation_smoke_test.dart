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

    expect(find.byType(NavigationBar), findsNothing);
    for (final label in ['Today', 'Calendar', 'Discover', 'Saved', 'Settings']) {
      final tooltip = find.byTooltip(label);
      expect(tooltip, findsOneWidget);

      final touchTarget = find.descendant(
        of: tooltip,
        matching: find.byType(InkResponse),
      );
      expect(touchTarget, findsOneWidget);
      final size = tester.getSize(touchTarget);
      expect(size.width, greaterThanOrEqualTo(48));
      expect(size.height, greaterThanOrEqualTo(48));
    }

    final compactNavGroup = find.ancestor(
      of: find.byTooltip('Today'),
      matching: find.byWidgetPredicate(
        (widget) =>
            widget is FocusTraversalGroup &&
            widget.policy is OrderedTraversalPolicy,
      ),
    );
    expect(compactNavGroup, findsOneWidget);

    final focusOrders = tester
        .widgetList<FocusTraversalOrder>(
          find.descendant(
            of: compactNavGroup,
            matching: find.byType(FocusTraversalOrder),
          ),
        )
        .map((widget) => (widget.order as NumericFocusOrder).order)
        .toList();
    expect(focusOrders, <double>[0, 1, 2, 3, 4]);

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
