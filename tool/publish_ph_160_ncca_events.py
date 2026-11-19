#!/usr/bin/env python3
"""Mass publisher: 160 PH NCCA-indexed individual historical/event explainers.

Source boundary: NCCA calendar certifies identities, event date and category,
NOT necessarily a formal yearly public holiday, founding statute or biography.
144 birth/death anniversaries get a person-specific narrative, 16 civic/cultural
items an observance-specific narrative. Never fabricate life years, professions,
award dates, legislation or a first annual celebration.

Run after 507+604+12 generation. Seven six-language workers read independent
ID subsets; a single ordered writer replaces 160 contextual runtime entries.
"""
import concurrent.futures
import json
import re
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"assets/data"
SOURCE=ROOT/"data/market"
LOCALES=("en","it","es","fr","de","pt")
SRC_FILES=("wave11_staged_144_ph_20261111.json",
           "wave10_hundred_kr_ph_20261111.json",
           "wave13_ncca_eures_100_20261111.json")
SOURCE_URL="https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/"
STATUS="AI_NCCA_EVENT_ANCHORED_SIX_LOCALE"
OLD="AI_CONTEXTUAL_SIX_LOCALE"
GROUPS={"artist":("National Artist","Artista nazionale","Artista Nacional",
                  "Artiste national","Nationalkünstler","Artista Nacional"),
        "treasure":("National Living Treasure","Maestro del patrimonio vivente",
                    "Tesoro Nacional Vivo","Trésor national vivant",
                    "Nationaler lebender Kulturschatz","Tesouro Nacional Vivo"),
        "president":("Philippine president","presidente filippino",
                     "presidente filipino","président philippin",
                     "philippinischer Präsident","presidente filipino"),
        "senate":("Philippine Senate president","presidente del Senato filippino",
                  "presidente del Senado filipino","président du Sénat philippin",
                  "Präsident des philippinischen Senats","presidente do Senado filipino")}
