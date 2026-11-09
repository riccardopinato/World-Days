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
  MarketOption('CA', '🇨🇦'),
  MarketOption('AU', '🇦🇺'),
  MarketOption('BR', '🇧🇷'),
  MarketOption('MX', '🇲🇽'),
  MarketOption('IN', '🇮🇳'),
  MarketOption('JP', '🇯🇵'),
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
    case 'CA':
      return l10n.countryCanada;
    case 'AU':
      return l10n.countryAustralia;
    case 'BR':
      return l10n.countryBrazil;
    case 'MX':
      return l10n.countryMexico;
    case 'IN':
      return l10n.countryIndia;
    case 'JP':
      return l10n.countryJapan;
    default:
      return l10n.globalMarket;
  }
}
