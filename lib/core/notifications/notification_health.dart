class NotificationHealth {
  const NotificationHealth({
    required this.available,
    required this.notificationsEnabled,
    required this.exactAlarmsEnabled,
    required this.reminderChannelEnabled,
    required this.pendingCount,
    this.lastError,
  });

  final bool available;
  final bool notificationsEnabled;
  final bool exactAlarmsEnabled;
  final bool reminderChannelEnabled;
  final int pendingCount;
  final String? lastError;

  bool get deliveryReady =>
      available && notificationsEnabled && reminderChannelEnabled;
}

class LocalNotificationDiagnostic {
  const LocalNotificationDiagnostic({
    required this.permissionGranted,
    required this.immediateShown,
    required this.scheduledCreated,
    required this.scheduledDelaySeconds,
    required this.health,
    this.error,
  });

  final bool permissionGranted;
  final bool immediateShown;
  final bool scheduledCreated;
  final int scheduledDelaySeconds;
  final NotificationHealth health;
  final String? error;

  bool get ok =>
      permissionGranted &&
      immediateShown &&
      scheduledCreated &&
      health.deliveryReady;
}