NAMES=[
 ("Birth of National Artist ", "birth","artist"),
 ("Death of National Artist ", "death","artist"),
 ("Birth of National Living Treasure ", "birth","treasure"),
 ("Death of National Living Treasure ", "death","treasure"),
 ("Birth of President ", "birth","president"),
 ("Death of President ", "death","president"),
 ("Birth of Senate President ", "birth","senate"),
]
T={
 "en":{
 "date":"The NCCA calendar marks {day} {month} as the {kind} anniversary of {name}.",
 "role":"The entry identifies this person as a {role}; it belongs to the Philippines' cultural and historical commemorations rather than a new statutory public holiday.",
 "why":"The anniversary follows the calendar date of the person's {event}, not a newly established annual holiday. No first-observance year or award date is inferred.",
 "take":"Discover the person's work and historical context through Philippine cultural institutions.",
 "other":"The NCCA lists {title} as a recurring cultural or civic observance. Its stated calendar period is {window}. The listing demonstrates inclusion in the national cultural calendar, not the passage of a public-holiday law or the date of its first celebration.",
 "whyOther":"The date or period follows the NCCA's published calendar entry. A separate founding rationale is not inferred from a listing alone.",
 "importance":"The annual date gives readers a starting point to learn about {subject}, its setting in Filipino society and the cultural institutions recording it.",
 "facts":("The date or period is indexed in the NCCA's national cultural calendar.","The official calendar listing does not itself establish a paid non-working holiday.","The founding year remains unspecified when no establishing instrument is cited."),
 },
 "it":{
 "date":"Il calendario NCCA ricorda il {day} {month} come anniversario della {kind} di {name}.",
 "role":"La scheda identifica questa persona come {role}; la ricorrenza appartiene alla memoria culturale e storica filippina e non costituisce di per sé una nuova festività legale.",
 "why":"L'anniversario coincide con la data della {event} della persona, non con l'istituzione di una nuova festa annuale. Non viene dedotto un anno della prima celebrazione o del riconoscimento.",
 "take":"Scopri le opere e il contesto storico della persona attraverso le istituzioni culturali filippine.",
 "other":"La NCCA registra {title} come ricorrenza culturale o civile annuale. Il periodo indicato nel calendario è {window}. L'inserimento dimostra che la ricorrenza è censita, non che sia stata istituita una festività non lavorativa o che sia nota la prima celebrazione.",
 "whyOther":"La data o il periodo provengono dal calendario della NCCA. Il motivo storico originario non può essere dedotto dalla sola presenza nell'elenco.",
 "importance":"La ricorrenza offre uno spunto per conoscere {subject}, il suo contesto nella società filippina e le istituzioni culturali che la ricordano.",
 "facts":("Data o periodo presenti nel calendario culturale ufficiale NCCA.","La registrazione nel calendario non dimostra l'esistenza di una festività non lavorativa.","L'anno di prima istituzione resta sconosciuto senza un atto specifico."),
 },
 "es":{
 "date":"El calendario NCCA recuerda el {day} de {month} como aniversario del {kind} de {name}.",
 "role":"La ficha identifica a esta persona como {role}; se trata de memoria cultural e histórica filipina, no de un nuevo día festivo legal.",
 "why":"El aniversario corresponde a la fecha del {event} de la persona y no a la creación de un nuevo festivo anual. No se deduce el primer año de celebración ni de reconocimiento.",
 "take":"Descubre la obra y el contexto histórico de esta persona en instituciones culturales filipinas.",
 "other":"La NCCA incluye {title} como conmemoración cultural o cívica recurrente. El período del calendario es {window}. Esta inclusión no demuestra una ley sobre días festivos ni documenta el primer año de celebración.",
 "whyOther":"La fecha o el período proceden del calendario publicado por la NCCA. No se infiere una razón fundacional independiente de la simple lista.",
 "importance":"La fecha invita a conocer {subject}, su contexto en la sociedad filipina y las instituciones culturales que la recuerdan.",
 "facts":("La fecha o período aparece en el calendario cultural de la NCCA.","Su inclusión no implica necesariamente un festivo no laborable.","El año de establecimiento sigue sin comprobarse si no hay documento específico."),
 },
 "fr":{
 "date":"Le calendrier de la NCCA indique le {day} {month} comme anniversaire de la {kind} de {name}.",
 "role":"La fiche désigne cette personne comme {role}. Il s'agit d'une commémoration culturelle et historique philippine, et non d'un nouveau jour férié légal.",
 "why":"L'anniversaire correspond à la date de la {event} de la personne, et non à l'instauration d'un jour férié annuel. Aucune première année de célébration ou de distinction n'est déduite.",
 "take":"Découvrez les œuvres et le contexte historique de la personne auprès d'institutions culturelles philippines.",
 "other":"La NCCA recense {title} comme commémoration culturelle ou civique récurrente. La période indiquée est {window}. Cette inscription ne prouve pas l'existence d'une loi instituant un jour férié ni la date de la première célébration.",
 "whyOther":"La date ou la période provient du calendrier de la NCCA. Une justification historique initiale distincte ne peut être déduite de la seule inscription.",
 "importance":"Cette commémoration invite à découvrir {subject}, son contexte dans la société philippine et les institutions culturelles qui la recensent.",
 "facts":("Date ou période inscrite au calendrier culturel de la NCCA.","L'inscription ne prouve pas un jour férié chômé.","L'année d'instauration demeure inconnue sans acte spécifique."),
 },
 "de":{
 "date":"Der NCCA-Kalender führt den {day}. {month} als Jahrestag der {kind} von {name}.",
 "role":"Der Eintrag bezeichnet die Person als {role}. Es handelt sich um philippinisches Kultur- und Geschichtsgedenken, nicht um einen neu eingeführten gesetzlichen Feiertag.",
 "why":"Der Jahrestag folgt dem Datum der {event} dieser Person, nicht dem Datum einer Feiertagsgründung. Ein Jahr der ersten Gedenkfeier oder Auszeichnung wird nicht behauptet.",
 "take":"Entdecken Sie Werk und historischen Hintergrund der Person bei philippinischen Kulturinstitutionen.",
 "other":"Die NCCA verzeichnet {title} als wiederkehrenden kulturellen oder gesellschaftlichen Gedenkanlass. Der Kalendereintrag umfasst {window}. Die Aufnahme belegt weder ein arbeitsfreies Feiertagsgesetz noch den Zeitpunkt der ersten Feier.",
 "whyOther":"Datum oder Zeitraum stammen aus dem veröffentlichten NCCA-Kalender. Ein eigenständiger historischer Gründungsgrund lässt sich daraus allein nicht ableiten.",
 "importance":"Der Anlass bietet die Gelegenheit, {subject}, seinen Kontext in der philippinischen Gesellschaft und die dokumentierenden Kulturinstitutionen kennenzulernen.",
 "facts":("Datum oder Zeitraum stehen im NCCA-Kulturkalender.","Ein solcher Eintrag belegt keinen arbeitsfreien gesetzlichen Feiertag.","Das Gründungsjahr bleibt ohne gesonderten Beleg offen."),
 },
 "pt":{
 "date":"O calendário da NCCA regista {day} de {month} como aniversário do {kind} de {name}.",
 "role":"A ficha identifica a pessoa como {role}. Trata-se de memória cultural e histórica filipina, não de um novo feriado legal.",
 "why":"O aniversário corresponde à data do {event} da pessoa, e não à criação de um feriado anual. Não se presume o primeiro ano de celebração ou de atribuição da distinção.",
 "take":"Explore as obras e o contexto histórico desta pessoa através das instituições culturais filipinas.",
 "other":"A NCCA identifica {title} como comemoração cultural ou cívica recorrente. O período indicado é {window}. A inclusão não comprova uma lei que institua feriado nem a data da primeira celebração.",
 "whyOther":"A data ou o período seguem o calendário publicado pela NCCA. A razão histórica inicial não é inferida da simples listagem.",
 "importance":"A comemoração convida a conhecer {subject}, o seu contexto na sociedade filipina e as instituições culturais que a documentam.",
 "facts":("Data ou período incluído no calendário cultural da NCCA.","A listagem não implica necessariamente feriado não laboral.","O ano de criação permanece desconhecido sem documento específico."),
 }
}
MONTHS={
"en":("January","February","March","April","May","June","July","August","September","October","November","December"),
"it":("gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"),
"es":("enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"),
"fr":("janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"),
"de":("Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"),
"pt":("janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro")}
KIND={
"en":("birth","death","birth","death"),
"it":("nascita","morte","nascita","morte"),
"es":("nacimiento","fallecimiento","nacimiento","fallecimiento"),
"fr":("naissance","mort","naissance","mort"),
"de":("Geburt","Tod","Geburt","Tod"),
"pt":("nascimento","falecimento","nascimento","falecimento")}
CATEGORIES=(
("Birth of National Artist ","birth","artist"),
("Death of National Artist ","death","artist"),
("Birth of National Living Treasure ","birth","treasure"),
("Death of National Living Treasure ","death","treasure"),
("Birth of President ","birth","president"),
("Death of President ","death","president"),
("Birth of Senate President ","birth","senate"),
)
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def event(row):
 title=row["canonicalTitleEn"]
 assert title.endswith(" — Philippines")
 stripped=title[:-len(" — Philippines")]
 for prefix,event,kind in CATEGORIES:
  if stripped.startswith(prefix):
   return event,kind,stripped[len(prefix):]
 return None,None,stripped
