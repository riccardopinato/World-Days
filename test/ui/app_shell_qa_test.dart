import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:world_days/app/app_controller.dart';
import 'package:world_days/app/world_days_app.dart';

Future<AppController> _controller() async {
  SharedPreferences.setMockInitialValues({});
  final controller = AppController();
  await controller.initialize();
  return controller;
}

void _phoneViewport(WidgetTester tester) {
  tester.view.physicalSize = const Size(390, 844);
  tester.view.devicePixelRatio = 1;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
}

void main() {
  testWidgets('mobile shell exposes all primary destinations', (tester) async {
    _phoneViewport(tester);
    final controller = await _controller();

    await tester.pumpWidget(WorldDaysApp(controller: controller));
    await tester.pumpAndSettle();

    expect(find.text('Today'), findsWidgets);
    expect(find.text('Calendar'), findsOneWidget);
    expect(find.text('Discover'), findsOneWidget);
    expect(find.text('Saved'), findsOneWidget);
    expect(find.text('Settings'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('discover lazily exposes records beyond the old 100 item cap',
      (tester) async {
    _phoneViewport(tester);
    final controller = await _controller();

    await tester.pumpWidget(WorldDaysApp(controller: controller));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Discover'));
    await tester.pumpAndSettle();

    final records = controller.catalog!.records;
    expect(records.length, greaterThan(100));
    expect(find.text('${records.length} observances'), findsOneWidget);

    final lastTitle = records.last.title;
    await tester.scrollUntilVisible(
      find.text(lastTitle),
      700,
      scrollable: find.byType(Scrollable).last,
      maxScrolls: records.length,
    );

    expect(find.text(lastTitle), findsWidgets);
    expect(tester.takeException(), isNull);
  });

  testWidgets('large text and Italian settings copy remain usable',
      (tester) async {
    _phoneViewport(tester);
    tester.platformDispatcher.textScaleFactorTestValue = 2;
    addTearDown(
      tester.platformDispatcher.clearTextScaleFactorTestValue,
    );

    final controller = await _controller();
    await controller.setLocale('it');

    await tester.pumpWidget(WorldDaysApp(controller: controller));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Impostazioni'));
    await tester.pumpAndSettle();

    expect(find.text('Politica dei dati'), findsOneWidget);
    expect(find.text('Disponibile offline'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
