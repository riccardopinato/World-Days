import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/market_options.dart';
import '../../core/visual/observance_visuals.dart';
import '../../core/widgets/world_days_share_card.dart';
import '../../domain/observance.dart';
import '../../domain/verified_metadata_summary.dart';
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
    final localizedTitle = record.titleForLocale(localeCode);
    final catalog = widget.controller.catalog;
    final editorial = catalog?.editorialFor(record.id, localeCode);
    final editorialFallback = editorial != null && editorial.locale != localeCode;
    final annualOverride = catalog?.yearOverrideFor(record.id, DateTime.now().year);
    final related = editorial == null
        ? const <Observance>[]
        : editorial.relatedObservanceIds
            .map((id) => catalog?.byId[id])
            .whereType<Observance>()
            .toList(growable: false);
    final visual = ObservanceVisuals.resolve(record);

    return Scaffold(
      appBar: AppBar(
        actions: [
          IconButton(
            tooltip: l10n.shareThisDay,
            onPressed: () => showWorldDaysShareCard(
              context: context,
              observance: record,
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
                  localizedTitle,
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        color: Colors.white,
                        fontWeight: FontWeight.w900,
                        height: 1.05,
                      ),
                ),
                const SizedBox(height: 14),
                Text(
                  record.authority.name,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        color: Colors.white.withValues(alpha: .88),
                        fontWeight: FontWeight.w600,
                      ),
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
            if (editorial.hook.trim().isNotEmpty) ...[
              Text(
                editorial.hook,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w900,
                      height: 1.25,
                    ),
              ),
              const SizedBox(height: 12),
            ],
            Text(
              editorial.summary,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    height: 1.5,
                  ),
            ),
            if (annualOverride != null &&
                annualOverride.campaignTheme.trim().isNotEmpty) ...[
              const SizedBox(height: 22),
              _EditorialSection(
                icon: Icons.campaign_outlined,
                title: l10n.annualTheme,
                body: annualOverride.campaignTheme,
              ),
            ],
            if (editorial.whyThisDate.trim().isNotEmpty) ...[
              const SizedBox(height: 22),
              _EditorialSection(
                icon: Icons.event_available_outlined,
                title: l10n.whyThisDate,
                body: editorial.whyThisDate,
              ),
            ],
            if (editorial.origin.trim().isNotEmpty) ...[
              const SizedBox(height: 22),
              _EditorialSection(
                icon: Icons.history_edu_outlined,
                title: l10n.originHistory,
                body: editorial.origin,
              ),
            ],
            const SizedBox(height: 22),
            _EditorialSection(
              icon: Icons.lightbulb_outline_rounded,
              title: l10n.whyItMatters,
              body: editorial.whyItMatters,
            ),
            if (editorial.quickFacts.isNotEmpty) ...[
              const SizedBox(height: 24),
              Text(
                l10n.quickFacts,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w900,
                    ),
              ),
              const SizedBox(height: 12),
              for (final fact in editorial.quickFacts) ...[
                _FactCard(text: fact),
                const SizedBox(height: 10),
              ],
            ],
            if (!editorial.hasExtendedEditorial) ...[
              const SizedBox(height: 18),
              Text(
                l10n.editorialCoveragePending,
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
              ),
            ],
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
            if (related.isNotEmpty) ...[
              const SizedBox(height: 18),
              Text(
                l10n.relatedObservances,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w900,
                    ),
              ),
              const SizedBox(height: 12),
              for (final relatedRecord in related)
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.link_rounded),
                    title: Text(relatedRecord.titleForLocale(localeCode)),
                    trailing: const Icon(Icons.chevron_right_rounded),
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute<void>(
                        builder: (_) => ObservanceDetailPage(
                          observance: relatedRecord,
                          controller: widget.controller,
                        ),
                      ),
                    ),
                  ),
                ),
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
                    Row(
                      children: [
                        Expanded(
                          child: Text(
                            _sourceTierLabel(source.tier, l10n),
                            style: Theme.of(context)
                                .textTheme
                                .titleSmall
                                ?.copyWith(fontWeight: FontWeight.w800),
                          ),
                        ),
                        if (source.verifiedAt case final verifiedAt?)
                          Text(
                            '${l10n.verifiedOn} $verifiedAt',
                            style: Theme.of(context).textTheme.labelSmall,
                          ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    SelectableText(
                      source.url,
                      style: TextStyle(
                        color: Theme.of(context).colorScheme.primary,
                      ),
                    ),
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


  String _sourceTierLabel(String value, AppLocalizations l10n) =>
      switch (value) {
        'A_PRIMARY' => l10n.sourcePrimary,
        'B_INSTITUTIONAL' => l10n.sourceInstitutional,
        'C_DISCOVERY' => l10n.sourceDiscovery,
        'D_ORIGINATOR' => l10n.sourceOriginator,
        _ => l10n.source,
      };

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

class _FactCard extends StatelessWidget {
  const _FactCard({required this.text});

  final String text;

  @override
  Widget build(BuildContext context) => Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(
                Icons.check_circle_outline_rounded,
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
