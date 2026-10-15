import 'dart:convert';

import 'package:flutter/services.dart';

import '../domain/editorial_entry.dart';
import '../domain/observance.dart';
import '../domain/occurrence.dart';
import '../domain/recurrence_engine.dart';
import '../domain/year_override.dart';
import '../domain/verified_record_overview.dart';

final class CatalogSnapshot {
  const CatalogSnapshot({
    required this.records,
    required this.byId,
    required this.occurrences2026,
    required this.editorialByLocale,
    required this.yearOverrides,
    required this.datasetVersion,
  });

  final List<Observance> records;
  final Map<String, Observance> byId;
  final List<ObservanceOccurrence> occurrences2026;
  final Map<String, Map<String, EditorialEntry>> editorialByLocale;
  final List<ObservanceYearOverride> yearOverrides;
  final String datasetVersion;

  Map<String, EditorialEntry> get editorialById =>
      editorialByLocale['en'] ?? const <String, EditorialEntry>{};

  EditorialEntry? editorialFor(String observanceId, String localeCode) {
    final normalized = localeCode.toLowerCase();
    return editorialByLocale[normalized]?[observanceId] ??
        editorialByLocale['en']?[observanceId];
  }

  VerifiedRecordOverview? verifiedMetadataFor(
    String observanceId,
    String localeCode,
  ) {
    final record = byId[observanceId];
    if (record == null) return null;
    return VerifiedMetadataSummary.forObservance(record, localeCode);
  }

  bool hasRichEditorial(String observanceId) =>
      editorialByLocale['en']?.containsKey(observanceId) ?? false;

  ObservanceYearOverride? yearOverrideFor(String observanceId, int year) {
    for (final item in yearOverrides) {
      if (item.observanceId == observanceId && item.year == year) return item;
    }
    return null;
  }
}

final class CatalogRepository {
  const CatalogRepository();

  static const editorialLocales = ['en', 'it', 'es', 'fr', 'de', 'pt'];

  Future<CatalogSnapshot> load({
    Map<String, dynamic>? contentPack,
  }) async {
    if (contentPack != null) {
      return decodeContentPack(contentPack);
    }

    final seed = await _bundleJson('assets/data/official_core.json');
    final occurrence =
        await _bundleJson('assets/data/occurrences_2026.json');
    final editorial = <String, Map<String, dynamic>>{};
    for (final locale in editorialLocales) {
      editorial[locale] =
          await _bundleJson('assets/data/editorial_$locale.json');
    }
    return _decodeSnapshot(
      seed: seed,
      occurrence: occurrence,
      editorial: editorial,
    );
  }

  static void validateContentPackPayload(Map<String, dynamic> payload) {
    decodeContentPack(payload);
  }

  static CatalogSnapshot decodeContentPack(Map<String, dynamic> payload) {
    if ((payload['schemaVersion'] as num?)?.toInt() != 1 ||
        payload['packId']?.toString() != 'world-days-catalog') {
      throw const FormatException('unsupported_world_days_content_pack');
    }

    final rawFiles = payload['files'];
    if (rawFiles is! Map) {
      throw const FormatException('content_pack_files_missing');
    }
    final files = Map<String, dynamic>.from(rawFiles);

    Map<String, dynamic> requiredFile(String name) {
      final value = files[name];
      if (value is! Map) {
        throw FormatException('content_pack_file_missing:$name');
      }
      return Map<String, dynamic>.from(value);
    }

    final seed = requiredFile('official_core.json');
    final payloadVersion = payload['version']?.toString() ?? '';
    final seedVersion = seed['datasetVersion']?.toString() ?? '';
    if (payloadVersion.isEmpty || payloadVersion != seedVersion) {
      throw const FormatException('content_pack_version_mismatch');
    }

    final editorial = <String, Map<String, dynamic>>{};
    for (final locale in editorialLocales) {
      editorial[locale] = requiredFile('editorial_$locale.json');
    }

    return _decodeSnapshot(
      seed: seed,
      occurrence: requiredFile('occurrences_2026.json'),
      editorial: editorial,
    );
  }

