final class EditorialEntry {
  const EditorialEntry({
    required this.observanceId,
    required this.locale,
    required this.status,
    required this.summary,
    required this.whyItMatters,
    required this.waysToTakePart,
    required this.lastReviewedAt,
    required this.sourcePolicy,
    this.hook = '',
    this.whyThisDate = '',
    this.origin = '',
    this.quickFacts = const <String>[],
    this.relatedObservanceIds = const <String>[],
  });

  final String observanceId;
  final String locale;
  final String status;
  final String summary;
  final String whyItMatters;
  final List<String> waysToTakePart;
  final String lastReviewedAt;
  final String sourcePolicy;

  /// Optional one-sentence editorial hook. Empty until source-reviewed.
  final String hook;

  /// Explains why the observance falls on this date/rule where documented.
  final String whyThisDate;

  /// Concise origin/history grounded in canonical sources.
  final String origin;

  /// Short source-reviewed facts. Empty is preferable to unsupported filler.
  final List<String> quickFacts;

  /// Canonical observance ids only. Kept separate from arbitrary hyperlinks.
  final List<String> relatedObservanceIds;

  bool get hasExtendedEditorial =>
      hook.trim().isNotEmpty ||
      whyThisDate.trim().isNotEmpty ||
      origin.trim().isNotEmpty ||
      quickFacts.isNotEmpty ||
      relatedObservanceIds.isNotEmpty;

  factory EditorialEntry.fromJson(Map<String, dynamic> json) => EditorialEntry(
        observanceId: json['observanceId'] as String,
        locale: json['locale']?.toString() ?? 'en',
        status: json['status']?.toString() ?? 'DRAFT',
        summary: json['summary']?.toString() ?? '',
        whyItMatters: json['whyItMatters']?.toString() ?? '',
        waysToTakePart: (json['waysToTakePart'] as List? ?? const [])
            .map((value) => value.toString())
            .toList(growable: false),
        lastReviewedAt: json['lastReviewedAt']?.toString() ?? '',
        sourcePolicy: json['sourcePolicy']?.toString() ?? '',
        hook: json['hook']?.toString() ?? '',
        whyThisDate: json['whyThisDate']?.toString() ?? '',
        origin: json['origin']?.toString() ?? '',
        quickFacts: (json['quickFacts'] as List? ?? const [])
            .map((value) => value.toString())
            .where((value) => value.trim().isNotEmpty)
            .toList(growable: false),
        relatedObservanceIds:
            (json['relatedObservanceIds'] as List? ?? const [])
                .map((value) => value.toString())
                .where((value) => value.trim().isNotEmpty)
                .toList(growable: false),
      );
}
