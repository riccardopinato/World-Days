import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/domain/observance.dart';
import 'package:world_days/domain/related_observances.dart';

Observance sample(String id, List<String> categories,
    {String authorityName = 'UN'}) {
  return Observance(
    id: id,
    title: id,
    periodKind: 'DAY',
    scope: 'GLOBAL',
    countries: const [],
    regions: const [],
    authority: ObservanceAuthority(
      name: authorityName,
      type: 'UN',
      officiality: 'OFFICIAL_UN',
    ),
    sources: const [],
    rules: const [],
    aliases: const [],
    categories: categories,
  );
}

void main() {
  final today = sample('today', ['PLANET']);
  final records = [
    today,
    sample('ocean', ['PLANET']),
    sample('forest', ['PLANET']),
    sample('health', ['HEALTH']),
    sample('climate', ['PLANET']),
    sample('wildlife', ['PLANET']),
  ];

  test('curated IDs are ordered first, deduplicated, never self', () {
    final result = RelatedObservances.suggest(
      current: today,
      records: records,
      curatedIds: ['ocean', 'ocean', 'today', 'missing'],
    );
    expect(result, hasLength(3));
    expect(result.first.id, 'ocean');
    expect(result.map((item) => item.id).toSet().length, 3);
    expect(result.any((item) => item.id == today.id), isFalse);
  });

  test('same category outranks unrelated reviewed content', () {
    final result = RelatedObservances.suggest(
      current: today,
      records: records,
      reviewedIds: {'health'},
    );
    expect(result.take(3).every((x) => x.categories.contains('PLANET')),
        isTrue);
  });

  test('deterministic, bounded and works without a reviewed story', () {
    final first = RelatedObservances.suggest(
      current: today,
      records: records,
      limit: 3,
    );
    final second = RelatedObservances.suggest(
      current: today,
      records: records.reversed,
      limit: 3,
    );
    expect(first.map((e) => e.id), second.map((e) => e.id));
    expect(first, hasLength(3));
    expect(RelatedObservances.suggest(
      current: today,
      records: records,
      limit: 0,
    ), isEmpty);
  });

  test('one-record catalog has no suggestions', () {
    expect(RelatedObservances.suggest(
      current: today,
      records: [today],
    ), isEmpty);
  });
}
