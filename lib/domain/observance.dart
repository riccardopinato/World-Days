import 'recurrence_engine.dart';

final class ObservanceSource {
  const ObservanceSource({required this.tier, required this.url});
  final String tier;
  final String url;

  factory ObservanceSource.fromJson(Map<String, dynamic> json) => ObservanceSource(
        tier: json['tier']?.toString() ?? 'UNKNOWN',
        url: json['url']?.toString() ?? '',
      );
}

final class ObservanceAuthority {
  const ObservanceAuthority({
    required this.name,
    required this.type,
    required this.officiality,
    this.resolution,
  });

  final String name;
  final String type;
  final String officiality;
  final String? resolution;

  factory ObservanceAuthority.fromJson(Map<String, dynamic> json) =>
      ObservanceAuthority(
        name: json['name']?.toString() ?? 'Unknown',
        type: json['type']?.toString() ?? 'OTHER',
        officiality: json['officiality']?.toString() ?? 'UNKNOWN',
        resolution: json['resolution']?.toString(),
      );
}

final class Observance {
  const Observance({
    required this.id,
    required this.title,
    required this.periodKind,
    required this.scope,
    required this.countries,
    required this.regions,
    required this.authority,
    required this.sources,
    required this.rules,
    required this.aliases,
    this.categories = const [],
    this.localizedTitles = const {},
    this.visualKey,
  });

  final String id;
  final String title;
  final String periodKind;
  final String scope;
  final List<String> countries;
  final List<String> regions;
  final ObservanceAuthority authority;
  final List<ObservanceSource> sources;
  final List<RecurrenceRule> rules;
  final List<String> aliases;
  final List<String> categories;
  final Map<String, String> localizedTitles;
  final String? visualKey;

  String titleForLocale(String? localeCode) {
    final normalized = (localeCode ?? '')
        .toLowerCase()
        .split(RegExp('[-_]'))
        .first;
    if (normalized.isEmpty || normalized == 'en') return title;
    final localized = localizedTitles[normalized]?.trim();
    return localized == null || localized.isEmpty ? title : localized;
  }

  Iterable<String> get searchableTitles sync* {
    yield title;
    yield* localizedTitles.values;
  }

  factory Observance.fromJson(Map<String, dynamic> json) => Observance(
        id: json['id'] as String,
        title: json['canonicalTitleEn'] as String,
        periodKind: json['periodKind']?.toString() ?? 'DAY',
        scope: json['scope']?.toString() ?? 'GLOBAL',
        countries: (json['countries'] as List? ?? const [])
            .map((e) => e.toString().toUpperCase())
            .toList(growable: false),
        regions: (json['regions'] as List? ?? const [])
            .map((e) => e.toString())
            .toList(growable: false),
        authority: ObservanceAuthority.fromJson(
          Map<String, dynamic>.from(json['authority'] as Map),
        ),
        sources: (json['sources'] as List? ?? const [])
            .map((e) => ObservanceSource.fromJson(Map<String, dynamic>.from(e as Map)))
            .toList(growable: false),
        rules: (json['recurrenceRules'] as List? ?? const [])
            .map((e) => recurrenceRuleFromJson(Map<String, dynamic>.from(e as Map)))
            .toList(growable: false),
        aliases: (json['aliases'] as List? ?? const [])
            .map((e) => e.toString())
            .toList(growable: false),
        categories: (json['categories'] as List? ?? const [])
            .map((e) => e.toString())
            .toList(growable: false),
        localizedTitles: (json['localizedTitles'] as Map? ?? const {})
            .map(
              (key, value) => MapEntry(
                key.toString().toLowerCase(),
                value.toString(),
              ),
            ),
        visualKey: json['visualKey']?.toString(),
      );
}

RecurrenceRule recurrenceRuleFromJson(Map<String, dynamic> json) {
  switch (json['kind']) {
    case 'FIXED_DATE':
      return FixedDateRule(month: json['month'] as int, day: json['day'] as int);
    case 'NTH_WEEKDAY':
      return NthWeekdayRule(
        month: json['month'] as int,
        weekday: json['weekday'] as int,
        occurrence: json['occurrence'] as int,
      );
    case 'LAST_WEEKDAY':
      return LastWeekdayRule(
        month: json['month'] as int,
        weekday: json['weekday'] as int,
      );
    case 'LAST_DAY_OF_MONTH':
      return LastDayOfMonthRule(
        month: json['month'] as int,
      );
    case 'FIXED_RANGE':
      return FixedRangeRule(
        startMonth: json['startMonth'] as int,
        startDay: json['startDay'] as int,
        endMonth: json['endMonth'] as int,
        endDay: json['endDay'] as int,
      );
    case 'LUNAR':
      return LunarRule(overrides: _parseOverrides(json['overrides']));
    case 'AUTHORITY_DEFINED':
      return AuthorityDefinedRule(overrides: _parseOverrides(json['overrides']));
    case 'ONE_OFF':
      return OneOffRule(span: _parseOneOff(json));
    default:
      throw FormatException('Unsupported recurrence kind: ${json['kind']}');
  }
}

Map<int, DateSpan> _parseOverrides(Object? raw) {
  if (raw is! Map) return const {};
  final result = <int, DateSpan>{};
  for (final entry in raw.entries) {
    final year = int.tryParse(entry.key.toString());
    if (year == null || entry.value is! Map) continue;
    final value = Map<String, dynamic>.from(entry.value as Map);
    final start = DateTime.tryParse(value['startDate']?.toString() ?? '');
    final end = DateTime.tryParse(value['endDate']?.toString() ?? '');
    if (start != null && end != null) {
      result[year] = DateSpan(
        start: DateTime.utc(start.year, start.month, start.day),
        end: DateTime.utc(end.year, end.month, end.day),
      );
    }
  }
  return result;
}


DateSpan _parseOneOff(Map<String, dynamic> json) {
  final start = DateTime.tryParse(json['startDate']?.toString() ?? '');
  final end = DateTime.tryParse(
    json['endDate']?.toString() ?? json['startDate']?.toString() ?? '',
  );
  if (start == null || end == null) {
    throw const FormatException('ONE_OFF requires startDate/endDate');
  }
  final startDay = DateTime.utc(start.year, start.month, start.day);
  final endDay = DateTime.utc(end.year, end.month, end.day);
  if (endDay.isBefore(startDay)) {
    throw const FormatException('ONE_OFF endDate precedes startDate');
  }
  return DateSpan(start: startDay, end: endDay);
}
