import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../app/app_controller.dart';
import '../../core/widgets/observance_card.dart';
import '../../domain/observance.dart';
import '../../features/detail/observance_detail_page.dart';
import '../../l10n/app_localizations.dart';

class CalendarPage extends StatefulWidget {
  const CalendarPage({super.key, required this.controller});
  final AppController controller;

  @override
  State<CalendarPage> createState() => _CalendarPageState();
}

class _CalendarPageState extends State<CalendarPage> {
  late DateTime month;
  late DateTime selected;

  @override
  void initState() {
    super.initState();
    final now = DateTime.now();
    month = DateTime(now.year, now.month);
    selected = DateTime(now.year, now.month, now.day);
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final locale = Localizations.localeOf(context).toLanguageTag();
    final records = widget.controller.observancesForDate(selected);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.calendar)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 28),
        children: [
          Row(
            children: [
              IconButton(
                tooltip: l10n.previousMonth,
                onPressed: () => setState(() {
                  month = DateTime(month.year, month.month - 1);
                  selected = DateTime(month.year, month.month, 1);
                }),
                icon: const Icon(Icons.chevron_left_rounded),
              ),
              Expanded(
                child: Text(
                  DateFormat.yMMMM(locale).format(month),
                  textAlign: TextAlign.center,
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.w900,
                      ),
                ),
              ),
              IconButton(
                tooltip: l10n.nextMonth,
                onPressed: () => setState(() {
                  month = DateTime(month.year, month.month + 1);
                  selected = DateTime(month.year, month.month, 1);
                }),
                icon: const Icon(Icons.chevron_right_rounded),
              ),
            ],
          ),
          const SizedBox(height: 12),
          _MonthGrid(
            month: month,
            selected: selected,
            controller: widget.controller,
            locale: locale,
            observancesLabel: l10n.observances,
            onSelected: (date) => setState(() => selected = date),
          ),
          const SizedBox(height: 22),
          Text(
            DateFormat.yMMMMd(locale).format(selected),
            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  fontWeight: FontWeight.w900,
                ),
          ),
          const SizedBox(height: 12),
          if (records.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 28),
              child: Text(l10n.noObservancesToday),
            )
          else
            for (final record in records) ...[
              ObservanceCard(
                observance: record,
                favorite: widget.controller.isFavorite(record.id),
                onFavorite: () =>
                    widget.controller.toggleFavorite(record.id),
                onTap: () => _open(record),
              ),
              const SizedBox(height: 10),
            ],
        ],
      ),
    );
  }

  void _open(Observance record) {
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ObservanceDetailPage(
          observance: record,
          controller: widget.controller,
        ),
      ),
    );
  }
}

class _MonthGrid extends StatelessWidget {
  const _MonthGrid({
    required this.month,
    required this.selected,
    required this.controller,
    required this.locale,
    required this.observancesLabel,
    required this.onSelected,
  });

  final DateTime month;
  final DateTime selected;
  final AppController controller;
  final String locale;
  final String observancesLabel;
  final ValueChanged<DateTime> onSelected;

  @override
  Widget build(BuildContext context) {
    final first = DateTime(month.year, month.month, 1);
    final days = DateTime(month.year, month.month + 1, 0).day;
    final leading = first.weekday - DateTime.monday;
    final itemCount = leading + days;

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 7,
        mainAxisSpacing: 4,
        crossAxisSpacing: 4,
        mainAxisExtent: 48,
      ),
      itemCount: itemCount,
      itemBuilder: (context, index) {
        if (index < leading) return const SizedBox.shrink();
        final day = index - leading + 1;
        final date = DateTime(month.year, month.month, day);
        final count = controller.observancesForDate(date).length;
        final active = _sameDate(date, selected);
        final dateLabel = DateFormat.yMMMMd(locale).format(date);
        final semanticLabel = count == 0
            ? dateLabel
            : '$dateLabel, $count $observancesLabel';

        return Semantics(
          button: true,
          selected: active,
          label: semanticLabel,
          child: InkWell(
            borderRadius: BorderRadius.circular(14),
            onTap: () => onSelected(date),
            child: DecoratedBox(
              decoration: BoxDecoration(
                color: active
                    ? Theme.of(context).colorScheme.primaryContainer
                    : null,
                borderRadius: BorderRadius.circular(14),
                border: active
                    ? Border.all(
                        color: Theme.of(context).colorScheme.primary,
                        width: 1.5,
                      )
                    : null,
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    '$day',
                    style: TextStyle(
                      fontWeight: active ? FontWeight.w900 : FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 3),
                  if (count > 0)
                    Container(
                      width: 6,
                      height: 6,
                      decoration: BoxDecoration(
                        color: Theme.of(context).colorScheme.primary,
                        shape: BoxShape.circle,
                      ),
                    ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }

  bool _sameDate(DateTime a, DateTime b) =>
      a.year == b.year && a.month == b.month && a.day == b.day;
}
