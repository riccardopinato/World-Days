import '../l10n/app_localizations.dart';

const semanticCategoryKeys = <String>[
  'PLANET',
  'HEALTH',
  'PEOPLE',
  'LEARNING',
  'CULTURE',
  'FOOD',
  'FUTURE',
  'COMMUNITY',
];

String semanticCategoryLabel(AppLocalizations l10n, String key) =>
    switch (key.toUpperCase()) {
      'PLANET' => l10n.categoryPlanet,
      'HEALTH' => l10n.categoryHealth,
      'PEOPLE' => l10n.categoryPeople,
      'LEARNING' => l10n.categoryLearning,
      'CULTURE' => l10n.categoryCulture,
      'FOOD' => l10n.categoryFood,
      'FUTURE' => l10n.categoryFuture,
      'COMMUNITY' => l10n.categoryCommunity,
      _ => key,
    };
