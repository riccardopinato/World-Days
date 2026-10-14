enum RetentionTab { today, calendar }

class RetentionTarget {
  const RetentionTarget._({this.tab, this.observanceId});

  const RetentionTarget.today() : this._(tab: RetentionTab.today);

  const RetentionTarget.calendar() : this._(tab: RetentionTab.calendar);

  const RetentionTarget.observance(String id)
      : this._(observanceId: id);

  final RetentionTab? tab;
  final String? observanceId;

  static RetentionTarget? fromPayload(String? payload) {
    final value = payload?.trim();
    if (value == null || value.isEmpty) return null;

    if (value == 'tab:today') return const RetentionTarget.today();
    if (value == 'tab:calendar') return const RetentionTarget.calendar();
    if (value.startsWith('observance:')) {
      final id = value.substring('observance:'.length).trim();
      if (id.isNotEmpty) return RetentionTarget.observance(id);
    }
    return null;
  }

  static RetentionTarget? fromWidgetUri(Uri? uri) {
    if (uri == null || uri.scheme != 'worlddays') return null;
    if (uri.host == 'today') return const RetentionTarget.today();
    if (uri.host == 'calendar') return const RetentionTarget.calendar();
    if (uri.host == 'observance' && uri.pathSegments.isNotEmpty) {
      final id = uri.pathSegments.first.trim();
      if (id.isNotEmpty) return RetentionTarget.observance(id);
    }
    return null;
  }
}
