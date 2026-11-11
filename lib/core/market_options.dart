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
  MarketOption('MT', '🇲🇹'),
  MarketOption('HR', '🇭🇷'),
  MarketOption('CY', '🇨🇾'),
  MarketOption('EE', '🇪🇪'),
  MarketOption('LV', '🇱🇻'),
  MarketOption('LT', '🇱🇹'),
  MarketOption('IS', '🇮🇸'),
  MarketOption('LU', '🇱🇺'),
  MarketOption('CU', '🇨🇺'),
  MarketOption('HT', '🇭🇹'),
  MarketOption('SD', '🇸🇩'),
  MarketOption('MM', '🇲🇲'),
  MarketOption('NR', '🇳🇷'),
  MarketOption('LK', '🇱🇰'),
  MarketOption('GD', '🇬🇩'),
  MarketOption('IR', '🇮🇷'),
  MarketOption('RS', '🇷🇸'),
  MarketOption('GM', '🇬🇲'),
  MarketOption('LC', '🇱🇨'),
  MarketOption('BN', '🇧🇳'),
  MarketOption('GY', '🇬🇾'),
  MarketOption('KW', '🇰🇼'),
  MarketOption('DO', '🇩🇴'),
  MarketOption('BG', '🇧🇬'),
  MarketOption('GH', '🇬🇭'),
  MarketOption('MU', '🇲🇺'),
  MarketOption('TN', '🇹🇳'),
  MarketOption('NA', '🇳🇦'),
  MarketOption('PK', '🇵🇰'),
  MarketOption('GR', '🇬🇷'),
  MarketOption('BD', '🇧🇩'),
  MarketOption('SN', '🇸🇳'),
  MarketOption('ZW', '🇿🇼'),
  MarketOption('TZ', '🇹🇿'),
  MarketOption('SL', '🇸🇱'),
  MarketOption('TG', '🇹🇬'),
  MarketOption('MH', '🇲🇭'),
  MarketOption('PY', '🇵🇾'),
  MarketOption('CM', '🇨🇲'),
  MarketOption('TL', '🇹🇱'),
  MarketOption('YE', '🇾🇪'),
  MarketOption('EC', '🇪🇨'),
  MarketOption('ER', '🇪🇷'),
  MarketOption('JO', '🇯🇴'),
  MarketOption('GE', '🇬🇪'),
  MarketOption('AZ', '🇦🇿'),
  MarketOption('ET', '🇪🇹'),
  MarketOption('WS', '🇼🇸'),
  MarketOption('RU', '🇷🇺'),
  MarketOption('SC', '🇸🇨'),
  MarketOption('MZ', '🇲🇿'),
  MarketOption('SI', '🇸🇮'),
  MarketOption('MG', '🇲🇬'),
  MarketOption('DJ', '🇩🇯'),
  MarketOption('CD', '🇨🇩'),
  MarketOption('BI', '🇧🇮'),
  MarketOption('SO', '🇸🇴'),
  MarketOption('BY', '🇧🇾'),
  MarketOption('CV', '🇨🇻'),
  MarketOption('RW', '🇷🇼'),
  MarketOption('VE', '🇻🇪'),
  MarketOption('KM', '🇰🇲'),
  MarketOption('MW', '🇲🇼'),
  MarketOption('SB', '🇸🇧'),
  MarketOption('SS', '🇸🇸'),
  MarketOption('BS', '🇧🇸'),
  MarketOption('MN', '🇲🇳'),
  MarketOption('KI', '🇰🇮'),
  MarketOption('ST', '🇸🇹'),
  MarketOption('ME', '🇲🇪'),
  MarketOption('CO', '🇨🇴'),
  MarketOption('BE', '🇧🇪'),
  MarketOption('EG', '🇪🇬'),
  MarketOption('LR', '🇱🇷'),
  MarketOption('MV', '🇲🇻'),
  MarketOption('MA', '🇲🇦'),
  MarketOption('VU', '🇻🇺'),
  MarketOption('BJ', '🇧🇯'),
  MarketOption('CH', '🇨🇭'),
  MarketOption('CK', '🇨🇰'),
  MarketOption('BO', '🇧🇴'),
  MarketOption('JM', '🇯🇲'),
  MarketOption('CI', '🇨🇮'),
  MarketOption('TD', '🇹🇩'),
  MarketOption('CG', '🇨🇬'),
  MarketOption('LI', '🇱🇮'),
  MarketOption('GA', '🇬🇦'),
  MarketOption('ID', '🇮🇩'),
  MarketOption('AF', '🇦🇫'),
  MarketOption('HU', '🇭🇺'),
  MarketOption('UA', '🇺🇦'),
  MarketOption('UY', '🇺🇾'),
  MarketOption('MD', '🇲🇩'),
  MarketOption('KG', '🇰🇬'),
  MarketOption('MY', '🇲🇾'),
  MarketOption('TT', '🇹🇹'),
  MarketOption('UZ', '🇺🇿'),
  MarketOption('VN', '🇻🇳'),
  MarketOption('SM', '🇸🇲'),
  MarketOption('SZ', '🇸🇿'),
  MarketOption('AD', '🇦🇩'),
  MarketOption('MK', '🇲🇰'),
  MarketOption('KP', '🇰🇵'),
  MarketOption('TJ', '🇹🇯'),
  MarketOption('CR', '🇨🇷'),
  MarketOption('SV', '🇸🇻'),
  MarketOption('GT', '🇬🇹'),
  MarketOption('HN', '🇭🇳'),
  MarketOption('NI', '🇳🇮'),
  MarketOption('PG', '🇵🇬'),
  MarketOption('CL', '🇨🇱'),
  MarketOption('KN', '🇰🇳'),
  MarketOption('NP', '🇳🇵'),
  MarketOption('AM', '🇦🇲'),
  MarketOption('BZ', '🇧🇿'),
  MarketOption('ML', '🇲🇱'),
  MarketOption('SA', '🇸🇦'),
  MarketOption('GW', '🇬🇼'),
  MarketOption('TM', '🇹🇲'),
  MarketOption('BW', '🇧🇼'),
  MarketOption('CN', '🇨🇳'),
  MarketOption('GN', '🇬🇳'),
  MarketOption('NG', '🇳🇬'),
  MarketOption('PW', '🇵🇼'),
  MarketOption('TV', '🇹🇻'),
  MarketOption('IQ', '🇮🇶'),
  MarketOption('LS', '🇱🇸'),
  MarketOption('UG', '🇺🇬'),
  MarketOption('FJ', '🇫🇯'),
  MarketOption('GQ', '🇬🇶'),
  MarketOption('NU', '🇳🇺'),
  MarketOption('ZM', '🇿🇲'),
  MarketOption('KZ', '🇰🇿'),
  MarketOption('AT', '🇦🇹'),
  MarketOption('VC', '🇻🇨'),
  MarketOption('TR', '🇹🇷'),
  MarketOption('DZ', '🇩🇿'),
  MarketOption('AG', '🇦🇬'),
  MarketOption('DM', '🇩🇲'),
  MarketOption('FM', '🇫🇲'),
  MarketOption('PA', '🇵🇦'),
  MarketOption('TO', '🇹🇴'),
  MarketOption('KH', '🇰🇭'),
  MarketOption('AO', '🇦🇴'),
  MarketOption('OM', '🇴🇲'),
  MarketOption('MC', '🇲🇨'),
  MarketOption('LB', '🇱🇧'),
  MarketOption('BA', '🇧🇦'),
  MarketOption('SR', '🇸🇷'),
  MarketOption('AL', '🇦🇱'),
  MarketOption('MR', '🇲🇷'),
  MarketOption('BB', '🇧🇧'),
  MarketOption('CF', '🇨🇫'),
  MarketOption('RO', '🇷🇴'),
  MarketOption('LA', '🇱🇦'),
  MarketOption('AE', '🇦🇪'),
  MarketOption('TH', '🇹🇭'),
  MarketOption('BF', '🇧🇫'),
  MarketOption('KE', '🇰🇪'),
  MarketOption('BH', '🇧🇭'),
  MarketOption('BT', '🇧🇹'),
  MarketOption('NE', '🇳🇪'),
  MarketOption('QA', '🇶🇦'),
  MarketOption('LY', '🇱🇾'),
];

