final class ObservanceYearOverride {
  const ObservanceYearOverride({
    required this.observanceId,
    required this.year,
    required this.campaignTheme,
    required this.campaignUrl,
    required this.verifiedAt,
    this.notes = const <String>[],
  });

  final String observanceId;
  final int year;
  final String campaignTheme;
  final String campaignUrl;
  final String verifiedAt;
  final List<String> notes;

  factory ObservanceYearOverride.fromJson(Map<String, dynamic> json) =>
      ObservanceYearOverride(
        observanceId: json['observanceId']?.toString() ?? '',
        year: (json['year'] as num?)?.toInt() ?? 0,
        campaignTheme: json['campaignTheme']?.toString() ?? '',
        campaignUrl: json['campaignUrl']?.toString() ?? '',
        verifiedAt: json['verifiedAt']?.toString() ?? '',
        notes: (json['notes'] as List? ?? const [])
            .map((value) => value.toString())
            .where((value) => value.trim().isNotEmpty)
            .toList(growable: false),
      );
}
