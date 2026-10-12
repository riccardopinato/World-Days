import 'package:flutter/material.dart';

import '../../domain/observance.dart';
import '../../l10n/app_localizations.dart';

class ObservanceCard extends StatelessWidget {
  const ObservanceCard({
    super.key,
    required this.observance,
    required this.onTap,
    this.favorite = false,
    this.onFavorite,
  });

  final Observance observance;
  final VoidCallback onTap;
  final bool favorite;
  final VoidCallback? onFavorite;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final l10n = AppLocalizations.of(context);

    return Semantics(
      container: true,
      label: '${observance.title}. ${observance.authority.name}',
      child: Card(
        child: InkWell(
          borderRadius: BorderRadius.circular(24),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(18),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ExcludeSemantics(
                  child: Container(
                    width: 52,
                    height: 52,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          colors.primaryContainer,
                          colors.tertiaryContainer,
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(18),
                    ),
                    child: Icon(
                      _iconFor(observance.title),
                      color: colors.onPrimaryContainer,
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        observance.title,
                        maxLines: 3,
                        overflow: TextOverflow.ellipsis,
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                              fontWeight: FontWeight.w800,
                              height: 1.15,
                            ),
                      ),
                      const SizedBox(height: 7),
                      Text(
                        observance.authority.name,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: Theme.of(context).textTheme.bodySmall?.copyWith(
                              color: colors.onSurfaceVariant,
                            ),
                      ),
                    ],
                  ),
                ),
                if (onFavorite != null)
                  IconButton(
                    tooltip: favorite ? l10n.removeFavorite : l10n.addFavorite,
                    onPressed: onFavorite,
                    icon: Icon(
                      favorite
                          ? Icons.favorite_rounded
                          : Icons.favorite_border_rounded,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  static IconData _iconFor(String title) {
    final value = title.toLowerCase();
    if (value.contains('health') || value.contains('disease')) {
      return Icons.favorite_rounded;
    }
    if (value.contains('water') ||
        value.contains('ocean') ||
        value.contains('sea')) {
      return Icons.water_drop_rounded;
    }
    if (value.contains('environment') ||
        value.contains('forest') ||
        value.contains('earth')) {
      return Icons.eco_rounded;
    }
    if (value.contains('women') || value.contains('girl')) {
      return Icons.diversity_1_rounded;
    }
    if (value.contains('science') || value.contains('space')) {
      return Icons.science_rounded;
    }
    if (value.contains('education') || value.contains('language')) {
      return Icons.school_rounded;
    }
    if (value.contains('peace') || value.contains('rights')) {
      return Icons.public_rounded;
    }
    return Icons.auto_awesome_rounded;
  }
}