const _additionalCountryLabels = <String, String>{
  'CU': 'Cuba',
  'HT': 'Haiti',
  'SD': 'Sudan',
  'MM': 'Myanmar',
  'NR': 'Nauru',
  'LK': 'Sri Lanka',
  'GD': 'Grenada',
  'IR': 'Iran',
  'RS': 'Serbia',
  'GM': 'The Gambia',
  'LC': 'Saint Lucia',
  'BN': 'Brunei',
  'GY': 'Guyana',
  'KW': 'Kuwait',
  'DO': 'Dominican Republic',
  'BG': 'Bulgaria',
  'GH': 'Ghana',
  'MU': 'Mauritius',
  'TN': 'Tunisia',
  'NA': 'Namibia',
  'PK': 'Pakistan',
  'GR': 'Greece',
  'BD': 'Bangladesh',
  'SN': 'Senegal',
  'ZW': 'Zimbabwe',
  'TZ': 'Tanzania',
  'SL': 'Sierra Leone',
  'TG': 'Togo',
  'MH': 'Marshall Islands',
  'PY': 'Paraguay',
  'CM': 'Cameroon',
  'TL': 'Timor-Leste',
  'YE': 'Yemen',
  'EC': 'Ecuador',
  'ER': 'Eritrea',
  'JO': 'Jordan',
  'GE': 'Georgia',
  'AZ': 'Azerbaijan',
  'ET': 'Ethiopia',
  'WS': 'Samoa',
  'RU': 'Russia',
  'SC': 'Seychelles',
  'MZ': 'Mozambique',
  'SI': 'Slovenia',
  'MG': 'Madagascar',
  'DJ': 'Djibouti',
  'CD': 'Democratic Republic of the Congo',
  'BI': 'Burundi',
  'SO': 'Somalia',
  'BY': 'Belarus',
  'CV': 'Cape Verde',
  'RW': 'Rwanda',
  'VE': 'Venezuela',
  'KM': 'Comoros',
  'MW': 'Malawi',
  'SB': 'Solomon Islands',
  'SS': 'South Sudan',
  'BS': 'Bahamas',
  'MN': 'Mongolia',
  'KI': 'Kiribati',
  'ST': 'São Tomé and Príncipe',
  'ME': 'Montenegro',
  'CO': 'Colombia',
  'BE': 'Belgium',
  'EG': 'Egypt',
  'LR': 'Liberia',
  'MV': 'Maldives',
  'MA': 'Morocco',
  'VU': 'Vanuatu',
  'BJ': 'Benin',
  'CH': 'Switzerland',
  'CK': 'Cook Islands',
  'BO': 'Bolivia',
  'JM': 'Jamaica',
  'CI': 'Côte d\'Ivoire',
  'TD': 'Chad',
  'CG': 'Republic of the Congo',
  'LI': 'Liechtenstein',
  'GA': 'Gabon',
  'ID': 'Indonesia',
  'AF': 'Afghanistan',
  'HU': 'Hungary',
  'UA': 'Ukraine',
  'UY': 'Uruguay',
  'MD': 'Moldova',
  'KG': 'Kyrgyzstan',
  'MY': 'Malaysia',
  'TT': 'Trinidad and Tobago',
  'UZ': 'Uzbekistan',
  'VN': 'Vietnam',
  'SM': 'San Marino',
  'SZ': 'Eswatini',
  'AD': 'Andorra',
  'MK': 'North Macedonia',
  'KP': 'North Korea',
  'TJ': 'Tajikistan',
  'CR': 'Costa Rica',
  'SV': 'El Salvador',
  'GT': 'Guatemala',
  'HN': 'Honduras',
  'NI': 'Nicaragua',
  'PG': 'Papua New Guinea',
  'CL': 'Chile',
  'KN': 'Saint Kitts and Nevis',
  'NP': 'Nepal',
  'AM': 'Armenia',
  'BZ': 'Belize',
  'ML': 'Mali',
  'SA': 'Saudi Arabia',
  'GW': 'Guinea-Bissau',
  'TM': 'Turkmenistan',
  'BW': 'Botswana',
  'CN': 'China',
  'GN': 'Guinea',
  'NG': 'Nigeria',
  'PW': 'Palau',
  'TV': 'Tuvalu',
  'IQ': 'Iraq',
  'LS': 'Lesotho',
  'UG': 'Uganda',
  'FJ': 'Fiji',
  'GQ': 'Equatorial Guinea',
  'NU': 'Niue',
  'ZM': 'Zambia',
  'KZ': 'Kazakhstan',
  'AT': 'Austria',
  'VC': 'Saint Vincent and the Grenadines',
  'TR': 'Türkiye',
  'DZ': 'Algeria',
  'AG': 'Antigua and Barbuda',
  'DM': 'Dominica',
  'FM': 'Micronesia',
  'PA': 'Panama',
  'TO': 'Tonga',
  'KH': 'Cambodia',
  'AO': 'Angola',
  'OM': 'Oman',
  'MC': 'Monaco',
  'LB': 'Lebanon',
  'BA': 'Bosnia and Herzegovina',
  'SR': 'Suriname',
  'AL': 'Albania',
  'MR': 'Mauritania',
  'BB': 'Barbados',
  'CF': 'Central African Republic',
  'RO': 'Romania',
  'LA': 'Laos',
  'AE': 'United Arab Emirates',
  'TH': 'Thailand',
  'BF': 'Burkina Faso',
  'KE': 'Kenya',
  'BH': 'Bahrain',
  'BT': 'Bhutan',
  'NE': 'Niger',
  'QA': 'Qatar',
  'LY': 'Libya',
};

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
    case 'MT':
      return l10n.countryMalta;
    case 'HR':
      return l10n.countryCroatia;
    case 'CY':
      return l10n.countryCyprus;
    case 'EE':
      return l10n.countryEstonia;
    case 'LV':
      return l10n.countryLatvia;
    case 'LT':
      return l10n.countryLithuania;
    case 'IS':
      return l10n.countryIceland;
    case 'LU':
      return l10n.countryLuxembourg;
    default:
      return _additionalCountryLabels[code.toUpperCase()] ?? l10n.globalMarket;
  }
}
