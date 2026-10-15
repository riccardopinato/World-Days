import '../../data/preferences_repository.dart';
import '../../domain/observance.dart';

typedef ObservancesForDate = List<Observance> Function(DateTime date);

class PlannedNotification {
  const PlannedNotification({
    required this.stableId,
    required this.title,
    required this.body,
    required this.when,
    required this.payload,
  });

  final String stableId;
  final String title;
  final String body;
  final DateTime when;
  final String payload;
}

class ReminderPlanBuilder {
  const ReminderPlanBuilder._();

  static List<PlannedNotification> build({
    required ReminderPreferences settings,
    required Set<String> favoriteIds,
    required String localeCode,
    required ObservancesForDate observancesForDate,
    DateTime? now,
  }) {
    final clock = now ?? DateTime.now();
    final start = DateTime(clock.year, clock.month, clock.day);
    final locale = _normalizeLocale(localeCode);
    final copy = _ReminderCopy.forLocale(locale);
    final plan = <PlannedNotification>[];

    if (settings.dailyEnabled) {
      for (var offset = 0; offset < 21; offset++) {
        final date = start.add(Duration(days: offset));
        final when = _at(
          date,
          settings.dailyHour,
          settings.dailyMinute,
        );
        if (!when.isAfter(clock)) continue;
        final records = observancesForDate(date);
        final first = records.isEmpty ? null : records.first;
        plan.add(
          PlannedNotification(
            stableId: 'daily:${_dateKey(date)}',
            title: first?.titleForLocale(locale) ?? copy.dailyGenericTitle,
            body: copy.dailyBody,
            when: when,
            payload: first == null
                ? 'tab:today'
                : 'observance:${first.id}',
          ),
        );
      }
    }

    if (settings.weeklyEnabled) {
      var date = start;
      while (date.weekday != settings.weeklyWeekday) {
        date = date.add(const Duration(days: 1));
      }
      for (var index = 0; index < 6; index++) {
        final candidate = date.add(Duration(days: index * 7));
        final when = _at(
          candidate,
          settings.weeklyHour,
          settings.weeklyMinute,
        );
        if (!when.isAfter(clock)) continue;
        plan.add(
          PlannedNotification(
            stableId: 'weekly:${_dateKey(candidate)}',
            title: copy.weeklyTitle,
            body: copy.weeklyBody,
            when: when,
            payload: 'tab:calendar',
          ),
        );
      }
    }

    if (settings.favoriteEnabled && favoriteIds.isNotEmpty) {
      final scheduledFavorites = <String>{};
      for (var offset = 0;
          offset <= 366 && scheduledFavorites.length < 12;
          offset++) {
        final date = start.add(Duration(days: offset));
        final records = observancesForDate(date);
        for (final record in records) {
          if (!favoriteIds.contains(record.id) ||
              scheduledFavorites.contains(record.id)) {
            continue;
          }
          final when = _at(
            date,
            settings.dailyHour,
            settings.dailyMinute,
          ).add(const Duration(minutes: 5));
          if (!when.isAfter(clock)) continue;
          scheduledFavorites.add(record.id);
          plan.add(
            PlannedNotification(
              stableId: 'favorite:${record.id}:${_dateKey(date)}',
              title: record.titleForLocale(locale),
              body: copy.favoriteBody,
              when: when,
              payload: 'observance:${record.id}',
            ),
          );
          if (scheduledFavorites.length >= 12) break;
        }
      }
    }

    if (settings.categoryEnabled &&
        settings.followedCategories.isNotEmpty) {
      var scheduled = 0;
      for (var offset = 0; offset <= 90 && scheduled < 10; offset++) {
        final date = start.add(Duration(days: offset));
        final records = observancesForDate(date);
        Observance? match;
        String? matchedCategory;
        for (final record in records) {
          for (final category in record.categories) {
            if (settings.followedCategories.contains(category.toUpperCase())) {
              match = record;
              matchedCategory = category.toUpperCase();
              break;
            }
          }
          if (match != null) break;
        }
        if (match == null || matchedCategory == null) continue;
        final when = _at(
          date,
          settings.dailyHour,
          settings.dailyMinute,
        ).add(const Duration(minutes: 10));
        if (!when.isAfter(clock)) continue;
        plan.add(
          PlannedNotification(
            stableId: 'category:${_dateKey(date)}:$matchedCategory',
            title: match.titleForLocale(locale),
            body: copy.categoryBody,
            when: when,
            payload: 'observance:${match.id}',
          ),
        );
        scheduled++;
      }
    }

    plan.sort((a, b) => a.when.compareTo(b.when));
    return plan;
  }

