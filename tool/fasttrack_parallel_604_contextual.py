#!/usr/bin/env python3
"""World Days bulk contextual editorial in seven disjoint 100-ID lanes.

Fast Track consumer layer. Facts originate ONLY from already admitted canonical
catalog metadata (including verified-at fields and source pointers). This is not
a claim that 604 separate founding histories have been individually researched.
All six descriptions are real localized text, never English fallback.
"""
import concurrent.futures as cf
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/"assets"/"data"
OUT=ROOT/"reports"/"fasttrack_parallel_604"
LANG=("en","it","es","fr","de","pt")
BASE_COUNT=507
REMAINING=604
BATCH_SIZE=100
TIER="AI_CONTEXTUAL_SIX_LOCALE"
THEMES={
 "planet":("ecology and care for natural systems","ambiente e tutela dei sistemi naturali","medio ambiente y protección de los sistemas naturales","environnement et protection des milieux naturels","Umwelt und Schutz natürlicher Lebensräume","ambiente e proteção dos sistemas naturais"),
 "health":("health, prevention and community wellbeing","salute, prevenzione e benessere collettivo","salud, prevención y bienestar colectivo","santé, prévention et bien-être collectif","Gesundheit, Vorsorge und gesellschaftliches Wohlergehen","saúde, prevenção e bem-estar coletivo"),
 "people":("human rights, collective memory and civic participation","diritti, memoria collettiva e partecipazione civica","derechos, memoria colectiva y participación cívica","droits, mémoire collective et participation civique","Rechte, gemeinsames Erinnern und gesellschaftliche Teilhabe","direitos, memória coletiva e participação cívica"),
 "learning":("education, knowledge and access to learning","istruzione, conoscenza e accesso all'apprendimento","educación, conocimiento y acceso al aprendizaje","éducation, savoir et accès à l'apprentissage","Bildung, Wissen und Zugang zum Lernen","educação, conhecimento e acesso à aprendizagem"),
 "culture":("culture, identity and shared traditions","cultura, identità e tradizioni condivise","cultura, identidad y tradiciones compartidas","culture, identité et traditions partagées","Kultur, Identität und gemeinsame Traditionen","cultura, identidade e tradições partilhadas"),
 "food":("food, farming and everyday consumption choices","cibo, agricoltura e scelte di consumo quotidiane","alimentación, agricultura y hábitos de consumo","alimentation, agriculture et habitudes de consommation","Ernährung, Landwirtschaft und alltägliche Konsumentscheidungen","alimentação, agricultura e hábitos de consumo"),
 "future":("science, technology and change in society","scienza, tecnologia e cambiamento sociale","ciencia, tecnología y cambio social","science, technologie et changement de société","Wissenschaft, Technologie und gesellschaftlicher Wandel","ciência, tecnologia e mudança social"),
 "community":("community life, civic initiatives and shared attention","vita comunitaria, iniziative civiche e attenzione condivisa","vida comunitaria, iniciativas cívicas y atención compartida","vie collective, initiatives civiques et intérêt partagé","Gemeinschaftsleben, Bürgerinitiativen und gemeinsame Aufmerksamkeit","vida comunitária, iniciativas cívicas e atenção partilhada"),
}
UNKNOWN=("not established (*)","non accertato (*)","no acreditado (*)","non établi (*)","nicht belegt (*)","não confirmado (*)")
DATE_UNKNOWN=("not determined for 2026","non determinata per il 2026","no determinada para 2026","non déterminée pour 2026","für 2026 nicht bestimmt","não determinada para 2026")
FIELDS={
 "en":{
  "hook":"Discover why {title} belongs on the calendar",
  "summary":"{title} invites a closer look at {theme}. Its place in the calendar gives this subject a moment of visibility, without implying that every community marks it in the same way.",
  "origin":"The catalog documents {title} alongside {authority} as its reference institution. That attribution identifies the source behind the listing; it does not establish the individual who first proposed the observance. The recorded introduction year is {year}. The listed occurrence in 2026 is {date}. An exact first edition or the original reason for the chosen date is not asserted where evidence is missing.",
  "why":"A commemorative date can start conversations about {theme} and encourage readers to explore the people, places and decisions connected with the topic.",
  "whyDate":"Calendar date for 2026: {date}. An original historical rationale for the date is not independently established here.",
  "facts":("2026 calendar occurrence: {date}.","Institution named by the catalog: {authority}.","Documented introduction year: {year}."),
  "actions":("Explore the accompanying source and its historical context.","Look for a community initiative connected with the subject."),
 },
 "it":{
  "hook":"Perché {title} è presente nel calendario",
  "summary":"{title} è un'occasione per conoscere meglio {theme}. La sua presenza nel calendario dà visibilità al tema, senza implicare che tutte le comunità lo celebrino nello stesso modo.",
  "origin":"Il catalogo associa {title} a {authority} come ente di riferimento. L'attribuzione indica la fonte della scheda, non dimostra chi abbia proposto per primo la ricorrenza. L'anno di introduzione documentato è {year}. La data prevista nel 2026 è {date}. Quando mancano prove specifiche, non vengono inventati né la prima celebrazione né il motivo originario della scelta della data.",
  "why":"Una ricorrenza può far nascere conversazioni su {theme} e stimolare la scoperta di persone, luoghi e decisioni collegati all'argomento.",
  "whyDate":"Data di calendario per il 2026: {date}. Il motivo storico originale della data non è qui accertato in modo indipendente.",
  "facts":("Ricorrenza prevista nel 2026: {date}.","Ente indicato dal catalogo: {authority}.","Anno di introduzione documentato: {year}."),
  "actions":("Approfondisci la fonte associata e il suo contesto storico.","Cerca un'iniziativa locale collegata al tema."),
 },
 "es":{
  "hook":"Por qué {title} figura en el calendario",
  "summary":"{title} invita a conocer mejor {theme}. Su presencia en el calendario da visibilidad al tema, sin suponer que todas las comunidades lo celebren del mismo modo.",
  "origin":"El catálogo vincula {title} con {authority} como institución de referencia. Esa atribución señala la fuente de la ficha, pero no demuestra quién propuso primero la conmemoración. El año de introducción documentado es {year}. La fecha indicada para 2026 es {date}. Cuando faltan pruebas concretas, no se inventa ni la primera celebración ni la razón original de la fecha.",
  "why":"Una conmemoración puede abrir conversaciones sobre {theme} y animar a descubrir personas, lugares y decisiones relacionados con el tema.",
  "whyDate":"Fecha del calendario para 2026: {date}. Aquí no se acredita de forma independiente el motivo histórico original de la fecha.",
  "facts":("Celebración prevista en 2026: {date}.","Institución identificada por el catálogo: {authority}.","Año de introducción documentado: {year}."),
  "actions":("Consulta la fuente vinculada y su contexto histórico.","Busca una iniciativa comunitaria relacionada con el tema."),
 },
 "fr":{
  "hook":"Pourquoi {title} figure au calendrier",
  "summary":"{title} permet de découvrir {theme}. Sa présence au calendrier attire l'attention sur ce sujet, sans supposer que toutes les communautés le célèbrent de la même façon.",
  "origin":"Le catalogue associe {title} à {authority} en tant qu'institution de référence. Cette attribution précise la source de la fiche, sans établir qui proposa la commémoration en premier. L'année d'introduction documentée est {year}. La date indiquée pour 2026 est {date}. En l'absence de preuve précise, la première célébration et le choix initial de la date ne sont pas inventés.",
  "why":"Une journée commémorative peut nourrir des échanges sur {theme} et faire découvrir les personnes, les lieux et les décisions liés à ce sujet.",
  "whyDate":"Date inscrite au calendrier pour 2026 : {date}. La raison historique initiale de cette date n'est pas établie ici de manière indépendante.",
  "facts":("Occurrence au calendrier en 2026 : {date}.","Institution indiquée par le catalogue : {authority}.","Année d'introduction documentée : {year}."),
  "actions":("Consultez la source citée et son contexte historique.","Recherchez une initiative locale liée au sujet."),
 },
 "de":{
  "hook":"Warum {title} im Kalender steht",
  "summary":"{title} lädt dazu ein, sich mit {theme} zu beschäftigen. Der Kalendereintrag macht das Thema sichtbar, ohne zu behaupten, dass alle Gemeinschaften den Anlass gleich begehen.",
  "origin":"Der Katalog führt {title} mit {authority} als Bezugsinstitution auf. Diese Zuordnung bezeichnet die Quelle des Eintrags, belegt jedoch nicht, wer den Gedenktag ursprünglich angeregt hat. Das dokumentierte Einführungsjahr ist {year}. Für 2026 nennt der Katalog {date}. Falls Nachweise fehlen, werden weder die erste Feier noch die ursprüngliche Wahl des Datums als gesicherte Geschichte ausgegeben.",
  "why":"Ein Gedenktag kann Gespräche über {theme} fördern und dazu anregen, Menschen, Orte und Entscheidungen hinter dem Thema kennenzulernen.",
  "whyDate":"Kalendertermin für 2026: {date}. Ein ursprünglicher historischer Grund für das Datum ist hier nicht unabhängig belegt.",
  "facts":("Kalendertermin 2026: {date}.","Im Katalog genannte Institution: {authority}.","Dokumentiertes Einführungsjahr: {year}."),
  "actions":("Lesen Sie die verknüpfte Quelle und ihren historischen Kontext.","Suchen Sie eine lokale Initiative zum Thema."),
 },
 "pt":{
  "hook":"Porque {title} faz parte do calendário",
  "summary":"{title} convida a conhecer melhor {theme}. A sua presença no calendário dá visibilidade ao tema, sem pressupor que todas as comunidades o celebrem da mesma forma.",
  "origin":"O catálogo associa {title} a {authority} como instituição de referência. Esta atribuição identifica a fonte da ficha, mas não prova quem propôs inicialmente a data. O ano de introdução documentado é {year}. A ocorrência indicada para 2026 é {date}. Quando faltam provas específicas, não se inventam a primeira celebração nem a razão original da escolha da data.",
  "why":"Uma data comemorativa pode promover conversas sobre {theme} e incentivar a descoberta de pessoas, lugares e decisões ligados ao assunto.",
  "whyDate":"Data do calendário para 2026: {date}. A justificação histórica original da data não está aqui comprovada de forma independente.",
  "facts":("Ocorrência no calendário em 2026: {date}.","Instituição indicada pelo catálogo: {authority}.","Ano de introdução documentado: {year}."),
  "actions":("Consulte a fonte associada e o seu contexto histórico.","Procure uma iniciativa comunitária ligada ao tema."),
 }
}

