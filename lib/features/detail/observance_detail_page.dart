import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/market_options.dart';
import '../../core/visual/observance_visuals.dart';
import '../../core/widgets/world_days_share_card.dart';
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
    final localeCode = Localizations.localeOf(context).languageCode;
    final editorial = widget.controller.catalog?.editorialFor(record.id, localeCode);
    final editorialFallback = editorial != null && editorial.locale != localeCode;
    final visual = ObservanceVisuals.resolve(record);

    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            tooltip: l10n.shareThisDay,
            onPressed: () => showWorldDaysShareCard(
              context: context,
              observance: record,
              badgeText: _officialityLabel(record.authority.officiality, l10n),
            ),
            icon: const Icon(Icons.ios_share_rounded),
          ),
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
                  ...visual.colors,
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
          if (editorial != null) ...[
            if (editorialFallback) ...[
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Row(
                    children: [
                      const Icon(Icons.translate_rounded, size: 20),
                      const SizedBox(width: 10),
                      Expanded(child: Text(l10n.editorialEnglishOnly)),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),
            ],
            Text(
              editorial.summary,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    height: 1.5,
                  ),
            ),
            const SizedBox(height: 26),
            _EditorialSection(
              icon: Icons.lightbulb_outline_rounded,
              title: l10n.whyItMatters,
              body: editorial.whyItMatters,
            ),
            const SizedBox(height: 24),
            Text(
              l10n.waysToTakePart,
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.w900,
                  ),
            ),
            const SizedBox(height: 12),
            for (final action in editorial.waysToTakePart) ...[
              _ActionCard(text: action),
              const SizedBox(height: 10),
            ],
            const SizedBox(height: 16),
          ] else ...[
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
            const SizedBox(height: 24),
          ],
          _InfoRow(label: l10n.authority, value: record.authority.name),
          if (record.authority.resolution case final resolution?)
            _InfoRow(label: l10n.resolution, value: resolution),
          _InfoRow(
            label: l10n.market,
            value: record.scope == 'GLOBAL'
                ? l10n.globalMarket
                : record.countries
                    .map((code) => marketLabel(l10n, code))
                    .join(', '),
          ),
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


class _EditorialSection extends StatelessWidget {
  const _EditorialSection({
    required this.icon,
    required this.title,
    required this.body,
  });

  final IconData icon;
  final String title;
  final String body;

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(18),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.w900,
                          ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      body,
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            height: 1.45,
                          ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      );
}

class _ActionCard extends StatelessWidget {
  const _ActionCard({required this.text});
  final String text;

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(
                Icons.arrow_forward_rounded,
                size: 20,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(width: 12),
              Expanded(child: Text(text)),
            ],
          ),
        ),
      );
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
