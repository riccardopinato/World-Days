import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:world_days/core/visual/observance_visuals.dart';
import 'package:world_days/core/widgets/observance_hero.dart';
import 'package:world_days/core/widgets/world_days_share_card.dart';
import 'package:world_days/domain/observance.dart';

const _authority = ObservanceAuthority(
  name: 'United Nations',
  type: 'UN',
  officiality: 'OFFICIAL_UN',
);

const _water = Observance(
  id: 'world-water-day',
  title: 'World Water Day',
  periodKind: 'DAY',
  scope: 'GLOBAL',
  countries: [],
  regions: [],
  authority: _authority,
  sources: [],
  rules: [],
  aliases: [],
  categories: ['WATER', 'ENVIRONMENT'],
  localizedTitles: {
    'it': 'Giornata mondiale dell’acqua',
  },
  visualKey: 'planet',
);

void main() {
  test('explicit visual key resolves to canonical style', () {
    expect(ObservanceVisuals.resolve(_water).key, 'planet');
  });

  test('legacy record falls back to deterministic visual inference', () {
    const record = Observance(
      id: 'world-heart-day',
      title: 'World Heart Day',
      periodKind: 'DAY',
      scope: 'GLOBAL',
      countries: [],
      regions: [],
      authority: _authority,
      sources: [],
      rules: [],
      aliases: [],
    );

    expect(ObservanceVisuals.resolve(record).key, 'health');
  });

  testWidgets('hero survives large text scale without layout exceptions',
      (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: MediaQuery(
            data: MediaQueryData(
              size: Size(390, 844),
              textScaler: TextScaler.linear(2),
            ),
            child: SingleChildScrollView(
              padding: EdgeInsets.all(20),
              child: ObservanceHero(
                observance: _water,
                eyebrow: 'Sunday',
                subtitle: '12 day streak',
                accentText: '22',
              ),
            ),
          ),
        ),
      ),
    );

    expect(find.text('World Water Day'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets('share card renders at large text scale', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: MediaQuery(
            data: MediaQueryData(
              size: Size(390, 844),
              textScaler: TextScaler.linear(1.6),
            ),
            child: Center(
              child: SizedBox(
                width: 320,
                child: WorldDaysShareCard(
                  observance: _water,
                ),
              ),
            ),
          ),
        ),
      ),
    );

    expect(find.text('WORLD DAYS'), findsOneWidget);
    expect(find.text('World Water Day'), findsOneWidget);
    expect(find.text('Official'), findsNothing);
    expect(tester.takeException(), isNull);
  });

  testWidgets('hero uses the active locale title', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        locale: Locale('it'),
        supportedLocales: [
          Locale('en'),
          Locale('it'),
        ],
        localizationsDelegates: GlobalMaterialLocalizations.delegates,
        home: Scaffold(
          body: SizedBox(
            width: 390,
            child: ObservanceHero(
              observance: _water,
              eyebrow: 'Domenica',
            ),
          ),
        ),
      ),
    );

    expect(find.text('Giornata mondiale dell’acqua'), findsOneWidget);
    expect(find.text('World Water Day'), findsNothing);
    expect(tester.takeException(), isNull);
  });
}
