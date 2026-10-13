import 'package:flutter/material.dart';

import '../../domain/observance.dart';
import '../../l10n/app_localizations.dart';
import '../visual/observance_visuals.dart';

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
    final visual = ObservanceVisuals.resolve(observance);
    final compactArtwork = MediaQuery.textScalerOf(context).scale(1) >= 1.7;

    return Semantics(
      container: true,
      label: observance.title + '. ' + observance.authority.name,
      child: Card(
        child: InkWell(
          borderRadius: BorderRadius.circular(24),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                ExcludeSemantics(
                  child: SizedBox.square(
                    dimension: compactArtwork ? 58 : 72,
                    child: ObservanceArtwork(
                      style: visual,
                      borderRadius: BorderRadius.circular(20),
                      foreground: Center(
                        child: Icon(
                          visual.icon,
                          color: Colors.white,
                          size: compactArtwork ? 24 : 28,
                        ),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.only(top: 2),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          observance.title,
                          maxLines: 4,
                          overflow: TextOverflow.ellipsis,
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.w900,
                                height: 1.12,
                              ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          observance.authority.name,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: Theme.of(context).textTheme.bodySmall?.copyWith(
                                color: colors.onSurfaceVariant,
                                height: 1.25,
                              ),
                        ),
                      ],
                    ),
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
}