def load(path):return json.loads(path.read_text(encoding="utf-8"))

def display_dates(id_, occs, loc):
    dates=[(o["startDate"],o["endDate"]) for o in occs if o["observanceId"]==id_]
    dates=sorted(set(dates))
    if not dates:return DATE_UNKNOWN[LANG.index(loc)]
    def fmt(d):
        y,m,day=d.split("-")
        return f"{int(day):02d}/{int(m):02d}/{y}"
    return ", ".join(fmt(s) if s==e else fmt(s)+"–"+fmt(e) for s,e in dates)

def make_article(item,locale,occ):
    title=item["localizedTitles"][locale].strip()
    authority=item["authority"]["name"]
    theme=THEMES.get(item.get("visualKey","community"),THEMES["community"])[LANG.index(locale)]
    year=item.get("introducedYear")
    yeartext=str(year) if isinstance(year,int) else UNKNOWN[LANG.index(locale)]
    date=display_dates(item["id"],occ,locale)
    t=FIELDS[locale]
    substitutions=dict(title=title,authority=authority,theme=theme,year=yeartext,date=date)
    facts=[x.format(**substitutions) for x in t["facts"]]
    assert all(len(x)>=20 for x in facts)
    return {
      "observanceId":item["id"],"locale":locale,
      "translationOf":"en" if locale!="en" else None,
      "status":TIER,
      "hook":t["hook"].format(**substitutions),
      "summary":t["summary"].format(**substitutions),
      "origin":t["origin"].format(**substitutions),
      "whyThisDate":t["whyDate"].format(**substitutions),
      "whyItMatters":t["why"].format(**substitutions),
      "quickFacts":facts,
      "waysToTakePart":list(t["actions"]),
      "relatedObservanceIds":[],
      "lastReviewedAt":"2026-11-19",
      "sourcePolicy":"AI-assisted, catalog-metadata-grounded contextual overview; specific founding history not individually researched; see canonical source URLs and provenance."
    }

