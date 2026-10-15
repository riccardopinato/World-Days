import 'observance.dart';

final class VerifiedMetadataSummary {
  const VerifiedMetadataSummary({
    required this.observanceId,
    required this.locale,
    required this.summary,
    required this.note,
    required this.authorityName,
    required this.sourceVerifiedAt,
  });

  static const status = 'VERIFIED_METADATA';

  final String observanceId;
  final String locale;
  final String summary;
  final String note;
  final String authorityName;
  final String sourceVerifiedAt;

  factory VerifiedMetadataSummary.forObservance(
    Observance observance,
    String? localeCode,
  ) {
    final requested = (localeCode ?? 'en')
        .toLowerCase()
        .split(RegExp('[-_]'))
        .first;
    final locale = const {'en', 'it', 'es', 'fr', 'de', 'pt'}.contains(requested)
        ? requested
        : 'en';
    final title = observance.titleForLocale(locale);
    final authority = observance.authority.name;
    final scope = _scopeLabel(locale, observance.scope);
    final sourceVerifiedAt = observance.lastVerifiedAt ??
        observance.sources
            .map((source) => source.verifiedAt ?? '')
            .firstWhere((value) => value.isNotEmpty, orElse: () => '');

    final copy = _copy(
      locale: locale,
      title: title,
      authority: authority,
      scope: scope,
    );

    return VerifiedMetadataSummary(
      observanceId: observance.id,
      locale: locale,
      summary: copy.$1,
      note: copy.$2,
      authorityName: authority,
      sourceVerifiedAt: sourceVerifiedAt,
    );
  }

  static (String, String) _copy({
    required String locale,
    required String title,
    required String authority,
    required String scope,
  }) =>
      switch (locale) {
        'it' => (
            '$title è una ricorrenza verificata di ambito $scope nel catalogo World Days. Il record canonico la attribuisce a $authority e mantiene data e provenienza collegate alle fonti verificate del catalogo.',
            'Questa sintesi usa solo metadati verificati del record. Il contesto editoriale più ricco viene mostrato soltanto quando è stato revisionato sulle fonti.',
          ),
        'es' => (
            '$title es una celebración verificada de ámbito $scope en el catálogo de World Days. El registro canónico la atribuye a $authority y mantiene la fecha y la procedencia vinculadas a las fuentes verificadas del catálogo.',
            'Este resumen utiliza únicamente metadatos verificados del registro. El contexto editorial más amplio solo se muestra cuando ha sido revisado con las fuentes.',
          ),
        'fr' => (
            '$title est une célébration vérifiée de portée $scope dans le catalogue World Days. La fiche canonique l’attribue à $authority et conserve la date et la provenance liées aux sources vérifiées du catalogue.',
            'Ce résumé utilise uniquement les métadonnées vérifiées de la fiche. Un contexte éditorial plus riche n’est affiché qu’après révision à partir des sources.',
          ),
        'de' => (
            '$title ist ein verifizierter Gedenk- oder Aktionstag mit $scope Reichweite im World-Days-Katalog. Der kanonische Datensatz ordnet ihn $authority zu und hält Datum und Herkunft an die verifizierten Katalogquellen gebunden.',
            'Diese Kurzbeschreibung verwendet nur verifizierte Metadaten des Datensatzes. Ausführlicher redaktioneller Kontext wird erst nach Quellenprüfung angezeigt.',
          ),
        'pt' => (
            '$title é uma data verificada de âmbito $scope no catálogo World Days. O registo canónico atribui-a a $authority e mantém a data e a proveniência ligadas às fontes verificadas do catálogo.',
            'Este resumo utiliza apenas metadados verificados do registo. O contexto editorial mais completo só é apresentado depois de revisto com base nas fontes.',
          ),
        _ => (
            '$title is a verified $scope observance in the World Days catalog. The canonical record attributes it to $authority and keeps its date and provenance tied to the catalog’s verified sources.',
            'This concise overview uses only verified record metadata. Richer editorial context is shown only after source review.',
          ),
      };

  static String _scopeLabel(String locale, String scope) {
    final normalized = scope.toUpperCase();
    return switch (locale) {
      'it' => switch (normalized) {
          'NATIONAL' => 'nazionale',
          'REGIONAL' => 'regionale',
          _ => 'globale',
        },
      'es' => switch (normalized) {
          'NATIONAL' => 'nacional',
          'REGIONAL' => 'regional',
          _ => 'global',
        },
      'fr' => switch (normalized) {
          'NATIONAL' => 'nationale',
          'REGIONAL' => 'régionale',
          _ => 'mondiale',
        },
      'de' => switch (normalized) {
          'NATIONAL' => 'nationaler',
          'REGIONAL' => 'regionaler',
          _ => 'globaler',
        },
      'pt' => switch (normalized) {
          'NATIONAL' => 'nacional',
          'REGIONAL' => 'regional',
          _ => 'global',
        },
      _ => switch (normalized) {
          'NATIONAL' => 'national',
          'REGIONAL' => 'regional',
          _ => 'global',
        },
    };
  }
}
