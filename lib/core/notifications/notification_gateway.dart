import 'notification_health.dart';
import 'reminder_plan.dart';

abstract interface class NotificationGateway {
  bool get supported;

  Stream<String> get notificationTapStream;

  String? takeInitialPayload();

  Future<void> initialize({bool force = false});

  Future<bool> requestPermissions();

  Future<NotificationHealth> health();

  Future<void> openSystemSettings();

  Future<void> reconcile(Iterable<PlannedNotification> plan);

  Future<LocalNotificationDiagnostic> runLocalDiagnostic({
    required String immediateTitle,
    required String immediateBody,
    required String scheduledTitle,
    required String scheduledBody,
    Duration scheduledDelay = const Duration(seconds: 12),
  });

  void dispose();
}
