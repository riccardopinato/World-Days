import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_timezone/flutter_timezone.dart';
import 'package:timezone/data/latest.dart' as tz_data;
import 'package:timezone/timezone.dart' as tz;

import 'notification_health.dart';
import 'reminder_plan.dart';

@pragma('vm:entry-point')
void notificationTapBackground(NotificationResponse response) {
  // World Days has no background notification actions. The user-visible
  // navigation is handled on the main isolate when the app opens.
}

class NotificationService {
  NotificationService._();

  static final NotificationService instance = NotificationService._();

  static const String reminderChannelId = 'world_days_reminders_v1';
  static const String reminderChannelName = 'World Days reminders';
  static const String reminderChannelDescription =
      'Daily, weekly, favorite and category reminders';

  final FlutterLocalNotificationsPlugin _plugin =
      FlutterLocalNotificationsPlugin();
  final StreamController<String> _tapController =
      StreamController<String>.broadcast();

  bool _initialized = false;
  bool _available = true;
  String? _lastError;
  String? _initialPayload;

  bool get supported =>
      !kIsWeb &&
      (defaultTargetPlatform == TargetPlatform.android ||
          defaultTargetPlatform == TargetPlatform.iOS);

  Stream<String> get notificationTapStream => _tapController.stream;

  String? takeInitialPayload() {
    final payload = _initialPayload;
    _initialPayload = null;
    return payload;
  }

  Future<void> initialize({bool force = false}) async {
    if (_initialized && !force) return;
    if (!supported) {
      _initialized = true;
      _available = false;
      _lastError = 'notifications_not_supported_on_this_platform';
      return;
    }

    _available = true;
    _lastError = null;
    tz_data.initializeTimeZones();

    try {
      final info = await FlutterTimezone.getLocalTimezone();
      tz.setLocalLocation(tz.getLocation(info.identifier));
    } catch (_) {
      // UTC/default timezone remains available as a safe fallback.
    }

    const android = AndroidInitializationSettings('@mipmap/ic_launcher');
    const darwin = DarwinInitializationSettings(
      requestAlertPermission: false,
      requestBadgePermission: false,
      requestSoundPermission: false,
    );

    try {
      final ok = await _plugin.initialize(
        settings: const InitializationSettings(
          android: android,
          iOS: darwin,
        ),
        onDidReceiveNotificationResponse: (response) {
          final payload = response.payload?.trim();
          if (payload != null && payload.isNotEmpty) {
            _tapController.add(payload);
          }
        },
        onDidReceiveBackgroundNotificationResponse: notificationTapBackground,
      );
      if (ok == false) {
        throw StateError('notification_plugin_initialize_failed');
      }

      final launch = await _plugin.getNotificationAppLaunchDetails();
      if (launch?.didNotificationLaunchApp == true) {
        _initialPayload = launch?.notificationResponse?.payload;
      }

      final androidPlugin =
          _plugin.resolvePlatformSpecificImplementation<
              AndroidFlutterLocalNotificationsPlugin>();
      await androidPlugin?.createNotificationChannel(
        const AndroidNotificationChannel(
          reminderChannelId,
          reminderChannelName,
          description: reminderChannelDescription,
          importance: Importance.high,
          playSound: true,
          enableVibration: true,
          showBadge: true,
        ),
      );

      _initialized = true;
      _available = true;
      _lastError = null;
    } catch (error) {
      _initialized = false;
      _available = false;
      _lastError = 'notification_initialize:$error';
    }
  }

  Future<bool> requestPermissions() async {
    await initialize(force: !_initialized || !_available);
    if (!_available) return false;

    var granted = true;
    try {
      final android =
          _plugin.resolvePlatformSpecificImplementation<
              AndroidFlutterLocalNotificationsPlugin>();
      final result = await android?.requestNotificationsPermission();
      if (result != null) granted = result;
    } catch (error) {
      _lastError = 'notification_permission_android:$error';
      granted = false;
    }

    try {
      final result = await _plugin
          .resolvePlatformSpecificImplementation<
              IOSFlutterLocalNotificationsPlugin>()
          ?.requestPermissions(
            alert: true,
            badge: true,
            sound: true,
          );
      if (result != null) granted = granted && result;
    } catch (error) {
      _lastError = 'notification_permission_ios:$error';
      granted = false;
    }
    return granted;
  }

