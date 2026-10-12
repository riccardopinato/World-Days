import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/core/widgets/observance_card.dart';
import 'package:world_days/domain/observance.dart';
import 'package:world_days/l10n/app_localizations.dart';

const record = Observance(
  id: 'world-test-day',
  title: 'World Test Day',
  periodKind: 'DAY',
  scope: 'GLOBAL',
  countries: [],
  regions: [],
  authority: ObservanceAuthority(
    name: 'Test Authority',
    type: 'TEST',
    officiality: 'POPULAR_VERIFIED',
  ),
  sources: [
    ObservanceSource(
      tier: 'D_ORIGINATOR',
      url: 'https://example.com/world-test-day',
    ),
  ],
  rules: [],
  aliases: [],
);

void main() {
  testWidgets('observance card stays usable with Italian copy and large text',
      (tester) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    tester.platformDispatcher.textScaleFactorTestValue = 2;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    addTearDown(tester.platformDispatcher.clearTextScaleFactorTestValue);

    var opened = false;
    var favorited = false;

    await tester.pumpWidget(
      MaterialApp(
        locale: const Locale('it'),
        localizationsDelegates: const [
          AppLocalizations.delegate,
          GlobalMaterialLocalizations.delegate,
          GlobalWidgetsLocalizations.delegate,
          GlobalCupertinoLocalizations.delegate,
        ],
        supportedLocales: AppLocalizations.supportedLocales,
        home: Scaffold(
          body: Padding(
            padding: const EdgeInsets.all(16),
            child: ObservanceCard(
              observance: record,
              onTap: () => opened = true,
              onFavorite: () => favorited = true,
            ),
          ),
        ),
      ),
    );
    await tester.pump(const Duration(milliseconds: 300));

    expect(find.text('World Test Day'), findsOneWidget);
    expect(find.byTooltip('Aggiungi ai preferiti'), findsOneWidget);
    expect(tester.takeException(), isNull);

    await tester.tap(find.byTooltip('Aggiungi ai preferiti'));
    expect(favorited, isTrue);

    await tester.tap(find.text('World Test Day'));
    expect(opened, isTrue);
  });
}
