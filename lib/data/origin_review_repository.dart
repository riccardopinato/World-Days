import 'dart:convert';

import 'package:flutter/services.dart';

/// Published, offline source-research ledger. Not every canonical observance
/// has an independently reviewed history: an absent rich story stays absent.
final class OriginReviewRepository {
  OriginReviewRepository._();

  static Future<Map<String, Map<String, dynamic>>>? _cache;

  static Future<Map<String, Map<String, dynamic>>> load() =>
      _cache ??= _read();

  static Future<Map<String, Map<String, dynamic>>> _read() async {
    final raw = await rootBundle.loadString('assets/data/origin_review_index.json');
    final data = jsonDecode(raw) as Map<String, dynamic>;
    if (data['schemaVersion'] != 1 ||
        data['recordCount'] != (data['records'] as List).length ||
        data['coverage'] != 'ALL_CANONICAL_ACCOUNTED_FOR_NOT_ALL_HISTORIES_CERTIFIED') {
      throw const FormatException('origin_research_ledger_invalid');
    }
    final items = <String, Map<String, dynamic>>{};
    for (final entry in data['records'] as List) {
      final item = Map<String, dynamic>.from(entry as Map);
      final id = item['observanceId'] as String;
      if (items.containsKey(id)) {
        throw FormatException('duplicate_origin_research_id:$id');
      }
      items[id] = item;
    }
    return Map.unmodifiable(items);
  }
}
