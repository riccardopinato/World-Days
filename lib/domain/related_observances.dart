import 'observance.dart';

/// Local, deterministic, privacy-preserving discovery based only on the
/// factual catalog and explicitly curated editorial relationships.
///
/// No network, personalization profile, engagement manipulation or ads.
/// Reviewed stories receive a small boost only within relevant subjects.
final class RelatedObservances {
  const RelatedObservances._();

  static List<Observance> suggest({
    required Observance current,
    required Iterable<Observance> records,
    Iterable<String> curatedIds = const <String>[],
    Set<String> reviewedIds = const <String>{},
    int limit = 3,
  }) {
    if (limit <= 0) return const <Observance>[];
    final byId = <String, Observance>{
      for (final record in records) record.id: record,
    };
    final result = <Observance>[];
    final seen = <String>{current.id};

    for (final id in curatedIds) {
      final match = byId[id];
      if (match != null && seen.add(id)) {
        result.add(match);
        if (result.length == limit) return result;
      }
    }

    final candidates = byId.values.where((item) => !seen.contains(item.id))
        .toList(growable: false);
    final categories = current.categories.toSet();

    int score(Observance candidate) {
      final overlap = candidate.categories
          .where(categories.contains)
          .length;
      final sameAuthority = candidate.authority.name == current.authority.name;
      return overlap * 30 +
          (reviewedIds.contains(candidate.id) ? 5 : 0) +
          (sameAuthority ? 2 : 0);
    }

    // Rotating stable tie-break avoids recommending the same alphabetical
    // three entries from each category on every page.
    int stableRotation(String candidateId) {
      final joined = '${current.id}/$candidateId';
      var hash = 7;
      for (final unit in joined.codeUnits) {
        hash = (hash * 31 + unit) % 2147483647;
      }
      return hash;
    }

    candidates.sort((a, b) {
      final byScore = score(b).compareTo(score(a));
      if (byScore != 0) return byScore;
      final rotated = stableRotation(a.id).compareTo(stableRotation(b.id));
      return rotated == 0 ? a.id.compareTo(b.id) : rotated;
    });
    for (final candidate in candidates) {
      if (seen.add(candidate.id)) result.add(candidate);
      if (result.length == limit) break;
    }
    return result;
  }
}
