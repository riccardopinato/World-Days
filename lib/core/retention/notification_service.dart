import 'package:flutter/foundation.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_timezone/flutter_timezone.dart';
import 'package:timezone/data/latest.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

final class ReminderRequest {
  const ReminderRequest({
    required this.id,
    required this.title,
    required this.body,
    required this.when,
    this.payload,
  });

  final int id;
  final String title;
  final String body;
  final DateTime when;
  final String? payload;
}

final class NotificationService {
  NotificationService();

  final FlutterLocalNotificationsPlugin _plugin =
      FlutterLocalNotificationsPlugin();

  bool _initialized = false;

  Future<String?> initialize({
    required ValueChanged<String> onPayload,
  }) async {
    if (kIsWeb) return null;
    try {
      tz.initializeTimeZones();
      final zone = await FlutterTimezone.getLocalTimezone();
      try {
        tz.setLocalLocation(tz.getLocation(zone.identifier));
      } catch (_) {
        tz.setLocalLocation(tz.UTC);
      }

      const settings = InitializationSettings(
        android: AndroidInitializationSettings('@mipmap/ic_launcher'),
        iOS: DarwinInitializationSettings(
          requestAlertPermission: false,
          requestBadgePermission: false,
          requestSoundPermission: false,
        ),
      );

      await _plugin.initialize(
        settings: settings,
        onDidReceiveNotificationResponse: (response) {
          final payload = response.payload;
          if (payload != null && payload.isNotEmpty) onPayload(payload);
        },
      );
      _initialized = true;

      final launch = await _plugin.getNotificationAppLaunchDetails();
      final payload = launch?.notificationResponse?.payload;
      return payload == null || payload.isEmpty ? null : payload;
    } catch (_) {
      _initialized = false;
      return null;
    }
  }

  Future<bool> requestPermission() async {
    if (kIsWeb || !_initialized) return false;
    try {
      switch (defaultTargetPlatform) {
        case TargetPlatform.android:
          return await _plugin
                  .resolvePlatformSpecificImplementation<
                      AndroidFlutterLocalNotificationsPlugin>()
                  ?.requestNotificationsPermission() ??
              true;
        case TargetPlatform.iOS:
          return await _plugin
                  .resolvePlatformSpecificImplementation<
                      IOSFlutterLocalNotificationsPlugin>()
                  ?.requestPermissions(
                    alert: true,
                    badge: true,
                    sound: true,
                  ) ??
              false;
        default:
          return false;
      }
    } catch (_) {
      return false;
    }
  }

  Future<void> replaceSchedule(List<ReminderRequest> requests) async {
    if (kIsWeb || !_initialized) return;
    try {
      await _plugin.cancelAllPendingNotifications();
      final now = tz.TZDateTime.now(tz.local);

      for (final request in requests) {
        final when = tz.TZDateTime(
          tz.local,
          request.when.year,
          request.when.month,
          request.when.day,
          request.when.hour,
          request.when.minute,
        );
        if (!when.isAfter(now)) continue;

        await _plugin.zonedSchedule(
          id: request.id,
          title: request.title,
          body: request.body,
          scheduledDate: when,
          notificationDetails: const NotificationDetails(
            android: AndroidNotificationDetails(
              'world_days_reminders',
              'World Days reminders',
              channelDescription:
                  'Daily, weekly, category and favorite observance reminders.',
              importance: Importance.defaultImportance,
              priority: Priority.defaultPriority,
            ),
            iOS: DarwinNotificationDetails(),
          ),
          androidScheduleMode: AndroidScheduleMode.inexactAllowWhileIdle,
          payload: request.payload,
        );
      }
    } catch (_) {
      // Reminder scheduling is non-critical. App content remains fully usable.
    }
  }

  Future<int> pendingCount() async {
    if (kIsWeb || !_initialized) return 0;
    try {
      return (await _plugin.pendingNotificationRequests()).length;
    } catch (_) {
      return 0;
    }
  }
}
