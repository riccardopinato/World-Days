import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/data/catalog_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('bundled catalog loads with stable identities', () async {
    final snapshot = await const CatalogRepository().load();
    expect(snapshot.records.length, greaterThanOrEqualTo(260));
    expect(snapshot.byId.length, snapshot.records.length);
    expect(snapshot.byId['world-habitat-day']?.title, 'World Habitat Day');
    expect(snapshot.occurrences2026.length, greaterThanOrEqualTo(260));
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
