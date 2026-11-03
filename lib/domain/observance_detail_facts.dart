import 'observance.dart';
import 'recurrence_engine.dart';

/// Source-backed date/period and optional introduction year for the detail UI.
///
/// The app never infers a foundation year from a date rule or a resolution
/// number. A missing year is intentionally displayed as '*'.
final class ObservanceDetailFacts {
  const ObservanceDetailFacts({
    required this.spans,
    required this.introducedYear,
    required this.introducedYearSource,
  });

  final List<DateSpan> spans;
  final int? introducedYear;
  final String? introducedYearSource;

  factory ObservanceDetailFacts.forYear(Observance record, int year) {
    final resolution = RecurrenceEngine.resolve(
      year: year,
      rules: record.rules,
    );
    if (resolution.spans.isNotEmpty) {
      return ObservanceDetailFacts(
        spans: resolution.spans,
        introducedYear: record.introducedYear,
        introducedYearSource: record.introducedYearSource,
      );
    }

    // ONE_OFF is historical and may not overlap the current year. Its
    // original date is still factual and should not disappear from detail.
    final historical = <DateSpan>[
      for (final rule in record.rules)
        if (rule is OneOffRule) rule.span,
    ]..sort();
    return ObservanceDetailFacts(
      spans: historical,
      introducedYear: record.introducedYear,
      introducedYearSource: record.introducedYearSource,
    );
  }
}