def date_window(rule,locale):
 k=rule["kind"]
 if k=="FIXED_DATE":
  return f'{rule["day"]} {MONTHS[locale][rule["month"]-1]}'
 if k=="FIXED_RANGE":
  return f'{rule["startDay"]} {MONTHS[locale][rule["startMonth"]-1]} – {rule["endDay"]} {MONTHS[locale][rule["endMonth"]-1]}'
 assert k=="NTH_WEEKDAY"
 return f'{rule["occurrence"]} / {rule["weekday"]} / {MONTHS[locale][rule["month"]-1]}'
def article(r,loc):
 t=T[loc]
 ev,k,name=event(r)
 rule=r["recurrenceRules"][0]
 window=date_window(rule,loc)
 title=r["canonicalTitleEn"]
 original={"id":r["id"],"source":r["source"],"scope":r["holidayClassification"]}
 if ev:
  assert rule["kind"]=="FIXED_DATE"
  idx=LOCALES.index(loc)
  role=GROUPS[k][idx]
  term={"birth":{"en":"birth","it":"nascita","es":"nacimiento","fr":"naissance","de":"Geburt","pt":"nascimento"},
        "death":{"en":"death","it":"morte","es":"fallecimiento","fr":"mort","de":"Tod","pt":"falecimento"}}[ev][loc]
  date_text=t["date"].format(day=rule["day"],month=MONTHS[loc][rule["month"]-1],kind=term,name=name)
  role_text=t["role"].format(role=role)
  origin=date_text+" "+role_text
  why=t["why"].format(event=term)
  fact=[date_text,role_text]
  hook=f'{name} · {window}'
  summary=date_text
  importance=t["importance"].format(subject=name)
  ways=[t["take"],"https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/"]
 else:
  origin=t["other"].format(title=title,window=window)
  why=t["whyOther"]
  summary=t["importance"].format(subject=title)
  importance=summary
  fact=[f'{title}: {window}',origin.split(".")[0]+"."]
  hook=f'{title} · {window}'
  ways=[t["take"],"https://ncca.gov.ph/events-calendar/monthly-observances-and-significant-dates/"]
 assert len(origin)>=115,(r["id"],loc,len(origin))
 return {"observanceId":r["id"],"locale":loc,"status":STATUS,
         "translationOf":"en" if loc!="en" else None,
         "hook":hook,"summary":summary,"whyThisDate":why,
         "origin":origin,"whyItMatters":importance,"quickFacts":fact,
         "waysToTakePart":ways,"relatedObservanceIds":[],
         "lastReviewedAt":"2026-11-19",
         "sourcePolicy":"NCCA-indexed individual event or cultural period, translated by AI; date or period and identity are sourced. Original founding year or full biography is not independently reconstructed.",
         "institutionalSourceUrls":[r["source"]],
         "editorialEvidenceScope":"INDIVIDUAL_EVENT_DATE_NOT_INDIVIDUAL_FOUNDING_HISTORY"}

