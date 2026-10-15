import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/semantic_categories.dart';
import '../../core/widgets/observance_card.dart';
import '../../domain/observance.dart';
import '../../features/detail/observance_detail_page.dart';
import '../../features/settings/settings_page.dart';
import '../../l10n/app_localizations.dart';

class SavedPage extends StatelessWidget {
  const SavedPage({super.key, required this.controller});
  final AppController controller;

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final catalog = controller.catalog;
    final favorites = catalog == null
        ? const <Observance>[]
        : controller.preferences.favoriteIds
            .map((id) => catalog.byId[id])
            .whereType<Observance>()
            .toList(growable: false);
    final recent = catalog == null
        ? const <Observance>[]
        : controller.preferences.recentIds
            .map((id) => catalog.byId[id])
            .whereType<Observance>()
            .toList(growable: false);
    final reminders = controller.preferences.reminders;
    final followedCategories = semanticCategoryKeys
        .where(reminders.followedCategories.contains)
        .toList(growable: false);
    final reminderSubscriptions = <String>[
      if (reminders.dailyEnabled) l10n.dailyReminder,
      if (reminders.weeklyEnabled) l10n.weeklyReminder,
      if (reminders.favoriteEnabled) l10n.favoriteReminders,
      if (reminders.categoryEnabled) l10n.categoryReminders,
    ];

    return Scaffold(
      appBar: AppBar(title: Text(l10n.saved)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 28),
        children: [
          _SectionTitle(l10n.favorites),
          if (favorites.isEmpty)
            _EmptyCopy(l10n.noFavorites)
          else
            for (final record in favorites) ...[
              ObservanceCard(
                observance: record,
                favorite: true,
                onFavorite: () => controller.toggleFavorite(record.id),
                onTap: () => _open(context, record),
              ),
              const SizedBox(height: 10),
            ],
          const SizedBox(height: 24),
          _SectionTitle(l10n.followedCategories),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: followedCategories.isEmpty
                  ? Text(l10n.noFollowedCategories)
                  : Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        for (final key in followedCategories)
                          Chip(
                            avatar: const Icon(Icons.category_rounded, size: 18),
                            label: Text(semanticCategoryLabel(l10n, key)),
                          ),
                      ],
                    ),
            ),
          ),
          const SizedBox(height: 24),
          _SectionTitle(l10n.reminderSubscriptions),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: reminderSubscriptions.isEmpty
                  ? Text(l10n.noReminderSubscriptions)
                  : Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        for (final label in reminderSubscriptions)
                          Chip(
                            avatar: const Icon(
                              Icons.notifications_active_rounded,
                              size: 18,
                            ),
                            label: Text(label),
                          ),
                      ],
                    ),
            ),
          ),
          const SizedBox(height: 8),
          Align(
            alignment: Alignment.centerLeft,
            child: OutlinedButton.icon(
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute<void>(
                  builder: (_) => SettingsPage(controller: controller),
                ),
              ),
              icon: const Icon(Icons.settings_rounded),
              label: Text(l10n.manageInSettings),
            ),
          ),
          const SizedBox(height: 24),
          _SectionTitle(l10n.recent),
          if (recent.isEmpty)
            _EmptyCopy(l10n.noRecent)
          else
            for (final record in recent) ...[
              ObservanceCard(
                observance: record,
                onTap: () => _open(context, record),
              ),
              const SizedBox(height: 10),
            ],
        ],
      ),
    );
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

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.label);
  final String label;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: Text(
          label,
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.w800,
              ),
        ),
      );
}

class _EmptyCopy extends StatelessWidget {
  const _EmptyCopy(this.label);
  final String label;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 20),
        child: Text(label),
      );
}
