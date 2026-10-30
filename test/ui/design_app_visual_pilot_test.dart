import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/core/theme/app_theme.dart';
import 'package:world_days/core/widgets/observance_card.dart';
import 'package:world_days/domain/observance.dart';
import 'package:world_days/l10n/app_localizations.dart';

/// Real first-party World Days screen component, adapted from Design-App
/// Visual QA v0.1's scenario matrix. No runtime imports or dependencies.
const _pilotRecord = Observance(
  id: 'world-days-visual-pilot',
  title: 'World Test Day',
  periodKind: 'DAY',
  scope: 'GLOBAL',
  countries: [],
  regions: [],
  authority: ObservanceAuthority(
    name: 'International Testing Authority',
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
  localizedTitles: {
    'it': 'Giornata mondiale per la verifica delle schermate e della navigazione accessibile',
  },
);

typedef _Scenario = ({
  String name,
  Size size,
  double scale,
  Brightness brightness,
  EdgeInsets padding,
  EdgeInsets viewInsets,
});

void main() {
  const screens = <_Scenario>[
    (name: 'small-phone', size: Size(360, 800), scale: 1,
     brightness: Brightness.light, padding: EdgeInsets.zero,
     viewInsets: EdgeInsets.zero),
    (name: 'large-phone', size: Size(412, 915), scale: 1,
     brightness: Brightness.light, padding: EdgeInsets.zero,
     viewInsets: EdgeInsets.zero),
    (name: 'tablet', size: Size(800, 1200), scale: 1,
     brightness: Brightness.light, padding: EdgeInsets.zero,
     viewInsets: EdgeInsets.zero),
    (name: 'landscape', size: Size(800, 360), scale: 1,
     brightness: Brightness.light, padding: EdgeInsets.zero,
     viewInsets: EdgeInsets.zero),
    (name: 'dark-phone', size: Size(360, 800), scale: 1,
     brightness: Brightness.dark, padding: EdgeInsets.zero,
     viewInsets: EdgeInsets.zero),
    (name: 'font-160', size: Size(360, 800), scale: 1.6,
     brightness: Brightness.light, padding: EdgeInsets.zero,
     viewInsets: EdgeInsets.zero),
    (name: 'font-200', size: Size(360, 800), scale: 2,
     brightness: Brightness.light, padding: EdgeInsets.zero,
     viewInsets: EdgeInsets.zero),
    (name: 'keyboard-250', size: Size(360, 800), scale: 1,
     brightness: Brightness.light, padding: EdgeInsets.only(top: 30, bottom: 24),
     viewInsets: EdgeInsets.only(bottom: 250)),
  ];

  for (final scenario in screens) {
    testWidgets('Design-App pilot: real ObservanceCard ${scenario.name}',
        (tester) async {
      tester.view.physicalSize = scenario.size;
      tester.view.devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(
        MaterialApp(
          locale: const Locale('it'),
          theme: AppTheme.light(),
          darkTheme: AppTheme.dark(),
          themeMode: scenario.brightness == Brightness.dark
              ? ThemeMode.dark : ThemeMode.light,
          supportedLocales: AppLocalizations.supportedLocales,
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          home: MediaQuery(
            data: MediaQueryData(
              size: scenario.size,
              textScaler: TextScaler.linear(scenario.scale),
              padding: scenario.padding,
              viewInsets: scenario.viewInsets,
              disableAnimations: true,
            ),
            child: Scaffold(
              body: SafeArea(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 700),
                    child: ObservanceCard(
                      observance: _pilotRecord,
                      onTap: () {},
                      onFavorite: () {},
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      );
      await tester.pump(const Duration(milliseconds: 350));
      expect(
        find.text(
          'Giornata mondiale per la verifica delle schermate e della navigazione accessibile',
        ),
        findsOneWidget,
      );
      expect(find.byType(ObservanceCard), findsOneWidget);
      expect(tester.takeException(), isNull,
          reason: 'RenderFlex overflow or layout error for ${scenario.name}');
    });
  }

  testWidgets('real card keeps localized favorite and navigation actions',
      (tester) async {
    var opened = 0;
    var favorited = 0;
    await tester.pumpWidget(MaterialApp(
      locale: const Locale('it'),
      theme: AppTheme.light(),
      supportedLocales: AppLocalizations.supportedLocales,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      home: Scaffold(
        body: SingleChildScrollView(
          child: ObservanceCard(
            observance: _pilotRecord,
            onTap: () => opened++,
            onFavorite: () => favorited++,
          ),
        ),
      ),
    ));
    final favorite = find.byTooltip('Aggiungi ai preferiti');
    expect(favorite, findsOneWidget);
    await tester.tap(favorite);
    await tester.pump();
    expect(favorited, 1);
    await tester.tap(find.byType(ObservanceCard));
    expect(opened, 1);
    expect(tester.takeException(), isNull);
  });
}