def main():
 catalog=read(DATA/"official_core.json")
 canon={r["id"]:r for r in catalog["records"]}
 assert len(canon)==1111
 old={loc:read(DATA/f"editorial_{loc}.json") for loc in LOCALES}
 baseline=[r["observanceId"] for r in old["en"]["entries"]]
 assert len(baseline)==1111
 assert all(x["entryCount"]==1111 and [r["observanceId"] for r in x["entries"]]==baseline for x in old.values())
 by_locale={loc:{r["observanceId"]:r for r in old[loc]["entries"]} for loc in LOCALES}
 source=[]
 counts=[]
 for name in SRC_FILES:
  d=read(SOURCE/name)
  subset=[r for r in d["records"] if r["country"]=="PH"]
  if name.startswith("wave11"):
   assert len(subset)==144
  for r in subset:
   if by_locale["en"][r["id"]]["status"]==OLD:
    source.append(r)
   else:
    assert by_locale["en"][r["id"]]["status"]!="AI_NCCA_EVENT_ANCHORED_SIX_LOCALE"
  counts.append(len(source)-sum(counts))
 assert counts==[144,11,5],counts
 assert len(source)==len({x["id"] for x in source})==160
 assert all(r["source"]==SOURCE_URL and r["country"]=="PH" for r in source)
 assert all(canon[r["id"]]["countries"]==["PH"] and canon[r["id"]]["sources"][0]["url"]==SOURCE_URL for r in source)
 assert sum(event(r)[0] is not None for r in source)==144
 source=sorted(source,key=lambda r:r["id"])
 cohorts=[source[i:i+40] for i in range(0,len(source),40)]
 assert len(cohorts)==4 and all(len(x)==40 for x in cohorts)
 def worker(task):
  i,group=task
  return i,{loc:[article(r,loc) for r in group] for loc in LOCALES}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  results=sorted(pool.map(worker,enumerate(cohorts)))
 ids=[r["id"] for r in source]
 for loc in LOCALES:
  out={r["observanceId"]:r for _,batch in results for r in batch[loc]}
  assert set(out)==set(ids)
  for oid,row in out.items():
   prev=by_locale[loc][oid]
   assert prev["status"]==OLD
   prev.update(row)
  assert sum(r["status"]==STATUS for r in old[loc]["entries"])==160
  assert sum(r["status"]==OLD for r in old[loc]["entries"])==432
  assert sum(r["status"]=="AI_SOURCE_REVIEWED_SIX_LOCALE" for r in old[loc]["entries"])==107
  (DATA/f"editorial_{loc}.json").write_text(
    json.dumps(old[loc],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 report={"scope":"NCCA_PERSON_EVENT_SOURCE_ONLY_NOT_FULL_BIOGRAPHICAL_RESEARCH",
 "country":"PH","totalCanonical":1111,"alreadyNonContextual":519,
 "philippinesPreviousContextual":160,"publishedNccaIndividualEvent":160,
 "individualBirthOrDeathAnniversaries":144,"otherNationalObservances":16,
 "remainingGenericContextual":432,"remainingWithoutIndividualFoundingHistory":592,
 "parallelCohortSizes":[40,40,40,40],"languages":list(LOCALES),
 "ids":ids}
 path=ROOT/"reports/editorial_ph_160_event_index.json"
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("PH_160_NCCA_EVENT_SIX_LOCALE_PASS",json.dumps({k:v for k,v in report.items() if k!="ids"},sort_keys=True))

if __name__=="__main__":main()
