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

  test('reviewed English editorial pack is linked by canonical id', () async {
    final snapshot = await const CatalogRepository().load();

    expect(snapshot.editorialById.length, greaterThanOrEqualTo(28));

    final water = snapshot.editorialById['world-water-day'];
    expect(water, isNotNull);
    expect(water!.locale, 'en');
    expect(water.status, 'REVIEWED');
    expect(water.summary.length, greaterThan(80));
    expect(water.waysToTakePart.length, 3);

    final cancer = snapshot.editorialById['world-cancer-day'];
    expect(cancer, isNotNull);
    expect(cancer!.whyItMatters, isNotEmpty);
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
