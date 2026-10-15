import '../../domain/observance.dart';

typedef WidgetObservancesForDate = List<Observance> Function(DateTime date);

abstract interface class HomeWidgetGateway {
  bool get supported;

  Stream<Uri> get clickStream;

  Future<Uri?> initialize();

  Future<void> sync({
    required String localeCode,
    required WidgetObservancesForDate observancesForDate,
  });

  Future<bool> isPinSupported();

  Future<bool> requestPin();

  void dispose();
}
