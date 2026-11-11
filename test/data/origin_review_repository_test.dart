import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/data/origin_review_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('1111 canonical source ledger entries remain unique and complete', () async {
    final entries = await OriginReviewRepository.load();
    expect(entries.length, 1111);
    expect(entries.keys.toSet().length, entries.length);
    expect(entries.values.where((e) =>
        e['originResearchStatus'] == 'PRIMARY_RESEARCHED_ORIGIN_IT_EN').length, 4);
    expect(entries.values.where((e) => e['primaryResearch'] == null).length, 1107);
  });

  test('Irish Brigid statutory holiday has a documented history distinct from traditional feast', () async {
    final entries = await OriginReviewRepository.load();
    final publicDay = entries['ie-w13-eures-st-brigid-s-day']!;
    expect(publicDay['introducedYear'], 2023);
    final research = publicDay['primaryResearch'] as Map;
    final languages = research['locale'] as Map;
    expect((languages['it'] as Map)['origin'].toString(), contains('2023'));
    expect((languages['en'] as Map)['origin'].toString(),
        contains('first Monday'));
    expect(entries['ie-st-brigids-day'], isNotNull);
    expect(entries['ie-st-brigids-day']!['primaryResearch'], isNull);
  });

  test('all editorial rich facts have source URLs and fallback transparency', () async {
    final entries = await OriginReviewRepository.load();
    for (final entry in entries.values) {
      final research = entry['primaryResearch'];
      if (research == null) continue;
      final r = research as Map;
      expect((r['sourceUrls'] as List).isNotEmpty, isTrue);
      expect((r['locale'] as Map).keys.toSet(), {'it', 'en'});
      expect(entry['editorialTranslationStatus'],
          'IT_EN_RESEARCHED_OTHERS_FALLBACK_EN');
    }
  });
}
