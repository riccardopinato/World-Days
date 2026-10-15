import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/market_options.dart';
import '../../core/widgets/observance_card.dart';
import '../../domain/observance.dart';
import '../../features/detail/observance_detail_page.dart';
import '../../l10n/app_localizations.dart';

class AroundTheWorldPage extends StatefulWidget {
  const AroundTheWorldPage({super.key, required this.controller});

  final AppController controller;

  @override
  State<AroundTheWorldPage> createState() => _AroundTheWorldPageState();
}

class _AroundTheWorldPageState extends State<AroundTheWorldPage> {
  String? marketCode;

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
    final records = selectedMarket == null
        ? const <Observance>[]
        : widget.controller.recordsForMarket(selectedMarket);

    return Scaffold(
      appBar: AppBar(title: Text(l10n.aroundTheWorld)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 4, 16, 32),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    l10n.aroundTheWorld,
                    style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                          fontWeight: FontWeight.w900,
                        ),
                  ),
                  const SizedBox(height: 8),
                  Text(l10n.aroundTheWorldDescription),
                  const SizedBox(height: 18),
                  DropdownButtonFormField<String?>(
                    initialValue: marketCode,
                    decoration: InputDecoration(
                      labelText: l10n.market,
                      hintText: l10n.chooseCountry,
                      prefixIcon: const Icon(Icons.public_rounded),
                    ),
                    items: [
                      for (final option in marketOptions.where(
                        (item) => item.code != 'GLOBAL',
                      ))
                        DropdownMenuItem<String?>(
                          value: option.code,
                          child: Text(
                            '${option.emoji}  ${marketLabel(l10n, option.code)}',
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
          const SizedBox(height: 22),
          if (selectedMarket == null)
            _BrowseStateCard(
              icon: Icons.travel_explore_rounded,
              title: l10n.chooseCountry,
              body: l10n.chooseCountryDescription,
            )
          else ...[
            Row(
              children: [
                Expanded(
                  child: Text(
                    l10n.countryObservances,
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.w900,
                        ),
                  ),
                ),
                Text(
                  '${records.length}',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w800,
                      ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            if (records.isEmpty)
              _BrowseStateCard(
                icon: Icons.public_off_rounded,
                title: marketLabel(l10n, selectedMarket),
                body: l10n.noCountryObservances,
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
