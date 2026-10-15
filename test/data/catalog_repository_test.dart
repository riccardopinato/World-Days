import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/data/catalog_repository.dart';
import 'package:world_days/domain/recurrence_engine.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('bundled catalog loads with stable identities', () async {
    final snapshot = await const CatalogRepository().load();
    expect(snapshot.records.length, greaterThanOrEqualTo(260));
    expect(snapshot.byId.length, snapshot.records.length);
    final habitat = snapshot.byId['world-habitat-day'];
    expect(habitat?.title, 'World Habitat Day');
    expect(habitat?.titleForLocale('it'), "Giornata mondiale dell'habitat");
    expect(habitat?.titleForLocale('nl'), 'World Habitat Day');
    expect(habitat?.localizedTitles.keys.toSet(), {
      'en', 'it', 'es', 'fr', 'de', 'pt',
    });
    expect(snapshot.occurrences2026.length, greaterThanOrEqualTo(260));
    expect(
      snapshot.records.every((record) => record.categories.isNotEmpty),
      isTrue,
    );
    expect(
      snapshot.records
          .expand((record) => record.sources)
          .every((source) => source.verifiedAt != null),
      isTrue,
    );
  });

  test('unresolved future dates remain explicit instead of disappearing', () async {
    final repository = const CatalogRepository();
    final snapshot = await repository.load();
    final unresolved = repository.unresolvedForYear(2027, snapshot);

    expect(
      unresolved.map((record) => record.id),
      contains('vesak-the-day-of-the-full-moon'),
    );
  });

  test('reviewed editorial packs keep locale parity and fallback', () async {
    final snapshot = await const CatalogRepository().load();

    expect(snapshot.editorialById.length, greaterThanOrEqualTo(28));
    expect(snapshot.editorialByLocale.keys.toSet(), {
      'en', 'it', 'es', 'fr', 'de', 'pt',
    });

    final english = snapshot.editorialFor('world-water-day', 'en');
    final italian = snapshot.editorialFor('world-water-day', 'it');
    final spanish = snapshot.editorialFor('world-water-day', 'es');
    final fallback = snapshot.editorialFor('world-water-day', 'nl');

    expect(english, isNotNull);
    expect(english!.locale, 'en');
    expect(english.status, 'REVIEWED');

    expect(italian, isNotNull);
    expect(italian!.locale, 'it');
    expect(italian.status, 'REVIEWED_TRANSLATION');
    expect(italian.summary, isNot(english.summary));

    expect(spanish, isNotNull);
    expect(spanish!.locale, 'es');
    expect(spanish.waysToTakePart.length, english.waysToTakePart.length);

    expect(fallback, isNotNull);
    expect(fallback!.locale, 'en');

    for (final locale in ['it', 'es', 'fr', 'de', 'pt']) {
      expect(
        snapshot.editorialByLocale[locale]!.keys.toSet(),
        snapshot.editorialById.keys.toSet(),
        reason: locale,
      );
    }
  });

  test('extended editorial schema and annual override load safely', () async {
    final snapshot = await const CatalogRepository().load();

    final editorial = snapshot.editorialFor('world-health-day', 'en');
    expect(editorial, isNotNull);
    expect(editorial!.hook, isA<String>());
    expect(editorial.whyThisDate, isA<String>());
    expect(editorial.origin, isA<String>());
    expect(editorial.quickFacts, isA<List<String>>());
    expect(editorial.relatedObservanceIds, isA<List<String>>());

    final annual = snapshot.yearOverrideFor('world-health-day', 2026);
    expect(annual, isNotNull);
    expect(annual!.campaignTheme, isNotEmpty);
    expect(annual.campaignUrl, isNotEmpty);
    expect(annual.verifiedAt, isNotEmpty);
    expect(snapshot.yearOverrideFor('world-health-day', 2027), isNull);
  });

  test('remote content pack decoder preserves bundled catalog semantics', () async {
    Future<Map<String, dynamic>> loadJson(String path) async {
      final raw = await rootBundle.loadString(path);
      return Map<String, dynamic>.from(jsonDecode(raw) as Map);
    }

    final seed = await loadJson('assets/data/official_core.json');
    final files = <String, dynamic>{
      'official_core.json': seed,
      'occurrences_2026.json':
          await loadJson('assets/data/occurrences_2026.json'),
      for (final locale in CatalogRepository.editorialLocales)
        'editorial_$locale.json':
            await loadJson('assets/data/editorial_$locale.json'),
    };

    final snapshot = CatalogRepository.decodeContentPack({
      'schemaVersion': 1,
      'packId': 'world-days-catalog',
      'version': seed['datasetVersion'],
      'files': files,
    });

    expect(snapshot.datasetVersion, seed['datasetVersion']);
    expect(snapshot.records.length, greaterThanOrEqualTo(260));
    expect(snapshot.byId['world-water-day'], isNotNull);
    expect(snapshot.editorialFor('world-water-day', 'it'), isNotNull);
  });

  test('remote content pack rejects version drift', () async {
    final raw = await rootBundle.loadString('assets/data/official_core.json');
    final seed = Map<String, dynamic>.from(jsonDecode(raw) as Map);

    expect(
      () => CatalogRepository.decodeContentPack({
        'schemaVersion': 1,
        'packId': 'world-days-catalog',
        'version': 'different-version',
        'files': {
          'official_core.json': seed,
          'occurrences_2026.json': const {'occurrences': []},
          for (final locale in CatalogRepository.editorialLocales)
            'editorial_$locale.json': const {'entries': []},
        },
      }),
      throwsFormatException,
    );
  });

  test('full catalog recurrence acceptance covers 2026 through 2028', () async {
    final repository = const CatalogRepository();
    final snapshot = await repository.load();

    String spanKey(String id, DateSpan span) =>
        '$id|${span.start.toIso8601String()}|${span.end.toIso8601String()}';

    for (final year in [2026, 2027, 2028]) {
      final occurrences = repository.occurrencesForYear(year, snapshot);
      final occurrenceKeys = <String>{};

      for (final occurrence in occurrences) {
        expect(snapshot.byId.containsKey(occurrence.observanceId), isTrue);
        expect(occurrence.end.isBefore(occurrence.start), isFalse);
        final overlapsYear = !occurrence.end.isBefore(DateTime.utc(year, 1, 1)) &&
            !occurrence.start.isAfter(DateTime.utc(year, 12, 31));
        expect(
          overlapsYear,
          isTrue,
          reason:
              '${occurrence.observanceId} does not overlap requested year $year',
        );
        expect(
          occurrenceKeys.add(
            '${occurrence.observanceId}|${occurrence.start.toIso8601String()}|${occurrence.end.toIso8601String()}',
          ),
          isTrue,
          reason: 'duplicate runtime occurrence in $year',
        );
      }

      final perRuleKeys = <String>{};
      for (final record in snapshot.records) {
        for (var ruleIndex = 0;
            ruleIndex < record.rules.length;
            ruleIndex++) {
          final resolution = RecurrenceEngine.resolve(
            year: year,
            rules: [record.rules[ruleIndex]],
          );
          for (final span in resolution.spans) {
            expect(span.end.isBefore(span.start), isFalse);
            expect(
              perRuleKeys.add(
                '${record.id}|$ruleIndex|${span.start.toIso8601String()}|${span.end.toIso8601String()}',
              ),
              isTrue,
              reason:
                  'duplicate occurrence for ${record.id} rule $ruleIndex in $year',
            );
          }
        }
      }

      expect(perRuleKeys, isNotEmpty, reason: 'no catalog rules resolved in $year');

      if (year == 2026) {
        final expectedById = <String, Set<String>>{};
        for (final record in snapshot.records) {
          final resolution = RecurrenceEngine.resolve(
            year: year,
            rules: record.rules,
          );
          expectedById[record.id] = {
            for (final span in resolution.spans) spanKey(record.id, span),
          };
        }

        final actualById = <String, Set<String>>{};
        for (final occurrence in snapshot.occurrences2026) {
          actualById
              .putIfAbsent(occurrence.observanceId, () => <String>{})
              .add(
                '${occurrence.observanceId}|${occurrence.start.toIso8601String()}|${occurrence.end.toIso8601String()}',
              );
        }

        for (final record in snapshot.records) {
          expect(
            actualById[record.id] ?? const <String>{},
            expectedById[record.id],
            reason: '2026 generated occurrence drift for ${record.id}',
          );
        }
      }
    }
  });

  test('cross-year fixed ranges carry into the following year', () {
    const rule = FixedRangeRule(
      startMonth: 12,
      startDay: 30,
      endMonth: 1,
      endDay: 2,
    );

    final resolution =
        RecurrenceEngine.resolve(year: 2027, rules: const [rule]);

    expect(resolution.resolved, isTrue);
    expect(resolution.spans, hasLength(1));
    expect(resolution.spans.single.start, DateTime.utc(2027, 12, 30));
    expect(resolution.spans.single.end, DateTime.utc(2028, 1, 2));
  });

  test('curated consumer records preserve provenance and classification', () async {
    final snapshot = await const CatalogRepository().load();

    final cancer = snapshot.byId['world-cancer-day'];
    expect(cancer, isNotNull);
    expect(cancer!.authority.officiality, 'RECOGNIZED_NGO');
    expect(cancer.sources.single.tier, 'D_ORIGINATOR');

    final emoji = snapshot.byId['world-emoji-day'];
    expect(emoji, isNotNull);
    expect(emoji!.authority.officiality, 'POPULAR');
    expect(emoji.sources.single.tier, 'D_ORIGINATOR');

    final safer = snapshot.byId['safer-internet-day'];
    expect(safer, isNotNull);
    expect(safer!.authority.officiality, 'OFFICIAL_INSTITUTIONAL');

    final saferDates = snapshot.occurrences2026
        .where((item) => item.observanceId == 'safer-internet-day')
        .map((item) => item.start.toIso8601String().substring(0, 10))
        .toList(growable: false);
    expect(saferDates, ['2026-02-10']);
  });
}
