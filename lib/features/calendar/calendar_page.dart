import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../app/app_controller.dart';
import '../../core/market_options.dart';
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
  late String marketCode;
  String? officialityFilter;
  String? categoryFilter;
  String scopeFilter = 'ALL';

  static const _categories = <String>[
    'PLANET',
    'HEALTH',
    'PEOPLE',
    'LEARNING',
    'CULTURE',
    'FOOD',
    'FUTURE',
    'COMMUNITY',
  ];

  @override
  void initState() {
    super.initState();
    marketCode = widget.controller.preferences.marketCode;
    _jumpToToday();
  }

  void _jumpToToday() {
    final now = DateTime.now();
    month = DateTime(now.year, now.month);
    selected = DateTime(now.year, now.month, now.day);
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final locale = Localizations.localeOf(context).toLanguageTag();
    final records = _recordsForDate(selected);
    final unresolved =
        widget.controller.unresolvedObservancesForYear(month.year);
    final filtersActive = officialityFilter != null ||
        categoryFilter != null ||
        scopeFilter != 'ALL' ||
        marketCode != widget.controller.preferences.marketCode;

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.calendar),
        actions: [
          IconButton(
            tooltip: l10n.filterCalendar,
            onPressed: _showFilters,
            icon: Badge(
              isLabelVisible: filtersActive,
              child: const Icon(Icons.tune_rounded),
            ),
          ),
          TextButton.icon(
            onPressed: () => setState(_jumpToToday),
            icon: const Icon(Icons.today_rounded),
            label: Text(l10n.today),
          ),
          const SizedBox(width: 8),
        ],
      ),
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
          Wrap(
            spacing: 8,
            runSpacing: 8,
            alignment: WrapAlignment.center,
            children: [
              OutlinedButton.icon(
                onPressed: () => _showUpcoming(7),
                icon: const Icon(Icons.view_week_outlined),
                label: Text(l10n.upcoming7Days),
              ),
              OutlinedButton.icon(
                onPressed: () => _showUpcoming(30),
                icon: const Icon(Icons.date_range_rounded),
                label: Text(l10n.upcoming30Days),
              ),
            ],
          ),
          const SizedBox(height: 12),
          if (unresolved.isNotEmpty) ...[
            Card(
              child: ListTile(
                leading: const Icon(Icons.event_busy_outlined),
                title: Text(l10n.unresolvedDatesNotice),
                subtitle: Text(
                  unresolved
                      .map(
                        (record) => record.titleForLocale(
                          Localizations.localeOf(context).languageCode,
                        ),
                      )
                      .take(3)
                      .join(' · '),
                ),
              ),
            ),
            const SizedBox(height: 12),
          ],
          _WeekdayHeader(locale: locale),
          const SizedBox(height: 4),
          _MonthGrid(
            month: month,
            selected: selected,
            locale: locale,
            observancesLabel: l10n.observances,
            countForDate: (date) => _recordsForDate(date).length,
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

  List<Observance> _recordsForDate(DateTime date) {
    final records = widget.controller.observancesForDate(
      date,
      marketCode: marketCode,
    );
    return records.where((record) {
      if (officialityFilter == 'OFFICIAL' &&
          !record.authority.officiality.startsWith('OFFICIAL_')) {
        return false;
      }
      if (officialityFilter != null &&
          officialityFilter != 'OFFICIAL' &&
          record.authority.officiality != officialityFilter) {
        return false;
      }
      if (categoryFilter != null &&
          !record.categories.contains(categoryFilter)) {
        return false;
      }
      if (scopeFilter != 'ALL' && record.scope != scopeFilter) {
        return false;
      }
      return true;
    }).toList(growable: false);
  }

  Future<void> _showFilters() async {
    final l10n = AppLocalizations.of(context);
    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (sheetContext) => StatefulBuilder(
        builder: (context, sheetSetState) {
          void update(VoidCallback callback) {
            setState(callback);
            sheetSetState(() {});
          }

          return SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(20, 4, 20, 28),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    l10n.filterCalendar,
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.w900,
                        ),
                  ),
                  const SizedBox(height: 20),
                  Text(l10n.market),
                  const SizedBox(height: 8),
                  DropdownButtonFormField<String>(
                    initialValue: marketCode,
                    items: [
                      for (final option in marketOptions)
                        DropdownMenuItem(
                          value: option.code,
                          child: Text(
                            '${option.emoji}  ${marketLabel(l10n, option.code)}',
                          ),
                        ),
                    ],
                    onChanged: (value) {
                      if (value != null) {
                        update(() => marketCode = value);
                      }
                    },
                  ),
                  const SizedBox(height: 20),
                  Text(l10n.official),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    children: [
                      ChoiceChip(
                        label: Text(l10n.all),
                        selected: officialityFilter == null,
                        onSelected: (_) =>
                            update(() => officialityFilter = null),
                      ),
                      ChoiceChip(
                        label: Text(l10n.official),
                        selected: officialityFilter == 'OFFICIAL',
                        onSelected: (_) =>
                            update(() => officialityFilter = 'OFFICIAL'),
                      ),
                      ChoiceChip(
                        label: Text(l10n.recognized),
                        selected: officialityFilter == 'RECOGNIZED_NGO',
                        onSelected: (_) => update(
                          () => officialityFilter = 'RECOGNIZED_NGO',
                        ),
                      ),
                      ChoiceChip(
                        label: Text(l10n.popular),
                        selected: officialityFilter == 'POPULAR',
                        onSelected: (_) =>
                            update(() => officialityFilter = 'POPULAR'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  Text(l10n.scope),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    children: [
                      for (final entry in <String, String>{
                        'ALL': l10n.all,
                        'GLOBAL': l10n.global,
                        'NATIONAL': l10n.national,
                      }.entries)
                        ChoiceChip(
                          label: Text(entry.value),
                          selected: scopeFilter == entry.key,
                          onSelected: (_) =>
                              update(() => scopeFilter = entry.key),
                        ),
                    ],
                  ),
                  const SizedBox(height: 20),
                  Text(l10n.themedCollections),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    children: [
                      ChoiceChip(
                        label: Text(l10n.all),
                        selected: categoryFilter == null,
                        onSelected: (_) =>
                            update(() => categoryFilter = null),
                      ),
                      for (final key in _categories)
                        ChoiceChip(
                          label: Text(_categoryLabel(l10n, key)),
                          selected: categoryFilter == key,
                          onSelected: (_) =>
                              update(() => categoryFilter = key),
                        ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    child: TextButton.icon(
                      onPressed: () => update(() {
                        marketCode = widget.controller.preferences.marketCode;
                        officialityFilter = null;
                        categoryFilter = null;
                        scopeFilter = 'ALL';
                      }),
                      icon: const Icon(Icons.restart_alt_rounded),
                      label: Text(l10n.clearFilters),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Future<void> _showUpcoming(int days) async {
    final l10n = AppLocalizations.of(context);
    final locale = Localizations.localeOf(context).toLanguageTag();
    final start = DateTime.now();
    final entries = <_UpcomingDay>[];
    for (var offset = 1; offset <= days; offset++) {
      final date = DateTime(start.year, start.month, start.day)
          .add(Duration(days: offset));
      final records = _recordsForDate(date);
      if (records.isNotEmpty) {
        entries.add(_UpcomingDay(date: date, records: records));
      }
    }

    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (context) => FractionallySizedBox(
        heightFactor: .86,
        child: ListView(
          padding: const EdgeInsets.fromLTRB(20, 4, 20, 28),
          children: [
            Text(
              days == 7 ? l10n.upcoming7Days : l10n.upcoming30Days,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.w900,
                  ),
            ),
            const SizedBox(height: 16),
            if (entries.isEmpty)
              Text(l10n.noSearchResults)
            else
              for (final entry in entries) ...[
                Text(
                  DateFormat.yMMMMd(locale).format(entry.date),
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w800,
                      ),
                ),
                const SizedBox(height: 8),
                for (final record in entry.records) ...[
                  ObservanceCard(
                    observance: record,
                    favorite: widget.controller.isFavorite(record.id),
                    onFavorite: () =>
                        widget.controller.toggleFavorite(record.id),
                    onTap: () {
                      Navigator.of(context).pop();
                      _open(record);
                    },
                  ),
                  const SizedBox(height: 10),
                ],
                const SizedBox(height: 10),
              ],
          ],
        ),
      ),
    );
  }

  String _categoryLabel(AppLocalizations l10n, String key) =>
      switch (key) {
        'PLANET' => l10n.categoryPlanet,
        'HEALTH' => l10n.categoryHealth,
        'PEOPLE' => l10n.categoryPeople,
        'LEARNING' => l10n.categoryLearning,
        'CULTURE' => l10n.categoryCulture,
        'FOOD' => l10n.categoryFood,
        'FUTURE' => l10n.categoryFuture,
        'COMMUNITY' => l10n.categoryCommunity,
        _ => key,
      };

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

class _WeekdayHeader extends StatelessWidget {
  const _WeekdayHeader({required this.locale});

  final String locale;

  @override
  Widget build(BuildContext context) {
    final monday = DateTime(2026, 1, 5);
    return Row(
      children: [
        for (var offset = 0; offset < 7; offset++)
          Expanded(
            child: Text(
              DateFormat.E(locale).format(
                monday.add(Duration(days: offset)),
              ),
              textAlign: TextAlign.center,
              maxLines: 1,
              overflow: TextOverflow.fade,
              style: Theme.of(context).textTheme.labelMedium?.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                    fontWeight: FontWeight.w700,
                  ),
            ),
          ),
      ],
    );
  }
}

class _MonthGrid extends StatelessWidget {
  const _MonthGrid({
    required this.month,
    required this.selected,
    required this.locale,
    required this.observancesLabel,
    required this.countForDate,
    required this.onSelected,
  });

  final DateTime month;
  final DateTime selected;
  final String locale;
  final String observancesLabel;
  final int Function(DateTime date) countForDate;
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
        final count = countForDate(date);
        final active = _sameDate(date, selected);
        final isToday = _sameDate(date, DateTime.now());
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
                border: active || isToday
                    ? Border.all(
                        color: active
                            ? Theme.of(context).colorScheme.primary
                            : Theme.of(context).colorScheme.outline,
                        width: active ? 1.5 : 1,
                      )
                    : null,
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    '$day',
                    style: TextStyle(
                      fontWeight: active || isToday
                          ? FontWeight.w900
                          : FontWeight.w700,
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

class _UpcomingDay {
  const _UpcomingDay({required this.date, required this.records});

  final DateTime date;
  final List<Observance> records;
}
