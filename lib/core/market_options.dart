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
  MarketOption('CZ', '🇨🇿'),
  MarketOption('SK', '🇸🇰'),
  MarketOption('NO', '🇳🇴'),
  MarketOption('FI', '🇫🇮'),
  MarketOption('SE', '🇸🇪'),
  MarketOption('PL', '🇵🇱'),
  MarketOption('IE', '🇮🇪'),
  MarketOption('NL', '🇳🇱'),
  MarketOption('ZA', '🇿🇦'),
  MarketOption('PH', '🇵🇭'),
  MarketOption('NZ', '🇳🇿'),
  MarketOption('SG', '🇸🇬'),
  MarketOption('KR', '🇰🇷'),
  MarketOption('AR', '🇦🇷'),
  MarketOption('PE', '🇵🇪'),
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
    case 'CZ':
      return l10n.countryCzechia;
    case 'SK':
      return l10n.countrySlovakia;
    case 'NO':
      return l10n.countryNorway;
    case 'FI':
      return l10n.countryFinland;
    case 'SE':
      return l10n.countrySweden;
    case 'PL':
      return l10n.countryPoland;
    case 'IE':
      return l10n.countryIreland;
    case 'NL':
      return l10n.countryNetherlands;
    case 'ZA':
      return l10n.countrySouthAfrica;
    case 'PH':
      return l10n.countryPhilippines;
    case 'NZ':
      return l10n.countryNewZealand;
    case 'SG':
      return l10n.countrySingapore;
    case 'KR':
      return l10n.countrySouthKorea;
    case 'AR':
      return l10n.countryArgentina;
    case 'PE':
      return l10n.countryPeru;
    default:
      return l10n.globalMarket;
  }
}
