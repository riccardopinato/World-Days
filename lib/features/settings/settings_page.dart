import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/market_options.dart';
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
        padding: const EdgeInsets.fromLTRB(16, 0, 16, 32),
        children: [
          _SectionTitle(l10n.theme),
          SegmentedButton<ThemeMode>(
            segments: [
              ButtonSegment(
                value: ThemeMode.system,
                label: Text(l10n.system),
                icon: const Icon(Icons.phone_android_rounded),
              ),
              ButtonSegment(
                value: ThemeMode.light,
                label: Text(l10n.light),
                icon: const Icon(Icons.light_mode_rounded),
              ),
              ButtonSegment(
                value: ThemeMode.dark,
                label: Text(l10n.dark),
                icon: const Icon(Icons.dark_mode_rounded),
              ),
            ],
            selected: {controller.preferences.themeMode},
            onSelectionChanged: (values) =>
                controller.setThemeMode(values.single),
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.language),
          DropdownButtonFormField<String?>(
            initialValue: controller.preferences.localeCode,
            decoration: const InputDecoration(
              prefixIcon: Icon(Icons.language_rounded),
            ),
            items: [
              DropdownMenuItem<String?>(
                value: null,
                child: Text(l10n.deviceLanguage),
              ),
              for (final entry in localeOptions.entries)
                DropdownMenuItem<String?>(
                  value: entry.key,
                  child: Text(entry.value),
                ),
            ],
            onChanged: controller.setLocale,
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.notifications),
          Card(
            child: Column(
              children: [
                SwitchListTile(
                  secondary: const Icon(Icons.notifications_active_outlined),
                  title: Text(l10n.dailyReminder),
                  subtitle: Text(l10n.dailyReminderDescription),
                  value: controller.preferences.dailyReminderEnabled,
                  onChanged: (value) async {
                    final ok = await controller.setDailyReminder(value);
                    if (!ok && context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(l10n.notificationPermissionDenied),
                        ),
                      );
                    }
                  },
                ),
                if (controller.preferences.dailyReminderEnabled)
                  ListTile(
                    leading: const Icon(Icons.schedule_rounded),
                    title: Text(l10n.reminderTime),
                    trailing: Text(
                      TimeOfDay(
                        hour: controller.preferences.dailyReminderHour,
                        minute: controller.preferences.dailyReminderMinute,
                      ).format(context),
                    ),
                    onTap: () async {
                      final current = TimeOfDay(
                        hour: controller.preferences.dailyReminderHour,
                        minute: controller.preferences.dailyReminderMinute,
                      );
                      final picked = await showTimePicker(
                        context: context,
                        initialTime: current,
                      );
                      if (picked != null) {
                        await controller.setDailyReminderTime(picked);
                      }
                    },
                  ),
                SwitchListTile(
                  secondary: const Icon(Icons.view_week_outlined),
                  title: Text(l10n.weeklyDigest),
                  subtitle: Text(l10n.weeklyDigestDescription),
                  value: controller.preferences.weeklyDigestEnabled,
                  onChanged: (value) async {
                    final ok = await controller.setWeeklyDigest(value);
                    if (!ok && context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(l10n.notificationPermissionDenied),
                        ),
                      );
                    }
                  },
                ),
              ],
            ),
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.market),
          Text(
            l10n.marketDescription,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            initialValue: controller.preferences.marketCode,
            decoration: const InputDecoration(
              prefixIcon: Icon(Icons.public_rounded),
            ),
            items: [
              for (final option in marketOptions)
                DropdownMenuItem<String>(
                  value: option.code,
                  child: Text(
                    '${option.emoji}  ${marketLabel(l10n, option.code)}',
                  ),
                ),
            ],
            onChanged: (value) {
              if (value != null) controller.setMarket(value);
            },
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.about),
          Card(
            child: ListTile(
              leading: const Icon(Icons.dataset_outlined),
              title: Text(l10n.dataset),
              subtitle: Text(
                '$recordCount ${l10n.observances} · ${l10n.offlineFirst}',
              ),
            ),
          ),
          const SizedBox(height: 10),
          Card(
            child: ListTile(
              leading: const Icon(Icons.verified_outlined),
              title: Text(l10n.dataPolicy),
              subtitle: Text(l10n.dataPolicyDescription),
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
        child: Text(
          text,
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                fontWeight: FontWeight.w800,
              ),
        ),
      );
}
