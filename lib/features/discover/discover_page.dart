import 'dart:math';

import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/widgets/observance_card.dart';
import '../../domain/observance.dart';
import '../../features/detail/observance_detail_page.dart';
import '../../l10n/app_localizations.dart';

class DiscoverPage extends StatefulWidget {
  const DiscoverPage({super.key, required this.controller});
  final AppController controller;

  @override
  State<DiscoverPage> createState() => _DiscoverPageState();
}

class _DiscoverPageState extends State<DiscoverPage> {
  final _search = TextEditingController();
  String? officiality;

  @override
  void dispose() {
    _search.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    var records = widget.controller.search(_search.text);
    if (officiality != null) {
      records = records.where((item) => item.authority.officiality == officiality).toList(growable: false);
    }

    return Scaffold(
      appBar: AppBar(title: Text(l10n.discover)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 28),
        children: [
          TextField(
            controller: _search,
            onChanged: (_) => setState(() {}),
            decoration: InputDecoration(
              hintText: l10n.searchHint,
              prefixIcon: const Icon(Icons.search),
              suffixIcon: _search.text.isEmpty
                  ? null
                  : IconButton(
                      onPressed: () {
                        _search.clear();
                        setState(() {});
                      },
                      icon: const Icon(Icons.close),
                    ),
            ),
          ),
          const SizedBox(height: 14),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              FilterChip(
                label: Text(l10n.all),
                selected: officiality == null,
                onSelected: (_) => setState(() => officiality = null),
              ),
              FilterChip(
                label: const Text('UN'),
                selected: officiality == 'OFFICIAL_UN',
                onSelected: (_) => setState(() => officiality = 'OFFICIAL_UN'),
              ),
              FilterChip(
                label: const Text('UNESCO'),
                selected: officiality == 'OFFICIAL_UNESCO',
                onSelected: (_) => setState(() => officiality = 'OFFICIAL_UNESCO'),
              ),
              FilterChip(
                label: const Text('WHO'),
                selected: officiality == 'OFFICIAL_WHO',
                onSelected: (_) => setState(() => officiality = 'OFFICIAL_WHO'),
              ),
            ],
          ),
          const SizedBox(height: 18),
          FilledButton.icon(
            onPressed: records.isEmpty ? null : () => _open(records[Random().nextInt(records.length)]),
            icon: const Icon(Icons.casino_rounded),
            label: Text(l10n.surpriseMe),
          ),
          const SizedBox(height: 22),
          Text('${records.length} ${l10n.observances}', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 12),
          for (final record in records.take(100)) ...[
            ObservanceCard(
              observance: record,
              favorite: widget.controller.isFavorite(record.id),
              onFavorite: () => widget.controller.toggleFavorite(record.id),
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
        builder: (_) => ObservanceDetailPage(observance: record, controller: widget.controller),
      ),
    );
  }
}
