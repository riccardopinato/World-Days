# World Days — Market Layer

Verified: 2026-10-12

## Product rule

Locale and market are independent dimensions.

- Locale controls interface language.
- Market controls which national observances are shown alongside global observances.
- `GLOBAL` shows only global records in Today, Calendar and normal Discover.
- Selecting a country shows global records plus that country's verified national layer.
- Around the World can browse the national layer directly.

This is not a public-holiday planner. The market layer contains selected civic, remembrance and national observances that fit the World Days product.

## Launch markets

| Code | Market | Curated records |
| --- | --- | ---: |
| IT | Italy | 2 |
| ES | Spain | 2 |
| FR | France | 2 |
| DE | Germany | 1 |
| PT | Portugal | 2 |
| GB | United Kingdom | 1 |
| US | United States | 4 |

Total first tranche: **14** national observances.

## Source policy

A national record may use `A_PRIMARY` when the cited page is the establishing law, official gazette, competent government authority or official programme maintained by the responsible public institution.

`B_INSTITUTIONAL` remains appropriate for institutional cross-checks that do not themselves establish or maintain the observance.

No Tier C discovery page can create an `OFFICIAL_INSTITUTIONAL` record.

## Market sources in the first tranche

### Italy
- Gazzetta Ufficiale — Law 92/2004, Giorno del ricordo.
- Presidenza della Repubblica — official Republic Day celebrations.

### Spain
- BOE — Law 18/1987, National Day of Spain.
- BOE — Royal Decree 2964/1983, Constitution Day.

### France
- Légifrance — Law 2013-642, National Day of the Resistance.
- Légifrance — Law of 6 July 1880, annual national day.

### Germany
- Bundesregierung — Unification Treaty, Article 2(2), German Unity Day.

### Portugal
- Government of Portugal — Portugal Day.
- Government of Portugal — official commemoration of the Implantation of the Republic.

### United Kingdom
- Armed Forces Day / Ministry of Defence programme — Armed Forces Day.

### United States
- U.S. Office of Personnel Management / 5 U.S.C. 6103 — Birthday of Martin Luther King Jr., Memorial Day, Independence Day and Veterans Day.

## Acceptance rules

Every market record must:
- have `scope=NATIONAL`;
- contain exactly one supported ISO country code;
- use `OFFICIAL_INSTITUTIONAL`;
- have at least one `A_PRIMARY` source;
- use a recurrence rule rather than a hard-coded 2026 date when the recurrence is deterministic;
- pass 2026 occurrence vectors for representative fixed and movable dates.

The first tranche is deliberately small and high-confidence. Expansion should add markets or observances only after the same source and recurrence checks.
