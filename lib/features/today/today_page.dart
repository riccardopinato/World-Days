import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../app/app_controller.dart';
import '../../core/widgets/observance_card.dart';
import '../../core/widgets/observance_hero.dart';
import '../../domain/observance.dart';
import '../../features/detail/observance_detail_page.dart';
import '../../l10n/app_localizations.dart';

class TodayPage extends StatelessWidget {
  const TodayPage({super.key, required this.controller});
  final AppController controller;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final now = DateTime.now();
    final locale = Localizations.localeOf(context).toLanguageTag();
    final records = controller.observancesForDate(now);
    final next = _nextObservances(controller, now);
    final colors = Theme.of(context).colorScheme;

    return CustomScrollView(
      slivers: [
        SliverAppBar.large(
          title: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(l10n.today),
              Text(
                DateFormat.yMMMMd(locale).format(now),
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ],
          ),
        ),
        SliverPadding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 32),
          sliver: SliverList.list(
            children: [
              if (records.isNotEmpty)
                ObservanceHero(
                  observance: records.first,
                  eyebrow: DateFormat.EEEE(locale).format(now),
                  subtitle: controller.preferences.streak.toString() +
                      ' ' +
                      l10n.streak,
                  accentText: now.day.toString(),
                  minHeight: 254,
                )
              else
                Container(
                padding: const EdgeInsets.all(22),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [colors.primaryContainer, colors.secondaryContainer],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  ),
                  borderRadius: BorderRadius.circular(30),
                ),
                child: Row(
                  children: [
                    Text(
                      '${now.day}',
                      style: Theme.of(context).textTheme.displayLarge?.copyWith(
                            fontWeight: FontWeight.w900,
                            height: .9,
                          ),
                    ),
                    const SizedBox(width: 18),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            records.isEmpty ? l10n.noObservancesToday : records.first.title,
                            style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
                          ),
                          const SizedBox(height: 8),
                          Text('${controller.preferences.streak} ${l10n.streak}'),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              if (records.isNotEmpty) ...[
                for (final record in records) ...[
                  ObservanceCard(
                    observance: record,
                    favorite: controller.isFavorite(record.id),
                    onFavorite: () => controller.toggleFavorite(record.id),
                    onTap: () => _open(context, record),
                  ),
                  const SizedBox(height: 12),
                ],
              ],
              const SizedBox(height: 12),
              Text(l10n.upNext, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
              const SizedBox(height: 12),
              for (final record in next.take(5)) ...[
                ObservanceCard(observance: record, onTap: () => _open(context, record)),
                const SizedBox(height: 12),
              ],
            ],
          ),
        ),
      ],
    );
  }

  List<Observance> _nextObservances(AppController controller, DateTime date) {
    final catalog = controller.catalog;
    if (catalog == null) return const [];
    final occurrences = controller.occurrencesForYear(date.year);
    final start = DateTime(date.year, date.month, date.day).add(const Duration(days: 1));
    final seen = <String>{};
    final result = <Observance>[];
    for (final occurrence in occurrences) {
      if (occurrence.end.isBefore(start)) continue;
      final record = catalog.byId[occurrence.observanceId];
      if (record != null &&
          controller.isVisibleForMarket(record) &&
          seen.add(record.id)) {
        result.add(record);
      }
      if (result.length >= 8) break;
    }
    return result;
  }

  void _open(BuildContext context, Observance record) {
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ObservanceDetailPage(observance: record, controller: controller),
      ),
    );
  }
}
