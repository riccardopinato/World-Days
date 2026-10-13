import 'package:flutter/material.dart';

import '../../domain/observance.dart';
import '../visual/observance_visuals.dart';

class ObservanceHero extends StatelessWidget {
  const ObservanceHero({
    super.key,
    required this.observance,
    required this.eyebrow,
    this.subtitle,
    this.accentText,
    this.badge,
    this.minHeight = 244,
  });

  final Observance observance;
  final String eyebrow;
  final String? subtitle;
  final String? accentText;
  final Widget? badge;
  final double minHeight;

  @override
  Widget build(BuildContext context) {
    final style = ObservanceVisuals.resolve(observance);
    final textScale = MediaQuery.textScalerOf(context).scale(1);
    final height = textScale >= 1.5 ? minHeight + 96 : minHeight;

    return Semantics(
      container: true,
      label: observance.title,
      child: SizedBox(
        height: height,
        child: ObservanceArtwork(
          style: style,
          borderRadius: BorderRadius.circular(32),
          foreground: Stack(
            fit: StackFit.expand,
            children: [
              if (accentText != null)
                Positioned(
                  right: 18,
                  bottom: -10,
                  child: IgnorePointer(
                    child: Text(
                      accentText!,
                      style: Theme.of(context).textTheme.displayLarge?.copyWith(
                            fontSize: 104,
                            height: 1,
                            fontWeight: FontWeight.w900,
                            color: Colors.white.withValues(alpha: .13),
                          ),
                    ),
                  ),
                ),
              Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (badge != null) ...[
                      badge!,
                      const SizedBox(height: 16),
                    ],
                    Text(
                      eyebrow.toUpperCase(),
                      style: Theme.of(context).textTheme.labelLarge?.copyWith(
                            color: Colors.white.withValues(alpha: .84),
                            fontWeight: FontWeight.w800,
                            letterSpacing: .7,
                          ),
                    ),
                    const Spacer(),
                    Icon(
                      style.icon,
                      size: 38,
                      color: Colors.white,
                    ),
                    const SizedBox(height: 12),
                    Text(
                      observance.title,
                      maxLines: 4,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                            color: Colors.white,
                            fontWeight: FontWeight.w900,
                            height: 1.02,
                          ),
                    ),
                    if (subtitle != null) ...[
                      const SizedBox(height: 10),
                      Text(
                        subtitle!,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              color: Colors.white.withValues(alpha: .88),
                              fontWeight: FontWeight.w600,
                            ),
                      ),
                    ],
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
