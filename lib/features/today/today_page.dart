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
                  subtitle: '${controller.preferences.streak} ${l10n.streak}',
                  accentText: now.day.toString(),
                  minHeight: 254,
                  onTap: () => _open(context, records.first),
                )
              else
                Container(
                  padding: const EdgeInsets.all(22),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [
                        colors.primaryContainer,
                        colors.secondaryContainer,
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(30),
                  ),
                  child: Row(
                    children: [
                      Text(
                        '${now.day}',
                        style:
                            Theme.of(context).textTheme.displayLarge?.copyWith(
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
                              l10n.noObservancesToday,
                              style: Theme.of(context)
                                  .textTheme
                                  .titleLarge
                                  ?.copyWith(fontWeight: FontWeight.w800),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              '${controller.preferences.streak} ${l10n.streak}',
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              if (records.length > 1) ...[
                const SizedBox(height: 24),
                for (final record in records.skip(1)) ...[
                  ObservanceCard(
                    observance: record,
                    favorite: controller.isFavorite(record.id),
                    onFavorite: () => controller.toggleFavorite(record.id),
                    onTap: () => _open(context, record),
                  ),
                  const SizedBox(height: 12),
                ],
              ],
              const SizedBox(height: 24),
              Text(
                l10n.upNext,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.w800,
                    ),
              ),
              const SizedBox(height: 12),
              for (final item in next.take(5)) ...[
                Padding(
                  padding: const EdgeInsets.only(left: 4, bottom: 8),
                  child: Text(
                    DateFormat.MMMd(locale).format(item.date),
                    style: Theme.of(context).textTheme.labelLarge?.copyWith(
                          color: Theme.of(context).colorScheme.primary,
                          fontWeight: FontWeight.w800,
                        ),
                  ),
                ),
                ObservanceCard(
                  observance: item.observance,
                  onTap: () => _open(context, item.observance),
                ),
                const SizedBox(height: 14),
              ],
            ],
          ),
        ),
      ],
    );
  }

  List<_UpcomingObservance> _nextObservances(
    AppController controller,
    DateTime date,
  ) {
    final start = DateTime(date.year, date.month, date.day);
    final seen = <String>{};
    final result = <_UpcomingObservance>[];

    for (var offset = 1; offset <= 366 && result.length < 8; offset++) {
      final candidate = start.add(Duration(days: offset));
      for (final record in controller.observancesForDate(candidate)) {
        if (!seen.add(record.id)) continue;
        result.add(_UpcomingObservance(date: candidate, observance: record));
        if (result.length >= 8) break;
      }
    }
    return result;
  }

  void _open(BuildContext context, Observance record) {
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ObservanceDetailPage(
          observance: record,
          controller: controller,
        ),
      ),
    );
  }
}

class _UpcomingObservance {
  const _UpcomingObservance({
    required this.date,
    required this.observance,
  });

  final DateTime date;
  final Observance observance;
}
