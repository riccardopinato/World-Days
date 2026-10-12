import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../domain/observance.dart';
import '../../l10n/app_localizations.dart';

class ObservanceDetailPage extends StatefulWidget {
  const ObservanceDetailPage({
    super.key,
    required this.observance,
    required this.controller,
  });

  final Observance observance;
  final AppController controller;

  @override
  State<ObservanceDetailPage> createState() => _ObservanceDetailPageState();
}

class _ObservanceDetailPageState extends State<ObservanceDetailPage> {
  @override
  void initState() {
    super.initState();
    widget.controller.recordOpen(widget.observance.id);
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final record = widget.observance;
    final favorite = widget.controller.isFavorite(record.id);
    final colors = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            tooltip: favorite ? l10n.removeFavorite : l10n.addFavorite,
            onPressed: () async {
              await widget.controller.toggleFavorite(record.id);
              if (mounted) setState(() {});
            },
            icon: Icon(
              favorite
                  ? Icons.favorite_rounded
                  : Icons.favorite_border_rounded,
            ),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 8, 20, 36),
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  colors.primaryContainer,
                  colors.tertiaryContainer,
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(32),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _Badge(
                  text: _officialityLabel(
                    record.authority.officiality,
                    l10n,
                  ),
                ),
                const SizedBox(height: 18),
                Text(
                  record.title,
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        fontWeight: FontWeight.w900,
                        height: 1.05,
                      ),
                ),
                const SizedBox(height: 14),
                Text(
                  record.authority.name,
                  style: Theme.of(context).textTheme.titleMedium,
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          _InfoRow(label: l10n.authority, value: record.authority.name),
          if (record.authority.resolution case final resolution?)
            _InfoRow(label: l10n.resolution, value: resolution),
          _InfoRow(label: l10n.global, value: record.scope),
          const SizedBox(height: 20),
          Text(
            l10n.sources,
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.w800,
                ),
          ),
          const SizedBox(height: 12),
          for (final source in record.sources) ...[
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      source.tier,
                      style: Theme.of(context).textTheme.labelMedium,
                    ),
                    const SizedBox(height: 6),
                    SelectableText(source.url),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 10),
          ],
          const SizedBox(height: 18),
          Text(
            l10n.editorialComingNext,
            style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w800,
                ),
          ),
          const SizedBox(height: 8),
          Text(
            l10n.editorialPlaceholder,
            style: Theme.of(context).textTheme.bodyLarge,
          ),
        ],
      ),
    );
  }

  String _officialityLabel(String value, AppLocalizations l10n) {
    if (value.startsWith('OFFICIAL_')) return l10n.official;
    if (value == 'RECOGNIZED_NGO') return l10n.recognized;
    if (value == 'POPULAR') return l10n.popular;
    return l10n.institutional;
  }
}

class _Badge extends StatelessWidget {
  const _Badge({required this.text});
  final String text;

  @override
  Widget build(BuildContext context) => Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surface.withValues(alpha: 0.72),
          borderRadius: BorderRadius.circular(999),
        ),
        child: Text(
          text,
          style: Theme.of(context).textTheme.labelLarge?.copyWith(
                fontWeight: FontWeight.w700,
              ),
        ),
      );
}

class _InfoRow extends StatelessWidget {
  const _InfoRow({required this.label, required this.value});
  final String label;
  final String value;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 8),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(
              width: 110,
              child: Text(
                label,
                style: Theme.of(context).textTheme.labelLarge,
              ),
            ),
            Expanded(child: Text(value)),
          ],
        ),
      );
}
