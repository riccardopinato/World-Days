import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../l10n/app_localizations.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key, required this.controller});
  final AppController controller;

  static const localeOptions = <String, String>{
    'en': 'English',
    'it': 'Italiano',
    'es': 'Español',
    'fr': 'Français',
    'de': 'Deutsch',
    'pt': 'Português',
  };

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final recordCount = controller.catalog?.records.length ?? 0;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.settings)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 28),
        children: [
          _SectionTitle(l10n.theme),
          SegmentedButton<ThemeMode>(
            segments: [
              ButtonSegment(value: ThemeMode.system, label: Text(l10n.system), icon: const Icon(Icons.phone_android)),
              ButtonSegment(value: ThemeMode.light, label: Text(l10n.light), icon: const Icon(Icons.light_mode)),
              ButtonSegment(value: ThemeMode.dark, label: Text(l10n.dark), icon: const Icon(Icons.dark_mode)),
            ],
            selected: {controller.preferences.themeMode},
            onSelectionChanged: (values) => controller.setThemeMode(values.single),
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.language),
          DropdownButtonFormField<String?>(
            value: controller.preferences.localeCode,
            decoration: const InputDecoration(prefixIcon: Icon(Icons.language)),
            items: [
              DropdownMenuItem<String?>(value: null, child: Text(l10n.deviceLanguage)),
              for (final entry in localeOptions.entries)
                DropdownMenuItem<String?>(value: entry.key, child: Text(entry.value)),
            ],
            onChanged: controller.setLocale,
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.about),
          Card(
            child: ListTile(
              leading: const Icon(Icons.dataset_outlined),
              title: Text(l10n.dataset),
              subtitle: Text('$recordCount ${l10n.observances} · bundled offline-first'),
            ),
          ),
          const SizedBox(height: 10),
          const Card(
            child: ListTile(
              leading: Icon(Icons.verified_outlined),
              title: Text('Data policy'),
              subtitle: Text('Official badges require primary/originator evidence. Discovery candidates remain separate until verified.'),
            ),
          ),
        ],
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  const _SectionTitle(this.text);
  final String text;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 12),
        child: Text(text, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800)),
      );
}
