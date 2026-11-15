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

  test('all launch records have six-locale verified concise coverage', () async {
    final snapshot = await const CatalogRepository().load();
    const locales = ['en', 'it', 'es', 'fr', 'de', 'pt'];

    expect(snapshot.editorialById.length, 502);
    for (final item in <String, int>{
      'international-day-of-commemoration-in-memory-of-the-victims-of-the-holocaust': 2005,
      'international-day-of-clean-energy': 2023,
      'world-interfaith-harmony-week': 2010,
      'world-radio-day': 2011,
      'world-day-of-social-justice': 2007,
      'international-day-of-forests': 2012,
      'international-day-for-the-elimination-of-racial-discrimination': 1966,
      'world-poetry-day': 1999,
      'world-down-syndrome-day': 2011,
      'international-day-of-zero-waste': 2022,
      'international-day-of-sport-for-development-and-peace': 2013,
      'world-book-and-copyright-day': 1995,
      'world-press-freedom-day': 1993,
      'world-bee-day': 2017,
      'international-jazz-day': 2011,
    }.entries) {
      final record = snapshot.byId[item.key]!;
      expect(record.introducedYear, item.value);
      expect(record.introducedYearSource, isNotEmpty);
      expect(record.sources.map((source) => source.url),
          contains(record.introducedYearSource));
      final english = snapshot.editorialFor(item.key, 'en')!;
      expect(english.origin, isNotEmpty);
      expect(english.relatedObservanceIds, isNotEmpty);
      for (final locale in <String>['it', 'es', 'fr', 'de', 'pt']) {
        final copy = snapshot.editorialFor(item.key, locale)!;
        expect(copy.locale, locale);
        expect(copy.summary, isNotEmpty);
        expect(copy.origin, isNot(english.origin));
        expect(copy.waysToTakePart, hasLength(2));
        expect(copy.relatedObservanceIds, english.relatedObservanceIds);
      }
    }
    for (final item in <String, int>{
      'international-mother-language-day': 1999,
      'international-day-of-happiness': 2012,
      'world-autism-awareness-day': 2007,
      'international-day-of-families': 1993,
      'world-refugee-day': 2000,
      'international-youth-day': 1999,
      'international-day-of-peace': 1981,
      'international-day-of-democracy': 2007,
      'international-day-of-older-persons': 1990,
      'human-rights-day': 1950,
      'international-day-of-persons-with-disabilities': 1992,
      'international-volunteer-day-for-economic-and-social-development': 1985,
      'international-anti-corruption-day': 2003,
      'international-literacy-day': 1966,
    }.entries) {
      expect(snapshot.byId[item.key]!.introducedYear, item.value);
      expect(snapshot.byId[item.key]!.introducedYearSource, isNotEmpty);
      expect(snapshot.editorialFor(item.key, 'en')!.origin, isNotEmpty);
      for (final locale in <String>['it', 'es', 'fr', 'de', 'pt']) {
        final translated = snapshot.editorialFor(item.key, locale)!;
        expect(translated.locale, locale);
        expect(translated.origin, isNotEmpty);
        expect(translated.origin, isNot(snapshot.editorialFor(item.key, 'en')!.origin));
      }
    }
    for (final item in <String, int>{
      'international-day-of-education': 2018,
      'world-environment-day': 1972,
      'world-oceans-day': 2008,
      'world-wildlife-day': 2013,
    }.entries) {
      expect(snapshot.byId[item.key]!.introducedYear, item.value);
      expect(snapshot.editorialFor(item.key, 'en')!.origin, isNotEmpty);
    }
    expect(
      snapshot.byId['africa-industrialization-day']!.introducedYear,
      1989,
    );
    expect(
      snapshot.byId['world-water-day']!.introducedYear,
      1992,
    );
    expect(
      snapshot.editorialFor('africa-industrialization-day', 'it')!.origin,
      isNotEmpty,
    );

    for (final record in snapshot.records) {
      for (final locale in locales) {
        final metadata = snapshot.verifiedMetadataFor(record.id, locale);
        expect(metadata, isNotNull, reason: '${record.id}/$locale');
        expect(metadata!.locale, locale, reason: '${record.id}/$locale');
        expect(
          metadata.verifiedAt.trim(),
          isNotEmpty,
          reason: '${record.id}/$locale',
        );
        expect(
          metadata.title,
          record.titleForLocale(locale),
          reason: '${record.id}/$locale',
        );
        expect(metadata.authorityName.trim(), isNotEmpty);
        expect(metadata.scope.trim(), isNotEmpty);
      }
    }

    expect(snapshot.editorialFor('world-habitat-day', 'en')?.status,
        'AI_SOURCE_REVIEWED_SIX_LOCALE');
    final english =
        snapshot.verifiedMetadataFor('world-habitat-day', 'en')!;
    final italian =
        snapshot.verifiedMetadataFor('world-habitat-day', 'it')!;
    expect(english.title, isNot(italian.title));
    expect(english.authorityName, isNotEmpty);
  });

  test('173 AI-certified country histories appear in all six locales', () async {
    final snapshot = await const CatalogRepository().load();
    const locales = ['en', 'it', 'es', 'fr', 'de', 'pt'];
    for (final locale in locales) {
      final enriched = snapshot.editorialByLocale[locale]!.values
          .where((entry) => entry.status == 'AI_CERTIFIED');
      expect(enriched.length, 173, reason: locale);
      expect(
        snapshot.editorialFor('ca-raoul-wallenberg-day', locale)!.origin,
        allOf(contains('2001'), contains('2002')),
        reason: locale,
      );
      expect(
        snapshot.editorialFor('kr-hangeul-day', locale)!.origin,
        isNotEmpty,
      );
      expect(
        snapshot.editorialFor(
          'ph-w13-panagyaman-rice-festival-month', locale,
        )!.origin,
        isNotEmpty,
      );
    }
  });

  test('90 additional six-locale source-reviewed articles retain status parity', () async {
    final snapshot = await const CatalogRepository().load();
    const languages = ['en', 'it', 'es', 'fr', 'de', 'pt'];
    for (final lang in languages) {
      final pack = snapshot.editorialByLocale[lang]!;
      expect(pack.values.where(
        (entry) => entry.status == 'AI_SOURCE_REVIEWED_SIX_LOCALE',
      ).length, 90);
      for (final id in <String>[
        'sk-carpathian-dukla-operation-heroes-day',
        'spain-exile-victims-remembrance-day',
        'italian-republic-day',
        'fi-finnish-independence-day',
        'cz-independent-state-restoration',
      ]) {
        final story = snapshot.editorialFor(id, lang)!;
        expect(story.locale, lang);
        expect(story.origin, isNotEmpty);
        expect(story.status, 'AI_SOURCE_REVIEWED_SIX_LOCALE');
      }
    }
  });

  test('183 older source histories have AI-certified six-locale translations', () async {
    final snapshot = await const CatalogRepository().load();
    const languages = <String>['en', 'it', 'es', 'fr', 'de', 'pt'];
    for (final lang in languages) {
      final pack = snapshot.editorialByLocale[lang]!;
      expect(
        pack.values.where((x) => x.status == 'AI_CERTIFIED_TRANSLATION_SIX_LOCALE').length,
        183,
        reason: lang,
      );
      for (final id in <String>[
        'world-wetlands-day',
        'international-day-against-illicit-trafficking-in-cultural-property',
        'world-day-for-glaciers',
        'international-day-of-nowruz',
      ]) {
        final story = snapshot.editorialFor(id, lang);
        expect(story, isNotNull, reason: '$id/$lang');
        expect(story!.status, 'AI_CERTIFIED_TRANSLATION_SIX_LOCALE');
        expect(story.locale, lang);
        expect(story.origin.length, greaterThan(75));
        expect(story.quickFacts.length, greaterThanOrEqualTo(2));
        expect(story.waysToTakePart, isEmpty);
      }
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

  test('PR119 three recovered stories preserve six-locale source chronology', () async {
    final snapshot = await const CatalogRepository().load();
    const ids = <String>[
      'world-day-for-african-and-afrodescendant-culture',
      'international-day-to-combat-islamophobia',
      'international-day-of-the-girl-child',
    ];
    for (final oid in ids) {
      for (final locale in <String>['en', 'it', 'es', 'fr', 'de', 'pt']) {
        final article = snapshot.editorialFor(oid, locale);
        expect(article, isNotNull, reason: '$oid/$locale');
        expect(article!.status, 'AI_SOURCE_REVIEWED_SIX_LOCALE');
        expect(article.origin, isNotEmpty);
        expect(article.quickFacts, hasLength(greaterThanOrEqualTo(2)));
        expect(article.waysToTakePart, isEmpty);
      }
    }
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

    String dateKey(DateTime value) =>
        '${value.year.toString().padLeft(4, '0')}-'
        '${value.month.toString().padLeft(2, '0')}-'
        '${value.day.toString().padLeft(2, '0')}';

    String spanKey(String id, DateSpan span) =>
        '$id|${dateKey(span.start)}|${dateKey(span.end)}';

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
                '${record.id}|$ruleIndex|${dateKey(span.start)}|${dateKey(span.end)}',
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
                '${occurrence.observanceId}|${dateKey(occurrence.start)}|${dateKey(occurrence.end)}',
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
