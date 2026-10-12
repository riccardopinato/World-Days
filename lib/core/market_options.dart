import '../l10n/app_localizations.dart';

final class MarketOption {
  const MarketOption(this.code, this.emoji);

  final String code;
  final String emoji;
}

const marketOptions = <MarketOption>[
  MarketOption('GLOBAL', '🌍'),
  MarketOption('IT', '🇮🇹'),
  MarketOption('ES', '🇪🇸'),
  MarketOption('FR', '🇫🇷'),
  MarketOption('DE', '🇩🇪'),
  MarketOption('PT', '🇵🇹'),
  MarketOption('GB', '🇬🇧'),
  MarketOption('US', '🇺🇸'),
];

String marketLabel(AppLocalizations l10n, String code) {
  switch (code.toUpperCase()) {
    case 'IT':
      return l10n.countryItaly;
    case 'ES':
      return l10n.countrySpain;
    case 'FR':
      return l10n.countryFrance;
    case 'DE':
      return l10n.countryGermany;
    case 'PT':
      return l10n.countryPortugal;
    case 'GB':
      return l10n.countryUnitedKingdom;
    case 'US':
      return l10n.countryUnitedStates;
    default:
      return l10n.globalMarket;
  }
}
