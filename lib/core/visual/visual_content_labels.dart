import 'package:flutter/widgets.dart';

final class VisualContentLabels {
  const VisualContentLabels._(this.locale);
  final String locale;

  factory VisualContentLabels.of(BuildContext context) =>
      VisualContentLabels._(Localizations.localeOf(context).languageCode);

  String get themedCollections => _pick('Themed collections','Collezioni tematiche','Colecciones temáticas','Collections thématiques','Thematische Sammlungen','Coleções temáticas');
  String get shareCard => _pick('Share card','Scheda da condividere','Tarjeta para compartir','Carte à partager','Share-Karte','Cartão para partilhar');
  String get shareCardDescription => _pick('Create a lightweight World Days card for this observance.','Crea una scheda leggera di World Days per questa ricorrenza.','Crea una tarjeta ligera de World Days para esta conmemoración.','Créez une carte World Days légère pour cette journée.','Erstelle eine leichte World-Days-Karte zu diesem Gedenktag.','Crie um cartão leve do World Days para esta observância.');
  String get shareThisDay => _pick('Share this day','Condividi questa giornata','Compartir este día','Partager cette journée','Diesen Tag teilen','Partilhar este dia');
  String get shareFailed => _pick('The share card could not be created.','Impossibile creare la scheda da condividere.','No se pudo crear la tarjeta para compartir.','Impossible de créer la carte à partager.','Die Share-Karte konnte nicht erstellt werden.','Não foi possível criar o cartão para partilhar.');

  String collection(String key) {
    final labels=<String,List<String>>{
      'planet':['Planet & nature','Pianeta e natura','Planeta y naturaleza','Planète et nature','Planet und Natur','Planeta e natureza'],
      'health':['Health & wellbeing','Salute e benessere','Salud y bienestar','Santé et bien-être','Gesundheit und Wohlbefinden','Saúde e bem-estar'],
      'people':['People & rights','Persone e diritti','Personas y derechos','Personnes et droits','Menschen und Rechte','Pessoas e direitos'],
      'learning':['Learning & science','Conoscenza e scienza','Aprendizaje y ciencia','Savoirs et sciences','Lernen und Wissenschaft','Aprendizagem e ciência'],
      'culture':['Culture & creativity','Cultura e creatività','Cultura y creatividad','Culture et créativité','Kultur und Kreativität','Cultura e criatividade'],
      'food':['Food & community','Cibo e comunità','Alimentación y comunidad','Alimentation et communauté','Ernährung und Gemeinschaft','Alimentação e comunidade'],
    };
    final values=labels[key];
    return values==null ? key : values[_index];
  }

  int get _index => switch(locale){'it'=>1,'es'=>2,'fr'=>3,'de'=>4,'pt'=>5,_=>0};
  String _pick(String en,String it,String es,String fr,String de,String pt)=>[en,it,es,fr,de,pt][_index];
}
