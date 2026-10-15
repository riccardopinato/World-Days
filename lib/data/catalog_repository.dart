import 'dart:convert';

import 'package:flutter/services.dart';

import '../domain/editorial_entry.dart';
import '../domain/observance.dart';
import '../domain/occurrence.dart';
import '../domain/recurrence_engine.dart';

final class CatalogSnapshot {
  const CatalogSnapshot({
    required this.records,
    required this.byId,
    required this.occurrences2026,
    required this.editorialByLocale,
  });

  final List<Observance> records;
  final Map<String, Observance> byId;
  final List<ObservanceOccurrence> occurrences2026;
  final Map<String, Map<String, EditorialEntry>> editorialByLocale;

  Map<String, EditorialEntry> get editorialById =>
      editorialByLocale['en'] ?? const <String, EditorialEntry>{};

  EditorialEntry? editorialFor(String observanceId, String localeCode) {
    final normalized = localeCode.toLowerCase();
    return editorialByLocale[normalized]?[observanceId] ??
        editorialByLocale['en']?[observanceId];
  }
}

final class CatalogRepository {
  const CatalogRepository();

  Future<CatalogSnapshot> load() async {
    final seedRaw = await rootBundle.loadString('assets/data/official_core.json');
    final occurrenceRaw = await rootBundle.loadString('assets/data/occurrences_2026.json');
    const editorialLocales = ['en', 'it', 'es', 'fr', 'de', 'pt'];
    final editorialRaw = <String, String>{};
    for (final locale in editorialLocales) {
      editorialRaw[locale] = await rootBundle.loadString(
        'assets/data/editorial_$locale.json',
      );
    }

    final seed = jsonDecode(seedRaw) as Map<String, dynamic>;
    final occurrence = jsonDecode(occurrenceRaw) as Map<String, dynamic>;

    final records = (seed['records'] as List)
        .map((e) => Observance.fromJson(Map<String, dynamic>.from(e as Map)))
        .toList(growable: false)
      ..sort((a, b) => a.title.compareTo(b.title));

    final byId = {for (final item in records) item.id: item};
    final occurrences = (occurrence['occurrences'] as List)
        .map((e) => ObservanceOccurrence.fromJson(Map<String, dynamic>.from(e as Map)))
        .toList(growable: false)
      ..sort((a, b) => a.start.compareTo(b.start));

    final editorialByLocale = <String, Map<String, EditorialEntry>>{};
    for (final locale in editorialLocales) {
      final payload =
          jsonDecode(editorialRaw[locale]!) as Map<String, dynamic>;
      final entries = (payload['entries'] as List? ?? const [])
          .map(
            (e) => EditorialEntry.fromJson(
              Map<String, dynamic>.from(e as Map),
            ),
          )
          .toList(growable: false);
      editorialByLocale[locale] = {
        for (final item in entries) item.observanceId: item,
      };
    }

    return CatalogSnapshot(
      records: records,
      byId: byId,
      occurrences2026: occurrences,
      editorialByLocale: editorialByLocale,
    );
  }


  List<Observance> unresolvedForYear(
    int year,
    CatalogSnapshot snapshot,
  ) {
    final result = <Observance>[];
    for (final record in snapshot.records) {
      final resolution = RecurrenceEngine.resolve(
        year: year,
        rules: record.rules,
      );
      if (!resolution.resolved) result.add(record);
    }
    return result;
  }

  List<ObservanceOccurrence> occurrencesForYear(
    int year,
    CatalogSnapshot snapshot,
  ) {
    if (year == 2026) return snapshot.occurrences2026;

    final result = <ObservanceOccurrence>[];
    for (final record in snapshot.records) {
      final resolution = RecurrenceEngine.resolve(year: year, rules: record.rules);
      for (final span in resolution.spans) {
        result.add(
          ObservanceOccurrence(
            observanceId: record.id,
            start: span.start,
            end: span.end,
          ),
        );
      }
    }
    result.sort((a, b) => a.start.compareTo(b.start));
    return result;
  }
}
