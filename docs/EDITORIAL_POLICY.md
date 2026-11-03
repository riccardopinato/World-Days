# World Days — Editorial Policy

Baseline: 2026-10-12

World Days keeps factual identity and editorial content in separate datasets.

## Canonical layer

The canonical observance record owns:
- title and aliases
- recurrence/date rules
- scope
- authority and officiality
- source provenance

Editorial copy must never modify those facts.

## Editorial layer

`assets/data/editorial_en.json` is generated from `tool/build_editorial.py`.

The English pack is the editorial master. Each reviewed entry contains:
- original summary
- original "why it matters" section
- 2–4 practical ways to take part
- review date
- a source-policy marker linking the copy back to the canonical authority/originator evidence

Initial Step 5 coverage: **28 reviewed English entries**.

## Writing rules

1. Do not copy prose from UN, WHO, UNESCO, NGOs, Wikipedia, magazines or discovery calendars.
2. Facts must be supportable by sources already attached to the canonical record.
3. Avoid unsupported statistics, campaign slogans and yearly themes in evergreen copy.
4. Do not give medical, legal or crisis advice as if World Days were a professional service.
5. Keep participation suggestions low-risk, realistic and non-judgmental.
6. If a claim requires a yearly update, keep it in a year override or campaign layer rather than evergreen editorial copy.
7. English is the source language. Translations are handled as separate locale packs and must preserve meaning rather than rewrite facts.

## Fallback

Observances without a reviewed article continue to show canonical authority/provenance and an editorial-coming-next state. Missing editorial content must never hide the observance itself.


## Localized editorial packs

The English pack remains the editorial master.

Runtime locale packs are generated for:
- Italian (`it`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Portuguese (`pt`)

Each localized pack must contain the same reviewed `observanceId` set as English, in the same order, with the same number of participation actions per entry. Localized entries use `status=REVIEWED_TRANSLATION` and `translationOf=en`.

Translations may adapt sentence structure for natural language, but must not introduce new factual claims, statistics, yearly campaign themes or changes to authority/officiality.

If a requested locale pack or entry is unavailable, runtime falls back to the reviewed English entry. Fallback is editorial-only and never changes the user's UI locale or market preference.

Current Step 7 coverage: **28 reviewed articles × 6 locales = 168 runtime editorial entries**.


## Source-reviewed narrative pilot — 2026-11-03

The detail screen now exposes factual event dates and source-backed establishment
years independently from prose. The English master expands to **29** reviewed
editorial entries (Africa Industrialization Day added) across six locales,
with original narrative/history for Africa and a documented 1992→1993
timeline for World Water Day.

- Africa: [UN observance](https://www.un.org/en/observances/africa-industrialization-day)
  and OAU 1989 resolution. Proclaimed/introduced **1989**.
- Water: [UN resolution A/RES/47/193](https://digitallibrary.un.org/record/159180?ln=en),
  adopted **1992**, first observed **1993**.
- For the other 294 catalog records, no establishment year is guessed: the
  detail UI shows `*` plus an explanation until primary-source evidence
  can support a new value.
- Only the reviewed master and five reviewed translations are classified as
  rich editorial. The remaining 267 records use a short localized discovery
  caption plus a transparent history-not-yet-reviewed disclosure.
- App Factory Core's
  `GOLDEN_VERSIONED_EDITORIAL_CATALOG_FLUTTER_v1_DRAFT` provides the
  fact/editorial separation, source provenance, translation parity and
  human review contract. No new persistent state or unverified import engine
  was introduced; the Golden remains a draft, not a certification.


## 2026-11-03 content delivery/versioning

The generated canonical catalog, six editorial packs and remote content
manifest now carry revision `2026.11.03.1`, a numeric bump from
`2026.10.14.1`. The review timestamps of Africa Industrialization Day and
World Water Day are `2026-11-03`, while the other 27 articles retain
their original `2026-10-12` review dates. Six-locale validators compare
each translation's date to its English source; they do not silently
claim that older articles received a new review.


## Old downloaded pack vs newer bundled content

The app now compares the source-catalog revision with any previously
downloaded catalog on startup. A **newer bundled** catalog wins for
rendering (so the 2026.11.03.1 reviewed articles cannot be hidden by an
older cached 2026.10.14.1 pack), while a genuinely newer installed pack
continues to win. The on-disk pack is not deleted; user-owned state and
rollback capability remain untouched. The remote update checker uses
the higher active/bundled version to refuse CDN downgrade.


## UN historical sources — batch 01 (2026-11-03)

Proposed content revision `2026.11.03.2` adds four source-backed
establishment years and expands four narratives in all six locales:

- International Day of Education — **2018**, resolution A/RES/73/25;
  [United Nations background](https://www.un.org/en/node/49970).
- World Environment Day — **1972**, resolution 2994 (XXVII),
  [UN historical background](https://www.un.org/en/observances/environment-day/background);
  first marked in 1973.
- World Oceans Day — **2008**, resolution A/RES/63/111,
  [UN historical background](https://www.un.org/en/observances/oceans-day/background).
  The concept arose in 1992; annual UN designation began from 2009.
- World Wildlife Day — **2013**, resolution A/RES/68/205,
  [UN historical background](https://www.un.org/en/node/56929);
  3 March commemorates the CITES treaty's 1973 signing, which is
  not the year this observance was established.

The original 29 reviewed entries become **30** after adding Wildlife.
Four source narratives are added or enriched in EN/IT/ES/FR/DE/PT,
without overwriting canonical IDs or user preferences. The 4 years
were not inferred from date rules or resolution numbering: the cited
UN history establishes them directly.

These are editorial proposals on a separate branch; treat actual CI
pass and protected-main merge as necessary acceptance conditions.
The remaining **266** unexpanded histories and **290** unverified
establishment years continue to display transparent fallback rather
than invented claims.