  static Future<Map<String, dynamic>> _bundleJson(String path) async {
    final raw = await rootBundle.loadString(path);
    final decoded = jsonDecode(raw);
    if (decoded is! Map) {
      throw FormatException('bundle_json_not_object:$path');
    }
    return Map<String, dynamic>.from(decoded);
  }

  static CatalogSnapshot _decodeSnapshot({
    required Map<String, dynamic> seed,
    required Map<String, dynamic> occurrence,
    required Map<String, Map<String, dynamic>> editorial,
  }) {
    final rawRecords = seed['records'];
    if (rawRecords is! List || rawRecords.isEmpty) {
      throw const FormatException('catalog_records_missing');
    }
    final records = rawRecords
        .map((e) => Observance.fromJson(Map<String, dynamic>.from(e as Map)))
        .toList(growable: false)
      ..sort((a, b) => a.title.compareTo(b.title));

    final ids = <String>{};
    for (final record in records) {
      if (!ids.add(record.id)) {
        throw FormatException('duplicate_observance_id:${record.id}');
      }
      if (record.sources.isEmpty) {
        throw FormatException('observance_sources_missing:${record.id}');
      }
      if (record.lastVerifiedAt?.trim().isNotEmpty != true) {
        throw FormatException(
          'observance_last_verified_missing:${record.id}',
        );
      }
      if (record.rules.isEmpty) {
        throw FormatException('observance_rules_missing:${record.id}');
      }
      for (final source in record.sources) {
        if (source.url.trim().isEmpty ||
            source.verifiedAt?.trim().isNotEmpty != true) {
          throw FormatException(
            'observance_source_verification_missing:${record.id}',
          );
        }
      }
    }

    final yearOverrides = (seed['yearOverrides'] as List? ?? const [])
        .map(
          (e) => ObservanceYearOverride.fromJson(
            Map<String, dynamic>.from(e as Map),
          ),
        )
        .where((item) => item.observanceId.isNotEmpty && item.year > 0)
        .toList(growable: false);

    final byId = {for (final item in records) item.id: item};

    final rawOccurrences = occurrence['occurrences'];
    if (rawOccurrences is! List) {
      throw const FormatException('catalog_occurrences_missing');
    }
    final occurrences = rawOccurrences
        .map(
          (e) => ObservanceOccurrence.fromJson(
            Map<String, dynamic>.from(e as Map),
          ),
        )
        .toList(growable: false)
      ..sort((a, b) => a.start.compareTo(b.start));

    for (final item in occurrences) {
      if (!byId.containsKey(item.observanceId)) {
        throw FormatException(
          'occurrence_unknown_observance:${item.observanceId}',
        );
      }
    }

    final editorialByLocale = <String, Map<String, EditorialEntry>>{};
    for (final locale in editorialLocales) {
      final payload = editorial[locale];
      if (payload == null) {
        throw FormatException('editorial_locale_missing:$locale');
      }
      final entries = (payload['entries'] as List? ?? const [])
          .map(
            (e) => EditorialEntry.fromJson(
              Map<String, dynamic>.from(e as Map),
            ),
          )
          .toList(growable: false);
      for (final item in entries) {
        if (!byId.containsKey(item.observanceId)) {
          throw FormatException(
            'editorial_unknown_observance:${item.observanceId}',
          );
        }
      }
      editorialByLocale[locale] = {
        for (final item in entries) item.observanceId: item,
      };
    }

    return CatalogSnapshot(
      records: records,
      byId: byId,
      occurrences2026: occurrences,
      editorialByLocale: editorialByLocale,
      yearOverrides: yearOverrides,
      datasetVersion: seed['datasetVersion']?.toString() ?? 'bundled',
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
      final resolution = RecurrenceEngine.resolve(
        year: year,
        rules: record.rules,
      );
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
