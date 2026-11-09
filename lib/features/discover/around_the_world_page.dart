import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/market_options.dart';
import '../../core/widgets/observance_card.dart';
import '../../domain/observance.dart';
import '../../features/detail/observance_detail_page.dart';
import '../../l10n/app_localizations.dart';

enum _ScopeFilter { all, national, global }

class AroundTheWorldPage extends StatefulWidget {
  const AroundTheWorldPage({super.key, required this.controller});
  final AppController controller;
  @override
  State<AroundTheWorldPage> createState() => _AroundTheWorldPageState();
}

class _AroundTheWorldPageState extends State<AroundTheWorldPage> {
  String? marketCode;
  _ScopeFilter scopeFilter = _ScopeFilter.all;

  @override
  void initState() {
    super.initState();
    final current = widget.controller.preferences.marketCode;
    marketCode = current == 'GLOBAL' ? null : current;
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final selectedMarket = marketCode;
    // Global observances are kept separate from country-issued observances.
    final national = selectedMarket == null
        ? const <Observance>[]
        : widget.controller.recordsForMarket(selectedMarket);
    final global = selectedMarket == null
        ? const <Observance>[]
        : widget.controller.recordsForMarket('GLOBAL', includeGlobal: true);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.aroundTheWorld)),
      body: CustomScrollView(
        slivers: [
          SliverPadding(
            padding: const EdgeInsets.fromLTRB(16, 4, 16, 18),
            sliver: SliverToBoxAdapter(
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(l10n.aroundTheWorld,
                          style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w900)),
                      const SizedBox(height: 8),
                      Text(l10n.aroundTheWorldDescription),
                      const SizedBox(height: 18),
                      DropdownButtonFormField<String?>(
                        isExpanded: true,
                        initialValue: marketCode,
                        decoration: InputDecoration(
                          labelText: l10n.market,
                          hintText: l10n.chooseCountry,
                          prefixIcon: const Icon(Icons.public_rounded),
                        ),
                        items: [
                          for (final option in marketOptions.where((item) => item.code != 'GLOBAL'))
                            DropdownMenuItem<String?>(
                              value: option.code,
                              child: Text(
                                '${option.emoji}  ${marketLabel(l10n, option.code)}',
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ),
                        ],
                        onChanged: (value) {
                          if (value == null) return;
                          setState(() => marketCode = value);
                        },
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
          if (selectedMarket == null)
            SliverPadding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              sliver: SliverToBoxAdapter(
                child: _BrowseStateCard(
                  icon: Icons.travel_explore_rounded,
                  title: l10n.chooseCountry,
                  body: l10n.chooseCountryDescription,
                ),
              ),
            )
          else ...[
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
              sliver: SliverToBoxAdapter(
                child: Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    ChoiceChip(
                      label: Text('${l10n.all} · ${national.length + global.length}'),
                      selected: scopeFilter == _ScopeFilter.all,
                      onSelected: (_) => setState(() => scopeFilter = _ScopeFilter.all),
                    ),
                    ChoiceChip(
                      label: Text('${l10n.national} · ${national.length}'),
                      selected: scopeFilter == _ScopeFilter.national,
                      onSelected: (_) => setState(() => scopeFilter = _ScopeFilter.national),
                    ),
                    ChoiceChip(
                      label: Text('${l10n.global} · ${global.length}'),
                      selected: scopeFilter == _ScopeFilter.global,
                      onSelected: (_) => setState(() => scopeFilter = _ScopeFilter.global),
                    ),
                  ],
                ),
              ),
            ),
            if (scopeFilter != _ScopeFilter.global) ...[
              _sectionHeader(context, l10n.countryObservances, national.length),
              if (national.isEmpty)
                SliverPadding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  sliver: SliverToBoxAdapter(
                    child: _BrowseStateCard(
                      icon: Icons.public_off_rounded,
                      title: marketLabel(l10n, selectedMarket),
                      body: l10n.noCountryObservances,
                    ),
                  ),
                )
              else
                _cards(national),
            ],
            if (scopeFilter != _ScopeFilter.national) ...[
              _sectionHeader(context, l10n.global, global.length),
              _cards(global),
            ],
          ],
          const SliverToBoxAdapter(child: SizedBox(height: 28)),
        ],
      ),
    );
  }

  Widget _sectionHeader(BuildContext context, String label, int count) =>
      SliverPadding(
        padding: const EdgeInsets.fromLTRB(16, 18, 16, 12),
        sliver: SliverToBoxAdapter(
          child: Row(
            children: [
              Expanded(child: Text(label,
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w900))),
              Text(count.toString(),
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800)),
            ],
          ),
        ),
      );

  Widget _cards(List<Observance> records) => SliverPadding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        sliver: SliverList.builder(
          itemCount: records.length,
          itemBuilder: (context, index) {
            final record = records[index];
            return Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: ObservanceCard(
                observance: record,
                favorite: widget.controller.isFavorite(record.id),
                onFavorite: () => widget.controller.toggleFavorite(record.id),
                onTap: () => _open(record),
              ),
            );
          },
        ),
      );

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

class _BrowseStateCard extends StatelessWidget {
  const _BrowseStateCard({
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
          padding: const EdgeInsets.all(20),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.w800,
                          ),
                    ),
                    const SizedBox(height: 6),
                    Text(body),
                  ],
                ),
              ),
            ],
          ),
        ),
      );
}
