final class ObservanceOccurrence {
  const ObservanceOccurrence({
    required this.observanceId,
    required this.start,
    required this.end,
  });

  final String observanceId;
  final DateTime start;
  final DateTime end;

  factory ObservanceOccurrence.fromJson(Map<String, dynamic> json) =>
      ObservanceOccurrence(
        observanceId: json['observanceId'] as String,
        start: DateTime.parse(json['startDate'] as String),
        end: DateTime.parse(json['endDate'] as String),
      );

  bool contains(DateTime date) {
    final d = DateTime(date.year, date.month, date.day);
    final s = DateTime(start.year, start.month, start.day);
    final e = DateTime(end.year, end.month, end.day);
    return !d.isBefore(s) && !d.isAfter(e);
  }
}
