import json, re, calendar
from datetime import date, timedelta
from pathlib import Path

VERIFIED='2026-10-12'
UN='https://www.un.org/en/observances/list-days-weeks'
UNESCO='https://www.unesco.org/en/days/list'
WHO='https://www.who.int/campaigns'

records=[]

def slug(s):
    s=s.lower().replace('’',"'")
    s=re.sub(r"\[[^\]]+\]",'',s)
    s=re.sub(r"[^a-z0-9]+",'-',s).strip('-')
    return s

def auth(name='United Nations',typ='UN',officiality='OFFICIAL_UN',resolution=None):
    return {'name':name,'type':typ,'officiality':officiality,'resolution':resolution}

def src(url,tier='A_PRIMARY'):
    return {'tier':tier,'url':url,'verifiedAt':VERIFIED}

def add(title, period, rules, authority, source_url, categories=None, aliases=None, notes=None, source_tier='A_PRIMARY'):
    rid=slug(title)
    if any(r['id']==rid for r in records):
        raise ValueError('duplicate id '+rid)
    records.append({
        'id':rid,
        'canonicalTitleEn':title,
        'aliases':aliases or [],
        'periodKind':period,
        'recurrenceRules':rules,
        'scope':'GLOBAL',
        'countries':[],
        'regions':[],
        'authority':authority,
        'categories':categories or [],
        'sources':[src(source_url,source_tier)],
        'visualKey':None,
        'editorialStatus':'STUB',
        'notes':notes or [],
        'lastVerifiedAt':VERIFIED,
    })

def fixed(title,m,d,res=None,name='United Nations',typ='UN',officiality='OFFICIAL_UN',source=UN,period='DAY',cats=None):
    add(title,period,[{'kind':'FIXED_DATE','month':m,'day':d}],auth(name,typ,officiality,res),source,cats)

def rng(title,sm,sd,em,ed,res=None,name='United Nations',typ='UN',officiality='OFFICIAL_UN',source=UN,period='WEEK'):
    add(title,period,[{'kind':'FIXED_RANGE','startMonth':sm,'startDay':sd,'endMonth':em,'endDay':ed}],auth(name,typ,officiality,res),source)

def nth(title,m,weekday,occ,res=None,name='United Nations',typ='UN',officiality='OFFICIAL_UN',source=UN,period='DAY'):
    add(title,period,[{'kind':'NTH_WEEKDAY','month':m,'weekday':weekday,'occurrence':occ}],auth(name,typ,officiality,res),source)

def lastwd(title,m,weekday,res=None,name='United Nations',typ='UN',officiality='OFFICIAL_UN',source=UN,period='DAY'):
    add(title,period,[{'kind':'LAST_WEEKDAY','month':m,'weekday':weekday}],auth(name,typ,officiality,res),source)

def multi_nth(title,rules,res=None,name='United Nations Environment Programme',typ='UNEP',officiality='OFFICIAL_UN_AGENCY',source=UN):
    add(title,'DAY',[{'kind':'NTH_WEEKDAY','month':m,'weekday':wd,'occurrence':o} for m,wd,o in rules],auth(name,typ,officiality,res),source)

def override(title,year,m,d,res=None,name='United Nations',typ='UN',officiality='OFFICIAL_UN',source=UN,kind='AUTHORITY_DEFINED'):
    add(title,'DAY',[{'kind':kind,'overrides':{str(year):{'startDate':f'{year:04d}-{m:02d}-{d:02d}','endDate':f'{year:04d}-{m:02d}-{d:02d}'}}}],auth(name,typ,officiality,res),source)

def consumer_fixed(title,m,d,name,typ,officiality,source,cats=None,aliases=None):
    add(
        title,
        'DAY',
        [{'kind':'FIXED_DATE','month':m,'day':d}],
        auth(name,typ,officiality),
        source,
        cats,
        aliases,
        source_tier='D_ORIGINATOR',
    )

def consumer_nth(title,m,weekday,occ,name,typ,officiality,source,cats=None,aliases=None,source_tier='D_ORIGINATOR'):
    add(
        title,
        'DAY',
        [{'kind':'NTH_WEEKDAY','month':m,'weekday':weekday,'occurrence':occ}],
        auth(name,typ,officiality),
        source,
        cats,
        aliases,
        source_tier=source_tier,
    )

# JANUARY
fixed('World Braille Day',1,4,'A/RES/73/161')
fixed('World Logic Day',1,14,'40 C/Resolution 39', 'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day of Education',1,24,'A/RES/73/25')
fixed('World Day for African and Afrodescendant Culture',1,24,'40 C/Resolution 50','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day of Clean Energy',1,26,'A/RES/77/327')
fixed('International Day of Commemoration in Memory of the Victims of the Holocaust',1,27,'A/RES/60/7')
fixed('International Day of Peaceful Coexistence',1,28,'A/RES/79/269')
fixed('World Neglected Tropical Diseases Day',1,30,None,'World Health Organization','WHO','OFFICIAL_WHO',WHO)

