import 'observance.dart';

final class VerifiedRecordOverview {
  static const status = 'VERIFIED_METADATA';

  const VerifiedRecordOverview({
    required this.observanceId,
    required this.locale,
    required this.title,
    required this.scope,
    required this.authorityName,
    required this.verifiedAt,
  });

  final String observanceId;
  final String locale;
  final String title;
  final String scope;
  final String authorityName;
  final String verifiedAt;

  factory VerifiedRecordOverview.fromObservance(
    Observance observance,
    String localeCode,
  ) {
    final locale = localeCode.toLowerCase().split(RegExp('[-_]')).first;
    return VerifiedRecordOverview(
      observanceId: observance.id,
      locale: locale,
      title: observance.titleForLocale(locale),
      scope: observance.scope.toUpperCase(),
      authorityName: observance.authority.name,
      verifiedAt: observance.lastVerifiedAt ?? '',
    );
  }
}