  static DateTime _at(DateTime date, int hour, int minute) =>
      DateTime(date.year, date.month, date.day, hour, minute);

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

class _ReminderCopy {
  const _ReminderCopy({
    required this.dailyGenericTitle,
    required this.dailyBody,
    required this.weeklyTitle,
    required this.weeklyBody,
    required this.favoriteBody,
    required this.categoryBody,
  });

  final String dailyGenericTitle;
  final String dailyBody;
  final String weeklyTitle;
  final String weeklyBody;
  final String favoriteBody;
  final String categoryBody;

  static _ReminderCopy forLocale(String locale) => switch (locale) {
        'it' => const _ReminderCopy(
            dailyGenericTitle: 'World Days di oggi',
            dailyBody: 'Apri World Days e scopri cosa si celebra oggi.',
            weeklyTitle: 'La tua settimana World Days',
            weeklyBody: 'Scopri le ricorrenze dei prossimi sette giorni.',
            favoriteBody: 'Oggi ricorre una giornata che hai salvato.',
            categoryBody: 'Oggi c’è una ricorrenza in una categoria che segui.',
          ),
        'es' => const _ReminderCopy(
            dailyGenericTitle: 'World Days de hoy',
            dailyBody: 'Abre World Days y descubre qué se celebra hoy.',
            weeklyTitle: 'Tu semana en World Days',
            weeklyBody: 'Descubre las conmemoraciones de los próximos siete días.',
            favoriteBody: 'Hoy se celebra un día que guardaste.',
            categoryBody: 'Hoy hay una conmemoración en una categoría que sigues.',
          ),
        'fr' => const _ReminderCopy(
            dailyGenericTitle: 'World Days aujourd’hui',
            dailyBody: 'Ouvrez World Days et découvrez ce qui est célébré aujourd’hui.',
            weeklyTitle: 'Votre semaine World Days',
            weeklyBody: 'Découvrez les journées des sept prochains jours.',
            favoriteBody: 'Une journée que vous avez enregistrée a lieu aujourd’hui.',
            categoryBody: 'Une catégorie que vous suivez a une journée à découvrir aujourd’hui.',
          ),
        'de' => const _ReminderCopy(
            dailyGenericTitle: 'World Days heute',
            dailyBody: 'Öffne World Days und entdecke, was heute begangen wird.',
            weeklyTitle: 'Deine World-Days-Woche',
            weeklyBody: 'Entdecke die Gedenk- und Aktionstage der nächsten sieben Tage.',
            favoriteBody: 'Heute findet ein von dir gespeicherter Tag statt.',
            categoryBody: 'Heute gibt es einen Tag in einer Kategorie, der du folgst.',
          ),
        'pt' => const _ReminderCopy(
            dailyGenericTitle: 'World Days de hoje',
            dailyBody: 'Abra o World Days e descubra o que se celebra hoje.',
            weeklyTitle: 'A sua semana World Days',
            weeklyBody: 'Descubra as datas dos próximos sete dias.',
            favoriteBody: 'Hoje celebra-se um dia que guardou.',
            categoryBody: 'Hoje há uma data numa categoria que segue.',
          ),
        _ => const _ReminderCopy(
            dailyGenericTitle: 'World Days today',
            dailyBody: 'Open World Days to discover what is observed today.',
            weeklyTitle: 'Your World Days week',
            weeklyBody: 'See the observances coming in the next seven days.',
            favoriteBody: 'A day you saved is observed today.',
            categoryBody: 'A category you follow has something to discover today.',
          ),
      };
}
