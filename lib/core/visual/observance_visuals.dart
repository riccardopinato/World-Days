import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../domain/observance.dart';

final class ObservanceVisualStyle {
  const ObservanceVisualStyle({
    required this.key,
    required this.colors,
    required this.icon,
  });

  final String key;
  final List<Color> colors;
  final IconData icon;
}

abstract final class ObservanceVisuals {
  static const knownKeys = <String>{
    'planet',
    'health',
    'people',
    'learning',
    'culture',
    'food',
    'future',
    'community',
  };

  static const collectionKeys = <String>[
    'planet',
    'health',
    'people',
    'learning',
    'culture',
    'food',
    'future',
    'community',
  ];

  static ObservanceVisualStyle resolve(Observance observance) {
    final explicit = observance.visualKey;
    if (explicit != null && knownKeys.contains(explicit)) {
      return forKey(explicit);
    }
    return forKey(inferKey(observance));
  }

  static String inferKey(Observance observance) {
    final haystack = <String>[
      observance.title,
      ...observance.categories,
    ].join(' ').toLowerCase().replaceAll('_', ' ');

    if (_containsAny(haystack, const [
      'health',
      'disease',
      'cancer',
      'nurse',
      'heart',
      'tuberculosis',
      'mental',
      'alzheimer',
      'suicide',
      'aids',
      'malaria',
      'hepatitis',
      'blood',
      'patient',
      'diabetes',
    ])) {
      return 'health';
    }
    if (_containsAny(haystack, const [
      'water',
      'ocean',
      'sea',
      'forest',
      'earth',
      'environment',
      'wildlife',
      'wetland',
      'climate',
      'biodiversity',
      'desert',
      'glacier',
      'mountain',
      'soil',
      'ozone',
      'meteorological',
      'turtle',
      'seagrass',
    ])) {
      return 'planet';
    }
    if (_containsAny(haystack, const [
      'education',
      'science',
      'braille',
      'language',
      'literacy',
      'logic',
      'teacher',
      'mathematics',
      'learning',
    ])) {
      return 'learning';
    }
    if (_containsAny(haystack, const [
      'culture',
      'poetry',
      'radio',
      'theatre',
      'dance',
      'museum',
      'jazz',
      'art',
      'music',
      'emoji',
      'tourism',
      'heritage',
    ])) {
      return 'culture';
    }
    if (_containsAny(haystack, const [
      'food',
      'vegan',
      'pulse',
      'gastronomy',
      'tea',
      'coffee',
      'agriculture',
    ])) {
      return 'food';
    }
    if (_containsAny(haystack, const [
      'women',
      'girl',
      'rights',
      'refugee',
      'peace',
      'justice',
      'discrimination',
      'slavery',
      'fraternity',
      'social',
      'family',
      'children',
      'youth',
      'kindness',
      'solidarity',
      'democracy',
      'indigenous',
      'disability',
    ])) {
      return 'people';
    }
    if (_containsAny(haystack, const [
      'space',
      'telecommunication',
      'internet',
      'innovation',
      'technology',
      'industrial',
      'energy',
      'digital',
    ])) {
      return 'future';
    }
    return 'community';
  }

  static ObservanceVisualStyle forKey(String key) {
    switch (key) {
      case 'planet':
        return const ObservanceVisualStyle(
          key: 'planet',
          colors: [Color(0xFF0E9F8A), Color(0xFF0878B9), Color(0xFF274690)],
          icon: Icons.public_rounded,
        );
      case 'health':
        return const ObservanceVisualStyle(
          key: 'health',
          colors: [Color(0xFFF15B6C), Color(0xFFE53E6F), Color(0xFF8B2F75)],
          icon: Icons.favorite_rounded,
        );
      case 'people':
        return const ObservanceVisualStyle(
          key: 'people',
          colors: [Color(0xFF7C4DFF), Color(0xFFB24592), Color(0xFFE85D9E)],
          icon: Icons.diversity_1_rounded,
        );
      case 'learning':
        return const ObservanceVisualStyle(
          key: 'learning',
          colors: [Color(0xFF3468C0), Color(0xFF5B4BDB), Color(0xFF8F67D5)],
          icon: Icons.auto_stories_rounded,
        );
      case 'culture':
        return const ObservanceVisualStyle(
          key: 'culture',
          colors: [Color(0xFFFF7A45), Color(0xFFE6508F), Color(0xFF8B4AB8)],
          icon: Icons.palette_rounded,
        );
      case 'food':
        return const ObservanceVisualStyle(
          key: 'food',
          colors: [Color(0xFFF59E0B), Color(0xFFE9792B), Color(0xFF5B8C51)],
          icon: Icons.restaurant_rounded,
        );
      case 'future':
        return const ObservanceVisualStyle(
          key: 'future',
          colors: [Color(0xFF3348A5), Color(0xFF526DFF), Color(0xFF00A8C6)],
          icon: Icons.rocket_launch_rounded,
        );
      default:
        return const ObservanceVisualStyle(
          key: 'community',
          colors: [Color(0xFF6750A4), Color(0xFFB35B9B), Color(0xFFF28B54)],
          icon: Icons.auto_awesome_rounded,
        );
    }
  }

  static bool _containsAny(String haystack, List<String> values) =>
      values.any(haystack.contains);
}

class ObservanceArtwork extends StatelessWidget {
  const ObservanceArtwork({
    super.key,
    required this.style,
    this.borderRadius = const BorderRadius.all(Radius.circular(28)),
    this.foreground,
  });

  final ObservanceVisualStyle style;
  final BorderRadius borderRadius;
  final Widget? foreground;

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: borderRadius,
      child: DecoratedBox(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: style.colors,
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: LayoutBuilder(
          builder: (context, constraints) {
            final shortest = constraints.biggest.shortestSide.isFinite
                ? constraints.biggest.shortestSide
                : 180.0;
            final bubble = math.max(42.0, shortest * .7);
            return Stack(
              fit: StackFit.expand,
              children: [
                Positioned(
                  right: -bubble * .28,
                  top: -bubble * .22,
                  child: _Orb(size: bubble, opacity: .16),
                ),
                Positioned(
                  left: -bubble * .38,
                  bottom: -bubble * .42,
                  child: _Orb(size: bubble * 1.22, opacity: .11),
                ),
                Positioned(
                  right: shortest * .08,
                  bottom: shortest * .06,
                  child: Transform.rotate(
                    angle: -.28,
                    child: Icon(
                      style.icon,
                      size: math.max(44.0, shortest * .58),
                      color: Colors.white.withValues(alpha: .16),
                    ),
                  ),
                ),
                if (foreground != null) foreground!,
              ],
            );
          },
        ),
      ),
    );
  }
}

class _Orb extends StatelessWidget {
  const _Orb({required this.size, required this.opacity});

  final double size;
  final double opacity;

  @override
  Widget build(BuildContext context) => Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.white.withValues(alpha: opacity),
          border: Border.all(
            color: Colors.white.withValues(alpha: opacity + .05),
          ),
        ),
      );
}
