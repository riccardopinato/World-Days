import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:home_widget/home_widget.dart';

import '../../domain/observance.dart';

typedef WidgetObservancesForDate = List<Observance> Function(DateTime date);

class WorldDaysWidgetProjection {
  const WorldDaysWidgetProjection._();

  static Map<String, Map<String, String>> build({
    required String localeCode,
    required WidgetObservancesForDate observancesForDate,
    DateTime? now,
    int days = 45,
  }) {
    final locale = _normalizeLocale(localeCode);
    final copy = _WidgetCopy.forLocale(locale);
    final clock = now ?? DateTime.now();
    final start = DateTime(clock.year, clock.month, clock.day);
    final schedule = <String, Map<String, String>>{};

    for (var offset = 0; offset < days; offset++) {
      final date = start.add(Duration(days: offset));
      final records = observancesForDate(date);
      final first = records.isEmpty ? null : records.first;
      schedule[_dateKey(date)] = {
        'date': '${date.day.toString().padLeft(2, '0')}/'
            '${date.month.toString().padLeft(2, '0')}',
        'title': first?.titleForLocale(locale) ?? copy.noObservance,
        'subtitle': records.isEmpty
            ? copy.openToExplore
            : records.length == 1
                ? copy.oneObservance
                : copy.manyObservances(records.length),
        'id': first?.id ?? '',
      };
    }
    return schedule;
  }

  static String _dateKey(DateTime date) =>
      '${date.year.toString().padLeft(4, '0')}-'
      '${date.month.toString().padLeft(2, '0')}-'
      '${date.day.toString().padLeft(2, '0')}';

  static String _normalizeLocale(String value) {
    final normalized = value.toLowerCase().split(RegExp('[-_]')).first;
    const supported = {'en', 'it', 'es', 'fr', 'de', 'pt'};
    return supported.contains(normalized) ? normalized : 'en';
  }
}

class WorldDaysHomeWidgetService {
  WorldDaysHomeWidgetService._();

  static final WorldDaysHomeWidgetService instance =
      WorldDaysHomeWidgetService._();

  static const qualifiedAndroidName =
      'com.riccardopinato.world_days.WorldDaysWidgetProvider';

  final StreamController<Uri> _clickController =
      StreamController<Uri>.broadcast();
  StreamSubscription<Uri?>? _widgetClickSubscription;

  bool get supported =>
      !kIsWeb && defaultTargetPlatform == TargetPlatform.android;

  Stream<Uri> get clickStream => _clickController.stream;

  Future<Uri?> initialize() async {
    if (!supported) return null;
    _widgetClickSubscription ??= HomeWidget.widgetClicked.listen((uri) {
      if (uri != null) _clickController.add(uri);
    });
    try {
      return await HomeWidget.initiallyLaunchedFromHomeWidget();
    } catch (_) {
      return null;
    }
  }

  Future<void> sync({
    required String localeCode,
    required WidgetObservancesForDate observancesForDate,
  }) async {
    if (!supported) return;
    final schedule = WorldDaysWidgetProjection.build(
      localeCode: localeCode,
      observancesForDate: observancesForDate,
    );
    try {
      await HomeWidget.saveWidgetData<String>(
        'world_days_schedule_json',
        jsonEncode(schedule),
      );
      await HomeWidget.updateWidget(
        qualifiedAndroidName: qualifiedAndroidName,
      );
    } catch (_) {
      // Widget projection must never block the app core.
    }
  }

  Future<bool> isPinSupported() async {
    if (!supported) return false;
    try {
      return await HomeWidget.isRequestPinWidgetSupported() ?? false;
    } catch (_) {
      return false;
    }
  }

  Future<bool> requestPin() async {
    if (!await isPinSupported()) return false;
    try {
      await HomeWidget.requestPinWidget(
        qualifiedAndroidName: qualifiedAndroidName,
      );
      return true;
    } catch (_) {
      return false;
    }
  }

  void dispose() {
    _widgetClickSubscription?.cancel();
    _clickController.close();
  }
}

class _WidgetCopy {
  const _WidgetCopy({
    required this.noObservance,
    required this.openToExplore,
    required this.oneObservance,
    required this.manyObservancesPrefix,
  });

  final String noObservance;
  final String openToExplore;
  final String oneObservance;
  final String manyObservancesPrefix;

  String manyObservances(int count) => '$count $manyObservancesPrefix';

  static _WidgetCopy forLocale(String locale) => switch (locale) {
        'it' => const _WidgetCopy(
            noObservance: 'Nessuna ricorrenza verificata',
            openToExplore: 'Apri World Days per esplorare',
            oneObservance: '1 ricorrenza oggi',
            manyObservancesPrefix: 'ricorrenze oggi',
          ),
        'es' => const _WidgetCopy(
            noObservance: 'Ninguna conmemoración verificada',
            openToExplore: 'Abre World Days para explorar',
            oneObservance: '1 conmemoración hoy',
            manyObservancesPrefix: 'conmemoraciones hoy',
          ),
        'fr' => const _WidgetCopy(
            noObservance: 'Aucune journée vérifiée',
            openToExplore: 'Ouvrez World Days pour explorer',
            oneObservance: '1 journée aujourd’hui',
            manyObservancesPrefix: 'journées aujourd’hui',
          ),
        'de' => const _WidgetCopy(
            noObservance: 'Kein verifizierter Aktionstag',
            openToExplore: 'World Days öffnen und entdecken',
            oneObservance: '1 Tag heute',
            manyObservancesPrefix: 'Tage heute',
          ),
        'pt' => const _WidgetCopy(
            noObservance: 'Nenhuma data verificada',
            openToExplore: 'Abra o World Days para explorar',
            oneObservance: '1 data hoje',
            manyObservancesPrefix: 'datas hoje',
          ),
        _ => const _WidgetCopy(
            noObservance: 'No verified observance',
            openToExplore: 'Open World Days to explore',
            oneObservance: '1 observance today',
            manyObservancesPrefix: 'observances today',
          ),
      };
}