# FEBRUARY
rng('World Interfaith Harmony Week',2,1,2,7,'A/RES/65/5')
fixed('World Wetlands Day',2,2,'A/RES/75/317')
fixed('International Day of Human Fraternity',2,4,'A/RES/75/200')
fixed('International Day of Zero Tolerance to Female Genital Mutilation',2,6,'A/RES/67/146')
fixed('World Pulses Day',2,10,'A/RES/73/251','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
fixed('International Day of the Arabian Leopard',2,10,'A/RES/77/295')
fixed('International Day of Women and Girls in Science',2,11,'A/RES/70/212')
fixed('International Day for the Prevention of Violent Extremism as and when Conducive to Terrorism',2,12,'A/RES/77/243')
fixed('World Radio Day',2,13,'A/RES/67/124','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('Global Tourism Resilience Day',2,17,'A/RES/77/269')
fixed('World Day of Social Justice',2,20,'A/RES/62/10')
fixed('International Mother Language Day',2,21,'A/RES/56/262','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)

# MARCH
fixed('Zero Discrimination Day',3,1,None,'UNAIDS','UNAIDS','OFFICIAL_UN_AGENCY',UN)
fixed('World Seagrass Day',3,1,'A/RES/76/265')
fixed('World Wildlife Day',3,3,'A/RES/68/205')
fixed('International Day for Disarmament and Non-Proliferation Awareness',3,5,'A/RES/77/51')
fixed("International Women's Day",3,8)
fixed('International Day of Women Judges',3,10,'A/RES/75/274')
fixed('International Day to Combat Islamophobia',3,15,'A/RES/76/254')
fixed('International Day for Digital Learning',3,19,'42 C/Resolution 14','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day of Happiness',3,20,'A/RES/66/281')
fixed('French Language Day',3,20,None,'United Nations','UN','OFFICIAL_UN',UN)
fixed('World Day for Glaciers',3,21,'A/RES/77/158')
fixed('International Day of Forests',3,21,'A/RES/67/200','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
rng('Week of Solidarity with the Peoples Struggling against Racism and Racial Discrimination',3,21,3,27,'A/RES/34/24')
fixed('International Day for the Elimination of Racial Discrimination',3,21,'A/RES/2142 (XXI)')
fixed('World Poetry Day',3,21,'30 C/Resolution 29','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('International Day of Nowruz',3,21,'A/RES/64/253')
fixed('World Down Syndrome Day',3,21,'A/RES/66/149')
fixed('World Water Day',3,22,'A/RES/47/193')
fixed('World Meteorological Day',3,23,'WMO/EC-XII/Res.6','World Meteorological Organization','WMO','OFFICIAL_UN_AGENCY',UN)
fixed('World Tuberculosis Day',3,24,None,'World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('International Day for the Right to the Truth concerning Gross Human Rights Violations and for the Dignity of Victims',3,24,'A/RES/65/196')
fixed('International Day of Remembrance of the Victims of Slavery and the Transatlantic Slave Trade',3,25,'A/RES/62/122')
fixed('International Day of Solidarity with Detained and Missing Staff Members',3,25,'A/RES/49/59')
fixed('International Day of Zero Waste',3,30,'A/RES/77/161')

# APRIL
fixed('World Autism Awareness Day',4,2,'A/RES/62/139')
fixed('International Day for Mine Awareness and Assistance in Mine Action',4,4,'A/RES/60/97')
fixed('International Day of Conscience',4,5,'A/RES/73/329')
fixed('International Day of Sport for Development and Peace',4,6,'A/RES/67/296')
fixed('International Day of Reflection on the 1994 Genocide against the Tutsi in Rwanda',4,7,'A/RES/58/234')
fixed('World Health Day',4,7,'WHA/A.2/Res.35','World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('International Day of Human Space Flight',4,12,'A/RES/65/271')
fixed('World Chagas Disease Day',4,14,None,'World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('World Art Day',4,15,'40 C/Resolution 48','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Wellness Day',4,15,'A/RES/80/249')
fixed('Chinese Language Day',4,20)
fixed('World Creativity and Innovation Day',4,21,'A/RES/71/284')
fixed('International Day of Greening the Planet',4,22,'A/RES/80/300')
fixed('International Mother Earth Day',4,22,'A/RES/63/278')
nth('International Girls in ICT Day',4,4,4,None,'International Telecommunication Union','ITU','OFFICIAL_UN_AGENCY',UN)
fixed('World Book and Copyright Day',4,23,'28 C/Resolution 3.18','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('English Language Day',4,23)
fixed('Spanish Language Day',4,23)
rng('World Immunization Week',4,24,4,30,None,'World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('International Day of Multilateralism and Diplomacy for Peace',4,24,'A/RES/73/127')
fixed('International Day for Small Island Developing States',4,25,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('World Malaria Day',4,25,None,'World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed("International Delegate's Day",4,25,'A/RES/73/286')
fixed('International Chernobyl Disaster Remembrance Day',4,26,'A/RES/71/125')
fixed('World Intellectual Property Day',4,26,None,'World Intellectual Property Organization','WIPO','OFFICIAL_UN_AGENCY',UN)
fixed('World Day for Safety and Health at Work',4,28,None,'International Labour Organization','ILO','OFFICIAL_UN_AGENCY',UN)
fixed('International Day in Memory of the Victims of Earthquakes',4,29,'A/RES/79/285')
fixed('International Jazz Day',4,30,'36 C/Resolution 39','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)

# MAY
# Vesak is lunar/authority-defined; 2026 occurrence is supplied by current UN calendar.
override('Vesak, the Day of the Full Moon',2026,5,1,'A/RES/54/115',kind='LUNAR')
fixed('World Tuna Day',5,2,'A/RES/71/124')
fixed('World Press Freedom Day',5,3,'26 C/Resolution 4.3','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('World Portuguese Language Day',5,5,'40 C/Resolution 75','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('African World Heritage Day',5,5,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('Time of Remembrance and Reconciliation for Those Who Lost Their Lives During the Second World War',5,8,'A/RES/59/26')
multi_nth('World Migratory Bird Day',[(5,6,2),(10,6,2)],name='United Nations Environment Programme',typ='UNEP',officiality='OFFICIAL_UN_AGENCY')
fixed('International Day of Argania',5,10,'A/RES/75/262')
fixed('International Day of Plant Health',5,12,'A/RES/76/256','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
fixed('International Day of Families',5,15,'A/RES/47/237')
fixed('International Day of Living Together in Peace',5,16,'A/RES/72/130')
fixed('International Day of Light',5,16,'39 C/Resolution 16','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('World Telecommunication and Information Society Day',5,17,'A/RES/60/252')
fixed('World Fair Play Day',5,19,'A/RES/78/310')
fixed('World Bee Day',5,20,'A/RES/72/211','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
fixed('World Metrology Day',5,20,'42 C/Resolution 21','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Tea Day',5,21,'A/RES/74/241','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
fixed('World Day for Cultural Diversity for Dialogue and Development',5,21,'A/RES/57/249')
fixed('International Day for Biological Diversity',5,22,'A/RES/55/201')
fixed('International Day to End Obstetric Fistula',5,23,'A/RES/67/147')
fixed('International Day of the Markhor',5,24,'A/RES/78/278')
fixed('World Football Day',5,25,'A/RES/78/281')
rng('Week of Solidarity with the Peoples of Non-Self-Governing Territories',5,25,5,31,'A/RES/54/91')
fixed('International Day of UN Peacekeepers',5,29,'A/RES/57/129')
fixed('International Day of Potato',5,30,'A/RES/78/123','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
fixed('World No Tobacco Day',5,31,'Resolution 42.19','World Health Organization','WHO','OFFICIAL_WHO',UN)

# JUNE
fixed('Global Day of Parents',6,1,'A/RES/66/292')
fixed('World Bicycle Day',6,3,'A/RES/72/272')
fixed('International Day of Innocent Children Victims of Aggression',6,4,'A/RES/ES-7/8')
fixed('World Environment Day',6,5,'A/RES/2994 (XXVII)')
fixed('International Day for the Fight against Illegal, Unreported and Unregulated Fishing',6,5,'A/RES/72/72')
fixed('Russian Language Day',6,6)
fixed('World Food Safety Day',6,7,'A/RES/73/250')
fixed('World Oceans Day',6,8,'A/RES/63/111')
fixed('International Day for Dialogue among Civilizations',6,10,'A/RES/78/286')
fixed('International Day of Play',6,11,'A/RES/78/268')
fixed('World Day Against Child Labour',6,12,None,'International Labour Organization','ILO','OFFICIAL_UN_AGENCY',UN)
fixed('International Albinism Awareness Day',6,13,'A/RES/69/170')
fixed('World Blood Donor Day',6,14,'WHA Resolution 58.13','World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('World Elder Abuse Awareness Day',6,15,'A/RES/66/127')
fixed('International Day of Family Remittances',6,16,'A/RES/72/281')
fixed('World Day to Combat Desertification and Drought',6,17,'A/RES/49/115')
fixed('Sustainable Gastronomy Day',6,18,'A/RES/71/246','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
fixed('International Day for Countering Hate Speech',6,18,'A/RES/75/309')
fixed('International Day for the Elimination of Sexual Violence in Conflict',6,19,'A/RES/69/293')
fixed('World Refugee Day',6,20,'A/RES/55/76')
fixed('International Day of Yoga',6,21,'A/RES/69/131')
fixed('International Day of the Celebration of the Solstice',6,21,'A/RES/73/300')
fixed('United Nations Public Service Day',6,23,'A/RES/57/277')
fixed("International Widows' Day",6,23,'A/RES/65/189')
fixed('International Day of Women in Diplomacy',6,24,'A/RES/76/269')
fixed('Day of the Seafarer',6,25,'STCW/CONF.2/DC/4','International Maritime Organization','IMO','OFFICIAL_UN_AGENCY',UN)
fixed('International Day against Drug Abuse and Illicit Trafficking',6,26,'A/RES/42/112')
fixed('United Nations International Day in Support of Victims of Torture',6,26,'A/RES/52/149')
fixed('International Day of Deafblindness',6,27,'A/RES/79/294')
fixed('Micro-, Small and Medium-sized Enterprises Day',6,27,'A/RES/71/279')
fixed('International Day of the Tropics',6,29,'A/RES/71/279')
fixed('International Asteroid Day',6,30,'A/RES/71/90')
fixed('International Day of Parliamentarism',6,30,'A/RES/72/278')

# JULY
nth('International Day of Cooperatives',7,6,1,'A/RES/47/90')
fixed('World Rural Development Day',7,6,'A/RES/78/326')
fixed('World Kiswahili Language Day',7,7,'A/RES/78/312')
fixed('International Day of Reflection and Commemoration of the 1995 Genocide in Srebrenica',7,11,'A/RES/78/282')
fixed('World Population Day',7,11,'A/RES/45/216')
fixed('World Horse Day',7,11,'A/RES/79/291')
fixed('International Day of Combating Sand and Dust Storms',7,12,'A/RES/77/294')
fixed('International Day of Hope',7,12,'A/RES/79/270')
fixed('World Youth Skills Day',7,15,'A/RES/69/145')
fixed('Nelson Mandela International Day',7,18,'A/RES/64/13')
fixed('World Chess Day',7,20,'A/RES/74/22')
fixed('International Moon Day',7,20,'A/RES/76/76')
fixed('International Day of Women and Girls of African Descent',7,25,'A/RES/78/323')
fixed('World Drowning Prevention Day',7,25,'A/RES/75/273','World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('International Day for Judicial Well-being',7,25,'A/RES/79/266')
fixed('International Day for the Conservation of the Mangrove Ecosystem',7,26,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('World Hepatitis Day',7,28,None,'World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('International Day of Friendship',7,30,'A/RES/65/275')
fixed('World Day against Trafficking in Persons',7,30,'A/RES/68/192')

# AUGUST
rng('World Breastfeeding Week',8,1,8,7,None,'World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('International Day of Awareness of the Special Development Needs and Challenges of Landlocked Developing Countries',8,6,'A/79/L.108')
fixed("International Day of the World's Indigenous Peoples",8,9,'A/RES/49/214')
fixed('World Steelpan Day',8,11,'A/RES/77/316')
fixed('International Youth Day',8,12,'A/RES/54/120')
fixed('World Humanitarian Day',8,19,'A/RES/63/139')
fixed('International Day of Remembrance and Tribute to the Victims of Terrorism',8,21,'A/RES/72/165')
fixed('International Day Commemorating the Victims of Acts of Violence Based on Religion or Belief',8,22,'A/RES/73/296')
fixed('International Day for the Remembrance of the Slave Trade and Its Abolition',8,23,'29 C/Resolution 40','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('World Lake Day',8,27,'A/RES/79/142')
fixed('International Day against Nuclear Tests',8,29,'A/RES/64/35')
fixed('International Day of the Victims of Enforced Disappearances',8,30,'A/RES/65/209')
fixed('International Day for People of African Descent',8,31,'A/RES/75/170')
fixed('International Day of Safe, Secure and Trustworthy Artificial Intelligence',8,31,'A/RES/80/302')

# SEPTEMBER
fixed('International Day of Charity',9,5,'A/RES/67/105')
fixed("International Day of the World's Indigenous Women and Girls",9,5,'A/RES/80/10')
fixed('International Day of Clean Air for Blue Skies',9,7,'A/RES/74/212','United Nations Environment Programme','UNEP','OFFICIAL_UN_AGENCY',UN)
fixed('International Day of Police Cooperation',9,7,'A/RES/77/241')
fixed('World Duchenne Awareness Day',9,7,'A/RES/78/12')
fixed('International Literacy Day',9,8,'14 C/Resolution 1.441','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('International Day to Protect Education from Attack',9,9,'A/RES/74/275')
fixed('United Nations Day for South-South Cooperation',9,12,'A/RES/58/220')
fixed('International Day for Caves and Karst',9,13,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day of Democracy',9,15,'A/RES/62/7')
fixed('International Day of Science, Technology and Innovation for the South',9,16,'A/RES/78/259')
fixed('International Day for Interventional Cardiology',9,16,'A/RES/76/302')
fixed('International Day for the Preservation of the Ozone Layer',9,16,'A/RES/49/114')
fixed('World Patient Safety Day',9,17,None,'World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('International Equal Pay Day',9,18,'A/RES/74/142')
fixed('International Day of University Sport',9,20,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('World Cleanup Day',9,20,'A/RES/78/122')
fixed('International Day of Peace',9,21,'A/RES/36/67')
fixed('International Day of Nomadic Heritage',9,21,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day of Sign Languages',9,23,'A/RES/72/161')
lastwd('World Maritime Day',9,4,None,'International Maritime Organization','IMO','OFFICIAL_UN_AGENCY',UN)
fixed('International Day for the Total Elimination of Nuclear Weapons',9,26,'A/RES/68/32')
fixed('World Tourism Day',9,27,None,'UN Tourism','UN_TOURISM','OFFICIAL_UN_AGENCY',UN)
fixed('International Day for Universal Access to Information',9,28,'A/RES/74/5')
fixed('International Day of Awareness of Food Loss and Waste',9,29,'A/RES/74/209','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
fixed('International Translation Day',9,30,'A/RES/71/288')

# OCTOBER
fixed('International Coffee Day',10,1,'A/RES/80/248')
fixed('International Day of Older Persons',10,1,'A/RES/45/106')
fixed('International Day of Non-Violence',10,2,'A/RES/61/271')
rng('World Space Week',10,4,10,10,'A/RES/54/68')
nth('World Habitat Day',10,1,1,'A/RES/40/202 A')
fixed("World Teachers' Day",10,5,'27 C/INF.7','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('International Geodiversity Day',10,6,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('World Cotton Day',10,7,'A/RES/75/318')
fixed('World Post Day',10,9,None,'Universal Postal Union','UPU','OFFICIAL_UN_AGENCY',UN)
fixed('World Mental Health Day',10,10,None,'World Health Organization','WHO','OFFICIAL_UN_AGENCY',UN)
fixed('International Day of the Girl Child',10,11,'A/RES/66/170')
fixed('International Day for Disaster Risk Reduction',10,13,'A/RES/64/200')
fixed('International Day of Rural Women',10,15,'A/RES/62/136')
fixed('World Food Day',10,16,'A/RES/35/70','Food and Agriculture Organization','FAO','OFFICIAL_UN_AGENCY',UN)
fixed('International Day of the Intangible Cultural Heritage',10,17,'42 C/Resolution 34','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day for the Eradication of Poverty',10,17,'A/RES/47/196')
fixed('International Day of the Snow Leopard',10,23,'A/RES/79/143')
rng('Disarmament Week',10,24,10,30,'A/RES/S-10/2')
fixed('United Nations Day',10,24,'A/RES/168 (II)')
fixed('World Development Information Day',10,24,'A/RES/3038 (XXVII)')
rng('Global Media and Information Literacy Week',10,24,10,31,'A/RES/75/267')
fixed('World Day for Audiovisual Heritage',10,27,'33 C/Resolution 5','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('World Coding Day',10,29,'42 C/Resolution 15','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day of Care and Support',10,29,'A/RES/77/317')
fixed('World Cities Day',10,31,'A/RES/68/239')

# NOVEMBER
fixed('International Day to End Impunity for Crimes against Journalists',11,2,'A/RES/68/163')
fixed('International Day for Biosphere Reserves',11,3,'41 C/Resolution 37','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('World Tsunami Awareness Day',11,5,'A/RES/70/203')
fixed('International Day for Preventing the Exploitation of the Environment in War and Armed Conflict',11,6,'A/RES/56/4')
rng('International Week of Science and Peace',11,9,11,15,'A/RES/43/61')
fixed('World Science Day for Peace and Development',11,10,'31 C/Resolution 20','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('World Diabetes Day',11,14,'A/RES/61/225')
fixed('International Day for the Prevention of and Fight against All Forms of Transnational Organized Crime',11,15,'A/RES/78/267')
fixed('World Prematurity Day',11,15,None,'World Health Organization','WHO','OFFICIAL_WHO',WHO)
fixed('International Day of the Mediterranean Diet',11,16,'A/RES/80/174')
fixed('International Day for Tolerance',11,16,'28 C/Resolution 5.61','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
nth('World Day of Remembrance for Road Traffic Victims',11,7,3,'A/RES/60/5')
fixed('World Cervical Cancer Elimination Day',11,17,None,'World Health Organization','WHO','OFFICIAL_WHO',WHO)
rng('World Antimicrobial Resistance Awareness Week',11,18,11,24,None,'World Health Organization','WHO','OFFICIAL_WHO',UN)
fixed('World Day for the Prevention of and Healing from Child Sexual Exploitation, Abuse and Violence',11,18,'A/RES/77/8')
nth('World Philosophy Day',11,4,3,'33 C/Resolution 37','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('World Toilet Day',11,19,'A/RES/67/291')
fixed('Africa Industrialization Day',11,20,'A/RES/44/237')
fixed("World Children's Day",11,20,'A/RES/836(IX)')
fixed('World Television Day',11,21,'A/RES/51/205')
fixed('World Conjoined Twins Day',11,24,'A/RES/78/313')
fixed('International Day for the Elimination of Violence against Women',11,25,'A/RES/54/134')
fixed('World Sustainable Transport Day',11,26,'A/RES/77/286')
fixed('World Olive Tree Day',11,26,'40 C/Resolution 49','UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day for the Elimination of Child, Early and Forced Marriage',11,27,'A/RES/80/309')
fixed('International Day of Engagement in Science for Sustainable Development',11,27,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day of Solidarity with the Palestinian People',11,29,'A/RES/32/40B')
fixed('Day of Remembrance for all Victims of Chemical Warfare',11,30,'OPCW C-20/DEC.10','Organisation for the Prohibition of Chemical Weapons','OPCW','OFFICIAL_INSTITUTIONAL',UN)

# DECEMBER
fixed('World AIDS Day',12,1,None,'World Health Organization / UNAIDS','WHO_UNAIDS','OFFICIAL_UN_AGENCY',UN)
fixed('International Day for the Abolition of Slavery',12,2,'A/RES/317(IV)')
fixed('World Futures Day',12,2,None,'UNESCO','UNESCO','OFFICIAL_UNESCO',UNESCO)
fixed('International Day of Persons with Disabilities',12,3,'A/RES/47/3')
fixed('International Day of Banks',12,4,'A/RES/74/245')
fixed('International Day Against Unilateral Coercive Measures',12,4,'A/RES/79/293')
fixed('International Volunteer Day for Economic and Social Development',12,5,'A/RES/40/212')
fixed('World Soil Day',12,5,'A/RES/68/232')
fixed('International Civil Aviation Day',12,7,'A/RES/51/33')
fixed('International Day of Commemoration and Dignity of the Victims of the Crime of Genocide and of the Prevention of this Crime',12,9,'A/RES/69/323')
fixed('International Anti-Corruption Day',12,9,'A/RES/58/4')
fixed('Human Rights Day',12,10,'A/RES/423 (V)')
fixed('International Mountain Day',12,11,'A/RES/57/245')
fixed('International Day of Neutrality',12,12,'A/RES/71/275')
fixed('International Universal Health Coverage Day',12,12,'A/RES/72/138')
fixed('International Day against Colonialism in All its Forms and Manifestations',12,14,'A/RES/80/106')
fixed('World Turkic Language Family Day',12,15,'43 C/57','UNESCO','UNESCO','OFFICIAL_UNESCO',UN)
fixed('International Migrants Day',12,18,'A/RES/55/93')
fixed('Arabic Language Day',12,18)
fixed('International Day of Recognition for Women Searchers of Missing Persons',12,19,'A/RES/80/301')
fixed('International Human Solidarity Day',12,20,'A/RES/60/209')
fixed('World Meditation Day',12,21,'A/RES/79/137')
fixed('World Basketball Day',12,21,'A/RES/77/324')
fixed('International Anti-Cybercrime Day',12,24,'A/RES/79/243')
fixed('International Day of Epidemic Preparedness',12,27,'A/RES/75/27')


# CURATED CONSUMER / ORIGINATOR-BACKED OBSERVANCES
# These records are intentionally distinct from the UN/UNESCO/WHO official core.
# They are published only when an originator or primary institutional source is known.
consumer_fixed(
    'World Cancer Day',2,4,
    'Union for International Cancer Control','UICC','RECOGNIZED_NGO',
    'https://www.uicc.org/what-we-do/events/world-cancer-day',
    ['Health'],
)
consumer_nth(
    'Safer Internet Day',2,2,2,
    'Better Internet for Kids / European Commission','EU_BIK','OFFICIAL_INSTITUTIONAL',
    'https://better-internet-for-kids.europa.eu/en/events/safer-internet-day-sid-2026',
    ['Technology','Children'],
    source_tier='A_PRIMARY',
)
consumer_fixed(
    'World Theatre Day',3,27,
    'International Theatre Institute','ITI','RECOGNIZED_NGO',
    'https://www.iti-worldwide.org/pdfs/How_to_Celebrate_World_Theatre_Day_2024.pdf',
    ['Culture'],
)
consumer_fixed(
    'International Dance Day',4,29,
    'International Theatre Institute / Dance Committee','ITI','RECOGNIZED_NGO',
    'https://www.iti-worldwide.org/pdfs/2019IDD_EventReport.pdf',
    ['Culture'],
)
consumer_fixed(
    'International Nurses Day',5,12,
    'International Council of Nurses','ICN','RECOGNIZED_NGO',
    'https://admin.icn.ch/how-we-do-it/campaigns/international-nurses-day',
    ['Health'],
)
consumer_fixed(
    'International Museum Day',5,18,
    'International Council of Museums','ICOM','RECOGNIZED_NGO',
    'https://icom.museum/en/news/international-museum-day-2026-a-message-from-the-president/',
    ['Culture','Education'],
)
consumer_fixed(
    'World Turtle Day',5,23,
    'American Tortoise Rescue','ATR','RECOGNIZED_NGO',
    'https://worldturtleday.org/about/',
    ['Animals','Environment'],
)
consumer_fixed(
    'World MS Day',5,30,
    'MS International Federation','MSIF','RECOGNIZED_NGO',
    'https://worldmsday.org/about/',
    ['Health'],
)
consumer_fixed(
    'World Emoji Day',7,17,
    'Emojipedia / Zedge','EMOJIPEDIA','POPULAR',
    'https://emojipedia.org/en/world-emoji-day',
    ['Technology','Culture'],
)
consumer_fixed(
    'World Suicide Prevention Day',9,10,
    'International Association for Suicide Prevention','IASP','RECOGNIZED_NGO',
    'https://www.iasp.info/wspd/',
    ['Health'],
)
consumer_fixed(
    "World Alzheimer's Day",9,21,
    "Alzheimer's Disease International",'ADI','RECOGNIZED_NGO',
    'https://www.alzint.org/get-involved/world-alzheimers-month/frequently-asked-questions/',
    ['Health'],
)
consumer_fixed(
    'World Heart Day',9,29,
    'World Heart Federation','WHF','RECOGNIZED_NGO',
    'https://world-heart-federation.org/',
    ['Health'],
)
consumer_fixed(
    'World Vegan Day',11,1,
    'The Vegan Society','VEGAN_SOCIETY','RECOGNIZED_NGO',
    'https://www.vegansociety.com/news/blog/celebrate-world-vegan-month-november',
    ['Food','Environment'],
)
consumer_fixed(
    'World Kindness Day',11,13,
    'World Kindness Movement','WKM','RECOGNIZED_NGO',
    'https://www.theworldkindnessmovement.org/about-us-2/story/',
    ['Culture','Rights'],
)

# 2026 annual campaign overrides known from primary WHO pages.
year_overrides=[
    {
      'observanceId':'world-health-day',
      'year':2026,
      'campaignTheme':'Together for health. Stand with science',
      'campaignUrl':'https://www.who.int/campaigns/world-health-day',
      'verifiedAt':VERIFIED,
    },
    {
      'observanceId':'world-patient-safety-day',
      'year':2026,
      'campaignTheme':'Safe care for life!',
      'campaignUrl':'https://www.who.int/campaigns/world-patient-safety-day/2026',
      'verifiedAt':VERIFIED,
    },
]

def resolve_rule(rule,year):
    k=rule['kind']
    if k=='FIXED_DATE':
        return [(date(year,rule['month'],rule['day']),date(year,rule['month'],rule['day']))]
    if k=='FIXED_RANGE':
        sy=year
        ey=year+1 if rule['endMonth'] < rule['startMonth'] else year
        return [(date(sy,rule['startMonth'],rule['startDay']), date(ey,rule['endMonth'],rule['endDay']))]
    if k=='NTH_WEEKDAY':
        # Dart weekdays: Monday=1..Sunday=7; Python Monday=0..Sunday=6
        target=rule['weekday']-1
        first=date(year,rule['month'],1)
        delta=(target-first.weekday())%7
        d=1+delta+7*(rule['occurrence']-1)
        return [(date(year,rule['month'],d),date(year,rule['month'],d))]
    if k=='LAST_WEEKDAY':
        target=rule['weekday']-1
        last_day=calendar.monthrange(year,rule['month'])[1]
        last=date(year,rule['month'],last_day)
        delta=(last.weekday()-target)%7
        d=last_day-delta
        return [(date(year,rule['month'],d),date(year,rule['month'],d))]
    if k in ('AUTHORITY_DEFINED','LUNAR'):
        ov=rule.get('overrides',{}).get(str(year))
        if not ov:
            return []
        return [(date.fromisoformat(ov['startDate']),date.fromisoformat(ov['endDate']))]
    raise ValueError(k)

# Cross-year recurrence oracle for deterministic rules.
vector_rules={
 'international-day-of-cooperatives': {2026:['2026-07-04'],2027:['2027-07-03'],2028:['2028-07-01']},
 'world-habitat-day': {2026:['2026-10-05'],2027:['2027-10-04'],2028:['2028-10-02']},
 'world-migratory-bird-day': {2026:['2026-05-09','2026-10-10'],2027:['2027-05-08','2027-10-09'],2028:['2028-05-13','2028-10-14']},
 'world-maritime-day': {2026:['2026-09-24'],2027:['2027-09-30'],2028:['2028-09-28']},
 'world-day-of-remembrance-for-road-traffic-victims': {2026:['2026-11-15'],2027:['2027-11-21'],2028:['2028-11-19']},
 'world-philosophy-day': {2026:['2026-11-19'],2027:['2027-11-18'],2028:['2028-11-16']},
 'international-girls-in-ict-day': {2026:['2026-04-23'],2027:['2027-04-22'],2028:['2028-04-27']},
}
by_id={r['id']:r for r in records}
for rid, year_map in vector_rules.items():
    for year, expected_dates in year_map.items():
        actual=[]
        for rule in by_id[rid]['recurrenceRules']:
            actual.extend(s.isoformat() for s,e in resolve_rule(rule,year))
        assert sorted(actual)==expected_dates,(rid,year,actual,expected_dates)

calendar_year_counts={}
unresolved_by_year={}
for year in (2026,2027,2028):
    calendar_year_counts[str(year)]=366 if calendar.isleap(year) else 365
    unresolved=[]
    for r in records:
        if any(rule['kind'] in ('AUTHORITY_DEFINED','LUNAR') and not rule.get('overrides',{}).get(str(year)) for rule in r['recurrenceRules']):
            unresolved.append(r['id'])
    unresolved_by_year[str(year)]=sorted(unresolved)


# Validate and generate 2026 full date index.
ids=[r['id'] for r in records]
assert len(ids)==len(set(ids))
for r in records:
    assert r['sources']
    if r['authority']['officiality'].startswith('OFFICIAL_'):
        assert any(s['tier']=='A_PRIMARY' for s in r['sources'])

occurrences=[]
for r in records:
    for idx,rule in enumerate(r['recurrenceRules']):
        for start,end in resolve_rule(rule,2026):
            occurrences.append({
                'observanceId':r['id'],'year':2026,'startDate':start.isoformat(),'endDate':end.isoformat(),
                'derivedFromRule':rule['kind'] not in ('AUTHORITY_DEFINED','LUNAR'),'ruleIndex':idx,
            })

# Date index for all 365 days, including empty dates.
index=[]
d=date(2026,1,1)
while d.year==2026:
    active=[]
    for o in occurrences:
        s=date.fromisoformat(o['startDate']); e=date.fromisoformat(o['endDate'])
        if s<=d<=e:
            active.append(o['observanceId'])
    index.append({'date':d.isoformat(),'observanceIds':sorted(set(active))})
    d += timedelta(days=1)
assert len(index)==365

# Known recurrence vectors checked independently.
expected={
 'international-day-of-cooperatives':['2026-07-04'],
 'world-habitat-day':['2026-10-05'],
 'world-migratory-bird-day':['2026-05-09','2026-10-10'],
 'world-maritime-day':['2026-09-24'],
 'world-day-of-remembrance-for-road-traffic-victims':['2026-11-15'],
 'world-philosophy-day':['2026-11-19'],
 'international-girls-in-ict-day':['2026-04-23'],
}
for rid,dates in expected.items():
    actual=sorted(o['startDate'] for o in occurrences if o['observanceId']==rid)
    assert actual==dates,(rid,actual,dates)

seed={
 'schemaVersion':1,
 'datasetId':'world-days-official-core',
 'datasetVersion':'2026.10.12.2',
 'generatedAt':'2026-10-11',
 'coverage':'Verified UN/UNESCO/WHO institutional core plus a separately classified originator-backed consumer tranche.'
 'records':sorted(records,key=lambda r:r['id']),
 'yearOverrides':year_overrides,
}
OUT = Path(__file__).resolve().parents[1] / 'assets' / 'data'
OUT.mkdir(parents=True, exist_ok=True)
Path(OUT / 'official_core.json').write_text(json.dumps(seed,ensure_ascii=False,indent=2),encoding='utf-8')
Path(OUT / 'occurrences_2026.json').write_text(json.dumps({
 'schemaVersion':1,
 'year':2026,
 'occurrenceCount':len(occurrences),
 'calendarDayCount':len(index),
 'occurrences':sorted(occurrences,key=lambda x:(x['startDate'],x['observanceId'])),
 'dateIndex':index,
},ensure_ascii=False,indent=2),encoding='utf-8')

report={
 'canonicalObservances':len(records),
 'occurrences2026':len(occurrences),
 'calendarDays2026':len(index),
 'daysWithAtLeastOneObservance':sum(1 for x in index if x['observanceIds']),
 'emptyCalendarDays':sum(1 for x in index if not x['observanceIds']),
 'calendarYearCounts':calendar_year_counts,
 'unresolvedAuthorityOrLunarByYear':unresolved_by_year,
 'crossYearRecurrenceVectors':'PASS',
 'officialityCounts':{},
 'authorityCounts':{},
}
for r in records:
    report['officialityCounts'][r['authority']['officiality']]=report['officialityCounts'].get(r['authority']['officiality'],0)+1
    report['authorityCounts'][r['authority']['name']]=report['authorityCounts'].get(r['authority']['name'],0)+1
Path(OUT / 'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
