import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/data/preferences_repository.dart';
import 'package:world_days/features/discover/around_the_world_page.dart';
import 'package:world_days/l10n/app_localizations.dart';

import '../support/world_days_test_support.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  // Regression for World Days #52: the old selector overflowed by 12px.
  for (final width in <double>[320, 360, 390, 480]) {
    for (final language in <String>['it', 'en', 'de']) {
      for (final scale in <double>[1, 1.5, 2]) {
        testWidgets(
          'country dropdown responsive ' +
              width.toInt().toString() +
              'px / ' + language + ' / ' + scale.toString() + 'x',
          (tester) async {
            tester.view.physicalSize = Size(width, 844);
            tester.view.devicePixelRatio = 1;
            tester.platformDispatcher.textScaleFactorTestValue = scale;
            addTearDown(tester.view.resetPhysicalSize);
            addTearDown(tester.view.resetDevicePixelRatio);
            addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);

            final controller = await buildLoadedTestController(
              preferences: const UserPreferences(marketCode: 'IT'),
            );
            addTearDown(controller.dispose);

            await tester.pumpWidget(
              wrapTestApp(
                AroundTheWorldPage(controller: controller),
                locale: Locale(language),
              ),
            );
            await tester.pumpAndSettle();

            expect(
              tester.takeException(),
              isNull,
              reason: 'Country selector must not overflow',
            );
            final dropdown = tester.widget<DropdownButtonFormField<String?>>(
              find.byType(DropdownButtonFormField<String?>),
            );
            expect(dropdown.isExpanded, isTrue);
            expect(controller.preferences.marketCode, 'IT');
          },
        );
      }
    }
  }

  testWidgets('changing country remains transient after responsive fix',
      (tester) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final controller = await buildLoadedTestController(
      preferences: const UserPreferences(marketCode: 'IT'),
    );
    addTearDown(controller.dispose);
    await tester.pumpWidget(
      wrapTestApp(
        AroundTheWorldPage(controller: controller),
        locale: const Locale('it'),
      ),
    );
    await tester.pumpAndSettle();

    final l10n = AppLocalizations.of(
      tester.element(find.byType(AroundTheWorldPage)),
    );
    await tester.tap(find.byType(DropdownButtonFormField<String?>));
    await tester.pumpAndSettle();
    await tester.tap(find.textContaining(l10n.countrySpain).last);
    await tester.pumpAndSettle();

    expect(find.text('Spain Test Day'), findsOneWidget);
    expect(find.text('Italy Test Day'), findsNothing);
    expect(controller.preferences.marketCode, 'IT');
    expect(tester.takeException(), isNull);
  });
}
