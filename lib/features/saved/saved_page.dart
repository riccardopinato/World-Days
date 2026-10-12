import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/widgets/observance_card.dart';
import '../../domain/observance.dart';
import '../../features/detail/observance_detail_page.dart';
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

    return Scaffold(
      appBar: AppBar(title: Text(l10n.saved)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 28),
        children: [
          Text(l10n.favorites, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
          const SizedBox(height: 12),
          if (favorites.isEmpty)
            Padding(padding: const EdgeInsets.symmetric(vertical: 20), child: Text(l10n.noFavorites))
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
          Text(l10n.recent, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
          const SizedBox(height: 12),
          if (recent.isEmpty)
            Padding(padding: const EdgeInsets.symmetric(vertical: 20), child: Text(l10n.noRecent))
          else
            for (final record in recent) ...[
              ObservanceCard(observance: record, onTap: () => _open(context, record)),
              const SizedBox(height: 10),
            ],
        ],
      ),
    );
  }

  void _open(BuildContext context, Observance record) {
    Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ObservanceDetailPage(observance: record, controller: controller),
      ),
    );
  }
}
