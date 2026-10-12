import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:home_widget/home_widget.dart';

import '../../domain/observance.dart';

final class HomeWidgetDay {
  const HomeWidgetDay({
    required this.date,
    required this.observances,
  });

  final DateTime date;
  final List<Observance> observances;
}

final class HomeWidgetService {
  const HomeWidgetService();

  Future<void> sync(List<HomeWidgetDay> days) async {
    if (kIsWeb) return;
    try {
      final schedule = <String, Object?>{};
      for (final day in days) {
        final key = _dateKey(day.date);
        final primary =
            day.observances.isEmpty ? null : day.observances.first;
        schedule[key] = {
          'title': primary?.title ?? 'No verified observance',
          'authority': primary?.authority.name ?? 'World Days',
          'count': day.observances.length,
        };
      }

      await HomeWidget.saveWidgetData<String>(
        'schedule_json',
        jsonEncode(schedule),
      );
      await HomeWidget.updateWidget(
        androidName: 'WorldDaysWidgetProvider',
      );
    } catch (_) {
      // Widgets are optional and must never block the app.
    }
  }

  static String _dateKey(DateTime date) =>
      '${date.year.toString().padLeft(4, '0')}-'
      '${date.month.toString().padLeft(2, '0')}-'
      '${date.day.toString().padLeft(2, '0')}';
}
