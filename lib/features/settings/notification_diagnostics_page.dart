import 'package:flutter/material.dart';

import '../../app/app_controller.dart';
import '../../core/notifications/notification_health.dart';
import '../../l10n/app_localizations.dart';

class NotificationDiagnosticsPage extends StatefulWidget {
  const NotificationDiagnosticsPage({
    super.key,
    required this.controller,
  });

  final AppController controller;

  @override
  State<NotificationDiagnosticsPage> createState() =>
      _NotificationDiagnosticsPageState();
}

class _NotificationDiagnosticsPageState
    extends State<NotificationDiagnosticsPage> {
  NotificationHealth? _health;
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _refresh();
  }

  Future<void> _refresh() async {
    if (!mounted) return;
    setState(() => _loading = true);
    final health = await widget.controller.notificationHealth();
    if (!mounted) return;
    setState(() {
      _health = health;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final health = _health;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.notificationStatus)),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 8, 16, 28),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(18),
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
                          style:
                              Theme.of(context).textTheme.titleMedium?.copyWith(
                                    fontWeight: FontWeight.w800,
                                  ),
                        ),
                      ),
                      if (_loading)
                        const SizedBox.square(
                          dimension: 18,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        ),
                    ],
                  ),
                  if (health != null) ...[
                    const SizedBox(height: 14),
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
                        padding: const EdgeInsets.only(top: 10),
                        child: SelectableText(
                          lastError,
                          style: Theme.of(context).textTheme.bodySmall,
                        ),
                      ),
                  ],
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          FilledButton.icon(
            onPressed: () async {
              final granted =
                  await widget.controller.requestNotificationPermission();
              if (!context.mounted) return;
              if (!granted) {
                _showMessage(l10n.notificationPermissionDenied);
              }
              await _refresh();
            },
            icon: const Icon(Icons.notifications_active_rounded),
            label: Text(l10n.enableNotifications),
          ),
          const SizedBox(height: 8),
          OutlinedButton.icon(
            onPressed: _runDiagnostic,
            icon: const Icon(Icons.science_outlined),
            label: Text(l10n.testNotifications),
          ),
          const SizedBox(height: 8),
          TextButton.icon(
            onPressed: () async {
              await widget.controller.openNotificationSettings();
              await _refresh();
            },
            icon: const Icon(Icons.settings_outlined),
            label: Text(l10n.openSystemNotificationSettings),
          ),
        ],
      ),
    );
  }

  Future<void> _runDiagnostic() async {
    final result = await widget.controller.runNotificationDiagnostic();
    if (!mounted) return;
    final l10n = AppLocalizations.of(context);
    _showMessage(
      result.ok ? l10n.notificationTestOk : l10n.notificationTestFailed,
    );
    await _refresh();
  }

  void _showMessage(String message) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(SnackBar(content: Text(message)));
  }
}

class _StatusLine extends StatelessWidget {
  const _StatusLine({required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 4),
        child: Row(
          children: [
            Icon(icon, size: 18),
            const SizedBox(width: 8),
            Expanded(child: Text(text)),
          ],
        ),
      );
}
