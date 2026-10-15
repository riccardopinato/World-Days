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
    final locale = Localizations.localeOf(context);
    final localeTag = locale.toLanguageTag();
    final records = controller.observancesForDate(now);
    final primary = records.isEmpty ? null : records.first;
    final editorial = primary == null
        ? null
        : controller.catalog?.editorialFor(primary.id, locale.languageCode);
    final tomorrowDate = DateTime(now.year, now.month, now.day)
        .add(const Duration(days: 1));
    final tomorrowRecords = controller.observancesForDate(tomorrowDate);
    final next = _nextObservances(controller, now, startOffset: 2);
    final colors = Theme.of(context).colorScheme;

    return CustomScrollView(
      slivers: [
        if (MediaQuery.textScalerOf(context).scale(1) >= 1.5)
          SliverAppBar(
            title: Text(l10n.today),
          )
        else
          SliverAppBar.large(
            title: Text(l10n.today),
          ),
        SliverPadding(
          padding: const EdgeInsets.fromLTRB(20, 0, 20, 32),
          sliver: SliverList.list(
            children: [
              Text(
                DateFormat.yMMMMd(localeTag).format(now),
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                      fontWeight: FontWeight.w600,
                    ),
              ),
              const SizedBox(height: 12),
              if (primary != null)
                ObservanceHero(
                  observance: primary,
                  eyebrow: DateFormat.EEEE(localeTag).format(now),
                  subtitle: '${controller.preferences.streak} ${l10n.streak}',
                  accentText: now.day.toString(),
                  minHeight: 254,
                  onTap: () => _open(context, primary),
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
              if (editorial != null) ...[
                const SizedBox(height: 24),
                _SectionTitle(l10n.todayIn30Seconds),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(18),
                    child: Text(
                      editorial.summary,
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            height: 1.45,
                          ),
                    ),
                  ),
                ),
              ],
              if (primary != null) ...[
                const SizedBox(height: 24),
                _SectionTitle(l10n.dailyQuiz),
                _DailyQuizCard(
                  primary: primary,
                  controller: controller,
                ),
              ],
              const SizedBox(height: 24),
              _SectionTitle(l10n.tomorrow),
              Text(
                DateFormat.yMMMMd(localeTag).format(tomorrowDate),
                style: Theme.of(context).textTheme.bodyMedium,
              ),
              const SizedBox(height: 10),
              if (tomorrowRecords.isEmpty)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(18),
                    child: Text(l10n.noObservancesToday),
                  ),
                )
              else
                for (final record in tomorrowRecords.take(2)) ...[
                  ObservanceCard(
                    observance: record,
                    favorite: controller.isFavorite(record.id),
                    onFavorite: () => controller.toggleFavorite(record.id),
                    onTap: () => _open(context, record),
                  ),
                  const SizedBox(height: 12),
                ],
              const SizedBox(height: 24),
              _SectionTitle(l10n.upNext),
              const SizedBox(height: 4),
              for (final item in next.take(5)) ...[
                Padding(
                  padding: const EdgeInsets.only(left: 4, bottom: 8),
                  child: Text(
                    DateFormat.MMMd(localeTag).format(item.date),
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
    DateTime date, {
    int startOffset = 1,
  }) {
    final start = DateTime(date.year, date.month, date.day);
    final seen = <String>{};
    final result = <_UpcomingObservance>[];

    for (var offset = startOffset;
        offset <= 366 && result.length < 8;
        offset++) {
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

class _DailyQuizCard extends StatefulWidget {
  const _DailyQuizCard({
    required this.primary,
    required this.controller,
  });

  final Observance primary;
  final AppController controller;

  @override
  State<_DailyQuizCard> createState() => _DailyQuizCardState();
}

class _DailyQuizCardState extends State<_DailyQuizCard> {
  String? selectedAuthority;

  @override
  void didUpdateWidget(covariant _DailyQuizCard oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.primary.id != widget.primary.id) selectedAuthority = null;
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final correct = widget.primary.authority.name;
    final distractor = _distractorAuthority(correct);
    final options = DateTime.now().day.isEven
        ? [correct, distractor]
        : [distractor, correct];

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              l10n.quizPrompt,
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w800,
                  ),
            ),
            const SizedBox(height: 12),
            for (final option in options) ...[
              SizedBox(
                width: double.infinity,
                child: OutlinedButton(
                  onPressed: () => setState(() => selectedAuthority = option),
                  child: Text(option),
                ),
              ),
              const SizedBox(height: 8),
            ],
            if (selectedAuthority != null)
              Row(
                children: [
                  Icon(
                    selectedAuthority == correct
                        ? Icons.check_circle_rounded
                        : Icons.info_outline_rounded,
                    size: 20,
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      selectedAuthority == correct
                          ? l10n.quizCorrect
                          : l10n.quizTryAgain,
                    ),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }

  String _distractorAuthority(String correct) {
    final records = widget.controller.catalog?.records ?? const <Observance>[];
    for (final record in records) {
      final candidate = record.authority.name;
      if (candidate.isNotEmpty && candidate != correct) return candidate;
    }
    return 'World Days';
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.text);

  final String text;

  @override
  Widget build(BuildContext context) => Text(
        text,
        style: Theme.of(context).textTheme.titleLarge?.copyWith(
              fontWeight: FontWeight.w800,
            ),
      );
}

class _UpcomingObservance {
  const _UpcomingObservance({
    required this.date,
    required this.observance,
  });

  final DateTime date;
  final Observance observance;
}
