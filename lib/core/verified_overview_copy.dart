import '../domain/verified_record_overview.dart';
import '../l10n/app_localizations.dart';

String verifiedOverviewCopy(
  AppLocalizations l10n,
  VerifiedRecordOverview overview,
) {
  final scope = switch (overview.scope) {
    'NATIONAL' => l10n.verifiedScopeNational,
    'REGIONAL' => l10n.verifiedScopeRegional,
    _ => l10n.verifiedScopeGlobal,
  };
  return l10n.verifiedOverviewSummary(
    overview.title,
    scope,
    overview.authorityName,
  );
}