  Future<NotificationHealth> health() async {
    await initialize(force: !_initialized || !_available);
    if (!_available) {
      return NotificationHealth(
        available: false,
        notificationsEnabled: false,
        exactAlarmsEnabled: false,
        reminderChannelEnabled: false,
        pendingCount: 0,
        lastError: _lastError,
      );
    }

    var enabled = true;
    var exact = false;
    var reminderChannelEnabled =
        defaultTargetPlatform != TargetPlatform.android;
    var pending = 0;

    try {
      final android =
          _plugin.resolvePlatformSpecificImplementation<
              AndroidFlutterLocalNotificationsPlugin>();
      final appEnabled = await android?.areNotificationsEnabled();
      if (appEnabled != null) enabled = appEnabled;

      final exactEnabled = await android?.canScheduleExactNotifications();
      if (exactEnabled != null) exact = exactEnabled;

      final channels = await android?.getNotificationChannels();
      if (channels != null) {
        for (final channel in channels) {
          if (channel.id == reminderChannelId) {
            reminderChannelEnabled = channel.importance != Importance.none;
          }
        }
      }
    } catch (error) {
      _lastError = 'notification_health_android:$error';
    }

    try {
      pending = (await _plugin.pendingNotificationRequests()).length;
    } catch (error) {
      _lastError = 'notification_pending:$error';
    }

    return NotificationHealth(
      available: true,
      notificationsEnabled: enabled,
      exactAlarmsEnabled: exact,
      reminderChannelEnabled: reminderChannelEnabled,
      pendingCount: pending,
      lastError: _lastError,
    );
  }

  Future<void> openSystemSettings() async {
    await initialize(force: !_initialized || !_available);
    if (!_available) return;
    try {
      await _plugin.openAppNotificationSettings();
    } catch (error) {
      _lastError = 'notification_settings:$error';
    }
  }

  Future<bool> showNow({
    required String stableId,
    required String title,
    required String body,
    String? payload,
  }) async {
    await initialize();
    if (!_available) return false;
    final status = await health();
    if (!status.deliveryReady) {
      _lastError = 'notification_delivery_not_ready';
      return false;
    }
    try {
      await _plugin.show(
        id: _notificationId(stableId),
        title: title,
        body: body,
        notificationDetails: _standardDetails,
        payload: payload ?? stableId,
      );
      _lastError = null;
      return true;
    } catch (error) {
      _lastError = 'notification_show:$stableId:$error';
      return false;
    }
  }

  Future<bool> schedule(PlannedNotification item) async {
    await initialize();
    if (!_available) return false;
    if (!item.when.isAfter(DateTime.now())) return false;

    final status = await health();
    if (!status.deliveryReady) {
      _lastError = 'notification_delivery_not_ready';
      return false;
    }

    try {
      await _plugin.zonedSchedule(
        id: _notificationId(item.stableId),
        title: item.title,
        body: item.body,
        scheduledDate: tz.TZDateTime.from(item.when, tz.local),
        notificationDetails: _standardDetails,
        androidScheduleMode: AndroidScheduleMode.inexactAllowWhileIdle,
        payload: item.payload,
        matchDateTimeComponents:
            item.repeatDaily ? DateTimeComponents.time : null,
      );
      _lastError = null;
      return true;
    } catch (error) {
      _lastError = 'notification_schedule:${item.stableId}:$error';
      return false;
    }
  }

  Future<void> reconcile(Iterable<PlannedNotification> plan) async {
    await initialize();
    if (!_available) return;
    try {
      await _plugin.cancelAll();
    } catch (_) {}
    final status = await health();
    if (!status.deliveryReady) return;
    for (final item in plan) {
      await schedule(item);
    }
  }

  Future<LocalNotificationDiagnostic> runLocalDiagnostic({
    required String immediateTitle,
    required String immediateBody,
    required String scheduledTitle,
    required String scheduledBody,
    Duration scheduledDelay = const Duration(seconds: 12),
  }) async {
    await initialize(force: true);
    final delaySeconds = scheduledDelay.inSeconds.clamp(5, 60).toInt();
    if (!_available) {
      return LocalNotificationDiagnostic(
        permissionGranted: false,
        immediateShown: false,
        scheduledCreated: false,
        scheduledDelaySeconds: delaySeconds,
        health: await health(),
        error: _lastError,
      );
    }

    final permissionGranted = await requestPermissions();
    var immediateShown = false;
    var scheduledCreated = false;
    if (permissionGranted) {
      immediateShown = await showNow(
        stableId: 'diagnostic:immediate',
        title: immediateTitle,
        body: immediateBody,
        payload: 'tab:today',
      );
      scheduledCreated = await schedule(
        PlannedNotification(
          stableId: 'diagnostic:scheduled',
          title: scheduledTitle,
          body: scheduledBody,
          when: DateTime.now().add(Duration(seconds: delaySeconds)),
          payload: 'tab:today',
        ),
      );
    }

    return LocalNotificationDiagnostic(
      permissionGranted: permissionGranted,
      immediateShown: immediateShown,
      scheduledCreated: scheduledCreated,
      scheduledDelaySeconds: delaySeconds,
      health: await health(),
      error: _lastError,
    );
  }

  static const NotificationDetails _standardDetails = NotificationDetails(
    android: AndroidNotificationDetails(
      reminderChannelId,
      reminderChannelName,
      channelDescription: reminderChannelDescription,
      importance: Importance.high,
      priority: Priority.high,
      playSound: true,
      enableVibration: true,
      category: AndroidNotificationCategory.reminder,
    ),
    iOS: DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    ),
  );

  int _notificationId(String value) {
    var hash = 0;
    for (final code in value.codeUnits) {
      hash = 0x1fffffff & (hash * 31 + code);
    }
    return hash;
  }

  void dispose() {
    _tapController.close();
  }
}
