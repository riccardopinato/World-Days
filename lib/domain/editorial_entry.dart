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
  });

  final String observanceId;
  final String locale;
  final String status;
  final String summary;
  final String whyItMatters;
  final List<String> waysToTakePart;
  final String lastReviewedAt;
  final String sourcePolicy;

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
      );
}