def main():
    catalog=load(ASSETS/"official_core.json")
    docs={loc:load(ASSETS/f"editorial_{loc}.json") for loc in LANG}
    original=[row["observanceId"] for row in docs["en"]["entries"]]
    assert len(catalog["records"])==1111 and len(set(original))==BASE_COUNT
    assert all(doc["entryCount"]==BASE_COUNT and [r["observanceId"] for r in doc["entries"]]==original for doc in docs.values())
    records={r["id"]:r for r in catalog["records"]}
    assert len(records)==1111
    pending=sorted(set(records)-set(original))
    assert len(pending)==REMAINING and len(set(pending))==REMAINING
    occ=load(ASSETS/"occurrences_2026.json")["occurrences"]
    cohorts=[pending[i:i+BATCH_SIZE] for i in range(0,len(pending),BATCH_SIZE)]
    assert len(cohorts)==7 and [len(c) for c in cohorts]==[100]*6+[4]
    OUT.mkdir(parents=True,exist_ok=True)
    def worker(pair):
        idx,ids=pair
        per_locale={loc:[] for loc in LANG}
        for id_ in ids:
            item=records[id_]
            assert item["sources"] and set(item["localizedTitles"])==set(LANG)
            for locale in LANG:
                per_locale[locale].append(make_article(item,locale,occ))
        report={"cohort":idx+1,"count":len(ids),"ids":ids,
                "status":"AI_CONTEXTUAL_METADATA_ONLY_NOT_ORIGIN_RESEARCH",
                "source":"Canonical World Days 1111 metadata; no fabricated founder/first edition"}
        (OUT/f"cohort_{idx+1:02d}.json").write_text(
            json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        return idx,ids,per_locale
    with cf.ThreadPoolExecutor(max_workers=7) as pool:
        results=list(pool.map(worker,enumerate(cohorts)))
    results.sort(key=lambda x:x[0])
    all_ids=[id_ for _,ids,_ in results for id_ in ids]
    assert all_ids==pending and len(set(all_ids))==REMAINING
    for locale in LANG:
        additions=[row for _,_,batch in results for row in batch[locale]]
        assert len(additions)==REMAINING
        doc=docs[locale]
        doc["entries"].extend(additions)
        doc["entryCount"]=len(doc["entries"])
        assert doc["entryCount"]==1111
        assert len({x["observanceId"] for x in doc["entries"]})==1111
        (ASSETS/f"editorial_{locale}.json").write_text(
            json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report={"catalog":1111,"sixLocaleEditorialArticles":1111,"originSpecificArticlesBefore":507,
            "newContextualArticles":604,"contextualNotOriginResearched":604,
            "onlyITEN":0,"missingAnyEditorialLocale":0,"cohortSizes":[len(c) for c in cohorts],
            "scope":"CONTEXTUAL_SIX_LOCALE_NOT_604_VERIFIED_HISTORICAL_FOUNDING_DOSSIERS"}
    (OUT/"manifest.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("FASTTRACK_604_PARALLEL_CONTEXT_COMPLETE",json.dumps(report,sort_keys=True))

if __name__=="__main__":main()
