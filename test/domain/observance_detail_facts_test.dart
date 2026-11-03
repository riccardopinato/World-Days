import 'package:flutter_test/flutter_test.dart';
import 'package:world_days/domain/observance.dart';
import 'package:world_days/domain/observance_detail_facts.dart';
import 'package:world_days/domain/recurrence_engine.dart';

const authority = ObservanceAuthority(
  name: 'United Nations',
  type: 'UN',
  officiality: 'OFFICIAL_UN',
);

Observance record({
  required List<RecurrenceRule> rules,
  int? year,
  String? source,
}) => Observance(
      id: 'test',
      title: 'Test day',
      periodKind: 'DAY',
      scope: 'GLOBAL',
      countries: const [],
      regions: const [],
      authority: authority,
      sources: const [],
      rules: rules,
      aliases: const [],
      introducedYear: year,
      introducedYearSource: source,
    );

void main() {
  test('date and introduced year remain independent', () {
    final facts = ObservanceDetailFacts.forYear(
      record(
        rules: const [FixedDateRule(month: 11, day: 20)],
        year: 1989,
        source: 'https://www.un.org/en/observances/africa-industrialization-day',
      ),
      2026,
    );
    expect(facts.spans.single.start, DateTime.utc(2026, 11, 20));
    expect(facts.introducedYear, 1989);
    expect(facts.introducedYearSource, isNotEmpty);
  });

  test('unknown introduction stays null, never guessed from recurrence', () {
    final facts = ObservanceDetailFacts.forYear(
      record(rules: const [FixedDateRule(month: 3, day: 22)]),
      2026,
    );
    expect(facts.introducedYear, isNull);
  });

  test('cross-year period remains a single full civil range', () {
    final facts = ObservanceDetailFacts.forYear(
      record(rules: const [
        FixedRangeRule(
          startMonth: 12, startDay: 29, endMonth: 1, endDay: 4,
        ),
      ]),
      2026,
    );
    expect(facts.spans.single.start, DateTime.utc(2026, 12, 29));
    expect(facts.spans.single.end, DateTime.utc(2027, 1, 4));
  });

  test('unverified authority-defined date is not invented', () {
    final facts = ObservanceDetailFacts.forYear(
      record(rules: const [AuthorityDefinedRule(overrides: {})]),
      2026,
    );
    expect(facts.spans, isEmpty);
  });

  test('historic one-off date is still visible after its year', () {
    final facts = ObservanceDetailFacts.forYear(
      record(rules: [
        OneOffRule(span: DateSpan(
          start: DateTime.utc(2024, 2, 29),
          end: DateTime.utc(2024, 2, 29),
        )),
      ]),
      2026,
    );
    expect(facts.spans.single.start, DateTime.utc(2024, 2, 29));
  });
}
