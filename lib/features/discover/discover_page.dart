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
      records = records
          .where((item) => item.authority.officiality == officiality)
          .toList(growable: false);
    }

    return Scaffold(
      appBar: AppBar(title: Text(l10n.discover)),
      body: CustomScrollView(
        slivers: [
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 18),
            sliver: SliverToBoxAdapter(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  TextField(
                    controller: _search,
                    onChanged: (_) => setState(() {}),
                    textInputAction: TextInputAction.search,
                    decoration: InputDecoration(
                      hintText: l10n.searchHint,
                      prefixIcon: const Icon(Icons.search_rounded),
                      suffixIcon: _search.text.isEmpty
                          ? null
                          : IconButton(
                              tooltip: l10n.clearSearch,
                              onPressed: () {
                                _search.clear();
                                setState(() {});
                              },
                              icon: const Icon(Icons.close_rounded),
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
                        onSelected: (_) =>
                            setState(() => officiality = 'OFFICIAL_UN'),
                      ),
                      FilterChip(
                        label: const Text('UNESCO'),
                        selected: officiality == 'OFFICIAL_UNESCO',
                        onSelected: (_) =>
                            setState(() => officiality = 'OFFICIAL_UNESCO'),
                      ),
                      FilterChip(
                        label: const Text('WHO'),
                        selected: officiality == 'OFFICIAL_WHO',
                        onSelected: (_) =>
                            setState(() => officiality = 'OFFICIAL_WHO'),
                      ),
                      FilterChip(
                        label: Text(l10n.recognized),
                        selected: officiality == 'RECOGNIZED_NGO',
                        onSelected: (_) =>
                            setState(() => officiality = 'RECOGNIZED_NGO'),
                      ),
                      FilterChip(
                        label: Text(l10n.popular),
                        selected: officiality == 'POPULAR',
                        onSelected: (_) =>
                            setState(() => officiality = 'POPULAR'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 18),
                  FilledButton.icon(
                    onPressed: records.isEmpty
                        ? null
                        : () => _open(
                              records[Random().nextInt(records.length)],
                            ),
                    icon: const Icon(Icons.casino_rounded),
                    label: Text(l10n.surpriseMe),
                  ),
                  const SizedBox(height: 22),
                  Text(
                    '${records.length} ${l10n.observances}',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w800,
                        ),
                  ),
                ],
              ),
            ),
          ),
          if (records.isEmpty)
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
              sliver: SliverToBoxAdapter(
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Row(
                      children: [
                        const Icon(Icons.search_off_rounded),
                        const SizedBox(width: 12),
                        Expanded(child: Text(l10n.noSearchResults)),
                      ],
                    ),
                  ),
                ),
              ),
            )
          else
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 32),
              sliver: SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    final record = records[index];
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: ObservanceCard(
                        observance: record,
                        favorite: widget.controller.isFavorite(record.id),
                        onFavorite: () =>
                            widget.controller.toggleFavorite(record.id),
                        onTap: () => _open(record),
                      ),
                    );
                  },
                  childCount: records.length,
                ),
              ),
            ),
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
