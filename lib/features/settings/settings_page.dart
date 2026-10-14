import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/market_options.dart';
import '../../core/notifications/notification_health.dart';
import '../../l10n/app_localizations.dart';

class SettingsPage extends StatefulWidget {
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
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  NotificationHealth? _health;
  bool _loadingHealth = false;
  bool _widgetPinSupported = false;

  static const _visualKeys = <String>[
    'planet',
    'health',
    'people',
    'learning',
    'culture',
    'food',
    'future',
    'community',
  ];

  @override
  void initState() {
    super.initState();
    _refreshNativeState();
  }

  @override
  void didUpdateWidget(covariant SettingsPage oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.controller != widget.controller) {
      _refreshNativeState();
    }
  }

  Future<void> _refreshNativeState() async {
    if (!mounted) return;
    setState(() => _loadingHealth = true);
    NotificationHealth? health;
    var widgetPinSupported = false;
    if (widget.controller.nativeNotificationsAvailable) {
      health = await widget.controller.notificationHealth();
    }
    if (widget.controller.androidWidgetAvailable) {
      widgetPinSupported =
          await widget.controller.isHomeWidgetPinSupported();
    }
    if (!mounted) return;
    setState(() {
      _health = health;
      _widgetPinSupported = widgetPinSupported;
      _loadingHealth = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final recordCount = widget.controller.catalog?.records.length ?? 0;
    final reminders = widget.controller.preferences.reminders;

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
            selected: {widget.controller.preferences.themeMode},
            onSelectionChanged: (values) =>
                widget.controller.setThemeMode(values.single),
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.language),
          DropdownButtonFormField<String?>(
            initialValue: widget.controller.preferences.localeCode,
            decoration: const InputDecoration(
              prefixIcon: Icon(Icons.language_rounded),
            ),
            items: [
              DropdownMenuItem<String?>(
                value: null,
                child: Text(l10n.deviceLanguage),
              ),
              for (final entry in SettingsPage.localeOptions.entries)
                DropdownMenuItem<String?>(
                  value: entry.key,
                  child: Text(entry.value),
                ),
            ],
            onChanged: widget.controller.setLocale,
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.market),
          Text(
            l10n.marketDescription,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            initialValue: widget.controller.preferences.marketCode,
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
              if (value != null) widget.controller.setMarket(value);
            },
          ),
          const SizedBox(height: 28),
          _SectionTitle(l10n.reminders),
          Text(
            l10n.remindersDescription,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 12),
          if (!widget.controller.nativeNotificationsAvailable)
            Card(
              child: ListTile(
                leading: const Icon(Icons.phone_android_rounded),
                title: Text(l10n.nativeFeaturesMobileOnly),
              ),
            )
          else ...[
            Card(
              child: SwitchListTile.adaptive(
                value: reminders.dailyEnabled,
                secondary: const Icon(Icons.today_rounded),
                title: Text(l10n.dailyReminder),
                subtitle: Text(l10n.dailyReminderDescription),
                onChanged: (value) =>
                    _setReminderToggle(
                  () => widget.controller
                      .setDailyReminderEnabled(value),
                ),
              ),
            ),
            Card(
              child: ListTile(
                enabled: reminders.dailyEnabled,
                leading: const Icon(Icons.schedule_rounded),
                title: Text(l10n.reminderTime),
                trailing: Text(
                  MaterialLocalizations.of(context).formatTimeOfDay(
                    TimeOfDay(
                      hour: reminders.dailyHour,
                      minute: reminders.dailyMinute,
                    ),
                  ),
                ),
                onTap: reminders.dailyEnabled
                    ? () => _pickDailyTime(context)
                    : null,
              ),
            ),
            Card(
              child: SwitchListTile.adaptive(
                value: reminders.weeklyEnabled,
                secondary: const Icon(Icons.date_range_rounded),
                title: Text(l10n.weeklyReminder),
                subtitle: Text(l10n.weeklyReminderDescription),
                onChanged: (value) =>
                    _setReminderToggle(
                  () => widget.controller
                      .setWeeklyReminderEnabled(value),
                ),
              ),
            ),
            Card(
              child: ListTile(
                enabled: reminders.weeklyEnabled,
                leading: const Icon(Icons.schedule_rounded),
                title: Text(l10n.weeklyTime),
                trailing: Text(
                  MaterialLocalizations.of(context).formatTimeOfDay(
                    TimeOfDay(
                      hour: reminders.weeklyHour,
                      minute: reminders.weeklyMinute,
                    ),
                  ),
                ),
                onTap: reminders.weeklyEnabled
                    ? () => _pickWeeklyTime(context)
                    : null,
              ),
            ),
            Card(
              child: SwitchListTile.adaptive(
                value: reminders.favoriteEnabled,
                secondary: const Icon(Icons.favorite_rounded),
                title: Text(l10n.favoriteReminders),
                subtitle: Text(l10n.favoriteRemindersDescription),
                onChanged: (value) =>
                    _setReminderToggle(
                  () => widget.controller
                      .setFavoriteReminderEnabled(value),
                ),
              ),
            ),
            Card(
              child: SwitchListTile.adaptive(
                value: reminders.categoryEnabled,
                secondary: const Icon(Icons.category_rounded),
                title: Text(l10n.categoryReminders),
                subtitle: Text(l10n.categoryRemindersDescription),
                onChanged: (value) =>
                    _setReminderToggle(
                  () => widget.controller
                      .setCategoryReminderEnabled(value),
                ),
              ),
            ),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      l10n.followedCategories,
                      style:
                          Theme.of(context).textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.w800,
                              ),
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        for (final key in _visualKeys)
                          FilterChip(
                            selected:
                                reminders.followedVisualKeys.contains(key),
                            label: Text(_categoryLabel(l10n, key)),
                            onSelected: (_) => widget.controller
                                .toggleFollowedVisualKey(key),
                          ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            _notificationHealthCard(context, l10n),
          ],
          if (widget.controller.androidWidgetAvailable) ...[
            const SizedBox(height: 28),
            _SectionTitle(l10n.homeWidget),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(l10n.homeWidgetDescription),
                    const SizedBox(height: 14),
                    FilledButton.icon(
                      onPressed: _widgetPinSupported
                          ? () => _pinWidget(context)
                          : null,
                      icon: const Icon(Icons.widgets_rounded),
                      label: Text(l10n.addHomeWidget),
                    ),
                    if (!_widgetPinSupported) ...[
                      const SizedBox(height: 8),
                      Text(
                        l10n.homeWidgetUnavailable,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ],
                ),
              ),
            ),
          ],
          if (widget.controller.monetization.supported &&
              widget.controller.monetization.privacyOptionsRequired) ...[
            const SizedBox(height: 28),
            _SectionTitle(l10n.monetization),
            Card(
              child: ListTile(
                leading: const Icon(Icons.privacy_tip_outlined),
                title: Text(l10n.privacyChoices),
                subtitle: Text(l10n.privacyChoicesDescription),
                trailing: const Icon(Icons.chevron_right_rounded),
                onTap: () => _openPrivacyChoices(context),
              ),
            ),
          ],
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

  Widget _notificationHealthCard(
    BuildContext context,
    AppLocalizations l10n,
  ) {
    final health = _health;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.health_and_safety_outlined),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    l10n.notificationStatus,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w800,
                        ),
                  ),
                ),
                if (_loadingHealth)
                  const SizedBox.square(
                    dimension: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
              ],
            ),
            if (health != null) ...[
              const SizedBox(height: 12),
              _StatusLine(
                icon: health.notificationsEnabled
                    ? Icons.check_circle_rounded
                    : Icons.notifications_off_rounded,
                text: health.notificationsEnabled
                    ? l10n.notificationsEnabled
                    : l10n.notificationsDisabled,
              ),
              _StatusLine(
                icon: health.reminderChannelEnabled
                    ? Icons.check_circle_rounded
                    : Icons.block_rounded,
                text: health.reminderChannelEnabled
                    ? l10n.reminderChannelReady
                    : l10n.reminderChannelBlocked,
              ),
              _StatusLine(
                icon: health.exactAlarmsEnabled
                    ? Icons.alarm_on_rounded
                    : Icons.timelapse_rounded,
                text: health.exactAlarmsEnabled
                    ? l10n.exactAlarmAvailable
                    : l10n.exactAlarmFallback,
              ),
              _StatusLine(
                icon: Icons.schedule_rounded,
                text:
                    '${l10n.pendingNotifications}: ${health.pendingCount}',
              ),
              if (health.lastError case final lastError?)
                Padding(
                  padding: const EdgeInsets.only(top: 8),
                  child: SelectableText(
                    lastError,
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ),
            ],
            const SizedBox(height: 14),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                OutlinedButton.icon(
                  onPressed: () async {
                    final granted = await widget.controller
                        .requestNotificationPermission();
                    if (!granted && context.mounted) {
                      _showMessage(
                        context,
                        l10n.notificationPermissionDenied,
                      );
                    }
                    await _refreshNativeState();
                  },
                  icon: const Icon(Icons.notifications_active_rounded),
                  label: Text(l10n.enableNotifications),
                ),
                OutlinedButton.icon(
                  onPressed: () => _runDiagnostic(context),
                  icon: const Icon(Icons.science_outlined),
                  label: Text(l10n.testNotifications),
                ),
                TextButton.icon(
                  onPressed: () async {
                    await widget.controller.openNotificationSettings();
                    await _refreshNativeState();
                  },
                  icon: const Icon(Icons.settings_outlined),
                  label: Text(l10n.openSystemNotificationSettings),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _setReminderToggle(
    Future<bool> Function() action,
  ) async {
    final ok = await action();
    if (!mounted) return;
    if (!ok) {
      _showMessage(
        context,
        AppLocalizations.of(context).notificationPermissionDenied,
      );
    }
    await _refreshNativeState();
  }

  Future<void> _pickDailyTime(BuildContext context) async {
    final reminders = widget.controller.preferences.reminders;
    final result = await showTimePicker(
      context: context,
      initialTime: TimeOfDay(
        hour: reminders.dailyHour,
        minute: reminders.dailyMinute,
      ),
    );
    if (result == null) return;
    await widget.controller.setDailyReminderTime(result);
    await _refreshNativeState();
  }

  Future<void> _pickWeeklyTime(BuildContext context) async {
    final reminders = widget.controller.preferences.reminders;
    final result = await showTimePicker(
      context: context,
      initialTime: TimeOfDay(
        hour: reminders.weeklyHour,
        minute: reminders.weeklyMinute,
      ),
    );
    if (result == null) return;
    await widget.controller.setWeeklyReminderTime(result);
    await _refreshNativeState();
  }

  Future<void> _runDiagnostic(BuildContext context) async {
    final result = await widget.controller.runNotificationDiagnostic();
    if (!context.mounted) return;
    final l10n = AppLocalizations.of(context);
    _showMessage(
      context,
      result.ok ? l10n.notificationTestOk : l10n.notificationTestFailed,
    );
    await _refreshNativeState();
  }

  Future<void> _openPrivacyChoices(BuildContext context) async {
    final ok = await widget.controller.monetization.showPrivacyOptions();
    if (!context.mounted) return;
    final l10n = AppLocalizations.of(context);
    _showMessage(
      context,
      ok ? l10n.privacyChoicesUpdated : l10n.privacyChoicesFailed,
    );
  }

  Future<void> _pinWidget(BuildContext context) async {
    final ok = await widget.controller.requestHomeWidgetPin();
    if (!ok && context.mounted) {
      _showMessage(
        context,
        AppLocalizations.of(context).homeWidgetUnavailable,
      );
    }
  }

  void _showMessage(BuildContext context, String message) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text(message)));
  }

  String _categoryLabel(AppLocalizations l10n, String key) =>
      switch (key) {
        'planet' => l10n.categoryPlanet,
        'health' => l10n.categoryHealth,
        'people' => l10n.categoryPeople,
        'learning' => l10n.categoryLearning,
        'culture' => l10n.categoryCulture,
        'food' => l10n.categoryFood,
        'future' => l10n.categoryFuture,
        'community' => l10n.categoryCommunity,
        _ => key,
      };
}

class _StatusLine extends StatelessWidget {
  const _StatusLine({required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 3),
        child: Row(
          children: [
            Icon(icon, size: 18),
            const SizedBox(width: 8),
            Expanded(child: Text(text)),
          ],
        ),
      );
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
